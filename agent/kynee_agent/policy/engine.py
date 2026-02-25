"""Policy enforcement engine for Rules of Engagement."""

import ipaddress
from datetime import datetime
from typing import Any, Optional

import structlog

from kynee_agent.core.exceptions import (
    OutOfScopeError,
    RateLimitExceededError,
    TimeWindowViolationError,
    UnauthorizedMethodError,
)
from kynee_agent.models.engagement import Engagement, Scope

logger = structlog.get_logger(__name__)


class PolicyEngine:
    """
    Enforces Rules of Engagement constraints.

    Responsibilities:
    - Validate targets are in scope (CIDR, hostnames, SSIDs)
    - Check time windows (engagement active period)
    - Enforce rate limits (scans/hour per method)
    - Authorize methods (network-scanning, credential-testing, etc.)
    """

    def __init__(self, engagement: Engagement):
        """
        Initialize policy engine.

        Args:
            engagement: Engagement with RoE to enforce
        """
        self.engagement = engagement
        self.method_counters: dict[str, int] = {}

    def validate_target_in_scope(
        self,
        ip_address: Optional[str] = None,
        hostname: Optional[str] = None,
        ssid: Optional[str] = None,
        mac_address: Optional[str] = None,
    ) -> bool:
        """
        Validate target is within engagement scope.

        Args:
            ip_address: IP address to check
            hostname: Hostname to check
            ssid: WiFi SSID to check
            mac_address: MAC address to check

        Returns:
            True if target is in scope

        Raises:
            OutOfScopeError: If target is outside scope
        """
        scope = self.engagement.scope

        # Check IP address
        if ip_address:
            if not self._check_ip_in_scope(ip_address, scope.ip_ranges):
                logger.warning(
                    "out_of_scope_ip",
                    ip=ip_address,
                    engagement_id=self.engagement.engagement_id,
                )
                raise OutOfScopeError(
                    f"IP address {ip_address} not in authorized scope"
                )

        # Check hostname
        if hostname:
            if hostname not in scope.hostnames and scope.hostnames:
                logger.warning(
                    "out_of_scope_hostname",
                    hostname=hostname,
                    engagement_id=self.engagement.engagement_id,
                )
                raise OutOfScopeError(
                    f"Hostname {hostname} not in authorized scope"
                )

        # Check SSID
        if ssid:
            if ssid not in scope.ssids and scope.ssids:
                logger.warning(
                    "out_of_scope_ssid",
                    ssid=ssid,
                    engagement_id=self.engagement.engagement_id,
                )
                raise OutOfScopeError(f"SSID {ssid} not in authorized scope")

        # Check MAC address
        if mac_address:
            if mac_address not in scope.mac_addresses and scope.mac_addresses:
                logger.warning(
                    "out_of_scope_mac",
                    mac=mac_address,
                    engagement_id=self.engagement.engagement_id,
                )
                raise OutOfScopeError(
                    f"MAC address {mac_address} not in authorized scope"
                )

        return True

    def validate_time_window(self) -> bool:
        """
        Validate current time is within engagement window.

        Returns:
            True if within time window

        Raises:
            TimeWindowViolationError: If outside engagement window
        """
        now = datetime.utcnow()

        if now < self.engagement.start_time:
            logger.warning(
                "before_engagement_start",
                now=now,
                start=self.engagement.start_time,
                engagement_id=self.engagement.engagement_id,
            )
            raise TimeWindowViolationError(
                f"Engagement has not yet started (starts {self.engagement.start_time})"
            )

        if now > self.engagement.end_time:
            logger.warning(
                "after_engagement_end",
                now=now,
                end=self.engagement.end_time,
                engagement_id=self.engagement.engagement_id,
            )
            raise TimeWindowViolationError(
                f"Engagement has expired (ended {self.engagement.end_time})"
            )

        return True

    def validate_method_authorized(self, method: str) -> bool:
        """
        Validate method is authorized.

        Args:
            method: Method to authorize (e.g., 'network-scanning')

        Returns:
            True if method is authorized

        Raises:
            UnauthorizedMethodError: If method not authorized
        """
        if method not in self.engagement.authorized_methods:
            logger.warning(
                "unauthorized_method",
                method=method,
                engagement_id=self.engagement.engagement_id,
            )
            raise UnauthorizedMethodError(
                f"Method '{method}' not authorized in engagement"
            )

        return True

    def check_rate_limit(self, method: str, max_per_hour: int = 10) -> bool:
        """
        Check if method call would exceed rate limit.

        Args:
            method: Method being called
            max_per_hour: Maximum calls allowed per hour

        Returns:
            True if within rate limit

        Raises:
            RateLimitExceededError: If rate limit exceeded
        """
        # Get configured limit or use default
        configured_limit = self.engagement.rate_limits.get(method, max_per_hour)

        current_count = self.method_counters.get(method, 0)
        if current_count >= configured_limit:
            logger.warning(
                "rate_limit_exceeded",
                method=method,
                count=current_count,
                limit=configured_limit,
                engagement_id=self.engagement.engagement_id,
            )
            raise RateLimitExceededError(
                f"Rate limit exceeded for method '{method}': "
                f"{current_count}/{configured_limit}"
            )

        self.method_counters[method] = current_count + 1
        return True

    def validate_scan_request(
        self,
        method: str,
        target: dict[str, Any],
    ) -> bool:
        """
        Comprehensive validation for a scan request.

        Args:
            method: Method being used
            target: Target information dict with 'ip', 'hostname', 'ssid', 'mac'

        Returns:
            True if request is valid

        Raises:
            Various PolicyViolationError subclasses if validation fails
        """
        # Check time window
        self.validate_time_window()

        # Check method authorized
        self.validate_method_authorized(method)

        # Check rate limit
        self.check_rate_limit(method)

        # Check target in scope
        self.validate_target_in_scope(
            ip_address=target.get("ip"),
            hostname=target.get("hostname"),
            ssid=target.get("ssid"),
            mac_address=target.get("mac"),
        )

        logger.info(
            "scan_request_validated",
            method=method,
            engagement_id=self.engagement.engagement_id,
        )

        return True

    @staticmethod
    def _check_ip_in_scope(ip_str: str, ip_ranges: list[str]) -> bool:
        """
        Check if IP is in any of the allowed CIDR ranges.

        Args:
            ip_str: IP address to check
            ip_ranges: List of CIDR ranges

        Returns:
            True if IP is in any range, or if no ranges configured (no scope)
        """
        if not ip_ranges:
            # No IP range restriction
            return True

        try:
            ip = ipaddress.ip_address(ip_str)
            for cidr in ip_ranges:
                if ip in ipaddress.ip_network(cidr, strict=False):
                    return True
            return False
        except ValueError as e:
            logger.error("invalid_ip_or_cidr", ip=ip_str, ranges=ip_ranges, error=str(e))
            return False
