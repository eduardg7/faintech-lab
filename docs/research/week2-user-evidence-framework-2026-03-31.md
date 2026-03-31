# Week 2 GTM User Evidence Collection Framework

**Created:** 2026-03-31 20:45 EET
**Owner:** faintech-user-researcher
**Purpose:** Systematic user evidence collection for Week 2 GTM execution (April 3-10)
**Goal:** Convert traffic insights into actionable improvements for 10-15 signups

---

## Executive Summary

Week 1 GTM failed with 0/5 signups despite healthy platform (100% tests, all agents active). Root cause: **external blockers + lack of user evidence collection**. Week 2 GTM has ready components (social: 67KB, UX: P0-P3 specs, technical: verified), but needs systematic user evidence collection to optimize conversion.

**This framework defines:**
- What evidence to collect (traffic, behavior, friction)
- How to collect it (tools, frequency, owners)
- How to use it (analysis triggers, action criteria)
- Success metrics (evidence → insight → action → conversion)

---

## Evidence Collection Dimensions

### 1. Traffic Sources (Where are users coming from?)

**Data points:**
- Referrer URLs (HN, Reddit, LinkedIn, direct)
- UTM parameters (campaign, source, medium)
- Geographic distribution (country, timezone)
- Device type (desktop, mobile, tablet)
- Time of visit (hour, day of week)

**Collection method:**
- Vercel Analytics (built-in)
- Custom UTM tracking (already configured in social content)
- Server-side logging (API request metadata)

**Frequency:** Real-time dashboard + daily summary

**Owner:** faintech-user-researcher

**Action trigger:**
- If >50% traffic from single source → Diversify channels
- If mobile traffic >40% → Prioritize P3 mobile optimization
- If geographic concentration → Consider timezone-specific posting

### 2. Behavioral Patterns (What are users doing?)

**Data points:**
- Landing page scroll depth (25%, 50%, 75%, 100%)
- Time on page (<30s, 30-60s, 1-3min, >3min)
- CTA click-through rate (primary, secondary CTAs)
- Navigation patterns (which sections visited)
- Exit points (where do they leave?)

**Collection method:**
- Vercel Analytics events
- Custom event tracking (CTA clicks, section views)
- Session recordings (Hotjar/FullStory if available, otherwise manual sampling)

**Frequency:** Real-time events + daily analysis

**Owner:** faintech-user-researcher

**Action trigger:**
- If scroll depth <50% for >70% visitors → Landing page clarity issue (P0)
- If CTA CTR <2% → Call-to-action optimization needed (P0)
- If exit at onboarding step 1 >60% → Onboarding flow friction (P1)

### 3. Conversion Funnel (Where are they dropping off?)

**Funnel stages:**
1. Landing page visit → Scroll to CTA (attention)
2. CTA click → Signup page (interest)
3. Signup form start → Signup form complete (commitment)
4. Email verification → First login (activation)
5. First memory write → First memory retrieve (value realization)

**Conversion targets (Week 2):**
- Stage 1→2: >15% (industry average: 10-20%)
- Stage 2→3: >60% (form completion rate)
- Stage 3→4: >80% (email verification rate)
- Stage 4→5: >70% (activation to value)

**Collection method:**
- Vercel Analytics funnel tracking
- Database queries (user creation, verification, first action timestamps)
- Event logging (form start, form complete, email sent, email clicked)

**Frequency:** Real-time funnel + daily cohort analysis

**Owner:** faintech-user-researcher + faintech-backend (data access)

**Action trigger:**
- If Stage 1→2 <10% → Landing page value prop unclear (P0)
- If Stage 2→3 <40% → Form friction (too many fields, unclear benefits)
- If Stage 3→4 <60% → Email deliverability or value prop issue
- If Stage 4→5 <50% → Onboarding fails to demonstrate value (P1)

### 4. Qualitative Feedback (Why are they behaving this way?)

**Data points:**
- Onboarding feedback (feedback widget already implemented)
- Exit intent surveys (why are you leaving?)
- Post-signup survey (what convinced you to sign up?)
- NPS score (would you recommend?)

**Collection method:**
- Feedback widget (already in place from design specs)
- Exit intent popup (implement if time permits, otherwise defer to Week 3)
- Email survey (send 24h after signup)

**Frequency:** Continuous collection + daily review

**Owner:** faintech-user-researcher

**Action trigger:**
- If >3 similar complaints → Create task for that friction point
- If positive feedback pattern emerges → Double down on that feature in marketing
- If NPS <30 → Fundamental product-market fit issue (escalate to CPO)

---

## Week 2 Evidence Collection Schedule

### Pre-Launch (April 1, before 17:00 EET)

**Actions:**
- [ ] Verify Vercel Analytics is enabled and tracking
- [ ] Test UTM parameters on all social content links
- [ ] Set up real-time dashboard (Vercel Analytics + custom metrics)
- [ ] Create daily evidence collection checklist (this document)
- [ ] Brief dev on data access requirements (backend queries for funnel stages)

**Evidence to collect:**
- Baseline metrics (current traffic, if any)
- Analytics configuration verification
- UTM parameter test results

### Launch Day (April 1, 17:00-23:59 EET)

**Actions:**
- [ ] Monitor real-time traffic every 2h
- [ ] Track HN submission performance (upvotes, comments, ranking)
- [ ] Record first visitor behavior patterns
- [ ] Note any immediate friction points (form errors, page loads)

**Evidence to collect:**
- Traffic volume by hour
- HN engagement metrics
- First visitor sessions (sample 5-10)
- Any technical issues reported

**Analysis trigger:** If <10 visitors in first 6h → HN launch failed, investigate why

### Days 2-3 (April 2-3)

**Actions:**
- [ ] Daily morning review: previous day's evidence (30 min)
- [ ] Identify top 3 friction points from behavioral data
- [ ] Review qualitative feedback (if any)
- [ ] Update P0-P3 optimization priorities based on evidence

**Evidence to collect:**
- Daily traffic summary (sources, volume, geography)
- Behavioral patterns (scroll depth, CTA CTR, exit points)
- Conversion funnel metrics (stages 1-5)
- Qualitative feedback compilation

**Analysis trigger:** If conversion rate <2% after 48h → Emergency optimization sprint

### Days 4-7 (April 4-7)

**Actions:**
- [ ] Continue daily evidence review (30 min)
- [ ] Reddit execution monitoring (April 4, 6 posts)
- [ ] Track Reddit traffic and engagement separately
- [ ] Compare HN vs Reddit traffic quality (conversion rates)

**Evidence to collect:**
- Channel-specific traffic (HN, Reddit, direct)
- Channel-specific conversion rates
- Reddit engagement metrics (upvotes, comments, click-through)
- Qualitative feedback from Reddit comments

**Analysis trigger:** If one channel outperforms by >2x → Shift focus to winning channel

### Days 8-10 (April 8-10)

**Actions:**
- [ ] Week 2 evidence synthesis (2h deep dive)
- [ ] Create Week 3 recommendations based on evidence
- [ ] Prepare user research report for C-suite review
- [ ] Document lessons learned for future GTM cycles

**Evidence to collect:**
- Complete Week 2 traffic and conversion data
- Channel performance comparison
- Top friction points and resolutions
- Qualitative feedback themes
- User interview candidates (if any signups agree to talk)

**Analysis trigger:** If <10 signups → Fundamental GTM strategy review needed

---

## Evidence → Action Mapping

### Scenario 1: High Traffic, Low Conversion (>100 visitors, <2% conversion)

**Evidence pattern:**
- Traffic sources healthy (HN, Reddit working)
- Scroll depth low (<50% for >70% visitors)
- CTA CTR low (<1%)
- Exit at landing page (>80%)

**Root cause hypothesis:** Value proposition unclear, landing page doesn't resonate

**Action:**
1. Review landing page copy against HN/Reddit messaging (consistency check)
2. A/B test headline (technical value vs business value)
3. Add social proof (if any early adopters exist)
4. Implement P0 landing page CTA optimization immediately

**Owner:** faintech-user-researcher (analysis) → faintech-frontend (implementation)

**Timeline:** Same-day implementation, 24h results check

### Scenario 2: Medium Traffic, Medium Conversion (50-100 visitors, 2-5% conversion)

**Evidence pattern:**
- Traffic moderate (HN or Reddit working, not both)
- Scroll depth good (>50% for >60% visitors)
- CTA CTR moderate (2-5%)
- Drop-off at signup form (Stage 2→3 <50%)

**Root cause hypothesis:** Form friction, unclear signup benefits

**Action:**
1. Simplify signup form (reduce fields if possible)
2. Add benefit messaging near form (what you get after signup)
3. Implement social login (Google, GitHub) if not already present
4. A/B test form copy (technical vs business benefits)

**Owner:** faintech-user-researcher (analysis) → faintech-frontend (implementation)

**Timeline:** 48h implementation, 48h results check

### Scenario 3: Low Traffic, High Conversion (<50 visitors, >5% conversion)

**Evidence pattern:**
- Traffic low (external blockers still affecting reach)
- Conversion healthy (those who visit, convert)
- Scroll depth high (>75% for >50% visitors)
- CTA CTR high (>5%)

**Root cause hypothesis:** Product-market fit exists, but distribution blocked

**Action:**
1. Focus on removing external blockers (HUNTER_API_KEY, LinkedIn credentials)
2. Double down on working channel (whichever is driving traffic)
3. Prepare for scale (ensure infrastructure handles 10x traffic)
4. Document what's working for future GTM cycles

**Owner:** faintech-user-researcher (analysis) → devops/cmo (distribution)

**Timeline:** Escalate blockers immediately, scale preparation 48h

### Scenario 4: Low Traffic, Low Conversion (<50 visitors, <2% conversion)

**Evidence pattern:**
- Traffic low (distribution failure)
- Conversion low (those who visit, don't convert)
- No clear behavioral patterns (insufficient data)

**Root cause hypothesis:** Both distribution and product issues

**Action:**
1. Fix distribution first (without traffic, can't diagnose product)
2. Remove external blockers (HUNTER_API_KEY critical)
3. Execute all prepared social content (don't wait for perfect)
4. Once traffic >50 visitors, re-evaluate conversion issues

**Owner:** faintech-user-researcher (analysis) → cmo (distribution) → cpo (if product issue)

**Timeline:** Immediate blocker escalation, re-evaluate in 72h

---

## Tools and Access Requirements

### Vercel Analytics (Primary)

**Status:** Should be enabled by default on Vercel deployments

**Access needed:**
- [ ] Verify analytics dashboard access for faintech-user-researcher
- [ ] Confirm real-time data availability (not just daily aggregates)
- [ ] Test custom event tracking (CTA clicks, form interactions)

**Fallback:** If Vercel Analytics insufficient, implement custom tracking with PostHog (credentials missing, blocked)

### Database Queries (Backend)

**Data needed:**
- User creation timestamps (funnel stage 3)
- Email verification timestamps (funnel stage 4)
- First memory write/retrieve timestamps (funnel stage 5)
- User metadata (signup source, device, geography)

**Access needed:**
- [ ] Read-only database access for faintech-user-researcher
- [ ] Pre-built queries for common funnel metrics
- [ ] Real-time dashboard or scheduled reports

**Owner:** faintech-backend (provide access and queries)

### Feedback Widget (Already Implemented)

**Status:** Design spec exists, implementation status unknown

**Access needed:**
- [ ] Verify widget is live on production
- [ ] Access to feedback submission data
- [ ] Real-time notifications for new feedback

**Fallback:** If widget not live, defer to Week 3 (not P0 for evidence collection)

---

## Success Metrics

### Week 2 Evidence Collection Targets

**Quantitative:**
- [ ] Traffic tracked for 100% of visitors (no data gaps)
- [ ] Behavioral events captured for >90% of sessions
- [ ] Conversion funnel metrics available for all 5 stages
- [ ] Daily evidence review completed 7/7 days
- [ ] Evidence-based action taken within 24h of trigger

**Qualitative:**
- [ ] Top 3 friction points identified by Day 3
- [ ] User feedback themes documented by Day 5
- [ ] Week 3 recommendations backed by evidence (not assumptions)
- [ ] C-suite report includes specific evidence citations

**Outcome:**
- [ ] Evidence directly leads to ≥1 optimization implemented in Week 2
- [ ] Conversion rate improves by ≥20% from Week 1 baseline (0% → any positive number)
- [ ] Team confidence in GTM strategy increases (subjective, but measurable via team chat)

---

## Risk Mitigation

### Risk 1: Insufficient Traffic (<50 visitors in Week 2)

**Mitigation:**
- Focus evidence collection on quality over quantity
- Manual user interviews with any signup (even 1-2 users valuable)
- Document what little evidence exists for Week 3 planning
- Don't draw conclusions from insufficient data

### Risk 2: Analytics Tool Failure

**Mitigation:**
- Server-side logging as backup (API request metadata)
- Manual sampling (review 10 random sessions per day)
- User feedback as qualitative backup
- Document any data gaps for future planning

### Risk 3: No Qualitative Feedback

**Mitigation:**
- Proactive outreach to any signup (email asking for 15-min call)
- Reddit comment analysis (what are people saying about the product?)
- HN comment analysis (feedback from launch thread)
- Internal team review (what would we want to know as users?)

### Risk 4: Analysis Paralysis (too much data, no action)

**Mitigation:**
- Pre-defined action triggers (this document)
- Daily timebox: 30 min review, 15 min decision, 45 min action planning
- Single friction point focus per day (don't try to fix everything)
- Escalate to CPO if unable to prioritize

---

## Handoff to Week 3

**Evidence package to prepare by April 10:**

1. **Traffic analysis:** Sources, volume, trends, channel comparison
2. **Behavioral insights:** Scroll depth, CTA CTR, navigation patterns, exit points
3. **Conversion funnel:** Stage-by-stage metrics, drop-off analysis, optimization impact
4. **Qualitative themes:** User feedback compilation, interview notes, comment analysis
5. **Recommendations:** Top 3 friction points to fix, channel strategy, product improvements
6. **Lessons learned:** What worked, what didn't, what to do differently

**Format:** Single markdown document (Week2-User-Research-Report-2026-04-10.md) + supporting data exports

**Audience:** C-suite (CEO, CPO, CMO), delivery team (pm, dev, frontend)

**Next cycle:** Week 3 GTM planning should start from this evidence base, not assumptions

---

## Appendix: Daily Evidence Collection Checklist

**Copy this checklist for each day of Week 2:**

### Date: ___________

**Morning Review (30 min):**
- [ ] Check Vercel Analytics dashboard (traffic, sources, geography)
- [ ] Review behavioral events (scroll depth, CTA clicks, exit points)
- [ ] Check conversion funnel metrics (stages 1-5)
- [ ] Read new qualitative feedback (if any)
- [ ] Identify top 3 friction points from yesterday's data

**Action Planning (15 min):**
- [ ] Compare evidence to action triggers (this document)
- [ ] Decide: Is an optimization needed today?
- [ ] If yes: Create task or escalate to implementation owner
- [ ] If no: Continue monitoring, document reasoning

**Evening Check (15 min):**
- [ ] Verify analytics data is flowing (no gaps)
- [ ] Note any anomalies or surprises
- [ ] Update daily note with key findings
- [ ] Prepare questions for tomorrow's review

**Weekly Synthesis (Day 7 only, 2h):**
- [ ] Compile all daily findings into themes
- [ ] Calculate Week 2 aggregate metrics
- [ ] Compare to Week 1 baseline (0 signups)
- [ ] Draft Week 3 recommendations
- [ ] Prepare evidence package for C-suite

---

**Document status:** Ready for Week 2 GTM execution
**Next update:** After first 24h of evidence collection (April 2)
**Owner:** faintech-user-researcher
**Review:** CPO (after Week 2 completion)
