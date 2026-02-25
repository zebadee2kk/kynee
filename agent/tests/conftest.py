"""Pytest configuration for KYNEĒ Agent tests."""

import asyncio
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from kynee_agent.core import Agent
from kynee_agent.models.engagement import Engagement, Scope


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_scope():
    """Create a sample engagement scope."""
    return Scope(
        ip_ranges=["192.168.1.0/24", "10.0.0.0/8"],
        hostnames=["target.local", "test.example.com"],
        ssids=["TestWiFi", "Corporate"],
        mac_addresses=["aa:bb:cc:dd:ee:ff"],
    )


@pytest.fixture
def sample_engagement(sample_scope):
    """Create a sample engagement with RoE."""
    return Engagement(
        engagement_id="test-engagement-001",
        client_name="Test Client",
        start_time=datetime.utcnow() - timedelta(hours=1),
        end_time=datetime.utcnow() + timedelta(hours=23),
        scope=sample_scope,
        authorized_methods=[
            "network-scanning",
            "wireless-enumeration",
            "bluetooth-enumeration",
        ],
        rate_limits={
            "network-scanning": 10,
            "wireless-enumeration": 5,
        },
        authorized_credentials=True,
        social_engineering_allowed=False,
        notes="Test engagement for unit testing",
    )


@pytest.fixture
def sample_agent():
    """Create a sample agent."""
    return Agent(agent_id="test-agent-001", config_path=None)
