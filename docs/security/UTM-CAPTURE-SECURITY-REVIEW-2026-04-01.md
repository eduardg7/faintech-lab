# UTM Parameter Capture - Security Review

**Created:** 2026-04-01T05:20:00+02:00
**Agent:** ciso
**Severity:** P1 - Security hardening required before implementation
**Scope:** Week 2 GTM analytics infrastructure (UTM capture task: LAB-ANALYTICS-20260401-UTMCAPTURE)

---

## Security Assessment

### Overview
The UTM parameter capture task adds 6 new fields to the User model and signup flow to enable channel attribution. While business-critical for Week 2 GTM, the implementation requires security hardening to prevent injection attacks and ensure GDPR compliance.

### Attack Surface Analysis

**Input Sources (User-Controlled):**
1. **URL Query Parameters** - `?utm_source=...`
   - Attacker can inject arbitrary values via crafted links
   - Values are extracted from `request.query_params`
   - No client-side validation proposed

2. **HTTP Headers** - `Referer: ...`
   - Attacker can spoof referrer header
   - Values are extracted from `request.headers.get("referer")`
   - No length limits or format validation

3. **Signup Form Body** - JSON payload
   - Attacker can POST arbitrary UTM values directly
   - Values are accepted via `UserRegister` schema
   - Pydantic validation is present but insufficient for injection attacks

---

## Security Concerns

### 🔴 CRITICAL: SQL Injection Risk

**Location:** `amc-backend/app/routers/auth.py`

**Problem:**
```python
# Current implementation extracts UTM directly without sanitization
user_data.utm_source = query_params.get("utm_source")
user_data.utm_medium = query_params.get("utm_medium")

# Then stores directly in database
user = User(
    # ...
    utm_source=user_data.utm_source,  # ← UNSANITIZED USER INPUT
    utm_medium=user_data.utm_medium,  # ← UNSANITIZED USER INPUT
)
```

**Attack Vector:**
- Attacker crafts malicious URL: `?utm_source=hacker'; DROP TABLE users; --`
- If ORM is used incorrectly, this could execute SQL

**Current Mitigation:**
- SQLAlchemy ORM is used (reduces SQLi risk)
- Pydantic schema validation is present

**Missing Mitigation:**
- ❌ No explicit input sanitization before ORM insertion
- ❌ No length limits enforced in backend code
- ❌ No SQL query logging for anomaly detection

**Recommendation:**
1. Use SQLAlchemy ORM's parameterized queries (already done)
2. Add explicit length validation (max_length already in schema, but not enforced)
3. Add input sanitization for special characters: `;`, `'`, `"`, `--`, `xp_`, `union`
4. Log all UTM values for security monitoring

### 🟡 HIGH: XSS Risk (Frontend Display)

**Location:** `amc-frontend` (not specified, but assumed)

**Problem:**
If UTM values are displayed on frontend (e.g., "You came from {utm_source}"), they could inject malicious scripts.

**Attack Vector:**
- Attacker crafts URL: `?utm_source=<script>alert(document.cookie)</script>`
- If displayed without escaping: XSS executes in victim's browser

**Current Mitigation:**
- Not applicable (frontend implementation not specified)

**Missing Mitigation:**
- ❌ No DOMPurify or HTML escaping mentioned
- ❌ No Content Security Policy (CSP) mentioned
- ❌ No XSS testing mentioned

**Recommendation:**
1. If displaying UTM values, use DOMPurify for sanitization
2. Implement strict CSP header: `default-src 'self'`
3. Add XSS testing to acceptance criteria

### 🟡 HIGH: Log Injection Risk

**Location:** `amc-backend/app/services/analytics.py`

**Problem:**
```python
def track_signup(...):
    self.identify(user_id, {
        "utm_source": utm_source,  # ← RAW USER INPUT IN LOGS
        "utm_medium": utm_medium,
        # ...
    })
```

**Attack Vector:**
- Attacker injects newline characters: `?utm_source=value\n[CRLF]Malicious: log`
- If logs are displayed in admin dashboard without escaping: XSS

**Current Mitigation:**
- Not applicable (PostHog analytics service, not local logs)

**Missing Mitigation:**
- ❌ No log sanitization before sending to analytics
- ❌ No rate limiting on signup with suspicious UTM patterns
- ❌ No anomaly detection for malicious UTM values

**Recommendation:**
1. Strip CRLF characters before logging: `utm_source.replace('\r', '').replace('\n', '')`
2. Rate limit signups with repeated suspicious UTM patterns
3. Add alerting for known attack signatures (e.g., `<script>`, `javascript:`, `onerror=`)

### 🟡 MEDIUM: Data Privacy (GDPR)

**Location:** `amc-backend/app/models/user.py` + signup flow

**Problem:**
UTM parameters are tracking data stored indefinitely without user consent.

**GDPR Implications:**
- ✅ Article 6(1)(f) - Lawfulness, fairness, transparency
- ⚠️ Article 7(4) - Clear and transparent information required
- ⚠️ Article 21(1) - Right to erasure (data deletion)

**Current Mitigation:**
- ✅ Privacy Policy exists (assumed)
- ❌ No cookie consent mentioned for tracking
- ❌ No data retention policy for UTM data
- ❌ No user-facing disclosure of tracking

**Recommendation:**
1. Update Privacy Policy to disclose UTM tracking
2. Add "tracking preferences" to user settings (opt-out option)
3. Define data retention period for UTM data (recommend 6 months)
4. Implement data deletion endpoint (GDPR Article 17)

### 🟡 MEDIUM: Performance Impact

**Location:** `amc-backend/app/models/user.py` (database indexes)

**Problem:**
```python
utm_source = Column(String(50), nullable=True, index=True)      # 50 chars
utm_campaign = Column(String(100), nullable=True, index=True)  # 100 chars
utm_referrer = Column(String(255), nullable=True, index=True)  # 255 chars
```

**Attack Vector:**
- Attacker submits maximum-length UTM values repeatedly
- Index rebuilds slow down database
- Storage bloat increases costs

**Current Mitigation:**
- ✅ Length limits defined in schema (50-255 chars)
- ✅ Indexes created (good for query performance)

**Missing Mitigation:**
- ❌ No rate limiting on signup attempts with UTM data
- ❌ No data cleanup job for old UTM data
- ❌ No monitoring for database growth

**Recommendation:**
1. Rate limit signups per IP: 5 attempts/hour
2. Add cron job to delete UTM data older than 6 months
3. Monitor `users` table size growth (alert at 10% increase/month)

---

## Required Hardening

### Priority P1 (Must Have Before Merge)

1. **Input Sanitization**
   ```python
   # In amc-backend/app/routers/auth.py
   import re

   def sanitize_utm(value: Optional[str]) -> Optional[str]:
       if not value:
           return None
       # Remove SQL injection patterns
       value = re.sub(r"[;'\-]", '', value)
       value = re.sub(r"(union|select|drop|insert|update|delete|create|alter)", '', value, flags=re.IGNORECASE)
       # Truncate to max length
       return value[:255]

   # Apply before storage
   user = User(
       # ...
       utm_source=sanitize_utm(user_data.utm_source),
       utm_medium=sanitize_utm(user_data.utm_medium),
       # ...
   )
   ```

2. **Log Injection Prevention**
   ```python
   # Strip CRLF and control characters
   def sanitize_for_logging(value: Optional[str]) -> Optional[str]:
       if not value:
           return None
       return value.replace('\r', '').replace('\n', '').replace('\x00', '')

   # In analytics service
   analytics.track_signup(
       # ...
       utm_source=sanitize_for_logging(user_data.utm_source),
       # ...
   )
   ```

3. **Rate Limiting**
   ```python
   # In amc-backend/app/routers/auth.py
   from slowapi import Request
   from slowapi.util import get_remote_address

   @router.post("/register")
   @limiter.limit("5/hour", key_func=get_remote_address)
   async def register(...):
       # Existing code
   ```

### Priority P2 (Should Have Week 2)

1. **GDPR Disclosure**
   - Update Privacy Policy with UTM tracking notice
   - Add "Tracking Preferences" to user settings
   - Implement data deletion endpoint

2. **Security Testing**
   - Add XSS test to acceptance criteria
   - Add SQLi test to acceptance criteria
   - Add log injection test to acceptance criteria

3. **Monitoring**
   - Alert on suspicious UTM patterns (`<script>`, `javascript:`)
   - Alert on abnormal signup rates (10x normal)
   - Log all UTM values for forensic analysis

---

## Updated Acceptance Criteria (Security Hardening)

### Add to Task LAB-ANALYTICS-20260401-UTMCAPTURE

**Existing AC:**
1. Add 6 UTM fields to User model
2. Update UserRegister schema to accept UTM parameters
3. Update /auth/register endpoint to extract UTM
4. Update analytics.track_signup() to pass UTM properties
5. Create Alembic database migration
6. Update frontend signup form to preserve UTM
7. Add indexes to UTM columns
8. Test signup flow with UTM → database → PostHog

**New Security AC:**
9. ✅ **Input sanitization:** Strip SQLi patterns before ORM insertion
10. ✅ **Log sanitization:** Strip CRLF/control characters before logging
11. ✅ **Rate limiting:** 5 signups/hour per IP address
12. ✅ **GDPR disclosure:** Privacy Policy updated with tracking notice
13. ✅ **Security testing:** XSS, SQLi, log injection tests added
14. ✅ **Monitoring:** Alert on suspicious UTM patterns

---

## Risk Summary

| Risk | Severity | Likelihood | Impact | Mitigation |
|-------|-----------|------------|------------|
| SQL Injection | HIGH | LOW | ORM + sanitization |
| XSS (Frontend) | MEDIUM | HIGH | DOMPurify + CSP |
| Log Injection | MEDIUM | MEDIUM | CRLF stripping |
| GDPR Non-Compliance | LOW | HIGH | Policy update + opt-out |
| Performance Degradation | LOW | MEDIUM | Rate limiting + cleanup |

**Overall Risk:** 🟡 MEDIUM (mitigated to LOW with P1 hardening)

---

## Recommendations

### Before Merge
1. ✅ Implement P1 hardening (sanitization, rate limiting)
2. ✅ Add security testing to acceptance criteria
3. ✅ Review by CISO before merge

### Week 2 GTM Execution
1. ✅ Update Privacy Policy with UTM tracking disclosure
2. ✅ Add monitoring for suspicious UTM patterns
3. ✅ Weekly review of UTM data for anomalies

### Future Considerations
1. Consider using UUID-based tracking instead of raw UTM values
2. Implement UTM hash for privacy-preserving analytics
3. Add consent banner for tracking (GDPR transparency)

---

**Status:** SECURITY REVIEW COMPLETE - P1 hardening required before implementation
**Next Action:** Update TASK_DB with security ACs, coordinate with faintech-backend
**Timeline:** Must complete before April 3, 2026 (Week 2 GTM start)

---

**Created:** 2026-04-01T05:20:00+02:00
**Agent:** ciso
**Size:** 7.8KB
