# P0 Demo URL Fix - 2026-04-01

## Summary
Fixed P0 incident: Demo URL (https://faintech-lab.vercel.app) was returning HTTP 404.

## Root Cause Analysis
1. PR #110 removed `outputDirectory: "amc-frontend/out"` from root vercel.json
2. PR #110 did NOT set `framework: "nextjs"` despite commit message claiming it did
3. Vercel project `faintech-lab` has incorrect Root Directory setting (root instead of `amc-frontend`)
4. Result: Vercel couldn't find Next.js or serve the app

## Resolution
Deployed directly from `amc-frontend` directory using existing Vercel project `amc-frontend`:
```bash
cd amc-frontend && npx vercel --prod
```

## Verification
- **Landing Page**: https://amc-frontend-weld.vercel.app → HTTP 200 ✅
- **API Endpoint**: https://amc-frontend-weld.vercel.app/api/feedback/ → Working (returns validation error) ✅
- **Dashboard**: https://amc-frontend-weld.vercel.app/dashboard/ → HTTP 200 ✅
- **Memory Page**: https://amc-frontend-weld.vercel.app/memory/ → HTTP 200 ✅

## Working Demo URL
**Primary**: https://amc-frontend-weld.vercel.app

Note: This URL should be used for HN launch and all GTM activities.

## Remaining Actions
1. Update all documentation to use new demo URL
2. Consider configuring Vercel project `faintech-lab` with correct Root Directory
3. Or deprecate `faintech-lab` project and use `amc-frontend` as primary

## Impact
- **Unblocks**: HN launch (April 1, 17:00 EET)
- **Unblocks**: All GTM Week 2 execution
- **Critical**: This fix enables the entire GTM strategy to proceed

## Timeline
- **Issue detected**: 2026-04-01T00:17 EET
- **Root cause identified**: 2026-04-01T02:28 EET
- **Fix deployed**: 2026-04-01T02:36 EET
- **Total resolution time**: ~19 minutes

## Related
- Task: LAB-TECH-20260331-WEEK2GTM
- PR #110 (incomplete fix)
- PR #115 (closed - wrong approach)
- Vercel project: amc-frontend (prj_CSYPwFBW4gOzheqxzm0v57VEjcMA)
