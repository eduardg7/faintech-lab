# EU Hosting Verification Checklist

**Task:** LAB-LEGAL-20260322-DPIA-PROD (AC4)
**Purpose:** Verify EU-based hosting for all production data before public launch (Mar 31)
**Privacy Policy Claim:** "Faintech Lab operates on servers located in the European Union. Your data is processed and stored within the EU/EEA."

---

## Verification Requirements

### 1. Frontend Hosting
**Status:** ⏸️ Pending verification
**Provider:** [To be confirmed - likely Vercel]
**Verification Needed:**
- [ ] Confirm hosting provider
- [ ] Verify region is EU-based (e.g., eu-west-1, eu-central-1)
- [ ] Confirm no data storage on frontend (static assets only)
- [ ] Document in privacy policy if CDN used for performance

**Evidence Required:**
- Screenshot of deployment configuration
- Provider documentation showing EU region
- Data processing agreement (DPA) if third-party provider

---

### 2. Backend API Hosting
**Status:** ⏸️ Pending verification
**Provider:** [To be confirmed]
**Verification Needed:**
- [ ] Confirm hosting provider
- [ ] Verify region is EU-based
- [ ] Confirm no data transfers outside EU/EEA
- [ ] Verify provider has GDPR-compliant DPA

**Evidence Required:**
- Deployment configuration
- Provider region settings
- Data processing agreement
- Sub-processor list (if applicable)

---

### 3. Database Hosting (Neon PostgreSQL)
**Status:** ⏸️ Pending verification
**Provider:** Neon (mentioned in DAILY-CONTEXT as TD-017-INFRA-001)
**Verification Needed:**
- [ ] Confirm Neon region is EU-based
- [ ] Verify Neon's data processing location
- [ ] Confirm Neon's GDPR compliance and DPA
- [ ] Verify Neon's sub-processor locations (if any)

**Evidence Required:**
- Neon dashboard screenshot showing region
- Neon DPA/GDPR compliance documentation
- Neon sub-processor list

**Note:** Task TD-017-INFRA-001 is currently blocked awaiting Neon credentials from Eduard

---

### 4. AI/LLM Providers
**Status:** ⏸️ Pending verification
**Providers:** [To be identified]
**Verification Needed:**
- [ ] List all AI/LLM providers used (e.g., OpenAI, Anthropic, local models)
- [ ] For each provider:
  - [ ] Verify data processing location
  - [ ] Confirm if data leaves EU/EEA
  - [ ] If US-based: Verify Standard Contractual Clauses (SCCs) or other safeguards
  - [ ] Document in privacy policy with opt-out mechanism if required

**Evidence Required:**
- List of all AI providers
- Data processing agreements for each
- SCCs or equivalent safeguards for non-EU providers
- Transparency in privacy policy about AI processing

**Risk:** High - AI providers may process data in US, requiring SCCs or EU-only alternatives

---

### 5. Vector Embedding Storage
**Status:** ⏸️ Pending verification
**Provider:** [To be confirmed - may be same as database]
**Verification Needed:**
- [ ] Where are vector embeddings stored?
- [ ] Is storage EU-based?
- [ ] If separate provider: verify DPA and location

**Evidence Required:**
- Storage provider confirmation
- Region documentation
- DPA if third-party provider

---

### 6. Analytics & Tracking
**Status:** ⏸️ Pending verification
**Providers:** [To be identified - Plausible mentioned in recent commits]
**Verification Needed:**
- [ ] List all analytics providers
- [ ] Verify Plausible is self-hosted or EU-based SaaS
- [ ] Confirm no data transfer outside EU/EEA
- [ ] Verify GDPR compliance

**Evidence Required:**
- Analytics provider list
- Hosting documentation
- DPA if third-party

---

### 7. CDN & Static Assets
**Status:** ⏸️ Pending verification
**Provider:** [To be identified - likely Vercel CDN or similar]
**Verification Needed:**
- [ ] Confirm CDN provider
- [ ] Verify CDN has EU edge locations
- [ ] Confirm no personal data stored in CDN (only static assets)

**Evidence Required:**
- CDN configuration
- Edge location list

---

## Compliance Summary

| Component | Provider | EU Region | DPA | Status |
|-----------|----------|-----------|-----|--------|
| Frontend | TBD | ❓ | ❓ | ⏸️ Pending |
| Backend | TBD | ❓ | ❓ | ⏸️ Pending |
| Database | Neon | ❓ | ❓ | ⏸️ Pending |
| AI/LLM | TBD | ❓ | ❓ | ⏸️ Pending |
| Embeddings | TBD | ❓ | ❓ | ⏸️ Pending |
| Analytics | Plausible? | ❓ | ❓ | ⏸️ Pending |
| CDN | TBD | ❓ | ❓ | ⏸️ Pending |

---

## Next Steps

### For DevOps (Owner: devops)
1. Complete hosting verification for all 7 components
2. Gather evidence (screenshots, DPAs, region documentation)
3. Update this checklist with verification results
4. Coordinate with Legal for privacy policy updates if needed

### For Legal (Owner: legal)
1. Review all DPAs and compliance documentation
2. Update privacy policy with accurate hosting information
3. Verify AI provider transparency requirements met
4. Coordinate with DevOps on any non-EU providers requiring SCCs

### Timeline
- **Beta Launch (Mar 24):** Not required - beta compliance already verified
- **Production Launch (Mar 31):** REQUIRED - must complete before public launch
- **Deadline for DevOps:** Mar 29 (2 days before production launch)

---

## Risk Assessment

### High Risk Items
1. **AI/LLM Providers:** If using US-based providers (OpenAI, Anthropic), need SCCs and transparency
2. **Database Region:** Neon credentials pending - could delay verification

### Medium Risk Items
1. **Backend Hosting:** Unknown provider - may require DPA review
2. **Analytics:** Plausible likely fine, but needs confirmation

### Low Risk Items
1. **Frontend/CDN:** Usually static assets only, minimal risk
2. **Embeddings:** Likely same as database, verification should be straightforward

---

## Acceptance Criteria Completion

This checklist completes **AC4: Hosting location verified as EU-based for all production data** when:

- [ ] All 7 components verified
- [ ] Evidence gathered for each
- [ ] DPAs reviewed and approved for all third-party providers
- [ ] Privacy policy updated with accurate hosting information
- [ ] Non-EU providers documented with appropriate safeguards (SCCs)

---

**Created:** 2026-03-22 23:55 EET
**Owner:** Legal (verification by DevOps)
**Task:** LAB-LEGAL-20260322-DPIA-PROD
**Deadline:** Mar 29 (2 days before production launch)
