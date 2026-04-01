# Week 2 GTM Technical Fallback Mechanisms

**Generated**: 2026-04-01T09:30:00+02:00
**Task**: LAB-TECH-20260331-WEEK2GTM (AC4)
**Owner**: dev
**Purpose**: Document fallback mechanisms and alternative approaches for critical technical dependencies during Week 2 GTM

---

## Overview

This document defines fallback strategies for external blockers and technical dependencies that cannot be resolved internally. Each fallback includes trigger conditions, implementation steps, and success criteria.

---

## Fallback Mechanisms by Dependency

### F1: Backend API Deployment Fallback

**Primary Plan**: Deploy FastAPI backend to Railway/Render/Fly.io
**Owner**: DevOps
**Timeline**: 2-4 hours

**Fallback Triggers**:
- Backend deployment fails after 2 attempts
- Cloud provider outage
- Database migration issues
- Time constraint (<4 hours to HN launch)

**Fallback Strategy 1: Local Demo with ngrok**
```bash
# Install ngrok
brew install ngrok

# Expose local backend
ngrok http 8000

# Update frontend environment
NEXT_PUBLIC_API_URL=https://<ngrok-url>/v1 vercel --prod
```

**Pros**:
- Immediate availability (5-10 minutes)
- No cloud provider dependency
- Full backend functionality

**Cons**:
- Unstable URL (changes on restart)
- Rate limits on free tier
- Not production-ready
- Requires local machine to stay running

**Fallback Strategy 2: Demo Mode with Mock Data**
```typescript
// Implement mock API responses in frontend
// File: amc-frontend/src/lib/mock-api.ts

export const mockSignup = async (email: string, password: string) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 800));

  return {
    success: true,
    user: { id: 'demo-user', email },
    token: 'demo-jwt-token'
  };
};

// Use environment variable to toggle
const USE_MOCK_API = process.env.NEXT_PUBLIC_USE_MOCK_API === 'true';
```

**Pros**:
- Immediate availability (30 minutes to implement)
- No backend dependency
- Demonstrates full UX flow

**Cons**:
- No real functionality
- Users cannot actually create memories
- No data persistence
- Deceptive for GTM validation

**Fallback Strategy 3: Manual Signup with Waitlist**
```typescript
// Simple email capture without backend
// File: amc-frontend/src/app/waitlist/page.tsx

export default function WaitlistPage() {
  const handleSubmit = async (email: string) => {
    // Store in localStorage or email to Eduard
    await fetch('/api/send-waitlist-email', {
      method: 'POST',
      body: JSON.stringify({ email })
    });
  };

  return (
    <div>
      <h1>Join Waitlist</h1>
      <p>Backend temporarily unavailable. We'll notify you when ready.</p>
      <EmailForm onSubmit={handleSubmit} />
    </div>
  );
}
```

**Pros**:
- Captures leads even without backend
- Honest about technical issues
- Can convert later when backend ready

**Cons**:
- No product validation
- Lower conversion than working demo
- Requires manual follow-up

**Decision Tree**:
1. If time >4 hours before HN launch: Use Primary Plan
2. If time 2-4 hours: Use Fallback Strategy 1 (ngrok)
3. If time <2 hours: Use Fallback Strategy 3 (waitlist)
4. Never use Fallback Strategy 2 for GTM (deceptive)

**Success Criteria**:
- Users can create accounts
- Basic functionality works (signup, login, create memory)
- Response time <2 seconds
- Uptime >95% during Week 2

---

### F2: PostHog Analytics Fallback

**Primary Plan**: Configure PostHog with credentials
**Owner**: DevOps
**Timeline**: 30 minutes

**Fallback Triggers**:
- PostHog credentials not provided
- PostHog service outage
- Implementation errors

**Fallback Strategy 1: Database Query Analytics**
```sql
-- Weekly signup count by channel
SELECT
  DATE(created_at) as date,
  utm_source,
  COUNT(*) as signups
FROM users
WHERE created_at >= '2026-04-01'
GROUP BY DATE(created_at), utm_source
ORDER BY date DESC, signups DESC;

-- Conversion funnel
SELECT
  COUNT(DISTINCT u.id) as users,
  COUNT(DISTINCT m.user_id) as activated,
  ROUND(COUNT(DISTINCT m.user_id) * 100.0 / COUNT(DISTINCT u.id), 2) as activation_rate
FROM users u
LEFT JOIN memories m ON m.user_id = u.id
WHERE u.created_at >= '2026-04-01';
```

**Pros**:
- No external dependency
- Accurate data (direct from database)
- No privacy concerns

**Cons**:
- No real-time data (queries must be run manually)
- No session replay or heatmaps
- Limited behavioral insights

**Fallback Strategy 2: UTM Parameter Capture Only**
```typescript
// Capture UTM params in user record
// File: amc-backend/app/routers/auth.py

@router.post("/register")
async def register(user_data: UserRegister, request: Request):
    # Extract UTM from query params
    utm_params = {
        "utm_source": request.query_params.get("utm_source"),
        "utm_medium": request.query_params.get("utm_medium"),
        "utm_campaign": request.query_params.get("utm_campaign"),
    }

    # Store with user
    user = await create_user(user_data, utm_params)

    return {"user": user, "token": token}
```

**Pros**:
- Channel attribution works
- No external service needed
- Simple implementation (2-4 hours)

**Cons**:
- No behavioral tracking
- No conversion funnel visibility
- Limited optimization insights

**Fallback Strategy 3: Manual Evidence Collection**
```markdown
# Daily Manual Evidence Log

## Date: 2026-04-01

### Channel Performance
- HN: [Manual count from comments/upvotes]
- Reddit: [Manual count from post analytics]
- LinkedIn: [Manual count from post views]

### Signups
- Total today: [Manual count from database]
- By channel: [Query users table]

### User Feedback
- [Copy-paste feedback from emails/chats]
```

**Pros**:
- No technical dependency
- Captures qualitative insights
- Better than no evidence

**Cons**:
- Time-intensive (30 min/day)
- Prone to human error
- Delayed insights

**Decision Tree**:
1. If PostHog available: Use Primary Plan
2. If UTM capture implemented (LAB-ANALYTICS-20260401-UTMCAPTURE): Use Fallback Strategy 2
3. If neither available: Use Fallback Strategy 1 + Fallback Strategy 3
4. Never proceed with zero analytics capability

**Success Criteria**:
- Can attribute signups to channels
- Can calculate conversion rates
- Can identify top-performing channels
- Evidence quality sufficient for decision-making

---

### F3: HUNTER_API_KEY Revenue Fallback

**Primary Plan**: Deploy HUNTER_API_KEY to production
**Owner**: DevOps (with CEO approval)
**Timeline**: 30 minutes

**Fallback Triggers**:
- Eduard does not approve deployment
- API key integration issues
- Hunter API service outage

**Fallback Strategy 1: Manual Email Verification**
```python
# Simple regex-based validation
import re

def validate_email_basic(email: str) -> dict:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    return {
        "valid": bool(re.match(pattern, email)),
        "confidence": "low",  # No verification
        "method": "regex"
    }
```

**Pros**:
- No external dependency
- Immediate availability

**Cons**:
- No bounce detection
- No spam trap detection
- Lower email deliverability
- Revenue still at risk

**Fallback Strategy 2: Third-Party Email Service**
```python
# Use alternative email verification API
import requests

async def verify_email_alternative(email: str) -> dict:
    # Examples: ZeroBounce, NeverBounce, Kickbox
    response = await requests.get(
        f"https://api.alternative-service.com/verify?email={email}",
        headers={"X-API-Key": settings.ALTERNATIVE_EMAIL_API_KEY}
    )

    return response.json()
```

**Pros**:
- Same functionality as Hunter
- Multiple providers available

**Cons**:
- Requires new API key (same blocker)
- Additional cost
- Integration time (2-4 hours)

**Fallback Strategy 3: Proceed Without Verification**
```python
# Accept all emails, handle bounces reactively
async def register_user_without_verification(email: str):
    # Create user immediately
    user = await create_user(email)

    # Handle bounces via email service webhook
    # (SendGrid, Postmark, etc. provide bounce notifications)

    return user
```

**Pros**:
- No blockers
- Immediate availability
- Can clean list later

**Cons**:
- Higher bounce rate
- Lower deliverability
- Damages sender reputation
- Revenue still at risk

**Decision Tree**:
1. If Eduard approves: Use Primary Plan
2. If alternative API key available: Use Fallback Strategy 2
3. If launch imminent: Use Fallback Strategy 3 (temporary)
4. Long-term: Implement Fallback Strategy 1 + reactive bounce handling

**Success Criteria**:
- Email deliverability >95%
- Bounce rate <5%
- User experience not degraded
- Revenue recovery begins

---

### F4: Custom Domain Fallback

**Primary Plan**: Configure custom domain (agentmemory.cloud)
**Owner**: Eduard (DNS configuration)
**Timeline**: 1-2 hours

**Fallback Triggers**:
- DNS propagation delays
- SSL certificate issues
- Domain configuration errors

**Fallback Strategy 1: Continue with Vercel Default Domain**
```
Current: https://amc-frontend-weld.vercel.app
Status: WORKING
```

**Pros**:
- Zero configuration
- Immediate availability
- Full functionality

**Cons**:
- Less professional appearance
- Harder to remember
- Not brand-aligned

**Fallback Strategy 2: Use Alternative Domain**
```
Options:
- faintech-lab.vercel.app (FIX NEEDED - currently 404)
- Create new Vercel project with cleaner name
```

**Pros**:
- More professional than default
- Full control

**Cons**:
- Still not ideal brand
- Requires configuration time

**Decision Tree**:
1. If custom domain critical for brand: Wait for DNS propagation (1-2 hours max)
2. If time constraint: Use Fallback Strategy 1
3. Never delay GTM for custom domain (nice-to-have)

**Success Criteria**:
- URL accessible and functional
- SSL working
- No user-facing errors

---

### F5: LinkedIn Credentials Fallback

**Primary Plan**: Obtain LinkedIn credentials
**Owner**: Eduard
**Timeline**: Unknown (Eduard availability)

**Fallback Triggers**:
- Eduard unavailable
- Credentials not provided
- Account access issues

**Fallback Strategy 1: Proceed Without LinkedIn**
```
Channels Active:
✅ HN (April 1)
✅ Reddit (April 4, 6, 8)
❌ LinkedIn (skip)

Rationale: 2/3 channels still executable
```

**Pros**:
- No dependency on credentials
- Can still validate GTM
- Reduce complexity

**Cons**:
- Missing B2B channel
- Lower total reach
- Incomplete GTM execution

**Fallback Strategy 2: Personal LinkedIn Account**
```
Option: Eduard or team member posts manually
- Use prepared content from LAB-SOCIAL-20260331-SOCIALCONTENT
- Manual posting (not automated)
- Personal brand (not company page)
```

**Pros**:
- Can execute LinkedIn strategy
- Authentic engagement
- No automation needed

**Cons**:
- Personal brand (not company)
- Manual effort required
- Lower scale potential

**Decision Tree**:
1. If credentials available: Use Primary Plan
2. If no credentials by April 3: Use Fallback Strategy 1
3. If team member willing: Use Fallback Strategy 2

**Success Criteria**:
- At least 2/3 channels executed
- Sufficient signups for GTM validation (10-15)
- Channel attribution data collected

---

## Implementation Priority

### Must-Have Fallbacks (Week 2 GTM Critical)
1. **F1: Backend API** - P0, no GTM without this
2. **F2: Analytics** - P0, no validation without data

### Should-Have Fallbacks (Revenue/Quality Impact)
3. **F3: Email Verification** - P1, revenue recovery
4. **F5: LinkedIn** - P1, channel coverage

### Nice-to-Have Fallbacks (Brand/Polish)
5. **F4: Custom Domain** - P2, brand appearance

---

## Fallback Activation Protocol

### Step 1: Assess Blocker
- Identify which dependency is blocked
- Estimate time to resolution
- Determine impact on Week 2 GTM

### Step 2: Choose Fallback
- Review fallback strategies above
- Select based on timeline and impact
- Document decision in c-suite-chat

### Step 3: Implement Fallback
- Follow implementation steps
- Test fallback mechanism
- Verify success criteria

### Step 4: Monitor and Switch Back
- Monitor primary plan resolution
- Switch back when available
- Document learnings

---

## Success Metrics

### Fallback Success Criteria
- Week 2 GTM executable despite blockers
- 10-15 signups achievable
- Channel attribution functional
- Revenue recovery begins (if F3 activated)

### Fallback Failure Indicators
- Zero signups despite fallbacks
- No channel attribution data
- User experience degraded
- GTM timeline missed

---

## Related Documents
- Recovery Procedures: `/docs/evidence/week2gtm-recovery-procedures-2026-04-01.md`
- Monitoring Dashboard: `/docs/evidence/week2gtm-monitoring-dashboard-2026-03-31.md`
- Technical Readiness Status: `/docs/evidence/week2gtm-technical-readiness-status-2026-03-31.md`
- Analytics Execution Brief: `/docs/analytics/week2-gtm-analytics-execution-brief-2026-04-01.md`

---

**Last Updated**: 2026-04-01T09:30:00+02:00
**Next Review**: 2026-04-02 (daily during Week 2 GTM)
**Owner**: dev
