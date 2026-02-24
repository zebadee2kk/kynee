"""Finding schemas."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    """Severity levels."""

    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingCreate(BaseModel):
    """Request schema for creating a finding."""

    engagement_id: str
    agent_id: str
    title: str
    description: str
    category: str
    severity: SeverityLevel
    tool: str


class FindingResponse(BaseModel):
    """Response schema for finding."""

    finding_id: str
    engagement_id: str
    agent_id: str
    title: str
    severity: str
    status: str = "new"
    created_at: datetime
