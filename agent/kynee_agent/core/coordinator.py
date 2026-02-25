"""Agent coordinator for managing multiple agents with policy enforcement."""

import asyncio
from typing import Any, Callable, Optional

import structlog

from kynee_agent.audit.writer import AuditLogWriter
from kynee_agent.core.agent import Agent
from kynee_agent.models.engagement import Engagement
from kynee_agent.policy.engine import PolicyEngine

logger = structlog.get_logger(__name__)


class AgentCoordinator:
    """
    Coordinates execution of multiple agents with centralized policy enforcement.

    Responsibilities:
    - Manage agent lifecycle (register, track, remove)
    - Enforce Rules of Engagement across all agents
    - Coordinate scan jobs and result aggregation
    - Maintain centralized audit logs
    - Handle agent-to-console communication
    """

    def __init__(
        self,
        engagement: Engagement,
        audit_log_path: str,
    ):
        """
        Initialize coordinator.

        Args:
            engagement: Engagement with RoE to enforce
            audit_log_path: Path to centralized audit log
        """
        self.engagement = engagement
        self.agents: dict[str, Agent] = {}
        self.policy_engine = PolicyEngine(engagement)
        self.audit_log = AuditLogWriter(audit_log_path)
        self.scan_results: dict[str, Any] = {}
        self.running = False

        logger.info(
            "coordinator_initialized",
            engagement_id=engagement.engagement_id,
            client=engagement.client_name,
        )

    async def register_agent(self, agent: Agent) -> str:
        """
        Register an agent under this coordinator.

        Args:
            agent: Agent instance to register

        Returns:
            Agent ID

        Raises:
            ValueError: If agent already registered
        """
        if agent.agent_id in self.agents:
            raise ValueError(f"Agent {agent.agent_id} already registered")

        self.agents[agent.agent_id] = agent

        self.audit_log.log_event(
            event_type="agent_registered",
            actor="system",
            action="agent_registered",
            result="success",
            details={
                "agent_id": agent.agent_id,
                "engagement_id": self.engagement.engagement_id,
            },
        )

        logger.info(
            "agent_registered",
            agent_id=agent.agent_id,
            total_agents=len(self.agents),
        )

        return agent.agent_id

    async def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent.

        Args:
            agent_id: ID of agent to unregister

        Returns:
            True if agent was registered and removed
        """
        if agent_id not in self.agents:
            return False

        del self.agents[agent_id]

        self.audit_log.log_event(
            event_type="agent_unregistered",
            actor="system",
            action="agent_unregistered",
            result="success",
            details={
                "agent_id": agent_id,
            },
        )

        logger.info("agent_unregistered", agent_id=agent_id)
        return True

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        return self.agents.get(agent_id)

    def get_agents(self) -> dict[str, Agent]:
        """Get all registered agents."""
        return self.agents.copy()

    async def execute_coordinated_scan(
        self,
        agent_id: str,
        scan_id: str,
        method: str,
        target: dict[str, Any],
        pre_scan_hook: Optional[Callable[[Agent, str, dict], Any]] = None,
        post_scan_hook: Optional[Callable[[Agent, str, dict, Any], Any]] = None,
    ) -> dict[str, Any]:
        """
        Execute a scan through coordinator with policy enforcement.

        Args:
            agent_id: ID of agent to execute scan
            scan_id: Unique scan identifier
            method: Scanning method
            target: Target specification
            pre_scan_hook: Optional callback before scan
            post_scan_hook: Optional callback after scan

        Returns:
            Scan result dict

        Raises:
            PolicyViolationError: If policy validation fails
        """
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not registered")

        try:
            # Validate against policies
            self.policy_engine.validate_scan_request(method, target)

            # Pre-scan hook
            if pre_scan_hook:
                await self._run_async_callback(
                    pre_scan_hook, agent, scan_id, target
                )

            # Log scan start
            self.audit_log.log_scan_started(
                agent_id=agent_id,
                scan_id=scan_id,
                method=method,
                target=target,
            )

            logger.info(
                "scan_started",
                scan_id=scan_id,
                agent_id=agent_id,
                method=method,
            )

            # Execute scan
            job = {
                "job_id": scan_id,
                "method": method,
                "target": target,
            }
            result = await agent.execute_scan(job)

            # Post-scan hook
            if post_scan_hook:
                await self._run_async_callback(
                    post_scan_hook, agent, scan_id, target, result
                )

            # Log scan completion
            findings_count = len(result.get("findings", []))
            self.audit_log.log_scan_completed(
                agent_id=agent_id,
                scan_id=scan_id,
                findings_count=findings_count,
                status="success",
            )

            # Store result
            self.scan_results[scan_id] = result

            logger.info(
                "scan_completed",
                scan_id=scan_id,
                agent_id=agent_id,
                findings_count=findings_count,
            )

            return result

        except Exception as e:
            logger.error(
                "scan_failed",
                scan_id=scan_id,
                agent_id=agent_id,
                error=str(e),
            )

            self.audit_log.log_event(
                event_type="scan_failed",
                actor=agent_id,
                action=f"scan_{method}",
                result="failure",
                details={
                    "scan_id": scan_id,
                    "error": str(e),
                },
            )

            raise

    async def broadcast_to_agents(
        self,
        message: dict[str, Any],
        callback: Optional[Callable[[Agent, dict[str, Any]], Any]] = None,
    ) -> dict[str, Any]:
        """
        Broadcast message to all agents.

        Args:
            message: Message to broadcast
            callback: Optional callback for each agent response

        Returns:
            Dict mapping agent_id to response
        """
        tasks = []
        for agent_id, agent in self.agents.items():
            tasks.append(self._broadcast_to_agent(agent_id, agent, message, callback))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        results = {}
        for agent_id, response in zip(self.agents.keys(), responses):
            if isinstance(response, Exception):
                logger.error(
                    "broadcast_failed",
                    agent_id=agent_id,
                    error=str(response),
                )
                results[agent_id] = {"error": str(response)}
            else:
                results[agent_id] = response

        return results

    async def start(self) -> None:
        """Start coordinator (begin managing agents)."""
        self.running = True
        logger.info("coordinator_started", engagement_id=self.engagement.engagement_id)

    async def stop(self) -> None:
        """Stop coordinator (gracefully shut down agents)."""
        self.running = False

        # Stop all agents
        tasks = [agent.stop() for agent in self.agents.values()]
        await asyncio.gather(*tasks, return_exceptions=True)

        logger.info("coordinator_stopped", engagement_id=self.engagement.engagement_id)

    def get_scan_result(self, scan_id: str) -> Optional[dict[str, Any]]:
        """Get cached scan result."""
        return self.scan_results.get(scan_id)

    def get_audit_entries(self, count: Optional[int] = None) -> list[dict[str, Any]]:
        """Get recent audit entries."""
        return self.audit_log.get_entries(count)

    @staticmethod
    async def _broadcast_to_agent(
        agent_id: str,
        agent: Agent,
        message: dict[str, Any],
        callback: Optional[Callable],
    ) -> Any:
        """Helper to broadcast to single agent."""
        try:
            if callback:
                result = await asyncio.to_thread(callback, agent, message)
            else:
                result = {"agent_id": agent_id, "message_received": True}
            return result
        except Exception as e:
            logger.error("broadcast_agent_error", agent_id=agent_id, error=str(e))
            raise

    @staticmethod
    async def _run_async_callback(
        callback: Callable,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run callback, handling both sync and async functions."""
        if asyncio.iscoroutinefunction(callback):
            return await callback(*args, **kwargs)
        else:
            return await asyncio.to_thread(callback, *args, **kwargs)
