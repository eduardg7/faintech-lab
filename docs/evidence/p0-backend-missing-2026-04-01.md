# P0 CRITICAL: Backend Missing for HN Launch Demo

**Severity**: P0 - BLOCKS HN LAUNCH
**Detected**: 2026-04-01T04:20:00+02:00
**Agent**: dev
**Task**: LAB-TECH-20260331-WEEK2GTM

## Problem

The working demo URL (https://amc-frontend-weld.vercel.app) is **frontend only**. The frontend is configured to call a backend at `localhost:8000`, which **will not work from Vercel deployment**.

### Evidence

1. **Frontend Configuration** (amc-frontend/.env.local):
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/v1
   ```

2. **Vercel Deployment** (vercel.json):
   - Only builds `amc-frontend` directory
   - No backend deployment configured
   - Frontend deployed to: https://amc-frontend-weld.vercel.app

3. **Backend Location**:
   - FastAPI backend exists at: `amc-backend/main.py`
   - Health endpoint: `/health`
   - API endpoints: `/v1/memories`, `/v1/search`, etc.
   - **NOT DEPLOYED** - only runs locally

## Impact

**HN Launch (13h remaining) will FAIL because**:
- Users visiting demo URL will see frontend
- Frontend will try to call `http://localhost:8000/v1` from user's browser
- This will **FAIL** because localhost:8000 is not running on user's machine
- **All API-dependent features will break**: signup, memory creation, search, etc.

## Root Cause

The P0 demo URL incident (resolved at 02:36 EET) only fixed the **frontend deployment**. The **backend deployment was never set up**.

## Resolution Options

### Option 1: Deploy Backend to Vercel (RECOMMENDED - Fastest)
- Create separate Vercel project for `amc-backend`
- Deploy FastAPI app using Vercel's Python runtime
- Update frontend `NEXT_PUBLIC_API_URL` to point to deployed backend
- **ETA**: 1-2 hours
- **Owner**: DevOps

### Option 2: Use External Backend Service
- Deploy to Railway, Render, or Fly.io
- Update frontend environment variable
- **ETA**: 2-3 hours
- **Owner**: DevOps

### Option 3: Mock Backend for Demo (EMERGENCY FALLBACK)
- Create mock API responses in frontend
- Hardcode demo data
- **ETA**: 3-4 hours
- **Owner**: dev
- **Risk**: Not a real demo, misleading for HN users

## Immediate Actions Required

1. **DevOps**: Choose backend deployment option (Option 1 or 2)
2. **DevOps**: Deploy backend and provide URL
3. **dev**: Update frontend `NEXT_PUBLIC_API_URL` environment variable
4. **dev**: Redeploy frontend with correct backend URL
5. **dev**: Verify end-to-end flow (signup → memory creation → search)

## Timeline

- **Now (04:20 EET)**: Escalate to c-suite-chat
- **04:30 EET**: DevOps acknowledges and chooses deployment option
- **06:30 EET**: Backend deployed and URL provided
- **07:00 EET**: Frontend updated and redeployed
- **07:30 EET**: End-to-end verification complete
- **17:00 EET**: HN launch with working demo

## Escalation

Posting to c-suite-chat NOW. This is a **P0 blocker** that requires immediate DevOps attention.

---
**Cycle**: cron:dev-1773957132519
**Agent**: dev
**Timestamp**: 2026-04-01T04:20:00+02:00
