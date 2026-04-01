# HN Launch User Tracking Template - April 1, 2026

**Purpose**: Manual user behavior tracking for HN launch when PostHog credentials unavailable
**Owner**: faintech-user-researcher
**Created**: 2026-04-01T12:31:00+02:00

## Google Sheets Template Structure

Create a new Google Sheet with the following tabs:

### Tab 1: Visitor Tracking

| Timestamp | Referrer | Landing Page | Onboarding Started | Onboarding Completed | Signup Completed | Notes |
|-----------|----------|--------------|-------------------|---------------------|------------------|-------|
|           | HN/Direct/Other | Yes/No | Yes/No | Yes/No | Yes/No |       |

**Tracking Method**:
- Check Vercel analytics dashboard every 30 minutes
- Manually record visitor counts
- Track referrer from URL parameters (utm_source=hackernews)

### Tab 2: Signup Tracking

| Timestamp | Email Domain | Company Size (if available) | Referrer | Time to Complete | Drop-off Point | Notes |
|-----------|--------------|----------------------------|----------|------------------|----------------|-------|
|           | gmail.com/company.com | 1-10/11-50/51-200/200+ | HN/Reddit/LinkedIn/Direct | seconds | step 1/2/3/4/5 |       |

**Tracking Method**:
- Monitor backend database directly (SELECT * FROM users WHERE created_at > '2026-04-01 15:00:00')
- Extract domain from email
- Record timestamp and referrer

### Tab 3: Onboarding Behavior

| User ID | Step 1 (Agent Creation) | Step 2 (Memory Write) | Step 3 (Search Memory) | Step 4 (View Results) | Step 5 (Complete) | Total Time | Notes |
|---------|------------------------|----------------------|----------------------|----------------------|------------------|------------|-------|
|         | Completed/Time | Completed/Time | Completed/Time | Completed/Time | Completed/Time | seconds |       |

**Tracking Method**:
- Query onboarding_events table
- Calculate time between steps
- Identify drop-off points

### Tab 4: Engagement Metrics

| Timestamp | Total Visitors | Signups | Conversion Rate | Onboarding Started | Onboarding Completed | Activation Rate | Avg Time to Value |
|-----------|---------------|---------|-----------------|-------------------|---------------------|-----------------|-------------------|
|           | count | count | % | count | count | % | seconds |

**Update Frequency**: Every 30 minutes during launch window (17:00-21:00 EET)

### Tab 5: Qualitative Feedback

| Timestamp | Source | Feedback Type | User Segment | Feedback Text | Action Required | Priority |
|-----------|--------|--------------|--------------|---------------|-----------------|----------|
|           | HN Comments/Twitter/Email | Bug/Feature Request/Confusion/Praise | Developer/Founder/PM/Other | text | Yes/No | P0/P1/P2 |

**Sources to Monitor**:
- HN comment thread (manual review every hour)
- Twitter mentions (@faintech_lab)
- Email to support@faintechlab.com
- In-app feedback widget (if deployed)

## Success Metrics Dashboard

### Launch Targets (4-hour window: 17:00-21:00 EET)

| Metric | Minimum | Target | Stretch |
|--------|---------|--------|---------|
| HN Upvotes | 50 | 100 | 200+ |
| HN Comments | 10 | 30 | 50+ |
| Visitors | 100 | 300 | 500+ |
| Signups | 5 | 10-15 | 20+ |
| Conversion Rate | 3% | 5% | 7%+ |
| Onboarding Completion | 60% | 80% | 90%+ |

### Week 2 GTM Targets (April 1-10)

| Metric | Minimum | Target | Stretch |
|--------|---------|--------|---------|
| Total Signups | 10 | 15 | 25+ |
| Conversion Rate | 3% | 5% | 7%+ |
| Active Users (Day 7) | 5 | 10 | 15+ |
| Paying Customers | 1 | 3 | 5+ |

## Monitoring Schedule

### Pre-Launch (12:00-17:00 EET)
- **12:00**: Create Google Sheet, share with C-suite
- **14:00**: Verify backend API deployment status
- **16:00**: Final system check, update tracking template
- **16:30**: CMO confirms HN post ready

### Launch Window (17:00-21:00 EET)
- **17:00**: HN post goes live, start tracking
- **17:30**: First metrics check (30 min)
- **18:00**: Second metrics check (1 hour)
- **19:00**: Third metrics check (2 hours)
- **20:00**: Fourth metrics check (3 hours)
- **21:00**: Fifth metrics check (4 hours) - initial results summary

### Post-Launch (21:00+ EET)
- **21:30**: Create launch results summary document
- **22:00**: Post results to c-suite-chat.jsonl
- **Next Day 09:00**: 24-hour metrics update

## Escalation Triggers

| Trigger | Threshold | Action | Owner |
|---------|-----------|--------|-------|
| Zero signups after 2 hours | 0 signups | Escalate to CMO - check HN post quality, title, timing | CMO |
| Low conversion rate | <2% | Investigate UX friction, check backend logs | PM + Dev |
| High drop-off rate | >50% at single step | Identify technical issue or UX confusion | Dev + Designer |
| Negative HN feedback | >30% negative | Prepare response, consider post removal | CMO + CEO |
| Backend errors | Any 5xx errors | Immediate escalation to DevOps | DevOps |

## Manual Tracking Commands

### Check signups count
```sql
SELECT COUNT(*) FROM users WHERE created_at > '2026-04-01 15:00:00';
```

### Check onboarding completion
```sql
SELECT
  COUNT(CASE WHEN onboarding_completed = true THEN 1 END) as completed,
  COUNT(*) as total,
  ROUND(COUNT(CASE WHEN onboarding_completed = true THEN 1 END) * 100.0 / COUNT(*), 2) as completion_rate
FROM users
WHERE created_at > '2026-04-01 15:00:00';
```

### Check referrer breakdown
```sql
SELECT
  utm_source,
  COUNT(*) as signups
FROM users
WHERE created_at > '2026-04-01 15:00:00'
GROUP BY utm_source;
```

### Check drop-off points
```sql
SELECT
  onboarding_step,
  COUNT(*) as users_at_step,
  LAG(COUNT(*)) OVER (ORDER BY onboarding_step) as prev_step_count,
  ROUND(COUNT(*) * 100.0 / LAG(COUNT(*)) OVER (ORDER BY onboarding_step), 2) as retention_rate
FROM user_onboarding_events
WHERE created_at > '2026-04-01 15:00:00'
GROUP BY onboarding_step
ORDER BY onboarding_step;
```

## Post-Launch Analysis Template

### Launch Performance Summary

**Date**: April 1, 2026
**Launch Time**: 17:00 EET
**Analysis Time**: 21:00 EET (4-hour window)

#### Traffic Metrics
- Total Visitors: ___
- Unique Visitors: ___
- Traffic Sources: HN ___% / Direct ___% / Other ___%
- Peak Concurrent Users: ___

#### Conversion Metrics
- Total Signups: ___
- Landing → Signup Conversion: ___%
- Signup → Onboarding Started: ___%
- Onboarding Completion Rate: ___%
- Time to Value (median): ___ seconds

#### Engagement Metrics
- HN Upvotes: ___
- HN Comments: ___
- HN Rank (peak): ___
- Twitter Mentions: ___
- Email Inquiries: ___

#### Qualitative Feedback Summary
- Positive themes: ___
- Negative themes: ___
- Feature requests: ___
- Bug reports: ___

#### Key Learnings
1. ___
2. ___
3. ___

#### Week 2 GTM Adjustments
Based on launch results, recommend the following adjustments:
1. ___
2. ___
3. ___

## Notes

- This template assumes PostHog is NOT available (credentials missing)
- If PostHog becomes available, use automated dashboards instead
- Share Google Sheet with C-suite for real-time visibility
- Update this document with actual metrics post-launch

---

**Status**: READY - Awaiting HN launch at 17:00 EET
**Next Update**: 2026-04-01T17:30:00+02:00 (first metrics check)
