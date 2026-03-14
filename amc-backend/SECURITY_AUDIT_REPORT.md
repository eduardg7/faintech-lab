# SECURITY AUDIT REPORT - AMC Backend
**Auditor:** Shield (Senior Security Engineer)
**Date:** 2026-03-13
**Repository:** ~/faintech-lab/amc-backend
**Scope:** auth.py, billing.py, api_keys.py, requirements.txt

---

## EXECUTIVE SUMMARY

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH | 3 |
| MEDIUM | 4 |
| LOW | 2 |

**Overall Risk Level: HIGH**

---

## CRITICAL FINDINGS

### CRIT-001: Credentials Committed to Repository
**File:** `.env` (line 10)
**Severity:** CRITICAL
**CVSS:** 9.1

**Description:**
Database credentials are hardcoded in the `.env` file:
```
DATABASE_URL=postgresql+asyncpg://amc:amc_password@localhost:5432/amc
```

**Impact:**
- Database credentials exposure if repository is shared or compromised
- Production database takeover if same credentials are reused

**Recommendation:**
1. Immediately rotate database credentials
2. Add `.env` to `.gitignore` (MISSING - no .gitignore file exists!)
3. Use `.env.example` with placeholder values
4. Use secrets management (AWS Secrets Manager, HashiCorp Vault)

---

### CRIT-002: Weak JWT Secret Key in Environment File
**File:** `.env` (line 14)
**Severity:** CRITICAL
**CVSS:** 9.8

**Description:**
JWT secret key appears to be a development placeholder:
```
JWT_SECRET_KEY=dev-secret...
```

**Impact:**
- Attackers can forge valid JWT tokens
- Complete authentication bypass
- Full account takeover for all users

**Recommendation:**
1. Generate cryptographically secure JWT secret (256+ bits)
2. Never commit secrets to version control
3. Use environment variables or secrets manager in production

---

## HIGH FINDINGS

### HIGH-001: Missing Rate Limiting Enforcement
**File:** `app/core/rate_limit.py`
**Severity:** HIGH
**CVSS:** 7.5

**Description:**
Rate limiting middleware tracks requests but does NOT block them when exceeded:
```python
# Line 46: Request is always processed regardless of rate limit
response = await call_next(request)
```

The middleware only adds headers but never returns 429 Too Many Requests.

**Impact:**
- API remains vulnerable to brute force attacks
- DoS attacks not mitigated
- Credential stuffing attacks possible

**Recommendation:**
```python
if minute_count >= self.requests_per_minute:
    return Response(
        status_code=429,
        content="Rate limit exceeded"
    )
```

---

### HIGH-002: In-Memory Rate Limiting Not Production-Ready
**File:** `app/core/rate_limit.py` (lines 23-24)
**Severity:** HIGH

**Description:**
```python
# In-memory rate limit tracking (should use Redis in production)
self.minute_tracker: Dict[str, list] = defaultdict(list)
```

**Impact:**
- Rate limits don't work across multiple instances
- Memory exhaustion possible with many clients
- Lost on restart - attackers can retry

**Recommendation:**
Implement Redis-backed rate limiting for production.

---

### HIGH-003: Missing .gitignore File
**File:** Repository root
**Severity:** HIGH

**Description:**
No `.gitignore` file exists in the repository, allowing sensitive files to be committed.

**Impact:**
- `.env`, `__pycache__`, `.pyc` files can be committed
- Secrets leakage

**Recommendation:**
Create `.gitignore` with:
```
.env
.env.*
!.env.example
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.venv/
```

---

## MEDIUM FINDINGS

### MED-001: No API Key Rate Limiting in Auth Context
**File:** `app/routers/auth.py` (lines 84-112)
**Severity:** MEDIUM

**Description:**
API key authentication does not have separate rate limiting from JWT auth.

**Impact:**
- API keys can be used for brute force attacks
- No differentiation between user types

---

### MED-002: Webhook Endpoint Exposes Configuration Status
**File:** `app/routers/billing.py` (lines 133-136)
**Severity:** MEDIUM

**Description:**
Webhook endpoint returns detailed error messages about configuration:
```python
detail="Webhook signature verification not configured - billing disabled"
```

**Impact:**
- Information disclosure about infrastructure
- Attackers can identify unconfigured services

**Recommendation:**
Return generic error: "Service temporarily unavailable"

---

### MED-003: User Auto-Verification in Registration
**File:** `app/routers/auth.py` (line 210)
**Severity:** MEDIUM

**Description:**
```python
is_verified=True,  # For MVP, auto-verify (add email verification later)
```

**Impact:**
- No email ownership verification
- Fake account creation possible
- Spam/abuse vector

---

### MED-004: Logging Uses Print Statements
**File:** `app/routers/memories.py` (lines 67-69)
**Severity:** MEDIUM

**Description:**
```python
print(f"[Validation] Memory rejected: content size {content_size}...")
```

**Impact:**
- No structured logging
- Sensitive data may leak to stdout
- No log level control

---

## LOW FINDINGS

### LOW-001: Passlib[bcrypt] Version Outdated
**File:** `requirements.txt` (line 9)
**Severity:** LOW

**Description:**
```
passlib[bcrypt]==1.7.4
```

Passlib 1.7.4 is from 2020. While no critical CVEs, it's unmaintained.

**Recommendation:**
Consider migrating to `bcrypt` directly or `argon2-cffi`.

---

### LOW-002: Stripe Price ID Fallback to Placeholder
**File:** `app/routers/billing.py` (lines 32, 44)
**Severity:** LOW

**Description:**
```python
"price_id": StripeConfig.STARTER_PRICE_ID or "price_starter_placeholder"
```

**Impact:**
- Development confusion
- Potential test data in production

---

## DEPENDENCIES VULNERABILITY ANALYSIS

| Package | Version | Status |
|---------|---------|--------|
| fastapi | 0.109.0 | OK - No known critical CVEs |
| uvicorn | 0.27.0 | OK |
| sqlalchemy | 2.0.25 | OK |
| asyncpg | 0.29.0 | OK |
| pydantic | 2.5.3 | OK |
| python-jose | 3.3.0 | OK - Latest stable |
| passlib | 1.7.4 | WARNING - Unmaintained |
| stripe | 8.8.0 | OK |

**Recommendation:** Run `pip-audit` regularly for CVE scanning.

---

## POSITIVE SECURITY OBSERVATIONS

1. **SQL Injection Protection:** All queries use SQLAlchemy ORM with parameterized queries
2. **Password Hashing:** bcrypt with proper 72-byte truncation
3. **API Key Security:** Keys are hashed before storage (SHA-256)
4. **Token Rotation:** Refresh tokens are rotated on use
5. **Workspace Isolation:** Multi-tenant data isolation implemented
6. **Stripe Webhook Verification:** Signature verification implemented
7. **Content Size Limits:** 10KB limit on memory content

---

## REMEDIATION PRIORITY

1. **IMMEDIATE (24h):**
   - Rotate database credentials
   - Generate new JWT secret
   - Add `.gitignore`

2. **SHORT-TERM (1 week):**
   - Implement rate limit enforcement
   - Remove `.env` from git history (`git filter-branch`)

3. **MEDIUM-TERM (1 month):**
   - Add Redis-based rate limiting
   - Implement email verification
   - Add structured logging

---

**Report Generated by Shield - FainTech Security Team**
