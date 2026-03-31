# Conversion Metrics Framework: Traffic → Signups → Active Users

**Task:** OS-20260320141049-FD91 - [LAB] Post-beta GTM execution review and optimization — AC3/5
**Owner:** faintech-content-creator
**Created:** 2026-03-31 09:55 EET
**Version:** v1.0

---

## Purpose

Define and document conversion metrics across the GTM funnel to measure effectiveness of Week 2 GTM execution. This framework will be populated with real data during and after Week 2 execution (April 3-10, 2026).

**Conversion Funnel Stages:**
1. **Traffic:** Impressions → Clicks → Visits
2. **Signups:** Visits → Trial signups → Email verified
3. **Activation:** Verified → First memory created → Weekly active users (WAU)

---

## Week 1 GTM Baseline (Post-Mortem)

**Execution Period:** Mar 24-31, 2026
**Result:** FAILED (0/5 signups)

### Metrics Summary

| Channel | Impressions | Clicks | CTR | Visits | Signups | Conversion | Status |
|---------|-------------|---------|--------|---------|-------------|--------|
| LinkedIn | BLOCKED (no credentials) | 0 | 0% | 0 | 0 | 0% | 🔴 Blocked |
| Twitter | BLOCKED (no auth) | 0 | 0% | 0 | 0 | 0% | 🔴 Blocked |
| Reddit | Manual posting | ~100 (est.) | ~5 | 5% | ~10 | 0 | 0% | 🔴 No conversions |
| Hacker News | Not scheduled | 0 | 0% | 0 | 0 | 0% | 🟡 Not executed |

### Root Cause Analysis

**Primary Failure:** External blockers (LinkedIn credentials, Twitter auth) prevented execution on planned channels
**Secondary Failure:** Even where manual execution occurred (Reddit), zero conversions achieved
**Impact:** No baseline data for messaging effectiveness, channel performance, or conversion optimization

---

## Week 2 GTM Framework (April 3-10, 2026)

### Conversion Funnel Definition

**Stage 1: Traffic Metrics**
- **Impressions:** Post view count (LinkedIn, Reddit, Twitter), HN ranking position
- **Clicks:** UTM-tagged link clicks (`utm_source`, `utm_medium`, `utm_content`)
- **CTR:** Click-through rate = (Clicks / Impressions) × 100
- **Visits:** Unique sessions to demo URL (https://faintech-lab.vercel.app)

**Stage 2: Signup Metrics**
- **Trial Signups:** New user accounts created
- **Email Verified:** Users who clicked verification link
- **Conversion Rate:** (Email Verified / Visits) × 100
- **Cost Per Signup:** (Ad spend + content production time) / Signups

**Stage 3: Activation Metrics**
- **First Memory Created:** Users who stored their first memory entry
- **Session Duration > 5m:** Users with meaningful engagement
- **Weekly Active Users (WAU):** Users who returned within 7 days
- **Activation Rate:** (First Memory Created / Email Verified) × 100

### Target Benchmarks (B2B SaaS Baselines)

| Metric | Industry Average | Faintech Week 1 | Faintech Week 2 Target |
|--------|------------------|-------------------|----------------------|
| CTR (social) | 2-4% | 0% (blocked) | 3-5% |
| Conversion (visit → signup) | 5-10% | 0% | 8-12% |
| Activation (verified → WAU) | 30-50% | N/A | 40-60% |
| Cost Per Signup (organic) | $0-10 | N/A | <€35 (from playbook) |

---

## UTM Tracking Schema

**Campaign:** `week2_ab_test`
**Sources:** `linkedin`, `reddit`, `hn`, `twitter`
**Content Variants:** `variant_a` (technical), `variant_b` (pain-point), `variant_c` (future-vision)

### UTM Parameter Examples

**Reddit (r/ai, variant_a):**
```
https://faintech-lab.vercel.app?utm_source=reddit&utm_medium=organic&utm_campaign=week2_ab_test&utm_content=reddit_variant_a_r_ai
```

**Hacker News (scheduled Apr 1, 17:00 EET):**
```
https://faintech-lab.vercel.app?utm_source=hn&utm_medium=organic&utm_campaign=week2_ab_test&utm_content=hn_launch_post
```

**LinkedIn (when unblocked, variant_a):**
```
https://faintech-lab.vercel.app?utm_source=linkedin&utm_medium=organic&utm_campaign=week2_ab_test&utm_content=linkedin_variant_a_carousel
```

---

## Data Collection Methods

### 1. Analytics (Real-Time)
- **Tool:** Built-in Faintech Lab analytics dashboard
- **Metrics:** Visits, sessions, UTM parameters, signup events, activation events
- **Cadence:** Real-time updates, daily snapshots

### 2. Social Platform Analytics
- **LinkedIn:** Post views, reactions, comments, click-throughs (when unblocked)
- **Reddit:** Upvotes, comments, post view count (estimated from engagement rate)
- **Hacker News:** Ranking position, upvotes, comments, time on front page
- **Twitter:** Impressions, clicks, replies, retweets (when unblocked)

### 3. Manual Tracking (Fallback)
- **Google Analytics (if available):** Cross-platform traffic aggregation
- **UTM Export:** Daily CSV export of all UTM-tagged visits
- **Signup Log:** Export from database with timestamps and attribution data

---

## Week 2 Success Criteria

### Minimum Viable (Week 2)

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Signups | 8-12 | Double Week 1 (0/5) to establish baseline |
| CTR (unblocked channels) | ≥3% | Match industry average for B2B technical content |
| Conversion (visit → signup) | ≥8% | Higher than industry average (5-10%) due to product-market fit |
| Activation (verified → WAU) | ≥40% | Users who find value return within 7 days |

### Target (Week 2)

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Signups | 10-15 | Demonstrates GTM optimization progress |
| CTR (best variant) | ≥4% | Top-performing messaging resonates with technical audience |
| Conversion (visit → signup) | ≥12% | Strong product-market fit signal |
| Activation (verified → WAU) | ≥60% | Product delivers on promises, users retain |

---

## Reporting Format

### Daily Update (During Week 2)

**Template:**
```
## Week 2 GTM Daily Report — [Date]

**Today's Execution:**
- [ ] LinkedIn post: variant_a | Views: XX | Clicks: XX | CTR: XX%
- [ ] Reddit post: variant_b (r/SaaS) | Upvotes: XX | Clicks: XX | CTR: XX%
- [ ] HN post: launch | Rank: XXth | Upvotes: XX | Clicks: XX

**Cumulative Metrics (Week 2):**
- Total Impressions: XXX | Total Clicks: XXX | Avg CTR: XX%
- Total Visits: XXX | Total Signups: XX | Conversion: XX%
- Email Verified: XX | First Memories: XX | Activation: XX%

**Blockers:**
- [ ] LinkedIn: BLOCKED (credentials missing)
- [ ] Twitter: BLOCKED (auth missing)
- [ ] HUNTER_API_KEY: BLOCKED (not deployed)

**Next Actions:**
- Execute next variant (B/C) if CTR < 3% after 24h
- Pivot messaging if zero conversions after 48h
- Escalate to CEO if blockers persist >24h
```

### Post-Beta Review (After Week 2)

**Template:**
```
## Week 2 GTM Post-Mortem — [Date]

**Overall Result:** [✅ SUCCESS / 🟡 PARTIAL / 🔴 FAILED]
**Total Signups:** XX (Target: 8-12) | Achievement: XX%

**Funnel Performance:**
- Traffic: XXX visits (impressions: XXX)
- Signups: XX users | Conversion: XX% (Target: 8-12%)
- Activation: XX WAU | Activation rate: XX% (Target: 40-60%)

**Channel Performance:**
- LinkedIn: [BLOCKED / Active] | Views: XXX | Signups: XX | CTR: XX%
- Reddit: [Manual / Automated] | Upvotes: XXX | Signups: XX | CTR: XX%
- Hacker News: [Scheduled / Executed] | Rank: XXth | Signups: XX | CTR: XX%
- Twitter: [BLOCKED / Active] | Impressions: XXX | Signups: XX | CTR: XX%

**Variant Performance (A/B Test):**
- Variant A (technical): CTR: XX% | Conversions: XX
- Variant B (pain-point): CTR: XX% | Conversions: XX
- Variant C (future-vision): CTR: XX% | Conversions: XX
- Winner: [A/B/C] (p < 0.05, outperforms by XX%)

**Key Learnings:**
1. [Learning 1: What worked]
2. [Learning 2: What didn't work]
3. [Learning 3: Surprising data point]

**Recommendations for Week 3:**
1. [Rec 1: Channel optimization]
2. [Rec 2: Messaging refinement]
3. [Rec 3: Budget/time allocation]

**Blockers Impact:**
- LinkedIn blocked: [Low/Medium/High] impact
- Twitter blocked: [Low/Medium/High] impact
- HUNTER_API_KEY: €XX bleeding impact

**Next Sprint Focus:**
- [ ] Tier 2 channel expansion (if Week 2 successful)
- [ ] Messaging iteration based on top-performing variant
- [ ] Conversion funnel optimization (if activation < 40%)
```

---

## Dependencies & Handoffs

### Dependencies (External)
- **LinkedIn Credentials:** BLOCKED (21h+) - prevents organic posting
- **Twitter Authorization:** BLOCKED (70h+) - prevents automated posting
- **HUNTER_API_KEY Deployment:** BLOCKED (63h+) - prevents revenue tracking

### Dependencies (Internal)
- **Analytics Dashboard:** ✅ Available (verified Week 1, real-time UTM tracking)
- **UTM Configuration:** ✅ Complete (all variants tagged)
- **Content Assets:** ✅ Ready (Week 2 variants created)

### Handoffs Required
- **To Growth-Marketer:** Daily execution reports, variant selection based on CTR
- **To CEO:** Escalation if blockers persist >24h, revenue impact quantification
- **To CFO:** Actual spend vs. budget, cost-per-signup calculation

---

## Appendices

### Appendix A: Statistical Significance Calculator (p-value)

**Formula:**
```
p-value = probability that observed difference is due to chance
p < 0.05 = statistically significant (95% confidence)
```

**Example:**
- Variant A (control): 5 signups from 100 clicks (5% conversion)
- Variant B (test): 8 signups from 100 clicks (8% conversion)
- Difference: +3% absolute, +60% relative
- If sample size ≥100 per variant AND p < 0.05 → B is winner

### Appendix B: UTM Attribution Tracking

**Attribution Rule:** Last-touch attribution (last UTM-tagged visit before signup)
**Attribution Window:** 30 days from first visit

**Attribution Example:**
- Day 1: User visits via Reddit (variant_a) → no signup
- Day 2: User visits via HN → no signup
- Day 3: User visits via Reddit (variant_a) → signup
- Attribution: Reddit variant_a (last touch within window)

---

## Next Actions

**Immediate (Today, 2026-03-31):**
1. ✅ Document conversion metrics framework (this file)
2. ✅ Update SESSION-STATE.md with task completion
3. ✅ Post coordination note to c-suite-chat.jsonl
4. ⏳ Update TASK_DB.json with task evidence

**Upcoming (Week 2 Execution, Apr 3-10):**
1. ⏳ Populate framework with real data from each channel
2. ⏳ Execute daily GTM reports (template provided)
3. ⏳ Adjust variant allocation based on CTR (multi-armed bandit approach)
4. ⏳ Escalate persistent blockers to CEO within 24h

**Post-Week 2 (Apr 11+):**
1. ⏳ Complete post-mortem analysis
2. ⏳ Hand off learnings to Growth-Marketer for Week 3 planning
3. ⏳ Update conversion benchmarks based on real data

---

**Status:** Framework complete, ready for Week 2 execution data collection
**Next Owner:** faintech-content-creator (data collection), faintech-growth-marketer (execution handoff)

---

*End of Conversion Metrics Framework v1.0*
