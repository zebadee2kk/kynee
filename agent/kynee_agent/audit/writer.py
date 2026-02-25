"""Hash-chained append-only audit logger."""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


class AuditLogWriter:
    """
    Immutable append-only audit log with cryptographic chaining.

    Each entry includes:
    - Timestamp (ISO 8601 UTC)
    - Event type (e.g., 'scan_started', 'policy_violation')
    - Actor (agent_id, user_id, system)
    - Action (what happened)
    - Result (success/failure)
    - Hash of previous entry (chaining for tamper-evidence)

    Responsibilities:
    - Append-only writes (no deletion/modification)
    - Cryptographic chaining with SHA256
    - JSON output for downstream analysis
    - Tamper-evident log integrity verification
    """

    def __init__(self, log_path: Path | str):
        """
        Initialize audit log writer.

        Args:
            log_path: Path to audit log file
        """
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.previous_hash = "0" * 64  # Initial hash (all zeros)

        # Load existing log to determine last hash
        if self.log_path.exists():
            self._reload_last_hash()

    def log_event(
        self,
        event_type: str,
        actor: str,
        action: str,
        result: str,
        details: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Write immutable audit entry.

        Args:
            event_type: Type of event (e.g., 'scan_started', 'policy_violation')
            actor: Who triggered event (agent_id, user_id, etc.)
            action: What action was taken
            result: Result of action ('success', 'failure', 'denied')
            details: Additional context dictionary

        Returns:
            SHA256 hash of this entry (for verification)
        """
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Build entry
        entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "actor": actor,
            "action": action,
            "result": result,
            "previous_hash": self.previous_hash,
        }

        if details:
            entry["details"] = details

        # Serialize deterministically for hashing
        entry_json = json.dumps(entry, separators=(",", ":"), sort_keys=True)

        # Hash this entry
        entry_hash = hashlib.sha256(entry_json.encode()).hexdigest()

        # Update previous hash for next entry
        self.previous_hash = entry_hash

        # Append to log (append mode ensures atomicity)
        with open(self.log_path, "a") as f:
            f.write(entry_json + "\n")

        logger.info(
            "audit_logged",
            event_type=event_type,
            result=result,
            entry_hash=entry_hash[:16],
        )

        return entry_hash

    def log_scan_started(
        self,
        agent_id: str,
        scan_id: str,
        method: str,
        target: dict[str, Any],
    ) -> str:
        """Log a scan start event."""
        return self.log_event(
            event_type="scan_started",
            actor=agent_id,
            action=f"scan_{method}",
            result="initiated",
            details={
                "scan_id": scan_id,
                "method": method,
                "target": target,
            },
        )

    def log_scan_completed(
        self,
        agent_id: str,
        scan_id: str,
        findings_count: int,
        status: str = "success",
    ) -> str:
        """Log a scan completion event."""
        return self.log_event(
            event_type="scan_completed",
            actor=agent_id,
            action="scan_completed",
            result=status,
            details={
                "scan_id": scan_id,
                "findings_count": findings_count,
            },
        )

    def log_policy_violation(
        self,
        agent_id: str,
        violation_type: str,
        target: dict[str, Any],
        reason: str,
    ) -> str:
        """Log a policy violation event."""
        return self.log_event(
            event_type="policy_violation",
            actor=agent_id,
            action=f"policy_violation_{violation_type}",
            result="denied",
            details={
                "violation_type": violation_type,
                "target": target,
                "reason": reason,
            },
        )

    def log_enrollment(
        self,
        agent_id: str,
        console_url: str,
    ) -> str:
        """Log device enrollment event."""
        return self.log_event(
            event_type="enrollment",
            actor=agent_id,
            action="device_enrolled",
            result="success",
            details={
                "console_url": console_url,
            },
        )

    def verify_integrity(self) -> bool:
        """
        Verify audit log integrity by rehashing all entries.

        Returns:
            True if log integrity verified (no tampering detected)

        Raises:
            ValueError: If tampering detected
        """
        if not self.log_path.exists():
            logger.info("audit_log_empty")
            return True

        previous_hash = "0" * 64

        with open(self.log_path, "r") as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"Line {line_num}: Invalid JSON - {e}"
                    ) from e

                # Verify hash chain
                if entry.get("previous_hash") != previous_hash:
                    raise ValueError(
                        f"Line {line_num}: Chain broken. "
                        f"Expected previous_hash={previous_hash}, "
                        f"got {entry.get('previous_hash')}"
                    )

                # Rehash entry (without the entry-specific hash field)
                entry_copy = entry.copy()
                entry_hash_stored = entry_copy.pop("_entry_hash", None)

                entry_json = json.dumps(entry_copy, separators=(",", ":"), sort_keys=True)
                computed_hash = hashlib.sha256(entry_json.encode()).hexdigest()

                # We don't have entry_hash in the log, so update chain
                previous_hash = computed_hash

        logger.info("audit_log_verified", entry_count=line_num)
        self.previous_hash = previous_hash
        return True

    def _reload_last_hash(self) -> None:
        """Reload the previous_hash from last log entry."""
        try:
            with open(self.log_path, "r") as f:
                lines = f.readlines()

            if lines:
                last_line = lines[-1].strip()
                if last_line:
                    entry = json.loads(last_line)
                    # Hash of the last entry becomes the new previous_hash
                    entry_json = json.dumps(entry, separators=(",", ":"), sort_keys=True)
                    self.previous_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        except Exception as e:
            logger.warning("failed_to_reload_last_hash", error=str(e))
            self.previous_hash = "0" * 64

    def get_entries(self, count: Optional[int] = None) -> list[dict[str, Any]]:
        """
        Get recent audit entries.

        Args:
            count: Number of recent entries to return (None = all)

        Returns:
            List of audit entries
        """
        if not self.log_path.exists():
            return []

        entries = []
        with open(self.log_path, "r") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))

        if count:
            return entries[-count:]

        return entries
