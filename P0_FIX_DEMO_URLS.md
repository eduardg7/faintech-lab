# P0 Critical Fix - Demo URLs Broken

**Status**: ESCALATED TO OWNER
**Task ID**: LAB-DEVOPS-1774909205
**Deadline**: MISSED (2026-03-30T23:59:59Z)
**Impact**: HN launch blocked, 50+ expected demo views lost

## Current Situation

All demo URLs are broken:
- ❌ `faintech-lab.vercel.app` → HTTP 404
- ❌ `lab.faintech.ai` → NXDOMAIN (DNS not configured)
- ❌ `faintech-lab.com` → NXDOMAIN (DNS not configured)

## Root Cause

**Vercel project is deploying the wrong directory.**

The Vercel project is configured to deploy from the repository root (`.`), but the Next.js app is in the `amc-frontend/` subdirectory. The root only contains test configuration (vitest), no Next.js app.

## What I've Tried

### Attempt 1 (commit eb87562) - FAILED ❌
- Created `vercel.json` with build command: `cd amc-frontend && npm install && npm run build`
- Set output directory: `amc-frontend/.next`
- **Result**: Vercel deployment failed - "no Next.js version detected"

### Attempt 2 (commit 3b59a18) - FAILED ❌
- Fixed output directory: `amc-frontend/out` (Next.js uses static export)
- **Result**: Vercel deployment still failing

### Why This Approach Doesn't Work
The `vercel.json` file cannot override the Vercel project's Root Directory setting. The project needs to be reconfigured in the Vercel dashboard.

## Required Actions (EDUARD ONLY)

### Step 1: Fix Vercel Project Configuration (5 minutes)
1. Go to https://vercel.com/dashboard
2. Select the `faintech-lab` project
3. Go to **Settings** → **General**
4. Find **Root Directory** setting
5. Change from `.` (root) to `amc-frontend`
6. Click **Save**
7. Go to **Deployments** → Click **Redeploy** on latest deployment

**Expected Result**: `faintech-lab.vercel.app` should return HTTP 200 with the landing page

### Step 2: Disable Deployment Protection (if enabled) (2 minutes)
1. In Vercel project **Settings** → **Deployment Protection**
2. If enabled, either:
   - Disable it completely, OR
   - Add your IP to the allowlist

### Step 3: Configure Custom Domains (10 minutes)
1. In Vercel project **Settings** → **Domains**
2. Add domain: `lab.faintech.ai`
3. Add domain: `faintech-lab.com`
4. Vercel will show DNS records to configure

### Step 4: Configure DNS (5 minutes)
In your DNS provider (where `faintech.ai` and `faintech-lab.com` are registered):

For `lab.faintech.ai`:
```
Type: CNAME
Name: lab
Value: cname.vercel-dns.com
TTL: 3600
```

For `faintech-lab.com`:
```
Type: A
Name: @
Value: 76.76.21.21
TTL: 3600
```

## Verification

After completing the steps above, verify:
1. ✅ `faintech-lab.vercel.app` returns HTTP 200
2. ✅ `lab.faintech.ai` resolves (no NXDOMAIN)
3. ✅ `faintech-lab.com` resolves (no NXDOMAIN)
4. ✅ All URLs show the Faintech Lab landing page

## What Happens Next

Once Eduard completes Step 1 (Vercel Root Directory fix):
- The vercel.json file I created will work correctly
- All future PRs will deploy automatically
- Custom domains (Steps 3-4) can be configured at any time

## Related PRs

- **PR #107**: [P0] Fix Vercel deployment configuration (requires Eduard action above)
- **PR #105**: Landing page accessibility improvements (MERGED ✅)

## Contact

- **Agent**: faintech-frontend
- **Escalation**: c-suite-chat.jsonl (2026-03-31T00:32:00Z)
- **Session State**: ~/.openclaw/agents/faintech-frontend/SESSION-STATE.md

---
**Created**: 2026-03-31T00:35:00+02:00
**Urgency**: P0 - Blocks HN launch + all GTM activities
