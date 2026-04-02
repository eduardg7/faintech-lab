# Week 2 GTM Technical Recovery Procedures

**Generated**: 2026-04-01T09:25:00+02:00
**Task**: LAB-TECH-20260331-WEEK2GTM (AC8)
**Owner**: dev
**Purpose**: Step-by-step recovery procedures for technical issues during Week 2 GTM execution

---

## Incident Classification

| Severity | Impact | Response Time | Escalation |
|----------|--------|---------------|------------|
| P0 | Complete service outage | <15 minutes | Immediate c-suite-chat |
| P1 | Feature degraded | <1 hour | #devops-alerts |
| P2 | Minor issue | <4 hours | Dev queue |

---

## P0 Recovery Procedures

### P0.1: Demo URL Down (HTTP 404/500)

**Symptoms:**
- https://amc-frontend-weld.vercel.app returns non-200 status
- Users cannot access landing page

**Diagnosis (5 minutes):**
```bash
# Check Vercel deployment status
curl -I https://amc-frontend-weld.vercel.app

# Check DNS resolution
nslookup amc-frontend-weld.vercel.app

# Check Vercel logs
vercel logs amc-frontend-weld.vercel.app
```

**Recovery Steps:**
1. **If Vercel deployment failed:**
   ```bash
   cd /Users/eduardgridan/faintech-lab/amc-frontend
   vercel --prod
   ```

2. **If DNS issue:**
   - Check Vercel project settings
   - Verify domain configuration
   - Escalate to DevOps if DNS requires manual intervention

3. **If code issue:**
   ```bash
   # Rollback to last working commit
   git log --oneline -5
   git reset --hard <last-working-commit>
   vercel --prod
   ```

**Verification:**
```bash
curl -I https://amc-frontend-weld.vercel.app
# Expected: HTTP 200
```

**Escalation Path:**
- Primary: DevOps
- Secondary: CTO (if DevOps unavailable >30 min)
- Final: CEO (if complete outage >1 hour)

**Recovery Time Target:** 15-30 minutes

---

### P0.2: Backend API Down (Once Deployed)

**Symptoms:**
- Frontend returns network errors
- Users cannot sign up, login, or create memories
- API health check returns non-200 status

**Diagnosis (5 minutes):**
```bash
# Check backend health
curl -I https://<backend-url>/health

# Check backend logs
railway logs # or render logs / fly logs

# Check database connectivity
curl https://<backend-url>/health | jq '.database.status'
```

**Recovery Steps:**
1. **If application crash:**
   ```bash
   # Restart service (varies by platform)
   railway restart # Railway
   # or
   fly apps restart <app-name> # Fly.io
   ```

2. **If database connection issue:**
   - Check database credentials in environment variables
   - Verify database is running (managed service status page)
   - Restart database if necessary

3. **If resource exhaustion (memory/CPU):**
   - Scale up instance size
   - Check for memory leaks in logs
   - Restart application

4. **If code issue:**
   ```bash
   # Rollback to last working deployment
   railway rollback # or equivalent
   ```

**Verification:**
```bash
curl https://<backend-url>/health
# Expected: {"status": "healthy", "database": {"status": "ok"}}
```

**Escalation Path:**
- Primary: DevOps
- Secondary: Backend engineer
- Final: CTO

**Recovery Time Target:** 30-60 minutes

---

### P0.3: Database Failure

**Symptoms:**
- Backend returns database connection errors
- All database operations fail
- Health check shows `database.status: "error"`

**Diagnosis (10 minutes):**
```bash
# Check database status via backend health
curl https://<backend-url>/health | jq '.database'

# Check managed database status (platform-specific)
# Railway: Check Railway dashboard
# Render: Check Render dashboard
# Fly.io: fly postgres status
```

**Recovery Steps:**
1. **If managed database down:**
   - Check cloud provider status page
   - Wait for automatic recovery (typically <10 min)
   - Contact provider support if >30 min

2. **If connection pool exhausted:**
   - Restart backend application
   - Review connection pool settings
   - Scale database if needed

3. **If data corruption:**
   - DO NOT ATTEMPT RECOVERY
   - Escalate immediately to CTO
   - Restore from latest backup (if available)

**Verification:**
```bash
curl https://<backend-url>/health
# Expected: database.status = "ok"
```

**Escalation Path:**
- Primary: DevOps
- Secondary: CTO (data corruption)
- Final: CEO (business impact)

**Recovery Time Target:** 30-90 minutes (depends on issue)

---

## P1 Recovery Procedures

### P1.1: Analytics Not Collecting (PostHog)

**Symptoms:**
- No user behavior data in PostHog
- Cannot measure conversion rates
- Missing traffic analytics

**Diagnosis (10 minutes):**
```bash
# Check PostHog credentials
echo $NEXT_PUBLIC_POSTHOG_KEY

# Test PostHog connection
curl -I https://app.posthog.com

# Check browser console for PostHog errors
# Open DevTools → Console → Filter: posthog
```

**Recovery Steps:**
1. **If credentials missing:**
   - Create PostHog account (https://posthog.com)
   - Get API key from Project Settings
   - Add to Vercel environment variables:
     ```bash
     vercel env add NEXT_PUBLIC_POSTHOG_KEY
     ```
   - Redeploy frontend:
     ```bash
     cd /Users/eduardgridan/faintech-lab/amc-frontend
     vercel --prod
     ```

2. **If PostHog service down:**
   - Check PostHog status page
   - Wait for recovery
   - Fallback to database queries for analytics

3. **If tracking code issue:**
   - Review analytics implementation in codebase
   - Test event firing in browser DevTools
   - Fix and redeploy

**Verification:**
- Create test signup
- Check PostHog dashboard for event
- Verify all tracking events firing

**Escalation Path:**
- Primary: DevOps
- Secondary: Frontend engineer
- Final: CMO (Week 2 GTM impact)

**Recovery Time Target:** 1-2 hours

---

### P1.2: Payment Processing Failure (Stripe)

**Symptoms:**
- Users cannot complete subscription signup
- Payment errors in frontend
- Stripe webhook failures

**Diagnosis (10 minutes):**
```bash
# Check Stripe API status
curl -I https://api.stripe.com

# Check backend logs for Stripe errors
railway logs | grep -i stripe

# Check Stripe webhook configuration
# Dashboard: https://dashboard.stripe.com/webhooks
```

**Recovery Steps:**
1. **If Stripe API down:**
   - Check Stripe status page
   - Wait for recovery
   - Communicate to users via banner

2. **If webhook configuration issue:**
   - Update webhook URL in Stripe dashboard
   - Verify webhook secret in backend env vars
   - Test with Stripe CLI:
     ```bash
     stripe listen --forward-to <backend-url>/v1/billing/webhook
     ```

3. **If subscription logic issue:**
   - Review backend logs for errors
   - Rollback to last working deployment if needed
   - Fix and redeploy

**Verification:**
- Complete test subscription signup
- Verify subscription created in Stripe dashboard
- Check user account upgraded correctly

**Escalation Path:**
- Primary: Backend engineer
- Secondary: DevOps
- Final: CEO (revenue impact)

**Recovery Time Target:** 1-2 hours

---

## P2 Recovery Procedures

### P2.1: Slow Response Times (>3s)

**Symptoms:**
- Page load times >3 seconds
- API response times >2 seconds
- User experience degraded

**Diagnosis (15 minutes):**
```bash
# Measure API response time
curl -w "@curl-format.txt" -o /dev/null -s https://<backend-url>/health

# Check backend resource usage
railway status # or equivalent

# Check database query performance
# Enable query logging if needed
```

**Recovery Steps:**
1. **If backend resource constrained:**
   - Scale up instance size
   - Enable auto-scaling if available
   - Review resource-intensive operations

2. **If database slow:**
   - Check for missing indexes
   - Review slow query logs
   - Optimize database queries

3. **If network latency:**
   - Check CDN configuration (Vercel)
   - Review API endpoint locations
   - Consider edge caching

**Verification:**
- Run load test: `k6 run load_tests/basic.js`
- Verify p95 latency <2s

**Escalation Path:**
- Primary: DevOps
- Secondary: Backend engineer
- Final: CTO (architecture issue)

**Recovery Time Target:** 2-4 hours

---

### P2.2: Certificate/SSL Issues

**Symptoms:**
- Browser warnings about invalid certificate
- HTTPS connection failures
- Mixed content warnings

**Diagnosis (5 minutes):**
```bash
# Check SSL certificate
openssl s_client -connect amc-frontend-weld.vercel.app:443

# Check certificate expiration
echo | openssl s_client -connect amc-frontend-weld.vercel.app:443 2>/dev/null | openssl x509 -noout -dates
```

**Recovery Steps:**
1. **If Vercel-managed certificate:**
   - Vercel auto-renews Let's Encrypt certificates
   - Force renewal in Vercel dashboard if needed
   - Contact Vercel support if issue persists

2. **If custom domain certificate:**
   - Check certificate provider
   - Renew or replace certificate
   - Update DNS configuration

**Verification:**
- Access site in browser (no warnings)
- Run SSL Labs test: https://www.ssllabs.com/ssltest/

**Escalation Path:**
- Primary: DevOps
- Secondary: CTO
- Final: CEO (user-facing issue)

**Recovery Time Target:** 1-2 hours

---

## Communication Templates

### P0 Incident - Initial Notification

```
🔴 P0 INCIDENT: <Brief Description>

**Impact**: <What users are experiencing>
**Started**: <Time>
**Status**: Investigating
**Owner**: <Name>

**Next Update**: <Time + 15 minutes>

#incident-response
```

### P0 Incident - Resolution

```
✅ P0 INCIDENT RESOLVED: <Brief Description>

**Duration**: <Total time>
**Root Cause**: <Brief explanation>
**Resolution**: <What was done>
**Prevention**: <Steps to prevent recurrence>

**Post-mortem**: <Time> (if needed)

#incident-response
```

### P1 Incident - Status Update

```
🟡 P1 INCIDENT: <Brief Description>

**Impact**: <What users are experiencing>
**Started**: <Time>
**Status**: <Investigating/Identified/Fixing>
**Owner**: <Name>
**ETA**: <Estimated resolution time>

**Next Update**: <Time + 30 minutes>

#devops-alerts
```

---

## Contact Information

### Primary Contacts
- **DevOps**: <devops-agent>
- **Backend Engineer**: <backend-agent>
- **Frontend Engineer**: <frontend-agent>
- **CTO**: <cto-agent>
- **CEO**: Eduard Gridan

### Escalation Timelines
- P0: Immediate escalation to c-suite-chat
- P1: Escalate after 30 minutes if unresolved
- P2: Escalate after 2 hours if unresolved

### External Support
- **Vercel Support**: https://vercel.com/support
- **Railway Support**: https://railway.app/help
- **Stripe Support**: https://support.stripe.com
- **PostHog Support**: https://posthog.com/support

---

## Recovery Checklist

### During Incident
- [ ] Classify incident severity (P0/P1/P2)
- [ ] Post initial notification to appropriate channel
- [ ] Begin diagnosis and recovery steps
- [ ] Update status every 15-30 minutes
- [ ] Verify fix with testing
- [ ] Post resolution notification

### Post-Incident
- [ ] Document timeline and root cause
- [ ] Create prevention task if needed
- [ ] Schedule post-mortem for P0/P1
- [ ] Update this document with learnings
- [ ] Close incident ticket

---

## Related Documents
- Monitoring Dashboard: `/docs/evidence/week2gtm-monitoring-dashboard-2026-03-31.md`
- Technical Readiness Status: `/docs/evidence/week2gtm-technical-readiness-status-2026-03-31.md`
- HN Launch Plan: `/docs/gtm/hn-launch-monitoring-response-plan-2026-04-01.md`

---

**Last Updated**: 2026-04-01T09:25:00+02:00
**Next Review**: 2026-04-02 (daily during Week 2 GTM)
**Owner**: dev
