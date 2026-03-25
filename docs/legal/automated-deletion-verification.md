# Automated Data Deletion Verification

**Task:** LAB-LEGAL-20260322-DPIA-PROD (AC2)
**Purpose:** Verify automated deletion scripts for 90-day memory and 30-day log retention
**Privacy Policy Claim:** "We are implementing automated data deletion to enforce these retention periods during beta"

---

## Retention Requirements (from Privacy Policy)

### Data Categories & Retention Periods

| Data Type | Retention Period | Enforcement Status |
|-----------|------------------|-------------------|
| Text content & memories | Until deletion by user | ✅ User-controlled |
| Voice/audio recordings | 90 days (training) / 30 days (experiment) | ⚠️ **NOT VERIFIED** |
| Behavioral patterns | 12 months (anonymized after 6 months) | ⚠️ **NOT VERIFIED** |
| System logs | 90 days | ⚠️ **NOT VERIFIED** |
| Technical data | 90 days | ⚠️ **NOT VERIFIED** |

---

## Verification Results

### Backend Code Review

**Location:** `/Users/eduardgridan/faintech-lab/amc-backend/`

**Findings:**
1. **Job Queue System:** `app/core/jobs.py` has `cleanup_completed()` method, but this only cleans up job metadata, not user data
2. **No Retention Scripts Found:** No automated deletion scripts found for:
   - Voice recordings (90-day/30-day retention)
   - Behavioral patterns (12-month retention, 6-month anonymization)
   - System logs (90-day retention)
   - Technical data (90-day retention)

**Conclusion:** ⚠️ **Automated deletion NOT YET IMPLEMENTED**

---

## Required Implementation

### 1. Voice/Audio Recordings Deletion (High Priority)
**Retention:** 90 days (training) / 30 days (experiment)
**Required Script:**
```python
# Location: /amc-backend/scripts/cleanup_voice_recordings.py
# Schedule: Daily cron job
# Logic:
# - Delete voice recordings older than 90 days
# - Delete experiment voice recordings older than 30 days
# - Log deletions for audit trail
```

**Owner:** Backend (faintech-backend)
**Estimated Effort:** 2-3 days
**Deadline:** Before production launch (Mar 31)

---

### 2. Behavioral Pattern Anonymization (Medium Priority)
**Retention:** 12 months (anonymized after 6 months)
**Required Script:**
```python
# Location: /amc-backend/scripts/anonymize_behavioral_data.py
# Schedule: Daily cron job
# Logic:
# - Identify behavioral patterns older than 6 months
# - Anonymize by removing user_id association
# - Retain anonymized data for up to 12 months
# - Delete after 12 months
```

**Owner:** Backend (faintech-backend)
**Estimated Effort:** 3-4 days
**Deadline:** Before production launch (Mar 31)

---

### 3. System Logs Deletion (High Priority)
**Retention:** 90 days
**Required Script:**
```python
# Location: /amc-backend/scripts/cleanup_system_logs.py
# Schedule: Daily cron job
# Logic:
# - Delete system logs older than 90 days
# - Maintain audit logs separately (GDPR Article 30 requires 90+ days)
# - Log deletions for compliance audit
```

**Owner:** Backend (faintech-backend) / DevOps
**Estimated Effort:** 1-2 days
**Deadline:** Before production launch (Mar 31)

**Note:** Breach response plan requires "90+ day log retention implemented" for GDPR Article 30 compliance

---

### 4. Technical Data Deletion (Medium Priority)
**Retention:** 90 days
**Required Script:**
```python
# Location: /amc-backend/scripts/cleanup_technical_data.py
# Schedule: Daily cron job
# Logic:
# - Delete technical data (IP addresses, device info, session tokens) older than 90 days
# - Log deletions for audit
```

**Owner:** Backend (faintech-backend)
**Estimated Effort:** 1-2 days
**Deadline:** Before production launch (Mar 31)

---

## Implementation Checklist

### Backend/DevOps Tasks

- [ ] **Create voice recording cleanup script** (2-3 days)
  - [ ] Identify voice recording storage location
  - [ ] Implement deletion logic with 90-day/30-day rules
  - [ ] Add audit logging
  - [ ] Schedule as daily cron job
  - [ ] Test with sample data

- [ ] **Create behavioral pattern anonymization script** (3-4 days)
  - [ ] Identify behavioral data storage
  - [ ] Implement anonymization logic (remove user_id)
  - [ ] Implement 12-month deletion logic
  - [ ] Add audit logging
  - [ ] Schedule as daily cron job
  - [ ] Test with sample data

- [ ] **Create system log cleanup script** (1-2 days)
  - [ ] Identify log storage location
  - [ ] Implement 90-day deletion logic
  - [ ] Preserve audit logs (GDPR Article 30 requirement)
  - [ ] Add audit logging
  - [ ] Schedule as daily cron job
  - [ ] Test with sample data

- [ ] **Create technical data cleanup script** (1-2 days)
  - [ ] Identify technical data storage
  - [ ] Implement 90-day deletion logic
  - [ ] Add audit logging
  - [ ] Schedule as daily cron job
  - [ ] Test with sample data

### DevOps Tasks

- [ ] **Set up cron jobs** (1 day)
  - [ ] Configure daily execution of all cleanup scripts
  - [ ] Set up monitoring/alerting for failed jobs
  - [ ] Configure log rotation for cleanup logs

- [ ] **Testing & Verification** (1 day)
  - [ ] Verify all scripts run successfully
  - [ ] Verify data is actually deleted
  - [ ] Verify audit logs are created
  - [ ] Document in operations runbook

---

## Monitoring & Compliance

### Required Monitoring
1. **Daily Cleanup Job Status:**
   - Success/failure alerts
   - Number of records deleted
   - Execution time

2. **Audit Trail:**
   - Log all deletions with timestamp, data type, count
   - Store audit logs separately (not subject to deletion)
   - Retain audit logs for 2+ years (GDPR best practice)

3. **Compliance Reporting:**
   - Monthly report on data deletion metrics
   - Annual review of retention policy effectiveness

---

## Risk Assessment

### High Risk (Must Fix Before Production)
1. **Voice Recording Retention:** Privacy policy promises 90-day deletion - MUST implement
2. **System Log Retention:** GDPR Article 30 requires 90+ day logs - MUST implement cleanup after 90 days

### Medium Risk (Should Fix Before Production)
1. **Behavioral Pattern Anonymization:** Privacy policy promises 6-month anonymization - SHOULD implement
2. **Technical Data Deletion:** Privacy policy promises 90-day deletion - SHOULD implement

### Low Risk (Can Fix Post-Launch)
1. **Audit Log Retention:** Implement 2-year audit log retention (best practice, not strict requirement)

---

## Acceptance Criteria Completion

This verification completes **AC2: Automated deletion scripts verified for 90-day memory and 30-day log retention** when:

- [ ] All 4 cleanup scripts implemented and tested
- [ ] Cron jobs configured and verified
- [ ] Audit logging implemented
- [ ] Monitoring and alerting configured
- [ ] Documentation added to operations runbook
- [ ] Privacy policy updated to remove "implementing" language

---

## Current Status

**Status:** ⚠️ **NOT IMPLEMENTED**
**Owner:** Backend (implementation), DevOps (deployment), Legal (verification)
**Estimated Total Effort:** 8-12 days
**Deadline:** Mar 30 (1 day before production launch)
**Critical Path:** Voice recordings and system logs are highest priority

---

## Next Steps

1. **Legal → Backend/DevOps:** Request implementation of cleanup scripts
2. **Backend:** Implement and test all 4 cleanup scripts
3. **DevOps:** Deploy scripts and configure cron jobs
4. **Legal:** Verify implementation and update privacy policy

---

**Created:** 2026-03-23 00:10 EET
**Last Updated:** 2026-03-23 00:10 EET
**Owner:** Legal (verification), Backend (implementation)
**Task:** LAB-LEGAL-20260322-DPIA-PROD
