# Data Protection Officer (DPO) Assignment Proposal

**Task:** LAB-LEGAL-20260322-DPIA-PROD (AC1)
**Purpose:** Assign DPO and publish contact in Privacy Policy for production launch
**Deadline:** Mar 31, 2026 (Production Launch)

---

## GDPR DPO Requirements

### When is a DPO Required? (GDPR Article 37)

A DPO is mandatory if the organization:
1. Is a public authority/body, OR
2. Core activities require **regular and systematic monitoring** of data subjects on a large scale, OR
3. Core activities involve **large-scale processing** of special categories of data (Article 9) or criminal convictions

**Faintech Assessment:**
- ✅ Core activities involve AI/LLM processing with potential voice biometrics (Article 9 data)
- ✅ Regular monitoring of user behavior for product improvement
- ⚠️ "Large-scale" threshold: Beta phase may not meet this, but production phase likely will

**Recommendation:** Appoint DPO proactively to demonstrate GDPR compliance commitment, even if not strictly required during beta.

---

## DPO Role & Responsibilities

### Core Responsibilities (GDPR Article 39)
1. **Inform and advise** the organization on GDPR obligations
2. **Monitor compliance** with GDPR, including assignment of responsibilities, awareness-training, and related audits
3. **Provide advice** on Data Protection Impact Assessments (DPIAs)
4. **Act as contact point** for supervisory authority (ANSPDCP) on issues relating to processing
5. **Cooperate with supervisory authority** and act as contact point for data subjects

### Time Commitment
- **Beta Phase:** 2-4 hours/week (monitoring, documentation review)
- **Production Phase:** 5-10 hours/week (compliance monitoring, DPIA reviews, data subject requests)

---

## DPO Assignment Options

### Option 1: Internal DPO (Eduard Gridan - Owner)
**Pros:**
- Deep understanding of company and product
- Direct access to decision-makers
- No additional cost
- Demonstrates personal commitment to compliance

**Cons:**
- May conflict with other roles (CEO, Owner)
- GDPR requires DPO to be independent (Article 38(3))
- Could be perceived as lack of separation between operations and oversight

**GDPR Compliance:** ⚠️ Risky - GDPR Article 38(3) states DPO "shall not be dismissed or penalised by the controller or the processor for performing his tasks" and should have independent reporting lines

**Recommendation:** Not recommended for long-term, but acceptable as **interim measure** for beta phase

---

### Option 2: External DPO Service
**Pros:**
- Full independence (GDPR requirement)
- Specialized GDPR expertise
- Access to compliance resources and best practices
- Scalable (can increase/decrease engagement as needed)

**Cons:**
- Cost: €500-2000/month for DPO services
- Less understanding of specific product/technology
- May require onboarding time

**GDPR Compliance:** ✅ Best practice - ensures independence and specialized expertise

**Recommendation:** Recommended for production phase

**Potential Providers:**
- [Research needed - Romanian/EU-based DPO service providers]

---

### Option 3: Internal Staff Member (Non-Executive)
**Pros:**
- Cost-effective
- Internal knowledge of product
- Can be trained on GDPR requirements

**Cons:**
- May lack specialized GDPR expertise
- Needs dedicated time allocation
- May have conflicts with other responsibilities

**GDPR Compliance:** ✅ Acceptable if given adequate resources and independence

**Recommendation:** Viable if no suitable external candidate and Eduard cannot commit

---

## Recommended Approach

### Phase 1: Beta Launch (Mar 24 - interim)
**DPO:** Eduard Gridan (Owner)
**Title:** Interim Data Protection Officer
**Contact:** dpo@faintech.ro (or dpo@faintechlab.com - pending email domain decision)
**Rationale:** Beta phase has limited users, acceptable risk for interim period

### Phase 2: Production Launch (Mar 31 - permanent)
**DPO:** [To be determined]
**Options:**
1. Hire external DPO service (recommended)
2. Appoint internal staff member with GDPR training
3. Eduard continues if no conflicts identified

**Decision Required:** CEO to decide on permanent DPO approach by Mar 28

---

## Privacy Policy Updates Required

### Current State
Privacy policy states: "For GDPR-specific inquiries: dpo@faintech.ro (beta interim contact)"

### Required Updates (after DPO decision)
1. **Update contact information:**
   - Replace "beta interim contact" with permanent DPO name and contact
   - Ensure email domain is consistent (pending CEO decision on faintech.ro vs faintechlab.com)

2. **Add DPO section:**
   ```markdown
   ## Data Protection Officer

   Our Data Protection Officer (DPO) is responsible for overseeing our data protection strategy and implementation.

   **Contact:**
   - Name: [DPO Name]
   - Email: [dpo@domain]
   - Phone: [Optional]
   ```

3. **Update breach response plan:**
   - Replace placeholder "[Email DPO sau legal contact]" with actual DPO contact

---

## Acceptance Criteria Completion

This proposal completes **AC1: Data Protection Officer assigned and contact published in Privacy Policy** when:

- [ ] CEO decides on DPO approach (interim vs permanent)
- [ ] Email domain decision made (faintech.ro vs faintechlab.com)
- [ ] DPO contact information published in:
  - [ ] Privacy Policy (privacy-policy-beta.md or production version)
  - [ ] Data Breach Response Plan
  - [ ] DPIA template
- [ ] ANSPDCP notified of DPO appointment (if required)

---

## Dependencies

1. **Email Domain Decision:** DPO contact email cannot be finalized until email domain is standardized
2. **CEO Approval:** Final DPO appointment requires CEO approval
3. **Budget (if external):** External DPO service requires budget allocation

---

## Timeline

| Date | Milestone | Owner |
|------|-----------|-------|
| Mar 22 | DPO proposal created | Legal |
| Mar 23 | CEO decision on interim DPO approach | CEO |
| Mar 24 | Interim DPO contact published (beta launch) | Legal |
| Mar 28 | CEO decision on permanent DPO approach | CEO |
| Mar 29 | Permanent DPO appointed (if external) | CEO/Legal |
| Mar 31 | Permanent DPO contact published (production launch) | Legal |

---

**Created:** 2026-03-22 23:58 EET
**Owner:** Legal (decision by CEO)
**Task:** LAB-LEGAL-20260322-DPIA-PROD
**Status:** Proposal - awaiting CEO decision
