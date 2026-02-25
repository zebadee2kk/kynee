"""Unit tests for KYNEĒ data models."""

from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from kynee_agent.models.engagement import Engagement, Scope
from kynee_agent.models.finding import (
    Finding,
    FindingCategory,
    FindingStatus,
    SeverityLevel,
    Target,
)
from kynee_agent.models.inventory import InventoryItem, DeviceType


class TestScope:
    """Test Scope model."""

    def test_scope_creation(self):
        """Should create scope with lists."""
        scope = Scope(
            ip_ranges=["192.168.1.0/24"],
            hostnames=["target.local"],
            ssids=["TestWiFi"],
        )

        assert len(scope.ip_ranges) == 1
        assert len(scope.hostnames) == 1
        assert len(scope.ssids) == 1

    def test_scope_empty_lists(self):
        """Scope should allow empty lists."""
        scope = Scope()

        assert scope.ip_ranges == []
        assert scope.hostnames == []
        assert scope.ssids == []


class TestEngagement:
    """Test Engagement (RoE) model."""

    def test_engagement_creation(self):
        """Should create engagement with all fields."""
        scope = Scope(ip_ranges=["192.168.1.0/24"])
        now = datetime.utcnow()

        engagement = Engagement(
            engagement_id="eng-001",
            client_name="Test Client",
            start_time=now,
            end_time=now + timedelta(days=1),
            scope=scope,
            authorized_methods=["network-scanning"],
            authorized_credentials=True,
        )

        assert engagement.engagement_id == "eng-001"
        assert engagement.client_name == "Test Client"
        assert engagement.authorized_credentials is True

    def test_engagement_rate_limits(self):
        """Should support custom rate limits."""
        scope = Scope()
        now = datetime.utcnow()

        engagement = Engagement(
            engagement_id="eng-001",
            client_name="Test Client",
            start_time=now,
            end_time=now + timedelta(days=1),
            scope=scope,
            rate_limits={"network-scanning": 10, "wifi-cracking": 5},
        )

        assert engagement.rate_limits["network-scanning"] == 10
        assert engagement.rate_limits["wifi-cracking"] == 5

    def test_engagement_required_fields(self):
        """Engagement should require key fields."""
        with pytest.raises(ValidationError):
            Engagement(
                # Missing engagement_id
                client_name="Test",
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                scope=Scope(),
            )


class TestFinding:
    """Test Finding model."""

    def test_finding_creation(self):
        """Should create finding with all fields."""
        target = Target(ip_address="192.168.1.1", port=22)

        finding = Finding(
            engagement_id="eng-001",
            agent_id="agent-001",
            tool="nmap",
            category=FindingCategory.NETWORK,
            severity=SeverityLevel.HIGH,
            title="Open SSH Port",
            description="SSH port is open and accessible",
            target=target,
        )

        assert finding.engagement_id == "eng-001"
        assert finding.category == FindingCategory.NETWORK
        assert finding.severity == SeverityLevel.HIGH

    def test_finding_categories(self):
        """Should support all finding categories."""
        for category in [
            FindingCategory.NETWORK,
            FindingCategory.WIRELESS,
            FindingCategory.BLUETOOTH,
            FindingCategory.PHYSICAL,
            FindingCategory.CREDENTIAL,
            FindingCategory.VULNERABILITY,
            FindingCategory.MISCONFIGURATION,
        ]:
            finding = Finding(
                engagement_id="eng",
                agent_id="agent",
                tool="test",
                category=category,
                severity=SeverityLevel.MEDIUM,
                title="Test",
                description="Test",
            )
            assert finding.category == category

    def test_finding_severity_levels(self):
        """Should support all severity levels."""
        for severity in [
            SeverityLevel.INFORMATIONAL,
            SeverityLevel.LOW,
            SeverityLevel.MEDIUM,
            SeverityLevel.HIGH,
            SeverityLevel.CRITICAL,
        ]:
            finding = Finding(
                engagement_id="eng",
                agent_id="agent",
                tool="test",
                category=FindingCategory.NETWORK,
                severity=severity,
                title="Test",
                description="Test",
            )
            assert finding.severity == severity

    def test_finding_status(self):
        """Should support finding status."""
        finding = Finding(
            engagement_id="eng",
            agent_id="agent",
            tool="test",
            category=FindingCategory.NETWORK,
            severity=SeverityLevel.MEDIUM,
            title="Test",
            description="Test",
            status=FindingStatus.CONFIRMED,
        )

        assert finding.status == FindingStatus.CONFIRMED

    def test_finding_cvss_validation(self):
        """CVSS score should be between 0 and 10."""
        target = Target(ip_address="192.168.1.1")

        # Valid CVSS
        finding = Finding(
            engagement_id="eng",
            agent_id="agent",
            tool="test",
            category=FindingCategory.VULNERABILITY,
            severity=SeverityLevel.MEDIUM,
            title="Test",
            description="Test",
            target=target,
            cvss_score=7.5,
        )
        assert finding.cvss_score == 7.5

        # Invalid CVSS too high
        with pytest.raises(ValidationError):
            Finding(
                engagement_id="eng",
                agent_id="agent",
                tool="test",
                category=FindingCategory.VULNERABILITY,
                severity=SeverityLevel.MEDIUM,
                title="Test",
                description="Test",
                target=target,
                cvss_score=11.0,
            )

    def test_finding_port_validation(self):
        """Port should be between 1 and 65535."""
        # Valid port
        target = Target(ip_address="192.168.1.1", port=443)
        assert target.port == 443

        # Invalid port too high
        with pytest.raises(ValidationError):
            Target(ip_address="192.168.1.1", port=70000)

        # Invalid port too low
        with pytest.raises(ValidationError):
            Target(ip_address="192.168.1.1", port=0)

    def test_finding_title_length(self):
        """Title should have max length."""
        with pytest.raises(ValidationError):
            Finding(
                engagement_id="eng",
                agent_id="agent",
                tool="test",
                category=FindingCategory.NETWORK,
                severity=SeverityLevel.MEDIUM,
                title="x" * 201,  # Too long
                description="Test",
            )


class TestInventoryItem:
    """Test InventoryItem model."""

    def test_inventory_creation(self):
        """Should create inventory item."""
        item = InventoryItem(
            engagement_id="eng-001",
            agent_id="agent-001",
            device_type=DeviceType.HOST,
            ip_address="192.168.1.1",
            hostname="target.local",
        )

        assert item.engagement_id == "eng-001"
        assert item.device_type == DeviceType.HOST
        assert item.ip_address == "192.168.1.1"

    def test_inventory_device_types(self):
        """Should support all device types."""
        for device_type in [
            DeviceType.HOST,
            DeviceType.NETWORK_DEVICE,
            DeviceType.WIRELESS_AP,
            DeviceType.BLUETOOTH_DEVICE,
            DeviceType.IOT_DEVICE,
            DeviceType.UNKNOWN,
        ]:
            item = InventoryItem(
                engagement_id="eng",
                agent_id="agent",
                device_type=device_type,
            )
            assert item.device_type == device_type

    def test_inventory_services(self):
        """Should track port-to-service mapping."""
        item = InventoryItem(
            engagement_id="eng",
            agent_id="agent",
            device_type=DeviceType.HOST,
            ip_address="192.168.1.1",
            services={22: "ssh", 80: "http", 443: "https"},
        )

        assert item.services[22] == "ssh"
        assert item.services[80] == "http"

    def test_inventory_open_ports(self):
        """Should track open ports."""
        item = InventoryItem(
            engagement_id="eng",
            agent_id="agent",
            device_type=DeviceType.HOST,
            ip_address="192.168.1.1",
            open_ports=[22, 80, 443],
        )

        assert len(item.open_ports) == 3
        assert 22 in item.open_ports

    def test_inventory_metadata(self):
        """Should support custom metadata."""
        item = InventoryItem(
            engagement_id="eng",
            agent_id="agent",
            device_type=DeviceType.HOST,
            metadata={"os": "Linux", "version": "5.10"},
        )

        assert item.metadata["os"] == "Linux"
