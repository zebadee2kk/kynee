"""Inventory model for discovered assets."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class DeviceType(str, Enum):
    """Types of discovered devices."""

    HOST = "host"
    NETWORK_DEVICE = "network_device"
    WIRELESS_AP = "wireless_ap"
    BLUETOOTH_DEVICE = "bluetooth_device"
    IOT_DEVICE = "iot_device"
    UNKNOWN = "unknown"


class InventoryItem(BaseModel):
    """Discovered asset in the network."""

    inventory_id: str = Field(default_factory=lambda: str(__import__("uuid").uuid4()))
    engagement_id: str
    agent_id: str
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    device_type: DeviceType
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    hostname: Optional[str] = None
    ssid: Optional[str] = None
    bssid: Optional[str] = None
    open_ports: list[int] = Field(default_factory=list)
    services: dict[int, str] = Field(
        default_factory=dict,
        description="Port -> Service name mapping",
    )
    os_info: Optional[str] = None
    vendor: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""

        use_enum_values = True
