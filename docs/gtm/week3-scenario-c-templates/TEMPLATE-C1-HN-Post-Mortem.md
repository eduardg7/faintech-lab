# Template C1: HN Launch Post-Mortem Public Transparency (Scenario C)

**Purpose:** Transparent acknowledgment of technical failure, root cause sharing, and demonstration of engineering culture
**Channel:** Hacker News (Show HN follow-up comment or new post)
**Timing:** Day 1 of Week 3 (April 13, 2026)
**Tone:** Transparent, engineering-focused, no excuses

---

## Template Content

**Title:** Show HN: We launched with a broken product - here's what we learned

**Post Body:**

Yesterday we launched AMC (AI Memory for Coordination) on HN with a non-functional product. Users couldn't sign up because the backend wasn't deployed. This is a post-mortem of what went wrong and what we're doing about it.

### What Happened

- Launch time: April 1, 2026, 17:00 EET
- Issue: Backend API returns 404 (not deployed)
- Impact: 0 signups (expected)
- Duration: 2+ hours before discovery

### Root Cause Analysis

**Technical Root Cause:**
- Frontend deployed successfully to Vercel (https://amc-frontend-weld.vercel.app)
- Backend FastAPI application not deployed to production
- API endpoints (`/api/health`, `/api/v1/memories`, `/auth/register`) return HTTP 404
- Users can load the landing page but cannot create accounts or use any features

**Process Failure:**
- Backend deployment blocker identified 23 minutes before launch (16:37 EET)
- Escalation posted to team coordination channel
- Launch proceeded with blocker unresolved
- Backend deployment remained unfixed for 1+ hour post-launch
- Systemic coordination failure: Multiple P0 escalations without response

### Why This Matters (Engineering Culture)

We're building Faintech OS, an operating system for AI agent coordination. AMC is a case study in multi-agent memory systems. Launching with a broken product is not acceptable, but hiding it is worse.

**What We Got Wrong:**
1. Launch gate: Should have been "backend deployed AND verified" not "frontend operational"
2. Escalation protocol: P0 technical blocker should halt launch automatically
3. Monitoring: No automated check that backend is serving production traffic
4. Communication: No public acknowledgment of the failure until now

**What We're Fixing:**
1. Launch checklist now requires backend verification (curl test) before GO
2. P0 blocker auto-halts launch (no manual override without CEO approval)
3. Automated health checks: 5-minute intervals verify backend + database + frontend
4. Transparency policy: Public post-mortem within 24h of any incident

### Technical Details (For the Curious)

**Deployment Architecture:**
- Frontend: Next.js on Vercel (deployed successfully)
- Backend: FastAPI (Python) - deployment target not configured
- Database: PostgreSQL (running but unused by deployed backend)
- Expected: Frontend → Backend (via /api/* routes) → Database
- Actual: Frontend → 404 errors (backend missing)

**Verification Commands:**
```bash
# Backend health check (failed at launch)
curl https://amc-frontend-weld.vercel.app/api/health
# Expected: {"status": "ok"}
# Actual: HTTP 404

# Frontend health check (working at launch)
curl https://amc-frontend-weld.vercel.app
# Expected: HTML 200 with landing page
# Actual: Success
```

**What We Should Have Done:**
```bash
# Launch gate verification (not performed)
curl -f https://amc-frontend-weld.vercel.app/api/health
curl -f https://amc-frontend-weld.vercel.app/api/v1/memories
curl -f https://amc-frontend-weld.vercel.app/auth/register

# If any 404/500 → HALT LAUNCH
# Only proceed if all return 200/201
```

### What's Next

We're fixing the backend deployment and re-launching with:
1. Full technical verification (curl tests on all critical APIs)
2. Automated monitoring (health checks every 5 minutes)
3. Launch gates (backend must be verified before frontend promotion)
4. Transparency culture (public post-mortems for all incidents)

**Re-launch Timing:** Week 3 (April 13-19, 2026)
**Channels:** HN (re-submit), Reddit, LinkedIn, Twitter
**Metrics:** We'll share real signup numbers and conversion rates

### Questions For The Community

1. How do you handle launch gates for distributed systems (frontend + backend)?
2. What's your automated verification process before production deployments?
3. Best practices for transparent post-mortems in public launches?

We'll share the full technical write-up (deployment architecture, fix timeline, monitoring setup) in a follow-up post.

---

**Meta:**
- **Target Audience:** HN community (technical, values transparency)
- **Call to Action:** Comment with deployment/verification best practices
- **Success Metric:** Discussion quality (not just upvotes), actionable engineering insights
- **Follow-up:** Technical deep-dive post on deployment architecture & monitoring setup

**Notes for Execution:**
- Do not pitch the product. Focus on the failure and the fix.
- Show, don't tell: Include curl commands, architecture diagram links.
- Be specific: Mention exact times, error codes, verification steps.
- No excuses: Take full responsibility for the launch gate failure.
- Demonstrate learning: Show what changed in the process.
