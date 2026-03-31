# Week 2 Data Collection Preparation

**Created:** 2026-03-30T23:23:00+02:00
**Owner:** analytics
**Purpose:** Prepare data collection infrastructure for Week 2 GTM analytics (April 3-9, 2026)

---

## Data Sources to Monitor

### 1. Channel Performance Metrics

**Sources:**
- UTM tracking parameters from all GTM channels
- Web analytics (page views, unique visitors, time on site)
- Signup conversion tracking
- A/B test variant assignment

**Required Data Points:**
| Metric | Source | Collection Method |
|--------|--------|------------------|
| Impressions | GTM channel APIs (HN, Twitter, LinkedIn, Reddit) | Daily scrape/aggregation |
| Clicks | UTM `utm_source` tracking | Server-side tracking |
| Signups | AMC signup API | Event tracking |
| Conversion rate | Calculated: signups / clicks | Derived metric |
| A/B test assignment | UTM `utm_content` parameter | Server-side capture |

### 2. A/B Test Data

**Test Variants:**
- Variant A: Control (baseline messaging)
- Variant B: Experimental A (value-focused tone)
- Variant C: Experimental B (technical depth focus)

**Required Data Points:**
| Variant | Assignments | Signups | CTR | Conversion Rate |
|---------|-------------|---------|------|----------------|
| A | Count | Count | signups/impressions | signups/clicks |
| B | Count | Count | signups/impressions | signups/clicks |
| C | Count | Count | signups/impressions | signups/clicks |

### 3. Conversion Funnel Metrics

**Funnel Stages:**
1. **Impression** - Post/page/content viewed
2. **Click** - User clicked through to lab.faintech.ai or demo URL
3. **Landing Page** - User reached lab.faintech.ai
4. **Demo Interaction** - User interacted with demo features
5. **Signup** - User completed signup flow

**Tracking Implementation:**
```typescript
// UTM parameter capture (all pages)
const trackUTM = (url: string) => {
  const params = new URLSearchParams(url.split('?')[1]);
  return {
    source: params.get('utm_source'),      // HN, Twitter, LinkedIn, Reddit
    medium: params.get('utm_medium'),      // social, organic, referral
    campaign: params.get('utm_campaign'),    // W2-gtm-2026
    content: params.get('utm_content'),      // variant-a, variant-b, variant-c
    term: params.get('utm_term'),           // tracking identifier
    timestamp: Date.now()
  };
};

// Funnel event tracking
const trackFunnelEvent = (stage: string, userId?: string, metadata?: object) => {
  // Send to analytics collection endpoint
  // Store in logs for batch processing
  // Include UTM context if available
};
```

## Daily Data Collection Checklist

For each day of Week 2 (April 3-9):

- [ ] Collect channel metrics from all 4 GTM channels
- [ ] Aggregate UTM parameters from server logs
- [ ] Count unique visitors vs. total visits
- [ ] Track demo interaction events (button clicks, feature usage)
- [ ] Record signup events with channel attribution
- [ ] Calculate daily conversion rates (CTR, funnel completion, signup conversion)
- [ ] Store daily snapshot for historical comparison

## Weekly Data Preparation

By end of Week 2 (April 9, 18:00 EET):

- [ ] Calculate aggregate metrics across all 7 days
- [ ] Perform chi-square test for CTR comparison (Template 2 formula)
- [ ] Perform t-test for conversion rate comparison (Template 2 formula)
- [ ] Generate p-values and determine statistical significance (threshold: p < 0.05)
- [ ] Create visualizations (line charts for trends, bar charts for variant comparison)
- [ ] Write weekly performance report (Template 3 structure, 1,000+ words)

## Statistical Analysis Notes

### Validity Constraints

**Sample Size Concern:**
- Expected signups: 15-30 total (2-4/day average)
- Signups per variant: 5-10 (assuming equal assignment)
- **Statistical power limitation:** With N=5-10 per group, detecting statistically significant differences (p < 0.05) is unlikely even with large effect sizes

### Recommended Approach

**Focus on Descriptive Analytics:**
1. **Trend analysis** - Compare daily performance across the week
2. **Funnel drop-off analysis** - Identify where users abandon the conversion path
3. **Channel performance ranking** - Rank channels by impressions, CTR, signups, conversion rate
4. **Qualitative insights** - Track user feedback, comments, questions from GTM channels
5. **A/B test learning value** - Focus on "learnings" section rather than statistical "winner" declaration

**Statistical Significance Disclaimer:**
> "Week 2 data collection is primarily for learning and optimization. With expected sample sizes of 15-30 total signups, formal statistical significance (p < 0.05) is unlikely. Analysis will focus on descriptive metrics, funnel efficiency, and qualitative insights rather than inferential statistics."

## Data Storage

**Location:** `/Users/eduardgridan/faintech-lab/data/analytics/week2/`
**Structure:**
```
week2/
├── daily/
│   ├── 2026-04-03.json
│   ├── 2026-04-04.json
│   └── ...
├── aggregated/
│   ├── channel-metrics.json
│   ├── ab-test-results.json
│   └── funnel-analysis.json
└── weekly-report.md
```

**Daily Data Schema:**
```json
{
  "date": "2026-04-03",
  "timestamp": "2026-04-03T18:00:00Z",
  "channel_metrics": {
    "hacker_news": { "impressions": 0, "clicks": 0, "signups": 0 },
    "twitter": { "impressions": 0, "clicks": 0, "signups": 0 },
    "linkedin": { "impressions": 0, "clicks": 0, "signups": 0 },
    "reddit": { "impressions": 0, "clicks": 0, "signups": 0 }
  },
  "funnel_metrics": {
    "impressions": 0,
    "clicks": 0,
    "landings": 0,
    "demo_interactions": 0,
    "signups": 0
  },
  "ab_test_data": {
    "variant_a": { "assignments": 0, "signups": 0 },
    "variant_b": { "assignments": 0, "signups": 0 },
    "variant_c": { "assignments": 0, "signups": 0 }
  }
}
```

## Integration with Existing Templates

This document complements the verified templates in `/Users/eduardgridan/faintech-lab/data/ops/GTM-WEEK2-ANALYTICS-TEMPLATES.md`:

- **Template 1 (Daily Metrics Aggregation):** Use daily/ folder structure above
- **Template 2 (A/B Test Statistical Analysis):** Apply chi-square and t-test formulas to aggregated data
- **Template 3 (Weekly Performance Report):** Aggregate weekly/ folder content into 1,000+ word report
- **Template 4 (Conversion Funnel Validation):** Verify UTM parameters are properly captured and attributed

---

**Next Action:** Set up data collection infrastructure by April 3, 09:00 EET to capture Week 2 GTM performance.
