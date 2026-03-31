# Week 2 GTM Market Validation Metrics

**Created:** 2026-03-31 19:45 EET
**Owner:** CPO
**Task:** LAB-MKTRSCH-20260331071347 (AC2)
**Purpose:** Define measurable success criteria for Week 2 GTM execution (April 3-10, 2026)

---

## Executive Summary

Week 1 GTM failed (0/5 signups) due to external blockers, not product-market fit failure. Week 2 GTM requires different validation approach:
- **Focus on controllable channels** (HN, Reddit) instead of blocked channels (LinkedIn, custom domains)
- **Use workarounds** (Vercel URL) instead of waiting for external fixes
- **Measure learning velocity** instead of pure conversion metrics

**Key shift:** Week 1 was "launch and pray" → Week 2 is "learn and iterate"

---

## Week 2 Validation Framework

### Primary Metrics (Must-Have)

| Metric | Target | Rationale | Tracking Method |
|--------|--------|-----------|-----------------|
| **Qualified conversations** | 15-25 | Indicates genuine market interest | Manual logging in tracking template |
| **Signups from target audience** | 5-10 | Validates product appeal to AI-savvy developers | Vercel analytics + manual verification |
| **Activation rate** | >60% | Users who create first memory | Backend analytics (memory creation events) |
| **Time to value** | <5 min | Speed of first value demonstration | Session timing from signup to first memory |

### Secondary Metrics (Should-Have)

| Metric | Target | Rationale | Tracking Method |
|--------|--------|-----------|-----------------|
| **HN engagement** | 50+ upvotes or 20+ comments | Validates technical audience interest | Hacker News API |
| **Reddit engagement** | 30+ upvotes per post | Validates founder/developer interest | Reddit API |
| **Demo URL traffic** | 200+ unique visitors | Indicates reach | Vercel analytics |
| **Content engagement** | 100+ LinkedIn article views | Brand awareness (if credentials unblocked) | LinkedIn analytics |

### Learning Metrics (Velocity)

| Metric | Target | Rationale | Tracking Method |
|--------|--------|-----------|-----------------|
| **User feedback collected** | 10+ pieces | Qualitative insights | Feedback widget + manual |
| **Feature requests logged** | 5+ requests | Identifies product gaps | Feedback widget |
| **Objection patterns documented** | 3+ patterns | Sales/marketing optimization | Manual logging |
| **Competitive mentions** | 2+ mentions | Market positioning | Manual logging |

---

## Week 2 Success/Failure Criteria

### ✅ Success (Green Light for Week 3)

**ANY of the following:**
- 5+ signups from target audience (AI developers, founders)
- 15+ qualified conversations with genuine interest
- HN post reaches front page (top 30) with positive comments
- 3+ beta user activation (>1 memory created)

**Rationale:** Indicates genuine market interest despite external blockers

### 🟡 Partial Success (Yellow Light)

**ANY of the following:**
- 2-4 signups with positive feedback
- 8-14 qualified conversations
- Strong engagement on one channel (HN or Reddit)
- 1-2 beta users activated

**Rationale:** Shows potential but needs optimization

### ❌ Failure (Red Light)

**ALL of the following:**
- 0-1 signups
- <8 qualified conversations
- No engagement on any channel
- No activations

**Rationale:** Indicates fundamental PMF issue or severe positioning problem

---

## Attribution Framework

### Channel Tracking

| Channel | UTM Source | URL Variant | Attribution |
|---------|-----------|-------------|-------------|
| Hacker News | `utm_source=hn` | `faintech-lab.vercel.app/?utm_source=hn` | Vercel analytics |
| Reddit | `utm_source=reddit` | `faintech-lab.vercel.app/?utm_source=reddit` | Vercel analytics |
| Direct | `utm_source=direct` | `faintech-lab.vercel.app` | Vercel analytics |
| LinkedIn | `utm_source=linkedin` | `faintech-lab.vercel.app/?utm_source=linkedin` | Vercel analytics (if unblocked) |

### Funnel Metrics

```
Impressions (HN/Reddit views)
    ↓ (CTR: target >3%)
Demo URL Visitors
    ↓ (Conversion: target >5%)
Signups
    ↓ (Activation: target >60%)
Activated Users (1+ memory)
    ↓ (Retention: target >40% D7)
Returning Users
```

---

## Daily Tracking Template

**Date:** [YYYY-MM-DD]
**Channel:** [HN/Reddit/LinkedIn/Direct]

### Quantitative
- Impressions: ___
- Clicks: ___
- Signups: ___
- Activations: ___

### Qualitative
- Top positive feedback: ___
- Top objection: ___
- Feature requests: ___
- Competitive mentions: ___

### Insights
- What worked: ___
- What didn't work: ___
- What to test tomorrow: ___

---

## Risk Mitigation

### External Blockers

| Blocker | Mitigation | Impact if Unresolved |
|---------|-----------|---------------------|
| HUNTER_API_KEY | Manual email collection | Lower conversion (friction) |
| LinkedIn credentials | Skip LinkedIn channel | Miss B2B audience |
| Custom domains | Use Vercel URL | Lower trust (technical audience OK) |
| faintech-lab repo private | N/A for Week 2 | N/A |

### Internal Risks

| Risk | Mitigation | Owner |
|------|-----------|-------|
| Low engagement | Post timing optimization | CMO |
| Poor conversion | UX optimization (P0-P1) | faintech-frontend |
| Technical issues | Monitoring dashboard | dev |
| Burnout | Bounded execution (April 3-10) | All |

---

## Decision Points

### End of Week 2 (April 10)

**Decision criteria:**
1. **Green Light:** Proceed to Week 3 with scale-up (increase budget, expand channels)
2. **Yellow Light:** Optimize and extend Week 2 approach (1 more week)
3. **Red Light:** Pivot strategy (reposition product, new channels, or kill decision)

**Decision owner:** CPO (recommendation) → CEO (final decision)

---

## Appendix: Week 1 vs Week 2 Comparison

| Dimension | Week 1 | Week 2 |
|-----------|--------|--------|
| **Goal** | 5 signups | 5-10 signups + learning |
| **Channels** | All blocked (LinkedIn, custom domains) | Focus on unblocked (HN, Reddit) |
| **URL** | lab.faintech.ai (DNS failed) | faintech-lab.vercel.app (working) |
| **Approach** | Launch and pray | Learn and iterate |
| **Success metric** | Signups only | Signups + conversations + activation |
| **Risk tolerance** | Low (external dependencies) | High (controllable factors) |
| **Learning velocity** | 0 (blocked) | High (daily tracking) |

---

**Status:** READY FOR EXECUTION
**Next Owner:** CMO (execution), CPO (metrics tracking)
**Dependencies:** None (all blockers have workarounds)
