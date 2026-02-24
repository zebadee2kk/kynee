"""Agent management routes."""

from fastapi import APIRouter
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
async def list_agents():
    """List all enrolled agents."""
    # TODO: Implement
    return {"agents": []}


@router.post("/enroll")
async def enroll_agent(agent_id: str):
    """Enroll a new agent."""
    # TODO: Implement
    logger.info("agent_enrollment_started", agent_id=agent_id)
    return {"agent_id": agent_id, "status": "pending"}


@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details."""
    # TODO: Implement
    return {"agent_id": agent_id, "status": "unknown"}
