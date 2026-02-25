"""Unit tests for AuditLogWriter."""

import hashlib
import json
from pathlib import Path

import pytest

from kynee_agent.audit.writer import AuditLogWriter


class TestAuditLogWriter:
    """Test audit log writing and verification."""

    def test_create_audit_log(self, temp_dir):
        """Audit log file should be created."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        assert writer.log_path == log_path

    def test_log_event_creates_entry(self, temp_dir):
        """Logging event should create entry in file."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        entry_hash = writer.log_event(
            event_type="test_event",
            actor="test-agent",
            action="test_action",
            result="success",
        )

        assert entry_hash is not None
        assert log_path.exists()

        # Verify file content
        with open(log_path) as f:
            content = f.read().strip()
            entry = json.loads(content)

        assert entry["event_type"] == "test_event"
        assert entry["actor"] == "test-agent"
        assert entry["result"] == "success"

    def test_multiple_events_create_chain(self, temp_dir):
        """Multiple events should create hash chain."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        hash1 = writer.log_event(
            event_type="event1",
            actor="actor1",
            action="action1",
            result="success",
        )

        hash2 = writer.log_event(
            event_type="event2",
            actor="actor2",
            action="action2",
            result="success",
        )

        # Hashes should be different
        assert hash1 != hash2

        # Verify chain in file
        with open(log_path) as f:
            lines = f.readlines()

        entry1 = json.loads(lines[0])
        entry2 = json.loads(lines[1])

        # Second entry should reference hash of first entry (not first's previous_hash)
        entry1_json = json.dumps(entry1, separators=(",", ":"), sort_keys=True)
        entry1_hash = hashlib.sha256(entry1_json.encode()).hexdigest()
        assert entry2["previous_hash"] == entry1_hash

    def test_log_event_with_details(self, temp_dir):
        """Event should include custom details."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        details = {"scan_id": "123", "targets": 3}
        writer.log_event(
            event_type="scan_completed",
            actor="agent-1",
            action="scan_completed",
            result="success",
            details=details,
        )

        with open(log_path) as f:
            entry = json.loads(f.read())

        assert entry["details"] == details

    def test_log_scan_started(self, temp_dir):
        """Should log scan start events."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        target = {"ip": "192.168.1.1", "port": 22}
        writer.log_scan_started(
            agent_id="agent-1",
            scan_id="scan-001",
            method="network-scanning",
            target=target,
        )

        with open(log_path) as f:
            entry = json.loads(f.read())

        assert entry["event_type"] == "scan_started"
        assert entry["actor"] == "agent-1"
        assert entry["details"]["scan_id"] == "scan-001"

    def test_log_scan_completed(self, temp_dir):
        """Should log scan completion events."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        writer.log_scan_completed(
            agent_id="agent-1",
            scan_id="scan-001",
            findings_count=5,
        )

        with open(log_path) as f:
            entry = json.loads(f.read())

        assert entry["event_type"] == "scan_completed"
        assert entry["details"]["findings_count"] == 5

    def test_log_policy_violation(self, temp_dir):
        """Should log policy violation events."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        target = {"ip": "8.8.8.8"}
        writer.log_policy_violation(
            agent_id="agent-1",
            violation_type="out_of_scope",
            target=target,
            reason="IP address not in authorized scope",
        )

        with open(log_path) as f:
            entry = json.loads(f.read())

        assert entry["event_type"] == "policy_violation"
        assert entry["result"] == "denied"

    def test_log_enrollment(self, temp_dir):
        """Should log enrollment events."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        writer.log_enrollment(
            agent_id="agent-1",
            console_url="https://console.example.com",
        )

        with open(log_path) as f:
            entry = json.loads(f.read())

        assert entry["event_type"] == "enrollment"
        assert entry["result"] == "success"

    def test_verify_integrity_empty_log(self, temp_dir):
        """Verify integrity on empty log should pass."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        assert writer.verify_integrity() is True

    def test_verify_integrity_valid_log(self, temp_dir):
        """Verify integrity on valid log should pass."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        writer.log_event(
            event_type="event1",
            actor="actor1",
            action="action1",
            result="success",
        )

        writer.log_event(
            event_type="event2",
            actor="actor2",
            action="action2",
            result="success",
        )

        # Should verify without error
        assert writer.verify_integrity() is True

    def test_verify_integrity_tampered_log(self, temp_dir):
        """Verify integrity should detect tampering."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        writer.log_event(
            event_type="event1",
            actor="actor1",
            action="action1",
            result="success",
        )

        # Tamper with log file
        with open(log_path, "r") as f:
            entry = json.loads(f.read())

        entry["previous_hash"] = "tampered"

        with open(log_path, "w") as f:
            f.write(json.dumps(entry) + "\n")

        # Create new writer to reload
        writer2 = AuditLogWriter(log_path)

        with pytest.raises(ValueError, match="Chain broken"):
            writer2.verify_integrity()

    def test_get_entries(self, temp_dir):
        """Should retrieve audit entries."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        for i in range(5):
            writer.log_event(
                event_type=f"event{i}",
                actor="actor",
                action="action",
                result="success",
            )

        entries = writer.get_entries()
        assert len(entries) == 5
        assert entries[0]["event_type"] == "event0"
        assert entries[-1]["event_type"] == "event4"

    def test_get_entries_limited(self, temp_dir):
        """Should retrieve limited audit entries."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        for i in range(10):
            writer.log_event(
                event_type=f"event{i}",
                actor="actor",
                action="action",
                result="success",
            )

        entries = writer.get_entries(count=3)
        assert len(entries) == 3
        assert entries[0]["event_type"] == "event7"
        assert entries[-1]["event_type"] == "event9"

    def test_log_persistence_across_instances(self, temp_dir):
        """Log should persist across writer instances."""
        log_path = temp_dir / "audit.log"

        # Write with first instance
        writer1 = AuditLogWriter(log_path)
        writer1.log_event(
            event_type="event1",
            actor="actor1",
            action="action1",
            result="success",
        )

        # Read with second instance
        writer2 = AuditLogWriter(log_path)
        entries = writer2.get_entries()

        assert len(entries) == 1
        assert entries[0]["event_type"] == "event1"

    def test_log_append_only_property(self, temp_dir):
        """Multiple events should append, not overwrite."""
        log_path = temp_dir / "audit.log"
        writer = AuditLogWriter(log_path)

        writer.log_event("event1", "actor", "action", "success")
        writer.log_event("event2", "actor", "action", "success")
        writer.log_event("event3", "actor", "action", "success")

        with open(log_path, "r") as f:
            lines = f.readlines()

        assert len(lines) == 3
