"""Unit tests for AgentCoordinator."""

import asyncio

import pytest

from kynee_agent.core import Agent, AgentCoordinator
from kynee_agent.core.exceptions import OutOfScopeError


@pytest.mark.asyncio
async def test_coordinator_initialization(sample_engagement, temp_dir):
    """Coordinator should initialize with engagement."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    assert coordinator.engagement == sample_engagement
    assert len(coordinator.agents) == 0
    assert coordinator.running is False


@pytest.mark.asyncio
async def test_register_agent(sample_engagement, sample_agent, temp_dir):
    """Should register agent."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    agent_id = await coordinator.register_agent(sample_agent)

    assert agent_id == sample_agent.agent_id
    assert coordinator.get_agent(agent_id) == sample_agent


@pytest.mark.asyncio
async def test_register_duplicate_agent_fails(sample_engagement, sample_agent, temp_dir):
    """Registering same agent twice should fail."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    await coordinator.register_agent(sample_agent)

    with pytest.raises(ValueError, match="already registered"):
        await coordinator.register_agent(sample_agent)


@pytest.mark.asyncio
async def test_unregister_agent(sample_engagement, sample_agent, temp_dir):
    """Should unregister agent."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    await coordinator.register_agent(sample_agent)
    result = await coordinator.unregister_agent(sample_agent.agent_id)

    assert result is True
    assert coordinator.get_agent(sample_agent.agent_id) is None


@pytest.mark.asyncio
async def test_unregister_nonexistent_agent(sample_engagement, temp_dir):
    """Unregistering nonexistent agent should return False."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    result = await coordinator.unregister_agent("nonexistent")

    assert result is False


@pytest.mark.asyncio
async def test_get_agents(sample_engagement, temp_dir):
    """Should retrieve all agents."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    agent1 = Agent(agent_id="agent-1")
    agent2 = Agent(agent_id="agent-2")

    await coordinator.register_agent(agent1)
    await coordinator.register_agent(agent2)

    agents = coordinator.get_agents()

    assert len(agents) == 2
    assert "agent-1" in agents
    assert "agent-2" in agents


@pytest.mark.asyncio
async def test_execute_coordinated_scan_valid(sample_engagement, sample_agent, temp_dir):
    """Should execute valid scan through coordinator."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    await coordinator.register_agent(sample_agent)
    await coordinator.start()

    result = await coordinator.execute_coordinated_scan(
        agent_id=sample_agent.agent_id,
        scan_id="scan-001",
        method="network-scanning",
        target={"ip": "192.168.1.50"},
    )

    assert result is not None
    assert result["job_id"] == "scan-001"


@pytest.mark.asyncio
async def test_execute_scan_policy_violation(sample_engagement, sample_agent, temp_dir):
    """Should reject scan with policy violation."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    await coordinator.register_agent(sample_agent)

    with pytest.raises(OutOfScopeError):
        await coordinator.execute_coordinated_scan(
            agent_id=sample_agent.agent_id,
            scan_id="scan-002",
            method="network-scanning",
            target={"ip": "8.8.8.8"},  # Out of scope
        )


@pytest.mark.asyncio
async def test_execute_scan_unregistered_agent(sample_engagement, temp_dir):
    """Should fail to execute scan on unregistered agent."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    with pytest.raises(ValueError, match="not registered"):
        await coordinator.execute_coordinated_scan(
            agent_id="nonexistent",
            scan_id="scan-001",
            method="network-scanning",
            target={"ip": "192.168.1.1"},
        )


@pytest.mark.asyncio
async def test_get_scan_result(sample_engagement, sample_agent, temp_dir):
    """Should retrieve cached scan result."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    await coordinator.register_agent(sample_agent)
    await coordinator.start()

    result = await coordinator.execute_coordinated_scan(
        agent_id=sample_agent.agent_id,
        scan_id="scan-001",
        method="network-scanning",
        target={"ip": "192.168.1.50"},
    )

    cached = coordinator.get_scan_result("scan-001")

    assert cached is not None
    assert cached == result


@pytest.mark.asyncio
async def test_coordinator_start_stop(sample_engagement, temp_dir):
    """Coordinator should start and stop."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    await coordinator.start()
    assert coordinator.running is True

    await coordinator.stop()
    assert coordinator.running is False


@pytest.mark.asyncio
async def test_broadcast_to_agents(sample_engagement, temp_dir):
    """Should broadcast to all agents."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    agent1 = Agent(agent_id="agent-1")
    agent2 = Agent(agent_id="agent-2")

    await coordinator.register_agent(agent1)
    await coordinator.register_agent(agent2)

    responses = await coordinator.broadcast_to_agents(
        message={"type": "heartbeat", "request_status": True}
    )

    assert len(responses) == 2
    assert "agent-1" in responses
    assert "agent-2" in responses


@pytest.mark.asyncio
async def test_get_audit_entries(sample_engagement, sample_agent, temp_dir):
    """Should retrieve audit entries."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    await coordinator.register_agent(sample_agent)

    entries = coordinator.get_audit_entries()

    # Should have at least registration entry
    assert len(entries) >= 1
    assert any(e["event_type"] == "agent_registered" for e in entries)


@pytest.mark.asyncio
async def test_pre_scan_hook(sample_engagement, sample_agent, temp_dir):
    """Should call pre-scan hook."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    await coordinator.register_agent(sample_agent)
    await coordinator.start()

    hook_called = False

    async def pre_hook(agent, scan_id, target):
        nonlocal hook_called
        hook_called = True

    await coordinator.execute_coordinated_scan(
        agent_id=sample_agent.agent_id,
        scan_id="scan-001",
        method="network-scanning",
        target={"ip": "192.168.1.50"},
        pre_scan_hook=pre_hook,
    )

    assert hook_called is True


@pytest.mark.asyncio
async def test_post_scan_hook(sample_engagement, sample_agent, temp_dir):
    """Should call post-scan hook."""
    audit_path = temp_dir / "audit.log"
    coordinator = AgentCoordinator(sample_engagement, str(audit_path))

    await coordinator.register_agent(sample_agent)
    await coordinator.start()

    hook_called = False

    async def post_hook(agent, scan_id, target, result):
        nonlocal hook_called
        hook_called = True

    await coordinator.execute_coordinated_scan(
        agent_id=sample_agent.agent_id,
        scan_id="scan-001",
        method="network-scanning",
        target={"ip": "192.168.1.50"},
        post_scan_hook=post_hook,
    )

    assert hook_called is True
