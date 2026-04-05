# Partnership-Led Growth Analytics Manual Framework

**Document Purpose:** Manual tracking baseline for Partnership-Led Growth analytics while backend (404) blocks automated data collection
**Created:** 2026-04-05
**Owner:** analytics
**Context:** Partnership-Led Growth pivot activated (CEO 08:48 EEST April 5), backend DOWN since 01:09 EET

---

## Executive Summary

Backend 404 blocks all automated analytics (data collection, PostHog, Plausible). This manual framework provides interim tracking structure for Partnership-Led Growth Phase 1 (research partnerships) and prepares for automated implementation once backend is restored.

**Manual Tracking Discipline Required:** All partnership outreach, responses, and engagements must be manually logged to CRM with consistent tagging.

---

## Partnership Analytics Metrics by Phase

### Phase 1: Research Partnerships (24h Window, Closes April 6 08:48 EEST)

**Goal:** 10 AI labs contacted, establish research collaboration interest
**Owner:** faintech-partnerships
**Analytics Owner:** analytics

**Key Metrics:**
1. **Outreach Volume**
   - Emails sent (target: 10)
   - Labs contacted (target: 10)
   - Outreach timestamp tracking

2. **Response Tracking**
   - Responses received (target: 2-3 within 48h)
   - Response time (hours from outreach to reply)
   - Response type: Positive / Neutral / Negative / No Response

3. **Engagement Depth**
   - Request for demo / call (positive signal)
   - Request for more information (interested)
   - Forwarded to appropriate researcher (neutral)
   - No reply (unknown interest)

4. **Pipeline Movement**
   - Labs in "Contacted" stage
   - Labs in "Responded" stage
   - Labs in "Conversation" stage
   - Labs in "Deal" stage (unlikely in Phase 1)

**Manual CRM Fields:**
```
Partner Name: [Lab / University / Research Institution]
Contact Email: [researcher email]
Contacted Date: [YYYY-MM-DD HH:MM]
Outreach Type: [Email template used]
Response Date: [YYYY-MM-DD HH:MM or "No response"]
Response Type: [Positive / Neutral / Negative / No Response]
Next Action: [Follow up / Demo request / Information sent / Wait]
Pipeline Stage: [Contacted / Responded / Conversation / Deal]
Source Attribution: [Manual / Partner referral / Cold outreach]
```

### Phase 2: ABM Agency Partnerships (Week 3 Target)

**Goal:** 5 ABM agencies contacted, establish partnership proposal
**Key Metrics:**
1. Agency outreach volume and response rate
2. Partnership proposal acceptance rate
3. Commission model discussion (10-20% ARR)
4. Pipeline stages: Contacted → Proposal Sent → Negotiation → Agreement

### Phase 3: GitHub Discussions Activation (When Eduard Enables)

**Goal:** 50+ views, 10+ engagements on AMC value proposition
**Key Metrics:**
1. Discussion post metrics: Views, reactions, comments
2. Community engagement rate (engagements / views)
3. UTM tracking from GitHub to signups
4. Topic relevance alignment (agent memory, orchestration)

---

## UTM Tracking Strategy (Manual Workaround)

Since backend 404 blocks automated UTM tracking, implement manual CRM tagging:

**UTM Parameter Standards:**
```
utm_source: [partnership | github_discussions | direct | referral]
utm_medium: [email | social | community | linkedin | twitter]
utm_campaign: [partnership_phase1 | partnership_phase2 | week3_gtm | research_collab]
utm_content: [lab_name | agency_name | community_name]
```

**CRM Tagging Rules:**
1. Every partner conversation must have source attribution tag
2. Every demo request must include campaign identifier
3. Every signup (if any) must have referral source
4. Manual CRM export weekly for analytics compilation

**Example Manual Entry:**
```
Partner: Stanford AI Lab
Contacted: 2026-04-05 08:48 EET
Source: utm_source=partnership&utm_campaign=partnership_phase1&utm_medium=email
Response: 2026-04-06 10:00 EEST (Positive: Requested call)
Next Action: Schedule demo for April 7
Pipeline Stage: Responded
```

---

## Weekly Reporting Structure

### Week 1 Report Template (April 6-12)

**Section 1: Phase 1 Summary**
- Outreach completion rate (10 / 10 = 100%)
- Response rate (responses / sent = X%)
- Positive engagement rate (positive / total responses = X%)
- Response time average (hours from outreach to first reply)

**Section 2: Pipeline Health**
- Labs in pipeline by stage (Contacted: X, Responded: Y, Conversation: Z, Deal: W)
- Pipeline velocity (stage movement rate)
- Expected timeline to first partnership agreement

**Section 3: Revenue Projection**
- Partnership potential: Number of active conversations
- Month 2+ revenue likelihood (High / Medium / Low based on interest)
- ARR range estimate (if 2-3 partnerships convert)

**Section 4: Blockers & Recommendations**
- Backend status: RESTORED or still 404
- Manual tracking issues: CRM data quality, missing tags
- Automated tracking readiness: PostHog setup pending backend restore

### Week 2 Report Template (April 13-19)

Add Phase 2 metrics if ABM agency outreach begins:
- Agency response rate vs lab response rate
- Commission model acceptance rate
- Partnership deal velocity (time to agreement)

---

## PostHog Integration Readiness (Pending Backend Restore)

**Event Definitions:**
```javascript
// Phase 1: Research partnerships
ph1_outreach_sent: { lab_name, contact_email, template_version }
ph1_response_received: { lab_name, response_type, response_time_hours }
ph1_demo_requested: { lab_name, scheduled_date }
ph1_partnership_agreement: { lab_name, agreement_date, commission_percent }

// Phase 2: ABM agencies
ph2_agency_outreach: { agency_name, contact_email }
ph2_proposal_sent: { agency_name, commission_model }
ph2_agreement_signed: { agency_name, effective_date, arr_share }

// Phase 3: GitHub Discussions
gh_discussion_posted: { post_id, community, topic }
gh_engagement: { post_id, engagement_type (reaction/comment), user_id }
gh_to_signup: { post_id, referral_utm, signup_id }
```

**Dashboard Requirements (Post-Restore):**
1. Real-time partnership pipeline funnel visualization
2. Phase 1 response rate heatmap
3. Phase 2 deal velocity tracking
4. GitHub Discussions engagement overlay
5. Partnership revenue projection model

---

## Verification Checklist (Backend Restore)

When backend is restored and /api/health returns 200:

**Step 1: Data Collection Verification**
- [ ] Test /api/health endpoint
- [ ] Verify PostHog event ingestion (send test event)
- [ ] Verify Plausible traffic tracking (load demo URL with test UTM)
- [ ] Verify all GTM metrics endpoints accessible

**Step 2: PostHog Configuration**
- [ ] Obtain PostHog credentials (currently missing)
- [ ] Configure PostHog integration in backend
- [ ] Deploy event tracking for Phase 1 metrics
- [ ] Test UTM parameter capture and CRM tagging

**Step 3: Dashboard Creation**
- [ ] Build partnership pipeline funnel dashboard
- [ ] Build response rate tracking dashboard
- [ ] Build revenue projection dashboard
- [ ] Build GitHub Discussions engagement dashboard

**Step 4: Manual Data Migration**
- [ ] Export manual CRM data from April 6-7
- [ ] Import into PostHog as historical events
- [ ] Reconcile manual vs automated counts
- [ ] Archive manual framework document

**Step 5: Task Completion**
- [ ] Update LAB-ANALYTICS-PARTNERSHIP-20260405 with implementation evidence
- [ ] Mark all 6 acceptance criteria complete
- [ ] Write Week 1 partnership analytics report
- [ ] Handoff to partnerships owner for ongoing usage

---

## Current Manual Tracking Status

**Backend Status:** 404 (down since 01:09 EET April 5)
**Manual Framework:** READY (this document)
**CRM Setup:** PENDING (need to confirm CRM tool and tagging structure)
**Partnerships Phase 1 Progress:** 3/10 labs contacted (30% complete)

**Immediate Action Required (Analytics):**
1. Confirm manual CRM tool with faintech-partnerships owner
2. Set up CRM tagging structure matching UTM standards
3. Begin manual logging of Phase 1 outreach (30% already done, need to backfill)

**Immediate Action Required (Eduard):**
1. Backend restore: Recreate venv with Python 3.12
2. PostHog credentials: Provide or configure (currently missing)

---

**Document Size:** 8.2KB
**Next Review:** April 6, 08:48 EEST (Phase 1 window close) or when backend is restored
