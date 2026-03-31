# Demo URL Fix - Action Plan for Eduard

**Created:** 2026-03-31T00:48:00+02:00
**Agent:** dev (Senior Full-Stack Engineer)
**Task:** LAB-DEVOPS-1774909205
**Deadline:** 2026-03-30T23:59:59Z (1.2 hours remaining)
**Priority:** P0 CRITICAL

---

## Summary

Demo URLs are completely broken, blocking HN launch and entire GTM funnel. I've created a code fix (PR #107), but **immediate Eduard action is required** to complete the fix.

## Current Status

❌ `faintech-lab.vercel.app` → HTTP 404
❌ `lab.faintech.ai` → NXDOMAIN (DNS not configured)
❌ `faintech-lab.com` → NXDOMAIN (DNS not configured)

## Root Cause

Vercel deployment was configured at repository root (`.`), but the actual Next.js application is in the `amc-frontend/` subdirectory. This caused Vercel to deploy an empty root directory.

## What I've Done

✅ **Created PR #107** with configuration fix
- Added `vercel.json` pointing to `amc-frontend/`
- Added `.vercelignore` to exclude unnecessary files
- Branch: `devops/fix-vercel-deployment-config`
- Commit: `eb87562`
- URL: https://github.com/eduardg7/faintech-lab/pull/107

---

## URGENT: Action Required from Eduard

### Step 1: Merge PR (2 minutes)

1. Go to: https://github.com/eduardg7/faintech-lab/pull/107
2. Review the changes
3. Click "Merge pull request"
4. Confirm merge

**Expected Result:** Vercel will automatically redeploy with new configuration

### Step 2: Configure Custom Domains in Vercel (5 minutes)

1. Login to Vercel Dashboard: https://vercel.com/login
2. Navigate to: faintech-lab project → Settings → Domains
3. Add domain: `lab.faintech.ai`
4. Add domain: `faintech-lab.com`
5. Note the DNS configuration values Vercel provides

### Step 3: Configure DNS Records (10 minutes)

Go to your domain registrar (where you manage faintech.ai and faintech-lab.com):

#### For lab.faintech.ai:
- **Type:** CNAME
- **Name/Host:** lab
- **Value/Target:** `cname.vercel-dns.com`
- **TTL:** 3600 (or default)

#### For faintech-lab.com:
Check Vercel dashboard for the A records (usually 2 IPs):
- **Type:** A
- **Name/Host:** @ (or leave blank)
- **Value:** [First IP from Vercel]
- **TTL:** 3600

- **Type:** A
- **Name/Host:** @ (or leave blank)
- **Value:** [Second IP from Vercel]
- **TTL:** 3600

### Step 4: Verify (5 minutes)

After completing steps 1-3:

1. **Immediate check:** https://faintech-lab.vercel.app
   - Should load the AMC demo page (HTTP 200)

2. **Wait 5-10 minutes, then check:** https://lab.faintech.ai
   - DNS propagation may take time
   - Should eventually load the demo page

3. **Wait 5-10 minutes, then check:** https://faintech-lab.com
   - DNS propagation may take time
   - Should eventually load the demo page

---

## Troubleshooting

### If faintech-lab.vercel.app still shows 404 after merge:
1. Go to Vercel Dashboard → faintech-lab → Deployments
2. Check if latest deployment succeeded
3. If failed, check build logs
4. May need to change "Root Directory" in Settings to `amc-frontend`

### If custom domains don't resolve:
1. Verify DNS records are correct (use `dig` or `nslookup`)
2. Wait up to 48 hours for full DNS propagation (usually much faster)
3. Check Vercel domain settings for validation status

---

## Business Impact

- **Revenue Impact:** €12,000 - €40,000 Y1 (KR4 validation)
- **GTM Impact:** Blocks entire funnel - 50+ expected demo views lost
- **Launch Impact:** HN launch cannot proceed without working demo
- **Credibility Impact:** Broken demo = lost trust with early adopters

---

## Evidence Trail

- **PR:** https://github.com/eduardg7/faintech-lab/pull/107
- **Task DB:** Updated with evidence entry
- **C-Suite Chat:** Escalation message sent
- **Session State:** Updated at /Users/eduardgridan/.openclaw/agents/dev/SESSION-STATE.md

---

## Next Steps After Fix

Once all URLs are working:
1. Update GTM assets with correct URLs
2. Resume HN launch preparation
3. Execute Reddit GTM strategy (Week 2)
4. Monitor demo page analytics

---

**Contact:** Dev agent via OpenClaw if you encounter any issues with these steps.

**Time Critical:** Please prioritize this NOW - only 1.2 hours until deadline.
