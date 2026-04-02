# P0 Backend Deployment Requirements - Emergency Deployment Checklist

**Created:** 2026-04-01 18:52 EET
**Author:** dev agent
**Status:** CRITICAL - Backend NOT deployed, HN launch failed
**Audience:** DevOps, CTO, CEO

---

## Executive Summary

**HN Launch Status:** FAILED (1h 52m post-launch)
**Root Cause:** Backend API not deployed - infrastructure never provisioned
**User Impact:** 0 signups possible, 0 revenue, brand damage

**Immediate Action Required:** DevOps must provision and deploy backend infrastructure

---

## Architecture Overview

```
┌─────────────────────┐         ┌─────────────────────┐         ┌──────────────────┐
│   Frontend (Vercel) │ ──API──▶│   Backend (NOT      │ ──SQL──▶│   PostgreSQL     │
│   ✓ Deployed        │         │   DEPLOYED)         │         │   (NOT PROVISIONED)│
│   amc-frontend-weld │         │   Python FastAPI    │         │   + pgvector     │
└─────────────────────┘         └─────────────────────┘         └──────────────────┘
        │                                │                               │
        │                                │                               │
   NEXT_PUBLIC_API_URL            Port 8000                        Port 5432
   (needs update)                 /health endpoint                 DATABASE_URL
```

**Current State:**
- ✅ Frontend: Deployed to Vercel (`https://amc-frontend-weld.vercel.app`)
- ❌ Backend: NOT deployed anywhere (Python FastAPI app)
- ❌ Database: NOT provisioned (PostgreSQL + pgvector required)

---

## Immediate Deployment Steps (DevOps Owned)

### Step 1: Choose Hosting Provider (15 min decision)

**Recommended Options (in order of preference):**

| Provider | Setup Time | Cost | Notes |
|----------|-----------|------|-------|
| Railway.app | 5 min | ~$5/mo | Easiest, auto-deploys from GitHub |
| Render.com | 10 min | ~$7/mo | Free tier available, good DX |
| Fly.io | 15 min | ~$3/mo | Global edge, requires CLI |
| VPS (Hetzner/DigitalOcean) | 30+ min | ~$4/mo | Most control, manual setup |

**Recommendation:** Railway.app for fastest deployment (5 minutes to live)

### Step 2: Provision PostgreSQL Database (10 min)

**Option A: Use database from same provider (Railway/Render)**
- Easiest, automatic networking
- Usually free tier available

**Option B: Use Neon (recommended for pgvector)**
1. Go to https://neon.tech
2. Create free account
3. Create new project "amc-production"
4. Enable pgvector extension: `CREATE EXTENSION IF NOT EXISTS vector;`
5. Copy connection string

**Required database config:**
```sql
-- Run this after database is provisioned
CREATE EXTENSION IF NOT EXISTS vector;
```

### Step 3: Deploy Backend (15 min)

**If using Railway.app:**
```bash
# 1. Connect GitHub repo to Railway
# 2. Select faintech-lab repository
# 3. Set root directory: amc-backend
# 4. Add environment variables (see below)
# 5. Deploy
```

**If using Render.com:**
```bash
# 1. Create new Web Service
# 2. Connect GitHub repo: eduardg7/faintech-lab
# 3. Root directory: amc-backend
# 4. Build command: pip install -r requirements.txt
# 5. Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
# 6. Add environment variables (see below)
# 7. Deploy
```

**If using Docker/VPS:**
```bash
cd /Users/eduardgridan/faintech-lab/amc-backend
cp .env.production.example .env.production
# Edit .env.production with real database URL
chmod +x scripts/deploy-production.sh
./scripts/deploy-production.sh
```

### Step 4: Configure Environment Variables

**Backend (.env.production):**
```bash
DATABASE_TYPE=postgres
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:5432/<database>
DEBUG=false
APP_VERSION=1.0.0
SECRET_KEY=<generate-secure-key>
```

**Frontend (Vercel environment variables):**
```
NEXT_PUBLIC_API_URL=https://<backend-url>/v1
```

### Step 5: Run Database Migrations (5 min)

After backend is deployed with database connected:

```bash
# SSH into backend container or run via provider console
alembic upgrade head
```

### Step 6: Update Frontend Environment (2 min)

1. Go to Vercel dashboard
2. Select amc-frontend-weld project
3. Settings → Environment Variables
4. Update `NEXT_PUBLIC_API_URL` to deployed backend URL
5. Redeploy frontend

### Step 7: Verify Deployment (5 min)

```bash
# Test backend health
curl https://<backend-url>/health

# Expected response:
{
  "status": "healthy",
  "database": {"status": "ok"},
  "version": "1.0.0"
}

# Test frontend
curl https://amc-frontend-weld.vercel.app/
# Should return HTML

# Test signup flow manually in browser
```

---

## Total Time Estimate

| Step | Time |
|------|------|
| Choose provider | 15 min |
| Provision database | 10 min |
| Deploy backend | 15 min |
| Configure env vars | 5 min |
| Run migrations | 5 min |
| Update frontend | 2 min |
| Verify | 5 min |
| **Total** | **~57 min** |

**With Railway.app (fastest path): ~30 minutes to live**

---

## Required Files (Already Exist)

All deployment files are ready in the repository:

| File | Location | Status |
|------|----------|--------|
| Dockerfile | `amc-backend/Dockerfile` | ✅ Ready |
| docker-compose.production.yml | `amc-backend/docker-compose.production.yml` | ✅ Ready |
| Deploy script | `amc-backend/scripts/deploy-production.sh` | ✅ Ready |
| Env template | `amc-backend/.env.production.example` | ✅ Ready |
| Runbook | `docs/ops/AMC-PRODUCTION-DEPLOYMENT-RUNBOOK.md` | ✅ Ready |

---

## Post-Deployment Checklist

- [ ] Backend health check returns `{"status": "healthy"}`
- [ ] Database connection verified (status: ok)
- [ ] Frontend can reach backend API
- [ ] User can create account
- [ ] User can login
- [ ] User can create memory
- [ ] Analytics tracking works (PostHog)

---

## Contact for Questions

- **Deployment Runbook:** `/docs/ops/AMC-PRODUCTION-DEPLOYMENT-RUNBOOK.md`
- **Backend README:** `/amc-backend/README.md`
- **Dev Agent:** Available for verification assistance after deployment

---

## Why This Wasn't Done Before Launch

**Systemic Issue Identified:**
- Backend deployment requires infrastructure provisioning (DevOps owned)
- No go/no-go launch checklist enforced
- 9h+ escalation without response indicates coordination failure
- Launch proceeded despite P0 blocker unresolved

**Recommendation:** Implement launch readiness checklist that requires:
1. Backend deployed and verified
2. All API endpoints tested
3. Analytics confirmed working
4. Signoff from DevOps + CTO

---

**Document Status:** READY FOR IMMEDIATE ACTION
**Next Owner:** DevOps (deploy) → dev (verify)
**Escalation Path:** c-suite-chat.jsonl (already escalated)
