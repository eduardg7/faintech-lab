# Data Breach Response Plan

**Project:** Faintech Labs (AMC - Agent Memory Component)
**Version:** 1.0
**Date:** 2026-03-21
**Status:** Draft - Production Readiness
**Deadline:** Mar 31, 2026 (Public Launch)

---

## 1. Purpose

This document defines the process Faintech Solutions SRL will follow to detect, assess, contain, and report personal data breaches in compliance with EU GDPR Article 33 (72-hour notification to supervisory authority) and Article 34 (communication to data subjects for high-risk breaches).

---

## 2. Internal Response Team

### Core Response Team

| Role | Responsibilities | Agent/Owner |
|-------|----------------|--------------|
| **Incident Commander** | Overall coordination, escalation decisions, final notifications | CISO |
| **Technical Lead** | Forensic analysis, system containment, log evidence | DevOps |
| **Legal Advisor** | GDPR interpretation, notification wording, regulatory compliance | Legal |
| **Communication Lead** | User messaging, transparency page updates, press coordination | CEO/CMO |

### Escalation Matrix

| Risk Level | Notification Required | Escalation Timeline |
|-------------|----------------------|---------------------|
| **Low** (no personal data exposed, minimal impact) | Internal logging only | Document in incident log |
| **Medium** (personal data accessed, potential misuse) | ANSPDCP notification within 72h | Immediate notification to CISO, assessment within 4h |
| **High** (special category data, large-scale exposure, identity theft risk) | ANSPDCP + data subject notification within 72h | Immediate callout, CEO/CTO/CISO involved, full team mobilization |

---

## 3. Breach Classification Criteria

### Notification Trigger (GDPR Article 33)

A breach **requires notification to ANSPDCP** if it is "likely to result in a risk to the rights and freedoms of natural persons."

**Classification Decision Tree:**

1. **Was personal data accessed, lost, or disclosed?**
   - No → Internal incident only (log, no notification)
   - Yes → Continue to #2

2. **Was the data encrypted or anonymized?**
   - Yes, and keys not compromised → Low risk (document, no notification)
   - No or keys compromised → Continue to #3

3. **What categories of data were affected?**
   - Email/name only → Medium risk (72h notification)
   - GitHub profile + usage patterns → Medium risk (72h notification)
   - Voice biometrics (special category per GDPR Article 9) → **HIGH risk** (72h notification + user communication)

4. **How many data subjects affected?**
   - 1-10 users → Medium risk
   - 10-100 users → Medium/High risk
   - 100+ users → **HIGH risk** (presumption of widespread impact)

### Risk Assessment Checklist

When a breach is detected, answer:

- [ ] Personal data accessed/lost/disclosed? (Yes/No)
- [ ] Data encrypted? (Yes/No)
- [ ] Special category data (voice biometrics, health, political opinions)? (Yes/No)
- [ ] Likely to result in identity theft or financial loss? (Yes/No)
- [ ] Likely to result in reputational damage or discrimination? (Yes/No)
- [ ] Number of affected users: ___

**If any "Yes" + special category OR 100+ users → HIGH RISK → Full notification required.**

---

## 4. Detection Procedures

### Monitoring Capabilities

1. **24/7 System Monitoring** (DevOps responsibility)
   - Database access logs (PostgreSQL query logs)
   - API endpoint access logs (FastAPI/Next.js routes)
   - Agent memory read/write operations
   - Authentication failures and unusual login patterns

2. **Log Retention** (90+ days minimum for GDPR Article 30 records)
   - Access logs stored in `/var/log/faintech-lab/access.log`
   - Backup logs retained for 180 days
   - Audit trail for all user data access

3. **Alert Triggers**
   - Failed authentication > 5 attempts from same IP within 10 min
   - Unusual database query patterns (SELECT * from user_accounts, mass export)
   - Agent memory bulk exports (>100 records in 5 min)
   - API rate limit breaches from non-authorized sources

### Initial Detection Steps

When an alert triggers or suspicious activity is reported:

1. **Acknowledge alert** within 15 minutes (DevOps on-call)
2. **Verify scope**: Which system, which data type, which users affected?
3. **Contain immediately**: Rotate credentials, block IPs, disable compromised endpoints
4. **Preserve evidence**: Snapshot logs, database state, memory dumps (do NOT delete)
5. **Escalate**: Notify CISO within 30 minutes with preliminary assessment

---

## 5. Breach Assessment Checklist

When breach is confirmed, document:

### Technical Details
- [ ] Breach discovery date/time: ___
- [ ] Breach start date/time (if known): ___
- [ ] Attack vector (SQL injection, auth bypass, insider threat, etc.): ___
- [ ] Affected systems (database, API, agent memory, logs): ___
- [ ] Data types exposed (email, name, GitHub ID, agent interactions, voice biometrics): ___

### Impact Assessment
- [ ] Number of user accounts affected: ___
- [ ] Number of records exposed: ___
- [ ] Special category data involved (Article 9): Yes/No
- [ ] Likelihood of misuse/identity theft: Low/Medium/High
- [ ] Likelihood of reputational damage: Low/Medium/High

### Containment Status
- [ ] Containment method applied (IP block, credential rotation, service shutdown): ___
- [ ] Containment completion time: ___
- [ ] Root cause identified: Yes/No (if Yes, describe): ___
- [ ] Additional vulnerabilities discovered: Yes/No

---

## 6. Notification Procedures

### ANSPDCP Notification (Article 33)

**Timeline:** Within 72 hours of becoming aware of the breach

**Required Content:**
1. Nature of the personal data breach
2. Categories and approximate number of data subjects concerned
3. Likely consequences of the breach
4. Measures taken or proposed to address the breach

**Draft Template (Romanian):**

```
Subiect: Notificare încălcare date cu caracter personal - [Nume Faintech Solutions SRL]

Stimate Domnule,

Vă informăm despre o încălcare a datelor cu caracter personal care a avut loc la sistemele noastre, care poate afecta drepturile și libertățile persoanelor vizate.

**Natura încălcării:**
[Descrie tipul de încălcare - acces neautorizat, pierdere accidentală, etc.]

**Categorii de date afectate:**
[Listează tipurile - nume, email, profil GitHub, înregistrări agenți, biometrie vocală]

**Număr estimat de persoane afectate:**
[Număr]

**Consecințe probabile:**
[Evaluează riscuri - furt de identitate, acces neautorizat la date, etc.]

**Măsuri luate:**
[Descrie acțiunile imediate - blocare IP, rotire credențiale, notificare utilizatori]

Contact pentru informații suplimentare:
[Email DPO sau legal contact]
Data notificării: [Data/Ora]
```

**Submission Method:**
- Email: anspdcp@dataprotection.ro
- Form: Contact via registratura (Mon-Fri 09:00-13:00) or phone +40.318.059.211
- Website: https://www.dataprotection.ro/

### User Communication (Article 34)

**Timeline:** "Without undue delay" for high-risk breaches (recommended within 24-48h of ANSPDCP notification)

**Required Content:**
1. Nature of the breach
2. Contact details for Data Protection Officer
3. Measures taken to address the breach
4. Likely consequences
5. Steps to mitigate risks

**Draft Template (Email/In-App Notification):**

```
Subject: Important: Security Incident Information

Dear [User Name],

We are writing to inform you about a security incident that may have affected your personal data.

**What Happened:**
On [date], we discovered unauthorized access to [system/component]. This incident affected user account data including [list data types].

**What We Did:**
- Immediately contained the incident by [containment method]
- Began investigation into root cause
- Implemented additional security measures
- Notified the relevant data protection authorities

**What This Means For You:**
[Describe risks - if any action needed from user, e.g., "We recommend changing your password"]

**What We're Doing to Protect You:**
- [Specific measures - enhanced monitoring, security audits, etc.]

**Questions?**
Contact our Data Protection Officer at [email] with subject "Security Inquiry - [Date]".

We sincerely apologize for any concern this may cause.

Sincerely,
Faintech Solutions SRL
```

### Transparency Page

**URL:** `https://faintech.lab/security/transparency` (to be created)

**Content:**
- Public incident log (date, summary, status)
- Current incident status (if active)
- Security best practices for users
- Contact information for security inquiries

---

## 7. Post-Incident Review

### Root Cause Analysis Timeline

Within 7 days of breach resolution:

1. **Document root cause**: Technical failure? Human error? Attack vector?
2. **Identify gaps**: Missing controls, process failures, training needs
3. **Propose fixes**: Technical patches, process updates, policy changes
4. **Assign owners**: Who implements each fix?
5. **Set deadline**: When will fixes be complete?

### Process Improvement Loop

After each breach, update:

- [ ] Risk register (add new threat scenario)
- [ ] Security checklist (new detection rule)
- [ ] Training materials (real-world example)
- [ ] This response plan (lessons learned)

---

## 8. Required Deliverables for Production Readiness

Before Mar 31, 2026 (Public Launch):

- [x] Data Breach Response Plan document (this file)
- [ ] Designated Data Protection Officer appointed
- [ ] ANSPDCP notification email/portal confirmed
- [ ] 24/7 monitoring setup and tested
- [ ] 90+ day log retention implemented
- [ ] Transparency page created and linked from footer
- [ ] Response team contact list published
- [ ] User notification templates localized (English + Romanian)
- [ ] Post-incident review process documented

---

## 9. References

- **GDPR Article 33:** Notification of a personal data breach to the supervisory authority
- **GDPR Article 34:** Communication of a personal data breach to the data subject
- **GDPR Article 35:** Data protection impact assessment (DPIA)
- **ANSPDCP Website:** https://www.dataprotection.ro/ (Romanian Data Protection Authority)
- **GDPR.eu Official Guidance:** https://gdpr.eu/data-breaches/

---

**Next Steps:**
1. Review with CISO and DevOps to verify technical detection capabilities
2. Confirm ANSPDCP notification channels
3. Create transparency page at `https://faintech.lab/security/transparency`
4. Conduct tabletop breach response simulation (pre-launch exercise)
5. Document DPO contact information
6. Translate user notification templates to Romanian

**Status:** Draft - Awaiting CISO/DevOps technical validation
