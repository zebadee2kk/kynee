"""Engagement (Rules of Engagement) model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Scope(BaseModel):
    """Target scope for engagement."""

    ip_ranges: list[str] = Field(default_factory=list)
    hostnames: list[str] = Field(default_factory=list)
    ssids: list[str] = Field(default_factory=list)
    mac_addresses: list[str] = Field(default_factory=list)


class Engagement(BaseModel):
    """Rules of Engagement (RoE) for authorized testing."""

    engagement_id: str
    client_name: str
    start_time: datetime
    end_time: datetime
    scope: Scope
    authorized_methods: list[str] = Field(
        default_factory=list,
        description="e.g., 'network-scanning', 'wireless-cracking', 'bluetooth-enumeration'",
    )
    rate_limits: dict[str, int] = Field(
        default_factory=dict,
        description="e.g., {'nmap-scans': 1, 'wifi-handshakes': 5}",
    )
    authorized_credentials: bool = Field(
        default=False,
        description="Whether credential testing is authorized",
    )
    social_engineering_allowed: bool = Field(
        default=False,
        description="Whether social engineering is authorized",
    )
    notes: Optional[str] = None

    class Config:
        """Pydantic config."""

        use_enum_values = True
