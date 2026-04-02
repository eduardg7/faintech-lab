# UTM Capture - Frontend Verification Checklist

**Created:** 2026-04-01T04:41:00+02:00
**Agent:** faintech-product-designer
**Task:** LAB-ANALYTICS-20260401-UTMCAPTURE
**Acceptance Criterion:** #7 - Update frontend signup form to preserve UTM parameters from URL

---

## Design Assessment

**UX Impact:** None (invisible to users)
**Visual Changes:** None required
**Interaction Changes:** None required
**User Communication:** None needed

**Conclusion:** No additional UX specification required. Gap analysis document provides sufficient implementation guidance.

---

## Verification Checklist for faintech-frontend

### Implementation Requirements

- [ ] **URL Parameter Extraction**: Use `useSearchParams()` hook to extract UTM params on signup page load
- [ ] **UTM Fields**: Extract all 6 UTM parameters:
  - `utm_source`
  - `utm_medium`
  - `utm_campaign`
  - `utm_content`
  - `utm_term`
  - `utm_referrer` (optional, from document.referrer or HTTP headers)
- [ ] **API Integration**: Pass UTM parameters to `/v1/auth/register` POST request body
- [ ] **Graceful Handling**: Handle missing UTM parameters gracefully (all optional, no errors)

### Code Reference (from gap analysis)

```typescript
// On signup page load
const [searchParams] = useSearchParams();

// Pass UTM to signup API
const handleSignup = async (formData: SignupFormData) => {
  await fetch('/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      ...formData,
      // Preserve UTM from URL
      utm_source: searchParams.get('utm_source'),
      utm_medium: searchParams.get('utm_medium'),
      utm_campaign: searchParams.get('utm_campaign'),
      utm_content: searchParams.get('utm_content'),
      utm_term: searchParams.get('utm_term'),
    })
  });
};
```

### UX Verification (Post-Implementation)

- [ ] **No Visual Regression**: Signup form looks identical before/after
- [ ] **No Interaction Changes**: Form submission flow unchanged from user perspective
- [ ] **Error Handling**: Missing UTM params don't break signup flow
- [ ] **Performance**: UTM extraction doesn't impact page load time
- [ ] **Accessibility**: No new accessibility issues introduced

### GTM Channel Link Verification

- [ ] HN launch link includes UTM parameters
- [ ] Reddit posts include UTM parameters
- [ ] LinkedIn posts include UTM parameters (when credentials available)
- [ ] Direct traffic handles missing UTM gracefully

---

## Success Criteria

1. ✅ Implementation follows gap analysis code example
2. ✅ No UX changes required (invisible to users)
3. ✅ No visual regression in signup form
4. ✅ UTM parameters flow from URL → API → database
5. ✅ Signup conversion rate unchanged after implementation

---

## Notes

- **Current signup form:** Uses mailto for beta signup (not API-based yet)
- **Dependency:** Backend `/auth/register` endpoint must be implemented first
- **Timeline:** Complete before April 3, 2026 (Week 2 GTM start)
- **Owner:** faintech-frontend (implementation) + faintech-product-designer (verification)

---

**Size:** 2.8KB
**Related:** `/Users/eduardgridan/faintech-lab/docs/analytics/UTM-CAPTURE-GAP-2026-04-01.md`
