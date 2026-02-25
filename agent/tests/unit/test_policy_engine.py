"""Unit tests for PolicyEngine."""

import pytest

from kynee_agent.core.exceptions import (
    OutOfScopeError,
    RateLimitExceededError,
    TimeWindowViolationError,
    UnauthorizedMethodError,
)
from kynee_agent.policy.engine import PolicyEngine


class TestPolicyEngineTargetValidation:
    """Test target scope validation."""

    def test_valid_ip_in_scope(self, sample_engagement):
        """IP within CIDR range should be valid."""
        engine = PolicyEngine(sample_engagement)
        assert engine.validate_target_in_scope(ip_address="192.168.1.100") is True

    def test_invalid_ip_out_of_scope(self, sample_engagement):
        """IP outside CIDR range should raise OutOfScopeError."""
        engine = PolicyEngine(sample_engagement)
        with pytest.raises(OutOfScopeError):
            engine.validate_target_in_scope(ip_address="8.8.8.8")

    def test_valid_hostname_in_scope(self, sample_engagement):
        """Hostname in scope list should be valid."""
        engine = PolicyEngine(sample_engagement)
        assert engine.validate_target_in_scope(hostname="target.local") is True

    def test_invalid_hostname_out_of_scope(self, sample_engagement):
        """Hostname not in scope list should raise OutOfScopeError."""
        engine = PolicyEngine(sample_engagement)
        with pytest.raises(OutOfScopeError):
            engine.validate_target_in_scope(hostname="unauthorized.com")

    def test_valid_ssid_in_scope(self, sample_engagement):
        """SSID in scope list should be valid."""
        engine = PolicyEngine(sample_engagement)
        assert engine.validate_target_in_scope(ssid="TestWiFi") is True

    def test_invalid_ssid_out_of_scope(self, sample_engagement):
        """SSID not in scope list should raise OutOfScopeError."""
        engine = PolicyEngine(sample_engagement)
        with pytest.raises(OutOfScopeError):
            engine.validate_target_in_scope(ssid="GuestWiFi")

    def test_empty_scope_allows_any_target(self, sample_engagement):
        """Empty scope lists should allow any target."""
        sample_engagement.scope.ip_ranges = []
        sample_engagement.scope.hostnames = []
        engine = PolicyEngine(sample_engagement)

        assert engine.validate_target_in_scope(ip_address="1.2.3.4") is True
        assert engine.validate_target_in_scope(hostname="any.host") is True


class TestPolicyEngineTimeValidation:
    """Test engagement time window validation."""

    def test_within_time_window(self, sample_engagement):
        """Scan within engagement window should be valid."""
        engine = PolicyEngine(sample_engagement)
        assert engine.validate_time_window() is True

    def test_before_engagement_start(self, sample_engagement):
        """Scan before engagement start should raise TimeWindowViolationError."""
        from datetime import datetime, timedelta

        sample_engagement.start_time = datetime.utcnow() + timedelta(hours=1)
        engine = PolicyEngine(sample_engagement)

        with pytest.raises(TimeWindowViolationError):
            engine.validate_time_window()

    def test_after_engagement_end(self, sample_engagement):
        """Scan after engagement end should raise TimeWindowViolationError."""
        from datetime import datetime, timedelta

        sample_engagement.end_time = datetime.utcnow() - timedelta(hours=1)
        engine = PolicyEngine(sample_engagement)

        with pytest.raises(TimeWindowViolationError):
            engine.validate_time_window()


class TestPolicyEngineMethodValidation:
    """Test method authorization validation."""

    def test_authorized_method(self, sample_engagement):
        """Authorized method should be valid."""
        engine = PolicyEngine(sample_engagement)
        assert engine.validate_method_authorized("network-scanning") is True

    def test_unauthorized_method(self, sample_engagement):
        """Unauthorized method should raise UnauthorizedMethodError."""
        engine = PolicyEngine(sample_engagement)
        with pytest.raises(UnauthorizedMethodError):
            engine.validate_method_authorized("physical-breaking-and-entering")


class TestPolicyEngineRateLimiting:
    """Test rate limit enforcement."""

    def test_within_rate_limit(self, sample_engagement):
        """Calls within limit should pass."""
        engine = PolicyEngine(sample_engagement)
        for i in range(5):
            assert engine.check_rate_limit("network-scanning", max_per_hour=10) is True

    def test_exceed_rate_limit(self, sample_engagement):
        """Exceeding limit should raise RateLimitExceededError."""
        engine = PolicyEngine(sample_engagement)

        # Make 5 calls (fixture has wireless-enumeration: 5)
        for i in range(5):
            engine.check_rate_limit("wireless-enumeration", max_per_hour=10)

        # 6th call should fail (already at max of 5)
        with pytest.raises(RateLimitExceededError):
            engine.check_rate_limit("wireless-enumeration", max_per_hour=10)

    def test_rate_limit_per_method(self, sample_engagement):
        """Rate limits should be per method."""
        engine = PolicyEngine(sample_engagement)

        # Max out one method
        for i in range(3):
            engine.check_rate_limit("wireless-enumeration", max_per_hour=3)

        # Different method should still work
        assert engine.check_rate_limit("network-scanning", max_per_hour=10) is True


class TestPolicyEngineComprehensiveValidation:
    """Test comprehensive scan request validation."""

    def test_valid_scan_request(self, sample_engagement):
        """Valid scan request should pass all checks."""
        engine = PolicyEngine(sample_engagement)

        request_valid = engine.validate_scan_request(
            method="network-scanning",
            target={"ip": "192.168.1.50"},
        )

        assert request_valid is True

    def test_invalid_method_fails_validation(self, sample_engagement):
        """Invalid method should fail comprehensive validation."""
        engine = PolicyEngine(sample_engagement)

        with pytest.raises(UnauthorizedMethodError):
            engine.validate_scan_request(
                method="unauthorized-method",
                target={"ip": "192.168.1.50"},
            )

    def test_out_of_scope_target_fails_validation(self, sample_engagement):
        """Out of scope target should fail comprehensive validation."""
        engine = PolicyEngine(sample_engagement)

        with pytest.raises(OutOfScopeError):
            engine.validate_scan_request(
                method="network-scanning",
                target={"ip": "8.8.8.8"},
            )


class TestPolicyEngineIPAddressChecking:
    """Test IP address CIDR matching."""

    def test_ipv4_in_cidr_range(self):
        """IPv4 should match CIDR range."""
        assert PolicyEngine._check_ip_in_scope("192.168.1.50", ["192.168.1.0/24"]) is True

    def test_ipv4_outside_cidr_range(self):
        """IPv4 should not match CIDR range."""
        assert PolicyEngine._check_ip_in_scope("192.168.2.50", ["192.168.1.0/24"]) is False

    def test_multiple_cidr_ranges(self):
        """Should match any CIDR range."""
        ranges = ["192.168.1.0/24", "10.0.0.0/8"]
        assert PolicyEngine._check_ip_in_scope("10.5.5.5", ranges) is True
        assert PolicyEngine._check_ip_in_scope("192.168.1.1", ranges) is True
        assert PolicyEngine._check_ip_in_scope("172.16.0.1", ranges) is False

    def test_invalid_ip_format(self):
        """Invalid IP should return False."""
        assert PolicyEngine._check_ip_in_scope("not-an-ip", ["192.168.1.0/24"]) is False
