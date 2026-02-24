"""Security finding model."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    """CVSS-style severity levels."""

    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingCategory(str, Enum):
    """Categories of security findings."""

    NETWORK = "network"
    WIRELESS = "wireless"
    BLUETOOTH = "bluetooth"
    PHYSICAL = "physical"
    CREDENTIAL = "credential"
    VULNERABILITY = "vulnerability"
    MISCONFIGURATION = "misconfiguration"


class FindingStatus(str, Enum):
    """Status of a finding."""

    NEW = "new"
    CONFIRMED = "confirmed"
    FALSE_POSITIVE = "false_positive"
    MITIGATED = "mitigated"
    ACCEPTED_RISK = "accepted_risk"


class Target(BaseModel):
    """Target affected by a finding."""

    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    hostname: Optional[str] = None
    ssid: Optional[str] = None
    bssid: Optional[str] = None
    port: Optional[int] = Field(None, ge=1, le=65535)
    protocol: Optional[str] = None


class Evidence(BaseModel):
    """Supporting evidence for a finding."""

    raw_output: Optional[str] = None
    screenshot_path: Optional[str] = None
    pcap_path: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class Finding(BaseModel):
    """Security assessment finding."""

    finding_id: str = Field(default_factory=lambda: str(__import__("uuid").uuid4()))
    engagement_id: str
    agent_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool: str
    category: FindingCategory
    severity: SeverityLevel
    title: str = Field(max_length=200)
    description: str
    target: Optional[Target] = None
    evidence: Optional[Evidence] = None
    cvss_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    cve_id: Optional[str] = None
    remediation: Optional[str] = None
    references: list[str] = Field(default_factory=list)
    status: FindingStatus = FindingStatus.NEW

    class Config:
        """Pydantic config."""

        use_enum_values = True
