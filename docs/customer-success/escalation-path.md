# Escalation Path for Beta Issues

**Version:** 1.0
**Launch Period:** March 24 - March 31, 2026

---

## Overview

This document defines the escalation path for issues reported by beta users, ensuring P0 blockers are resolved quickly and lower-priority issues are routed to the right owners with clear SLAs.

---

## Issue Severity Levels

| Severity | Description | Examples | Response SLA | Resolution SLA |
|-----------|-------------|-------------|-----------------|
| P0 - Critical | System down, data loss, security breach | 30 min | 2 hours |
| P1 - Major | Core feature broken, severe UX friction | 2 hours | 24 hours |
| P2 - Minor | Edge case bug, non-core feature issue | 8 hours | 72 hours |
| P3 - Trivial | Cosmetic issue, minor UX improvement | 24 hours | 14 days |

---

## Escalation Flow

### Level 0: Automated Triage

**Who:** Workflow-runner (auto)

**When:** Issue reported via any channel

**Action:**
1. Categorize by keywords (bug / feature / ux)
2. Assign severity (P0-P3) based on patterns
3. Route to Level 1 owner

---

### Level 1: Customer Success

**Owner:** CSM

**When:** All incoming issues first

**SLA:** Respond within 2-4 hours (depending on severity)

**Actions:**
- Acknowledge receipt
- Gather more details if needed
- Attempt quick resolution for P2-P3 (documentation, guidance)
- Escalate to Level 2 for P0-P1

**Authority:** Can resolve P2-P3, escalate P0-P1

---

### Level 2a: Engineering (Bugs)

**Owner:** dev

**When:** P0-P1 bugs escalated from Level 1

**SLA:** Acknowledge in 30 min, resolve per severity SLA

**Actions:**
- Reproduce bug
- Fix and test
- Deploy to staging/production
- Confirm resolution with user

**Authority:** Can resolve all bugs, escalates architecture issues to CTO

---

### Level 2b: Product (Features/UX)

**Owner:** CPO / PM

**When:** Feature requests, UX feedback escalated from Level 1

**SLA:** Acknowledge in 2 hours, triage in 24 hours

**Actions:**
- Evaluate against roadmap
- Estimate effort
- Prioritize for post-beta or immediate iteration

**Authority:** Can commit to roadmap items, escalates strategic decisions to CEO

---

### Level 3: Architecture/Strategic

**Owner:** CTO (architecture), CEO (strategic)

**When:** Complex issues requiring higher-level decisions

**SLA:** Acknowledge in 1 hour, decision in 24 hours

**Actions (CTO):**
- Technical veto if unsafe
- Architecture decision for complex bugs
- Resource allocation for fixes

**Actions (CEO):**
- Strategic priority decisions
- Go/No-Go on feature work
- Resource/budget approval

---

## Escalation Triggers

### Automatic Escalation (System-Triggered)

Escalate to next level if:
- ⚠️ Response SLA exceeded (no acknowledgment)
- ⚠️ Resolution SLA exceeded (no fix)
- ⚠️ User re-opens issue (not resolved)
- ⚠️ 3+ users report same issue (cluster)

### Manual Escalation (Owner-Triggered)

Owner can escalate if:
- 🔴 Issue is outside their authority
- 🔴 Issue requires cross-team coordination
- 🔴 Issue is blocked on another owner
- 🔴 User is escalating to CEO/Eduard

---

## Escalation Communication

### When Escalating

**Format:**
```
[ESCALATION] P{X} - {Brief Title}
Original Reporter: {User}
Issue Summary: {1-2 sentences}
Escalation Reason: {Why this needs higher level}
Suggested Owner: {Who should handle this}
```

**Channel:** c-suite-chat.jsonl + DM to next owner

**Example:**
```
[ESCALATION] P0 - Database down for 3 users
Original Reporter: user@example.com
Issue Summary: Users cannot access memories - getting 500 errors
Escalation Reason: Level 1 cannot resolve - requires dev investigation
Suggested Owner: dev
```

---

## SLA Monitoring

### Daily SLA Check (CSM)

At 10:00 EET daily:
1. Review all open issues
2. Flag any approaching SLA breach (<2 hours remaining)
3. Escalate if SLA at risk

### Weekly SLA Report (COO)

Sundays:
1. SLA compliance rate (met / total)
2. Avg. response time by severity
3. Avg. resolution time by severity
4. Escalations by owner

**Target:** 95% SLA compliance rate

---

## Emergency Contacts

| Severity | Contact | Method |
|-----------|----------|--------|
| P0 (Critical) | Eduard (CEO) | Telegram/DM (2h max) |
| P0 (Critical) | dev | c-suite-chat + Slack/DM |
| P1 (Major) | CSM | Email (4h max) |
| P1 (Major) | CPO / dev | c-suite-chat (24h max) |
| P2-P3 | CSM | Email (24h max) |

---

## Beta-Specific Considerations

### Beta Grace Period

For first 24 hours of beta (Mar 24-25):
- Treat all issues as P1 (elevated from actual severity)
- CSM responds to all feedback within 1 hour
- Post-mortem for any P0/P1 at beta end

### Beta Feedback vs. Production Support

**Beta Feedback (D1-D30):**
- Focus on learning, not just fixing
- Collect for product iteration
- Document all feedback even if not acted on immediately

**Production Support (Post-Beta):**
- Focus on stability, uptime
- Fix quickly, minimize disruption
- Standard SLAs apply

---

*Last Updated: March 21, 2026*
