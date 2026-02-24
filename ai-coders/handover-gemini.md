# Handover: Gemini 1.5 Pro

## Profile
- **Strengths**: Google ecosystem, data analysis, BigQuery, Python ML/data science
- **Token Limit**: 1M tokens
- **Session Cost**: Variable (API pricing)
- **Best For**: Analytics queries, data pipeline design, schema optimization

---

## Current Sprint: Week 2 (Mar 3 - Mar 9, 2026)
**Theme**: Hardware Bring-Up + Minimal OS Image

### Assigned Tasks

#### 1. Data Schema Design
- [ ] **PostgreSQL Schema** (`console/backend/migrations/001_initial_schema.sql`)
  - Tables: users, engagements, devices, findings, audit_logs
  - Indexes: Optimize for common queries (find by engagement_id, time-range scans)
  - Constraints: Foreign keys, unique constraints, check constraints
  - Partitioning: `findings` table by engagement_id (scalability)

- [ ] **Schema Documentation** (`docs/architecture/database-schema.md`)
  - ER diagram (Mermaid syntax)
  - Table descriptions (purpose, size estimates)
  - Query patterns (common SELECT/INSERT/UPDATE operations)

#### 2. Analytics Queries
- [ ] **Reporting Views** (`console/backend/app/services/analytics.py`)
  - View 1: "Top 10 vulnerable hosts per engagement"
  - View 2: "Findings by severity over time" (time series)
  - View 3: "Agent uptime and scan frequency"
  - View 4: "AI suggestion approval rate"
  - Implementation: SQLAlchemy ORM or raw SQL

- [ ] **Export Functions**
  - CSV export: Findings for Excel analysis
  - JSON export: Findings for external tools (Splunk, ELK)
  - PDF export: Executive summary (use ReportLab)

#### 3. Data Pipeline
- [ ] **Findings Ingestion** (`console/backend/app/services/ingest.py`)
  - Validate: Incoming JSON against `schemas/findings.schema.json`
  - Deduplicate: Check for duplicate findings (hash of target + finding type)
  - Enrich: GeoIP lookup, reverse DNS, WHOIS
  - Store: PostgreSQL + optional BigQuery (future)

- [ ] **Audit Log Chain Verification**
  - Function: `verify_audit_chain(engagement_id: str) -> bool`
  - Check: Hash chain integrity (no gaps, no tampering)
  - Alert: If chain broken, flag engagement for review

#### 4. Performance Optimization
- [ ] **Query Performance Analysis**
  - Tool: EXPLAIN ANALYZE on slow queries
  - Identify: Missing indexes, sequential scans, N+1 queries
  - Fix: Add indexes, rewrite queries, use joins vs. subqueries
  - Document: `docs/ops/database-performance.md`

- [ ] **Bulk Insert Optimization**
  - Problem: Agent sends 1000+ findings per scan
  - Solution: Batch inserts, COPY command, or bulk ORM operations
  - Benchmark: Compare throughput (findings/sec)

#### 5. Data Retention Policy
- [ ] **Retention Script** (`scripts/data-retention.py`)
  - Policy: Delete findings older than 90 days (per ETHICAL_USE_POLICY)
  - Implementation: Cron job, soft delete (mark as deleted), or hard delete
  - Logging: Record what was deleted (audit trail)
  - Backup: Ensure backups exist before deletion

---

## Context

**Project State**:
- Week 1: Schemas defined (Haiku)
- Week 2: Implement database + analytics layer
- Week 2 (your role): Design efficient data storage and queries

**Your Mission**:
- Ensure console can handle 10K+ findings per engagement
- Optimize for fast queries (dashboards, reports)
- Prepare for future BigQuery integration (if console scales to SaaS)

**Why You**:
- Strong at SQL, data modeling, analytics
- 1M context allows reviewing entire schema + sample data
- Google ecosystem expertise (if BigQuery needed later)

---

## Files to Create

```
console/backend/
├── migrations/
│   └── 001_initial_schema.sql
├── app/services/
│   ├── analytics.py
│   └── ingest.py

scripts/
└── data-retention.py

docs/
├── architecture/database-schema.md
└── ops/database-performance.md
```

---

## Example: Database Schema

```sql
CREATE TABLE engagements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_name TEXT NOT NULL,
  start_date TIMESTAMPTZ NOT NULL,
  end_date TIMESTAMPTZ NOT NULL,
  roe_document_path TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE findings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  engagement_id UUID NOT NULL REFERENCES engagements(id) ON DELETE CASCADE,
  timestamp TIMESTAMPTZ NOT NULL,
  type TEXT NOT NULL,
  severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
  target TEXT NOT NULL,
  details JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
) PARTITION BY LIST (engagement_id);

CREATE INDEX idx_findings_engagement_id ON findings(engagement_id);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_findings_timestamp ON findings(timestamp);
CREATE INDEX idx_findings_details_gin ON findings USING gin(details);
```

---

## Success Criteria

- [ ] Schema created, all tables have primary/foreign keys
- [ ] Sample data (1000 findings) inserts in <1 second
- [ ] Analytics queries return in <500ms
- [ ] Audit chain verification function works correctly
- [ ] Data retention script tested on staging database
- [ ] Performance doc lists 5+ optimization tips

---

## Constraints

**Token Budget**:
- This sprint: ~100K tokens (schema + queries + optimization)
- Single session sufficient

**Time Estimate**:
- 6-8 hours

**Dependencies**:
- JSON schemas (Haiku, Week 1)
- Console backend skeleton (Sonnet, Week 5)

---

## Blockers

None currently.

---

## Notes for Future Sprints

**Future Tasks**:
- Week 5: Integrate analytics into console UI (charts, dashboards)
- Week 8: Optimize for beta testing load (stress test)

**When to Call Gemini**:
- "Design a database schema for X"
- "Optimize this SQL query"
- "Write analytics code for Y"
- "Export data to Z format"

---

## Handoff to Other AIs

**After completing this sprint**:

→ **Sonnet**: Implement `analytics.py` and `ingest.py` functions  
→ **Haiku**: Create sample SQL queries for testing  
→ **ChatGPT**: Document database schema in user guide  

---

**Status**: 🔵 QUEUED (starts Mar 3)  
**Last Updated**: February 24, 2026  
**Next Review**: March 9, 2026
