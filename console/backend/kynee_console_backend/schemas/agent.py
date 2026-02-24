"""Agent schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AgentCreate(BaseModel):
    """Request schema for agent enrollment."""

    agent_id: str
    hostname: Optional[str] = None
    ip_address: Optional[str] = None


class AgentResponse(BaseModel):
    """Response schema for agent info."""

    agent_id: str
    status: str = "unknown"
    enrolled_at: Optional[datetime] = None
    last_heartbeat: Optional[datetime] = None
