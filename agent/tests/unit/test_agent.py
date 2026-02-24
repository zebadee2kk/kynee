"""Unit tests for Agent core."""

import pytest

from kynee_agent.core import Agent


class TestAgent:
    """Tests for Agent class."""

    def test_agent_initialization(self) -> None:
        """Test agent initialization."""
        agent = Agent()
        assert agent.agent_id is not None
        assert agent.state == "initialized"

    def test_agent_with_custom_id(self) -> None:
        """Test agent initialization with custom ID."""
        custom_id = "test-agent-001"
        agent = Agent(agent_id=custom_id)
        assert agent.agent_id == custom_id

    def test_get_status(self) -> None:
        """Test agent status retrieval."""
        agent = Agent()
        status = agent.get_status()

        assert "agent_id" in status
        assert "state" in status
        assert "timestamp" in status
        assert "uptime_seconds" in status
        assert status["state"] == "initialized"

    @pytest.mark.asyncio
    async def test_agent_start_stop(self) -> None:
        """Test agent start/stop lifecycle."""
        agent = Agent()
        assert agent.state == "initialized"

        await agent.start()
        assert agent.state == "running"

        await agent.stop()
        assert agent.state == "stopped"

    @pytest.mark.asyncio
    async def test_execute_scan(self) -> None:
        """Test scan execution."""
        agent = Agent()
        job = {"job_id": "job-001", "target": "10.0.0.0/24"}

        result = await agent.execute_scan(job)
        assert result["job_id"] == "job-001"
        assert "status" in result
        assert "findings" in result
