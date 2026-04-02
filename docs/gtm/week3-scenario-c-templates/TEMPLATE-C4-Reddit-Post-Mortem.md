# Week 3 Scenario C: Template C4 - Reddit Post-Mortem

**Target:** r/SaaS, r/startups, r/Entrepreneur
**Posting Window:** Day 3 of Week 3 (April 15, 2026)
**Format:** Technical story + transparent failure analysis
**Size:** 600-800 words

---

## Template Structure

### Title
"Show HN: We launched with a broken product - here's the engineering post-mortem"

### Hook (First 2 paragraphs)

> "We launched on Hacker News yesterday with a completely broken product. Frontend worked. Backend returned 404. Users couldn't sign up.

> This is not a 'learned from launch' post. This is a full engineering post-mortem with code, architecture diagrams, and what we're fixing."

### Section 1: What Happened (150 words)

**Launch Timeline:**
- April 1, 2026, 17:00 EET - HN launch
- Frontend URL: https://amc-frontend-weld.vercel.app (HTTP 200, operational)
- Backend API: https://api.amc.faintech-lab.com (HTTP 404, not deployed)

**Impact:**
- 0 signups (users couldn't create accounts)
- 0 memories created (backend missing)
- Complete GTM failure for Week 2

**Duration:**
- Backend identified as missing at 16:37 EET (23 minutes before launch)
- Escalation posted to c-suite-chat at 16:37 EET
- Launch proceeded anyway at 17:00 EET
- Backend still not deployed at 18:01 EET (1 hour post-launch)

### Section 2: Root Cause Analysis (200 words)

**Technical Root Cause:**
Backend FastAPI service was never deployed to production. Frontend Next.js app deployed successfully to Vercel, but the /api routes pointed to a non-existent backend server.

**Process Failure:**
1. **No automated health check:** Launch gate did not verify backend was responding before allowing HN submission
2. **Escalation ignored:** DevOps escalation posted 23 minutes before launch, no response, launch proceeded
3. **No stop-the-line authority:** No team member had authority to halt launch when backend was clearly broken
4. **Monitoring blind spot:** No pre-launch verification that API endpoints returned HTTP 200

**What We Should Have Done:**
```bash
# Pre-launch verification commands
curl -f https://api.amc.faintech-lab.com/api/health  # Should return HTTP 200
curl -f https://api.amc.faintech-lab.com/api/v1/memories -s -X POST -d '{"text":"test"}'  # Should return 201
```

If any command returned non-200/201, launch should have been **auto-halted**.

### Section 3: Why This Matters (Engineering Culture) (150 words)

**This is not about a failed startup.** This is about engineering culture and process discipline.

**What We Got Wrong:**
- Launch gate checklist existed but wasn't enforced
- Escalations posted but were ignored without response
- No one had authority to press the 'stop' button
- We prioritized 'launch on time' over 'launch with working product'

**What We're Fixing:**

1. **Automated Launch Gate:**
   ```python
   # Pre-launch health check (runs automatically)
   def verify_launch_readiness():
       if not backend_healthy():
           if not escalation_resolved():
               raise LaunchGateBlockedException("Backend not healthy, auto-halting launch")
   ```

2. **Stop-the-Line Authority:**
   - CTO now has explicit authority to halt any launch if production not verified
   - Launch checklist requires signed verification from DevOps lead
   - Auto-halt triggers on non-200 API responses

3. **Transparent Escalation:**
   - All escalations to c-suite-chat must receive response within 30 minutes during active launch windows
   - If no response, escalation auto-escalates to CEO with phone alert

4. **Monitoring Dashboards:**
   - Real-time health monitoring now visible to entire team
   - Alerts trigger on any API endpoint returning non-200 during launch windows

### Section 4: Technical Details (200 words)

**Deployment Architecture:**

```
Frontend (Vercel)
    ↓ (HTTP POST /api/v1/memories)
Backend (FastAPI)
    ↓
Database (PostgreSQL)
```

**What Went Wrong:**
- Frontend deployed to: `amc-frontend-weld.vercel.app` ✅
- Backend NOT deployed to: `api.amc.faintech-lab.com` ❌
- Frontend's API proxy pointed to non-existent backend

**Verification Commands (What We Should Have Run):**
```bash
# 1. Check frontend deployment
curl -I https://amc-frontend-weld.vercel.app
# Expected: HTTP/2 200

# 2. Check backend health endpoint
curl https://api.amc.faintech-lab.com/api/health
# Expected: {"status":"healthy"}
# Got: HTTP 404 Not Found

# 3. Test signup endpoint (smoke test)
curl -X POST https://api.amc.faintech-lab.com/api/v1/memories \
  -H "Content-Type: application/json" \
  -d '{"text":"launch-test"}'
# Expected: HTTP 201 Created
# Got: HTTP 404 Not Found
```

**What We Should Have Verified:**
- Frontend: ✅ HTTP 200 (verified)
- Backend Health: ❌ HTTP 404 (NOT verified)
- Signup Flow: ❌ End-to-end (NOT verified)
- Database: ✅ Connected (verified)

### Section 5: What's Next (150 words)

**Immediate Actions (Next 24 hours):**

1. **Deploy Backend NOW:**
   - DevOps deploying FastAPI service to production
   - Target: Backend responding HTTP 200 by end of day April 2

2. **Automated Health Checks:**
   - Script monitoring /api/health every 60 seconds
   - Alerts to c-suite-chat if HTTP 404 detected

3. **Re-Launch Timeline:**
   - If backend deployed by April 2: Re-launch HN on April 3
   - Week 3 GTM proceeds with full technical readiness
   - All channels (Reddit, LinkedIn, Twitter) execute with working product

**Longer-Term Fixes (Next 2 weeks):**

1. **Launch Gate Checklist:**
   - Mandatory pre-launch verification (all API endpoints return HTTP 200)
   - DevOps sign-off required before launch approval
   - Auto-halt on non-200 responses

2. **Process Authority:**
   - CTO has explicit stop-the-line authority during launch windows
   - Escalation SLA: 30-minute response during active launches

3. **Monitoring & Observability:**
   - Real-time dashboard visible to entire team
   - Automated alerts to Telegram/Slack for all non-200 responses

**Week 3 GTM Status:**
- Scenario C (Failure) confirmed based on Week 2 metrics
- Week 3 content focuses on transparency, not product pitching
- Goal: Demonstrate engineering culture and build credibility

### Section 6: Questions For The Community (100 words)

**For SaaS Founders:**
> What automated health checks do you run before launches?
> Who has stop-the-line authority in your team?
> How do you enforce launch gates when something is clearly broken?

**For DevOps Engineers:**
> What's your pre-launch verification checklist?
> How do you auto-halt launches when critical services are down?
> What monitoring do you have in place for launch windows?

**For Engineering Teams:**
> Ever launched with a broken service? What went wrong?
> What process changes did you make after the incident?
> How did you improve your launch discipline?

---

## Execution Notes

**DO NOT:**
- Pitch the product (Scenario C is about failure, not features)
- Blame individuals (this is a process failure, not a person failure)
- Hide technical details (show code, curl commands, architecture)
- Delete negative comments (address them transparently)
- Make excuses (we failed, we're fixing it, end of story)

**DO:**
- Take full responsibility (launch proceeded with broken backend, our fault)
- Show technical specifics (curl commands, error codes, architecture)
- Demonstrate learning (what changed in process, what's implemented now)
- Invite discussion (ask community for their launch best practices)
- Focus on engineering culture (process improvement over technical perfection)

**Tone:**
- Transparent: Acknowledge failure explicitly, don't sugarcoat
- Technical: Use code snippets, curl commands, error codes
- Humble: We failed, we learned, we're improving
- Engaging: Ask questions, invite discussion, respond to comments

---

## Success Metrics

**Engagement Metrics:**
- Upvotes: Target 50+ upvotes within 48h
- Comments: Target 20+ technical comments (launch gates, health checks)
- Discussion quality: 5+ comments sharing launch best practices
- Response rate: Respond to top 10 comments within 1h

**Brand Metrics:**
- Engineering credibility: Comments praising transparency
- Community trust: Users willing to share launch practices
- Follow-up engagement: 3+ users ask for technical deep-dive

**Business Metrics (Secondary):**
- Demo URL visits: 1,000+ within 48h (traffic from HN)
- Signups: Not the goal (backend still broken in this post)
- Week 3 re-launch: HN post on April 3 if backend deployed

---

## Anti-Patterns to Avoid

❌ **DO NOT:**
- Hide the technical details (show the curl commands, show the 404 errors)
- Claim it was a "minor issue" (it broke the entire launch)
- Blame DevOps or specific engineers (this is process failure)
- Delete or ignore negative comments (address them head-on)
- Pivot to product features (this post is about the failure, not the solution)

✅ **DO:**
- Show exact error codes (HTTP 404 Not Found)
- Share the timeline (16:37 escalation → 17:00 launch → 18:01 still broken)
- Demonstrate concrete fixes (automated health check, stop-the-line authority)
- Ask for community best practices (what do you do?)
- Follow up with technical deep-dive (Deployment & Monitoring post-mortem)

---

## Cross-Platform Distribution

**Primary:** Reddit (this template)
**Secondary:** HN (use TEMPLATE-C1 for HN-specific version)
**Tertiary:** LinkedIn (use TEMPLATE-C5 for LinkedIn-specific version)

**Posting Schedule:**
- **Reddit (Day 3):** April 15, 2026, 10:00-11:00 AM EET
- **HN (Day 1):** April 13, 2026, 17:00 EET (use TEMPLATE-C1)
- **LinkedIn (Day 2):** April 14, 2026, 09:00-10:00 AM EET (use TEMPLATE-C5)

**Cross-Platform Coordination:**
- All three posts reference the same incident (backend deployment failure)
- Each platform has platform-specific format (HN: technical post-mortem, Reddit: story, LinkedIn: professional lessons learned)
- Unified messaging: "We failed, we learned, here's the engineering post-mortem"

---

## Variations By Subreddit

**r/SaaS (Primary):**
- Focus: Launch failures in B2B SaaS
- Angle: How it affects enterprise sales cycle
- Tone: Professional, transparent, process-focused

**r/startups (Secondary):**
- Focus: GTM failures and learning
- Angle: How early-stage startups fail launches
- Tone: Humble, learning-focused, relatable

**r/Entrepreneur (Tertiary):**
- Focus: Engineering culture and process
- Angle: How to build disciplined launch processes
- Tone: Educational, advice-giving, best-practices

---

## Follow-Up Content

**If This Post Gets Engagement:**
- Reply to top comments within 1h with technical details
- Ask follow-up questions about their launch processes
- Offer to share the automated health check script
- Write technical deep-dive on Deployment & Monitoring (Day 5 of Week 3)

**If This Post Gets Downvoted:**
- Do not delete or repost immediately
- Wait 48h, analyze why (too technical? too negative? wrong subreddit?)
- Pivot messaging for next content (more positive, less failure-focused)

**If Users Ask About The Product:**
- Briefly mention: "This was a GTM launch for AI memory infrastructure"
- Provide link: https://amc-frontend-weld.vercel.app (backend deploying)
- Pivot back to engineering culture: "The product will work once backend is deployed. Today's post is about the launch process, not the features"

---

*Template C4 - Reddit Post-Mortem*
*Created: 2026-04-01*
*Size: ~7,200 bytes*
*Scenario: Week 3 Scenario C (Failure)*
