/**
 * Type definitions for KYNEĒ Console
 */

export interface Agent {
  agent_id: string;
  status: string;
  enrolled_at?: string;
  last_heartbeat?: string;
}

export interface Finding {
  finding_id: string;
  engagement_id: string;
  agent_id: string;
  title: string;
  description: string;
  severity: "informational" | "low" | "medium" | "high" | "critical";
  category: string;
  status: "new" | "confirmed" | "false_positive" | "mitigated" | "accepted_risk";
  created_at: string;
}

export interface Engagement {
  engagement_id: string;
  client_name: string;
  start_time: string;
  end_time: string;
  status: string;
}
