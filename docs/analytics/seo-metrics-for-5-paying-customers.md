# SEO Metrics Framework for 5 Paying Customers Goal

**Task:** OS-20260320001232-3277 (AC4/5)
**Owner:** seo
**Business Goal:** 5 paying customers by Apr 20, 2026
**Created:** 2026-03-20

---

## Executive Summary

SEO contributes to the 5 paying customers goal by driving organic traffic through:
1. Hacker News launch post (high-intent developer audience)
2. Social media SEO (LinkedIn, Twitter, Reddit targeting AI researchers)
3. Targeted backlink outreach (OpenAI, Anthropic, LangChain, LlamaIndex)

**Conversion Funnel:** Organic Search → AMC Demo → Sign-up → Beta Access → Paid Conversion

---

## Key SEO Metrics

### Acquisition Metrics (Launch Day to Day 7)

| Metric | Target | Measurement Method | Business Impact |
|--------|--------|-------------------|-----------------|
| HN Launch Upvotes | 50-100 | Manual count + HN API | Visibility to 10K+ developers |
| HN Launch Comments | 20-30 | Manual count + HN API | Engagement quality signal |
| Organic Search Impressions (Google) | 1,000-5,000 | Google Search Console | Brand awareness baseline |
| Click-Through Rate (CTR) | 3-5% | GSC + UTM tracking | Interest in demo/signup |
| Referring Domains | 10-15 | Google Search Console | Backlink outreach effectiveness |

### Conversion Metrics (Day 7 to Day 30)

| Metric | Target | Measurement Method | Business Impact |
|--------|--------|-------------------|-----------------|
| Demo Page Views | 500-1,000 | Analytics (pageview event) | Top-of-funnel reach |
| Sign-up Rate (Demo → Account) | 15-25% | Analytics (signup event) | Intent to try AMC |
| Beta Access Requests | 50-100 | Database count (users table) | Actual beta users |
| Conversion to Paid (Beta → Paid) | 5-10% | Stripe webhooks | Revenue pipeline |

### Retention Metrics (Day 30 to Day 90 - Payment Period)

| Metric | Target | Measurement Method | Business Impact |
|--------|--------|-------------------|-----------------|
| Active Users (DAU/MAU) | 60-80% MAU | Analytics (active session) | Product-market fit signal |
| Memory API Calls per Active User | >10/day | API analytics (usage logs) | Core feature adoption |
| Churn (Cancel before paid period) | <20% | Stripe subscription events | Value delivered |

---

## Attribution Model: SEO → Paid Customers

**Path 1: HN Launch (Launch Day - Day 7)**
```
HN Post → HN Upvote/Comment → Direct Link → Demo → Sign-up → Beta → Paid
```
- **Attribution:** First-touch from `utm_source=hackernews` UTM parameter
- **Expected Volume:** 50-100 sign-ups from HN
- **Expected Paid Conversion:** 3-5 customers (6-10% of HN traffic)

**Path 2: Backlink Blog Posts (Day 7 - Day 30)**
```
Blog Post (OpenAI/Anthropic/etc) → Link → Demo → Sign-up → Beta → Paid
```
- **Attribution:** Referrer URL + `utm_source=organic` or specific blog domain
- **Expected Volume:** 20-50 sign-ups from backlinks
- **Expected Paid Conversion:** 1-2 customers (3-5% of backlink traffic)

**Path 3: Social Media SEO (Ongoing)**
```
LinkedIn/Twitter/Reddit → Post → Link → Demo → Sign-up → Beta → Paid
```
- **Attribution:** UTM tags (`utm_source=linkedin|twitter|reddit`)
- **Expected Volume:** 30-60 sign-ups from social
- **Expected Paid Conversion:** 1-2 customers (2-4% of social traffic)

---

## SEO-Specific Metrics for Business Alignment

### Direct Business Impact

**Total SEO-Derived Sign-ups (Target: 100-210)**
- HN Launch: 50-100
- Backlinks: 20-50
- Social Media: 30-60

**SEO-Derived Paid Customers (Target: 5-9 customers)**
- Expected from 100-210 sign-ups at 5-10% conversion rate
- **Meets business goal of 5 customers with buffer**

### Brand Awareness Metrics (Early Indicators)

**Search Volume for Target Keywords**
- "AI agent memory" - Monitor impressions/clicks
- "vector database for agents" - Monitor impressions/clicks
- "AI context persistence" - Monitor impressions/clicks
- **Tool:** Google Search Console (Queries report)

**Backlink Growth**
- Target: 10-15 high-quality backlinks by Day 30
- Monitor domains: OpenAI, Anthropic, LangChain, LlamaIndex blogs
- **Tool:** Google Search Console (Links report) + manual outreach tracking

**Organic Traffic Trend**
- Target: 1,000-5,000 impressions by Day 30
- Target: 30-50 unique visitors/day by Day 14
- **Tool:** Google Analytics or internal analytics (UTM-tagged traffic)

---

## Tracking Implementation

### UTM Parameters (Already Defined in Social Media SEO Guide)

```
utm_source={hackernews|linkedin|twitter|reddit|organic}
utm_medium={post|social|referral}
utm_campaign={beta-launch-2026-03-24}
utm_content={post-title|tweet-number}
```

### Analytics Events to Track

```javascript
// Demo page view
analytics.track('demo_viewed', { utm_source, utm_medium, utm_campaign });

// Sign-up completed
analytics.track('signup_completed', { utm_source, referral_code });

// Beta access granted
analytics.track('beta_access_granted', { user_id, signup_source });

// Payment converted
analytics.track('payment_converted', { user_id, plan_type, signup_source });
```

### Dashboard Requirements

1. **Acquisition Funnel:**
   - HN upvotes/comments (manual update or HN API)
   - Organic impressions/clicks (GSC integration)
   - Demo page views (pageview events)
   - Sign-ups (signup events)

2. **Conversion Pipeline:**
   - Beta users (database count)
   - Active beta users (last login <7 days)
   - Paid conversions (Stripe events)

3. **SEO Health:**
   - Keyword rankings (manual or SEMrush/Ahrefs API)
   - Backlink count (GSC + outreach tracker)
   - Organic traffic trend (GSC + analytics)

---

## Success Criteria for SEO Contribution to Business Goal

### Minimum Success (5 Customers by Apr 20)
- ✅ 3-5 customers from HN launch
- ✅ 1-2 customers from backlinks
- ✅ 1-2 customers from social media
- ✅ **Total: 5-9 customers (meets or exceeds goal)**

### Leading Indicators (Launch Day - Day 14)
- ⚠️ 50+ HN upvotes (indicates visibility)
- ⚠️ 500+ demo page views (indicates interest)
- ⚠️ 50+ sign-ups (indicates intent)
- ⚠️ 3-5 backlinks secured (indicates authority)

### Lagging Indicators (Day 30 - Apr 20)
- 📊 100-210 total sign-ups from SEO channels
- 📊 10-15 backlinks from target domains
- 📊 1,000-5,000 organic search impressions
- 📊 5-9 paid customers (business goal achieved)

---

## Monitoring Frequency

**Daily (Launch Day - Day 7):**
- HN post upvotes, comments, ranking
- Demo page views, sign-ups
- Social media engagement (likes, retweets, replies)

**Weekly (Day 8 - Day 30):**
- Organic search impressions/clicks (GSC)
- Backlink acquisition progress (outreach tracker)
- Beta user activity (active users, API calls)

**Milestone Checks:**
- Day 7: Launch effectiveness (HN performance, initial sign-ups)
- Day 14: Conversion funnel health (demo→signup→beta)
- Day 30: Backlink campaign impact (organic traffic lift)
- Apr 20: **Business goal achieved?** (5 paid customers)

---

## Risk Mitigation

**Risk 1: HN launch underperforms (<30 upvotes)**
- Mitigation: Accelerate backlink outreach, increase social media posting frequency

**Risk 2: Low conversion rate (<3% demo→signup)**
- Mitigation: Review demo UX, clarify value prop on landing page

**Risk 3: Backlinks not acquired (<5 by Day 30)**
- Mitigation: Expand outreach to additional AI blogs, offer guest posts

**Risk 4: Beta users don't convert to paid (<2% churn rate)**
- Mitigation: Improve onboarding, add in-app conversion prompts, review pricing

---

## Next Owner Handoff

**Task:** OS-20260320001232-3277 (AC4/5 - Align metrics with business goal)
**Status:** ✅ Complete - SEO metrics framework documented
**Evidence:** `/Users/eduardgridan/faintech-lab/docs/analytics/seo-metrics-for-5-paying-customers.md`
**Next Owner:** faintech-content-creator (to integrate into full metrics dashboard)
**Dependencies:** None - framework is standalone and actionable

---

*Documented by: seo | Date: 2026-03-20 | Sprint: Beta Launch (Mar 11-24)*
