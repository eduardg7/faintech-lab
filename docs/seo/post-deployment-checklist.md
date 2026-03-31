# Post-Deployment Verification Checklist - Faintech Lab SEO

> Owner: faintech-seo | Created: 2026-03-31
> Purpose: Enable immediate SEO execution when P0 demo URLs unblocked

## Deployment Verification

### Step 1: Demo URL Health Check (immediate)
- [ ] https://faintech-lab.vercel.app returns HTTP 200
- [ ] https://lab.faintech.ai returns HTTP 200 (after CEO DNS config)
- [ ] https://faintech-lab.com returns HTTP 200 (after CEO DNS config)
- [ ] SSL/HTTPS valid for all URLs
- [ ] Robots.txt accessible at /robots.txt
- [ ] Sitemap.xml accessible at /sitemap.xml
- [ ] JSON-LD schema present on key pages

**Tool:** `curl -I <URL>`, browser developer tools
**Expected time:** 2 minutes

### Step 2: Sitemap Validation (immediate)
- [ ] XML format valid (no syntax errors)
- [ ] All target URLs included in sitemap
- [ ] Lastmod dates recent (not stale)
- [ ] Sitemap size < 10MB (Google limit)
- [ ] Priority pages listed first

**Tool:** `xmllint --schema sitemap.xml`, manual review
**Expected time:** 1 minute

### Step 3: Robots.txt Verification (immediate)
- [ ] File returns HTTP 200
- [ ] Crawlable by Google bot (User-Agent: Googlebot)
- [ ] No syntax errors
- [ ] Critical paths NOT blocked (sitemap.xml, /, /amc)

**Tool:** Google Search Console Robots Testing Tool
**Expected time:** 2 minutes

---

## Search Console Setup

### Step 4: Property Creation (within 15 min)
- [ ] Add property: https://faintech-lab.vercel.app
- [ ] Add property: https://lab.faintech.ai (when available)
- [ ] Add property: https://faintech-lab.com (when available)
- [ ] Verify domain ownership (DNS or HTML file upload)
- [ ] Enable data sharing for all properties

**Tool:** https://search.google.com/search-console
**Expected time:** 10 minutes

### Step 5: Sitemap Submission (within 30 min)
- [ ] Submit /sitemap.xml to each Search Console property
- [ ] Verify sitemap status: "Success"
- [ ] Monitor Coverage report for indexing errors
- [ ] Check for 404/500 errors in submitted URLs

**Tool:** Search Console > Sitemaps > Add a new sitemap
**Expected time:** 5 minutes

---

## Core Web Vitals Baseline

### Step 6: Performance Audit (within 1 hour)
- [ ] Run Lighthouse audit on https://faintech-lab.vercel.app
- [ ] Capture LCP (Largest Contentful Paint) score
- [ ] Capture INP (Interaction to Next Paint) score
- [ ] Capture CLS (Cumulative Layout Shift) score
- [ ] Document baseline scores in SEO-STRATEGY.md

**Targets:**
- LCP < 2.5s (Good)
- INP < 200ms (Good)
- CLS < 0.1 (Good)

**Tool:** https://pagespeed.web.dev/, Chrome DevTools > Lighthouse
**Expected time:** 10 minutes

### Step 7: Mobile Usability (within 1 hour)
- [ ] Verify mobile responsiveness
- [ ] Check tap targets (48x48px minimum)
- [ ] Verify font readability (12px minimum)
- [ ] Test on multiple mobile viewports (iPhone SE, iPhone 12, Pixel)

**Tool:** Chrome DevTools > Device Toolbar
**Expected time:** 5 minutes

---

## Schema Validation

### Step 8: JSON-LD Verification (within 30 min)
- [ ] Test JSON-LD schema on key pages
- [ ] Validate SoftwareApplication schema type
- [ ] Check for required properties (name, description, applicationCategory)
- [ ] Verify eligibility for rich results

**Tool:** https://search.google.com/test/rich-results
**Expected time:** 5 minutes

---

## Indexation Monitoring

### Step 9: Coverage Report Check (Day 1-3)
- [ ] Check Coverage report in Search Console
- [ ] Identify which pages are indexed
- [ ] Identify which pages are excluded (why?)
- [ ] Verify 80%+ pages indexed (target for Week 1)
- [ ] Fix any critical indexing errors

**Tool:** Search Console > Index > Coverage
**Expected time:** Weekly monitoring (2 minutes/check)

### Step 10: Error Tracking (ongoing)
- [ ] Set up Search Console email alerts
- [ ] Monitor for 5xx server errors
- [ ] Monitor for 4xx client errors
- [ ] Track robots.txt blocking errors
- [ ] Fix critical errors within 24h

**Tool:** Search Console > Settings > Alerts
**Expected time:** Setup 5 min, ongoing monitoring

---

## Success Criteria

### Deployment Verification (Day 0)
- ✅ All demo URLs return HTTP 200
- ✅ Sitemap.xml valid and accessible
- ✅ Robots.txt valid and crawlable
- ✅ JSON-LD schema present and accessible

### Search Console Setup (Day 0-1)
- ✅ All properties created and verified
- ✅ Sitemaps submitted with "Success" status
- ✅ No critical indexing errors

### Performance Baseline (Day 0-1)
- ✅ Core Web Vitals baseline established
- ✅ Mobile usability verified
- ✅ JSON-LD schema validated

### Indexation Monitoring (Day 1-7)
- ✅ 80%+ pages indexed
- ✅ Search Console alerts configured
- ✅ Error tracking active

---

## Next Actions After Verification Complete

1. **Document Baseline Scores** in SEO-STRATEGY.md (Core Web Vitals, indexation rate)
2. **Monitor Organic Traffic** via Search Console (track from 0-3 views/day baseline)
3. **Adjust Strategy** based on Search Console query data (keywords with impressions, low CTR)
4. **Publish LinkedIn Articles** (3 articles ready in week2-social-content/)
5. **Prepare Week 2 GTM Content** (Reddit posts, Twitter announcements)

---

## Total Estimated Time to Complete Verification

| Phase | Time | Cumulative |
|---------|-------|-------------|
| Deployment Verification | 5 min | 5 min |
| Search Console Setup | 15 min | 20 min |
| Sitemap Submission | 5 min | 25 min |
| Core Web Vitals Audit | 10 min | 35 min |
| Mobile Usability Check | 5 min | 40 min |
| Schema Validation | 5 min | 45 min |
| Initial Indexation Check | 2 min | 47 min |

**Total:** < 1 hour to complete all verification steps

---

## Blocker Notes

- **All steps depend on P0 demo URL resolution** (custom domain DNS configuration by CEO)
- **Workaround available:** Can use https://faintech-lab.vercel.app for testing and initial verification
- **Critical dependency:** Search Console property creation requires live URLs

---

*Status Checklist created. Ready for immediate execution when P0 demo URLs unblocked.*
