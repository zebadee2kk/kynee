# MCP Integration Plan for KYNEĒ

## Executive Summary

MCP can revolutionize KYNEĒ's AI-assisted penetration testing workflows by providing standardized interfaces for security tool orchestration, secure data collection, and real-time threat intelligence integration.

## Why MCP for KYNEĒ

### Current Security Challenge
Penetration testing tools generate diverse data formats requiring custom parsing and integration logic for each AI assistant analyzing results.

### MCP Security Benefits
1. **Standardized Tool Interface:** One integration for all security tools
2. **Air-Gapped Operation:** MCP servers run locally on assessment networks
3. **Audit Trail:** All AI interactions logged through MCP protocol
4. **Access Control:** Per-tool permissions via MCP server configuration

## Recommended MCP Servers for KYNEĒ

### 1. Filesystem MCP Server (for Tool Output)
**Repository:** `modelcontextprotocol/servers` (filesystem)  
**Security Use Case:**
- Secure access to scan results (nmap, BloodHound, etc.)
- Read-only access to target information
- Sandboxed environment for AI analysis

**Configuration:**
```json
{
  "mcpServers": {
    "pentest-data": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/opt/kynee/results"],
      "env": {
        "ALLOWED_OPERATIONS": "read"
      }
    }
  }
}
```

### 2. Custom Security Tools MCP Server
**Purpose:** Execute authorized security tools with AI oversight

**Exposed Tools:**
- `run_nmap_scan` - Network reconnaissance
- `execute_bloodhound` - AD enumeration
- `analyze_vulnerabilities` - Result aggregation
- `generate_report` - AI-assisted documentation

**Safety Features:**
- Authorization checks before tool execution
- Scope validation (target whitelisting)
- Rate limiting and resource controls
- Full audit logging

### 3. SQLite MCP Server (Engagement Database)
**Use Case:** Store and query engagement data
- Target inventory
- Discovered vulnerabilities
- Remediation tracking
- Compliance evidence

### 4. GitHub MCP Server (for Reporting)
**Integration:** Automated security report generation
- Create private repos for each engagement
- AI-generated findings documentation
- Issue tracking for remediation

## Custom KYNEĒ MCP Server Architecture

### kynee-mcp Server Design

```python
# kynee-mcp/server.py
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent
import subprocess
import json
from pathlib import Path

app = Server("kynee")

# Tool definitions
SECURITY_TOOLS = {
    "nmap": {
        "binary": "/usr/bin/nmap",
        "allowed_args": ["-sV", "-sC", "-p-", "-A"],
        "requires_auth": True
    },
    "bloodhound": {
        "binary": "/opt/bloodhound/sharphound",
        "allowed_args": ["--CollectionMethods", "All"],
        "requires_auth": True
    }
}

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="run_authorized_scan",
            description="Execute authorized security scan with scope validation",
            inputSchema={
                "type": "object",
                "properties": {
                    "tool": {"type": "string", "enum": ["nmap", "bloodhound"]},
                    "target": {"type": "string"},
                    "args": {"type": "array"},
                    "engagement_id": {"type": "string"}
                },
                "required": ["tool", "target", "engagement_id"]
            }
        ),
        Tool(
            name="analyze_scan_results",
            description="AI-powered analysis of security scan output",
            inputSchema={
                "type": "object",
                "properties": {
                    "scan_file": {"type": "string"},
                    "analysis_type": {"type": "string"}
                },
                "required": ["scan_file"]
            }
        ),
        Tool(
            name="validate_scope",
            description="Check if target is within authorized engagement scope",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string"},
                    "engagement_id": {"type": "string"}
                },
                "required": ["target", "engagement_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "run_authorized_scan":
        # Validate engagement authorization
        if not await validate_engagement(arguments["engagement_id"]):
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Unauthorized engagement"})
            )]
        
        # Validate target in scope
        if not await check_scope(arguments["target"], arguments["engagement_id"]):
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Target out of scope"})
            )]
        
        # Execute tool with sanitized arguments
        result = await execute_security_tool(
            arguments["tool"],
            arguments["target"],
            arguments.get("args", [])
        )
        
        # Log to audit trail
        await log_security_event({
            "action": "scan_executed",
            "tool": arguments["tool"],
            "target": arguments["target"],
            "engagement": arguments["engagement_id"],
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return [TextContent(type="text", text=json.dumps(result))]
    
    elif name == "analyze_scan_results":
        # Read scan output and perform AI analysis
        scan_data = await read_scan_file(arguments["scan_file"])
        analysis = await ai_analyze_security_data(scan_data)
        return [TextContent(type="text", text=json.dumps(analysis))]
    
    # ... other tool implementations
```

## Security-Specific MCP Features

### Authorization Framework
```json
// engagement-authorization.json
{
  "engagement_id": "ENG-2026-001",
  "client": "Acme Corp",
  "authorized_scope": [
    "192.168.1.0/24",
    "*.acmecorp.internal",
    "app.acmecorp.com"
  ],
  "authorized_tools": ["nmap", "bloodhound", "burpsuite"],
  "ai_assistants": ["claude", "local-ollama"],
  "start_date": "2026-03-01",
  "end_date": "2026-03-15",
  "report_repo": "github.com/zebadee2kk/pentest-acme-2026"
}
```

### Audit Logging via MCP
All AI interactions with security tools are logged:
```json
{
  "timestamp": "2026-02-25T19:15:00Z",
  "mcp_server": "kynee",
  "tool": "run_authorized_scan",
  "ai_assistant": "claude-3.5-sonnet",
  "engagement_id": "ENG-2026-001",
  "action": "nmap_scan",
  "target": "192.168.1.100",
  "result": "success",
  "findings_count": 12
}
```

## Integration with Existing KYNEĒ Workflow

### Before MCP
```
Pentester → Manual tool execution → Manual result parsing → Claude API → Manual report
```

### With MCP
```
Pentester → Engagement setup → AI Assistant (via MCP) → Automated tool execution + analysis → Real-time reporting
```

### Workflow Benefits
1. **Real-time AI Analysis:** Results analyzed as scans complete
2. **Scope Enforcement:** AI cannot execute out-of-scope actions
3. **Multi-AI Support:** Use Claude for advanced analysis, local Ollama for offline/sensitive work
4. **Automated Documentation:** AI generates findings as they're discovered

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Install MCP Python SDK on KYNEĒ portable environment
- [ ] Create custom kynee-mcp server with authorization framework
- [ ] Implement scope validation and audit logging
- [ ] Test with read-only filesystem access to sample scans

### Phase 2: Tool Integration (Week 3-4)
- [ ] Integrate nmap with MCP tool interface
- [ ] Add BloodHound data collection via MCP
- [ ] Implement vulnerability aggregation tools
- [ ] Create engagement database (SQLite MCP)

### Phase 3: AI Assistant Integration (Week 5-6)
- [ ] Configure Claude Desktop with kynee-mcp
- [ ] Test Ollama local models via MCP (air-gapped mode)
- [ ] Build AI-assisted finding documentation workflows
- [ ] Integrate with GitHub MCP for report generation

### Phase 4: Advanced Features (Week 7-8)
- [ ] Real-time vulnerability prioritization via AI
- [ ] Automated exploit suggestion (within scope)
- [ ] AI-powered remediation guidance
- [ ] Integration with echo-vault for knowledge retention

## Security Hardening

### MCP Server Security
1. **Input Validation:** All tool arguments sanitized
2. **Scope Enforcement:** Target validation before every operation
3. **Resource Limits:** Rate limiting and execution timeouts
4. **Privilege Separation:** MCP server runs with minimal permissions
5. **Audit Trail:** Immutable logs of all AI-driven actions

### Air-Gapped Operation
- kynee-mcp runs on isolated assessment network
- No external MCP server dependencies for core operations
- Local Ollama integration for offline AI analysis
- Results exported only through authorized channels

## Compliance Benefits

### Audit Requirements
- **CREST/Tiger:** Full audit trail of all testing activities
- **ISO 27001:** Documented AI-assisted processes
- **SOC 2:** Access controls and authorization checks

### Evidence Collection
MCP audit logs provide:
- Timestamped record of all scan executions
- AI assistant decision rationale
- Scope validation evidence
- Tool version and configuration data

## Cost-Benefit Analysis

### Time Savings
- **Manual scan analysis:** 4-6 hours/engagement → 30 minutes with AI
- **Report generation:** 8-12 hours → 2 hours with AI assistance
- **Finding prioritization:** 2 hours → 15 minutes real-time

### Quality Improvements
- Consistent finding documentation
- Reduced false positives through AI correlation
- Faster turnaround for clients
- Enhanced remediation guidance

## Success Metrics

1. **Authorization Enforcement:** 100% scope validation before tool execution
2. **Audit Completeness:** Full logs for all AI-driven security actions
3. **Time Efficiency:** 50%+ reduction in engagement documentation time
4. **Multi-AI Support:** Successfully tested with Claude, ChatGPT, and Ollama
5. **Security:** Zero unauthorized scope violations

## References

- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/security)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [CREST Penetration Testing Guide](https://crest-approved.org)

## Next Steps

1. **Immediate:** Create sample engagement configuration for testing
2. **This Week:** Develop kynee-mcp server MVP with nmap integration
3. **Next Sprint:** Test with controlled scope environment
4. **Month 1:** Production deployment for internal engagements

---

**Document Status:** Ready for Security Review  
**Owner:** KYNEĒ Lead (AI-assisted)  
**Security Classification:** Internal Use  
**Last Updated:** 2026-02-25
