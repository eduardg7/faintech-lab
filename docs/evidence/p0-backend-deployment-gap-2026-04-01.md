# P0 CRITICAL: Backend API Not Deployed - Week 2 GTM Blocked

**Status:** 🔴 P0 BLOCKER
**Discovered:** 2026-04-01T08:25:00+02:00
**Impact:** Week 2 GTM completely blocked - users cannot sign up or use app

## Problem Statement

The frontend is deployed on Vercel (https://amc-frontend-weld.vercel.app) and serving HTTP 200, but the backend FastAPI application is NOT deployed. All API calls fail because the backend URL is configured as `http://localhost:8000/v1` in the frontend's default configuration.

## Evidence

### 1. Frontend Configuration
```bash
# .env.local in amc-frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/v1
```

Source: `/Users/eduardgridan/faintech-lab/amc-frontend/.env.local`

### 2. API Client Code
```typescript
// amc-frontend/src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';
```

If `NEXT_PUBLIC_API_URL` is not set in Vercel environment variables, it defaults to localhost.

### 3. Backend Structure
- Backend is a FastAPI application in `/amc-backend`
- Has Dockerfile and docker-compose.production.yml
- NOT deployed to any cloud service
- Only runs locally on port 8000

### 4. Critical API Routes Missing
- `/api/coordination/wake` - Returns HTML (404 page)
- `/api/search/memory` - Returns HTML (404 page)
- `/api/feedback` - Returns JSON (frontend-only endpoint)

Backend routes that need deployment:
- `/v1/auth/register` - User signup
- `/v1/auth/login` - User authentication
- `/v1/memories` - Memory storage
- `/v1/search/*` - Search functionality
- `/v1/analytics/*` - Analytics tracking

## Impact on Week 2 GTM

### User Journey Broken
1. ✅ User lands on homepage (frontend works)
2. ✅ User reads value proposition (static content)
3. ❌ User clicks "Get Started" → signup form loads
4. ❌ User submits signup form → API call to localhost:8000 FAILS
5. ❌ User sees error, cannot create account
6. ❌ No signup, no conversion, Week 2 GTM fails

### Conversion Rate Impact
- **Expected without backend:** 0% conversion (users cannot sign up)
- **Required for Week 2:** 10-15 signups, >5% conversion
- **Result:** Complete GTM failure if not resolved before April 3

## Root Cause

The frontend was deployed as a static Next.js app on Vercel, but the backend FastAPI application was never deployed to a production environment. This is a fundamental architecture gap.

## Required Actions

### Immediate (P0 - Before HN Launch)
1. **Deploy backend to cloud service** (Railway, Render, Fly.io, or VPS)
   - Estimated time: 2-4 hours
   - Owner: DevOps or backend engineer

2. **Configure Vercel environment variable**
   - Set `NEXT_PUBLIC_API_URL` to deployed backend URL
   - Estimated time: 5 minutes
   - Owner: DevOps

3. **Verify full signup flow**
   - Test: Landing page → signup → email verification → login → create memory
   - Estimated time: 30 minutes
   - Owner: QA or dev

### Total Resolution Time
- **Best case:** 3 hours (if DevOps available immediately)
- **Worst case:** 8 hours (if deployment issues arise)

## Recommendations

### Option 1: Railway/Render (Fastest)
- Deploy FastAPI backend to Railway or Render
- Free tier sufficient for testing
- Automatic HTTPS and domain
- Time to deploy: 1-2 hours

### Option 2: Fly.io (More Control)
- Deploy using existing Dockerfile
- Better for production workloads
- Time to deploy: 2-3 hours

### Option 3: VPS (Most Control)
- Deploy to DigitalOcean/Linode VPS
- Manual Docker setup
- Time to deploy: 3-4 hours

## Escalation

- **Owner:** DevOps (deployment), CTO (architecture decision)
- **Urgency:** P0 - Must resolve before HN launch (April 1, 17:00 EET)
- **Time remaining:** ~8.5 hours

## Verification Steps

After deployment, verify:
1. Backend health check returns 200: `GET /health`
2. Frontend can reach backend: Test signup form
3. User can create account and login
4. Memory creation and search work
5. Analytics events are tracked

---

**Next Action:** Escalate to c-suite-chat immediately. DevOps must prioritize backend deployment over all other work.
