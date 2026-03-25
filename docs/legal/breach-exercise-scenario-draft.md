# Data Breach Tabletop Exercise - Scenario Draft

**Task:** LAB-LEGAL-20260322-DPIA-PROD (AC3)
**Purpose:** Test breach response plan before production launch (Mar 31)
**Duration:** 2-3 hours
**Participants:** CISO (Incident Commander), DevOps (Technical Lead), Legal (Compliance), Communication Lead

---

## Exercise Objectives

1. **Test Response Timeline:** Verify 72-hour ANSPDCP notification capability
2. **Validate Communication Flow:** Test internal escalation and external notification procedures
3. **Identify Gaps:** Discover missing tools, contacts, or procedures
4. **Build Muscle Memory:** Ensure team knows their roles in crisis

---

## Scenario: Ransomware Attack with Data Exfiltration

### Background (T-0: Friday 22:00 EET - Before Holiday Weekend)

**Situation:**
- DevOps on-call engineer receives automated alert: unusual database query patterns detected
- Initial investigation suggests possible SQL injection attack
- Further analysis reveals: attacker accessed database 4 hours ago (18:00 EET)
- Evidence of data exfiltration: large outbound transfer to unknown IP

**Data Potentially Affected:**
- User email addresses (all beta users)
- User interaction history (last 30 days)
- Vector embeddings (memory content)
- No voice recordings in database (stored separately)
- No payment data (not yet implemented)

**Attacker Claim:**
- Ransom note received at 22:30 EET
- Demands €50,000 in Bitcoin
- Threatens to publish user data on dark web
- Claims to have 10,000 user records (actual beta users: ~50)

---

## Exercise Timeline (Real-Time Simulation)

### Phase 1: Detection & Triage (T+0 to T+1 hour)

**00:00 - Alert Received**
- DevOps: What do you do first?
- What tools do you have for detection?
- Who do you notify immediately?

**00:15 - Initial Assessment**
- Legal: Is this a personal data breach under GDPR?
- What data categories are affected?
- How many data subjects impacted?

**00:30 - Escalation**
- CISO: Do you activate the breach response team?
- How do you contact team members at 22:00 on Friday?
- Communication Lead: Who needs to be informed internally?

**01:00 - Classification**
- Using breach response plan, classify risk level (Low/Medium/High)
- Decision: Is ANSPDCP notification required?
- Decision: Is data subject notification required?

---

### Phase 2: Containment & Investigation (T+1 to T+12 hours)

**02:00 - Containment Actions**
- DevOps: How do you stop the ongoing attack?
- Do you shut down production?
- How do you preserve evidence?
- Do you isolate affected systems?

**04:00 - Forensic Investigation**
- What logs do you need to collect?
- How do you determine exactly what data was accessed?
- Do you have the technical capability to investigate?
- Do you need external forensic support?

**08:00 - Scope Assessment**
- Legal: Final determination of breach scope
- How many data subjects affected?
- What categories of data compromised?
- Is this "likely to result in a risk to rights and freedoms"?

**12:00 - Evidence Preservation**
- What evidence do you need for ANSPDCP?
- What evidence do you need for potential law enforcement?
- How do you document the timeline?

---

### Phase 3: Notification Preparation (T+12 to T+48 hours)

**24:00 - ANSPDCP Notification Draft**
- Legal: Draft notification to ANSPDCP (anspdcp@dataprotection.ro)
- Required content: nature of breach, categories of data, approximate number of data subjects, likely consequences, measures taken
- Review with CISO and CEO

**36:00 - Data Subject Notification Draft**
- Communication Lead: Draft email to affected users
- Required content: plain language description, contact details, likely consequences, measures taken, recommendations
- Legal review for accuracy

**48:00 - Internal Communication**
- CEO: Draft internal communication for team
- Board notification (if applicable)
- Customer support script

---

### Phase 4: Notification Execution (T+48 to T+72 hours)

**60:00 - ANSPDCP Submission**
- Legal: Submit notification to ANSPDCP
- Document submission time (72-hour deadline: T+72 hours)
- Prepare for potential follow-up questions

**66:00 - Data Subject Notification**
- Communication Lead: Send notifications to affected users
- Legal: Ensure GDPR Article 34 compliance
- Monitor for user responses/questions

**72:00 - Deadline Check**
- Are we within 72-hour window?
- What if we couldn't complete investigation in time?
- Document any delays and reasons

---

## Exercise Discussion Questions

### Detection & Response
1. **Detection Capability:** Do we have automated alerts for unusual database access?
2. **On-Call Procedures:** Who is on-call during off-hours? How do we reach them?
3. **Initial Triage:** What's the decision tree for "is this a breach?"

### Containment
4. **Shutdown Authority:** Who has authority to shut down production?
5. **Evidence Preservation:** Do we have forensic logging enabled?
6. **Backup Verification:** Are backups tested? Can we restore from clean backup?

### Investigation
7. **Log Retention:** Do we have 90+ days of logs as required by GDPR Article 30?
8. **Data Inventory:** Do we know exactly what data is stored where?
9. **Third-Party Involvement:** Do we have forensic vendor on retainer?

### Notification
10. **ANSPDCP Contact:** Do we have correct contact (anspdcp@dataprotection.ro)?
11. **Template Readiness:** Do we have pre-drafted notification templates?
12. **User Contact:** Do we have current email addresses for all users?

### Communication
13. **Spokesperson:** Who is authorized to speak to media?
14. **Internal Communication:** How do we keep team informed without leaking?
15. **Customer Support:** Is support team trained to handle breach inquiries?

### Legal & Compliance
16. **Documentation:** Are we documenting everything for ANSPDCP and potential litigation?
17. **Insurance:** Do we have cyber insurance? Does it cover this scenario?
18. **Regulatory Follow-Up:** Are we prepared for ANSPDCP investigation?

---

## Exercise Evaluation Criteria

### Success Indicators
- ✅ Detected breach within 1 hour
- ✅ Activated response team within 2 hours
- ✅ Classified breach risk within 4 hours
- ✅ Completed ANSPDCP notification within 72 hours
- ✅ Notified data subjects within 72 hours (if required)
- ✅ Preserved evidence for investigation
- ✅ Maintained documentation throughout

### Failure Indicators
- ❌ Detection delayed >4 hours
- ❌ No clear escalation path
- ❌ Missing contact information for team members
- ❌ No access to logs or evidence
- ❌ Missed 72-hour notification deadline
- ❌ Incomplete or inaccurate notification
- ❌ No documentation of response actions

---

## Post-Exercise Actions

### Immediate (Within 24 hours)
1. Document exercise outcomes and timeline
2. Identify gaps in response plan
3. List missing tools or contacts
4. Prioritize improvements

### Short-Term (Within 1 week)
1. Update breach response plan based on learnings
2. Fill identified gaps (contacts, tools, procedures)
3. Train team members on updated procedures
4. Schedule follow-up exercise if needed

### Long-Term (Before Production Launch)
1. Implement automated detection capabilities
2. Establish forensic logging
3. Create notification templates
4. Brief customer support on breach procedures

---

## Exercise Materials Needed

1. **Breach Response Plan:** /Users/eduardgridan/faintech-lab/docs/legal/data-breach-response-plan.md
2. **Contact List:** Updated contact information for all participants
3. **ANSPDCP Template:** Draft notification template
4. **User Notification Template:** Draft data subject notification
5. **Timeline Tracker:** Spreadsheet or tool to track response timeline
6. **Documentation Template:** Template for recording all response actions

---

## Facilitator Notes

### Role-Playing Guidelines
- CISO: Make decisions as if this is real - don't assume you have information you don't have
- DevOps: Be realistic about technical capabilities and limitations
- Legal: Focus on GDPR compliance and documentation requirements
- Communication Lead: Consider user impact and media response

### Injects (Additional Complications)
- **Inject 1 (T+2 hours):** CEO is traveling and unavailable for 6 hours
- **Inject 2 (T+8 hours):** Media inquiry received - "Is it true Faintech was hacked?"
- **Inject 3 (T+24 hours):** User posts on Twitter about receiving suspicious email
- **Inject 4 (T+48 hours):** ANSPDCP requests additional information

### Hot Wash (Debrief)
After exercise, conduct hot wash to discuss:
1. What went well?
2. What didn't go well?
3. What gaps did we identify?
4. What do we need to fix before production launch?

---

**Created:** 2026-03-23 00:15 EET
**Owner:** Legal (facilitation), CISO (coordination)
**Task:** LAB-LEGAL-20260322-DPIA-PROD
**Status:** Draft - awaiting CISO scheduling confirmation
