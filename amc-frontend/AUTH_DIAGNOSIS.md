# Authentication Diagnosis - AMC-FIX-001

## Problem Statement
Dashboard returns 401 errors on all API requests after login.

## Current Implementation Analysis

### Frontend (amc-frontend)
1. **Token Storage**: localStorage with key `amc_api_key` ✅
2. **Auth Headers**: `Authorization: Bearer ${token}` format ✅
3. **Token Validation**: Calls `/v1/auth/me` on login ✅
4. **Missing Feature**: No automatic token refresh ❌

### Backend (amc-backend)
1. **Auth Endpoints**: `/v1/auth/login`, `/v1/auth/register`, `/v1/auth/refresh`, `/v1/auth/me` ✅
2. **Token Expiry**: Access tokens expire in 30 minutes ✅
3. **Refresh Tokens**: 7-day expiry with rotation ✅
4. **Auth Middleware**: `get_current_user` dependency validates JWT ✅

## Root Cause Analysis

**Primary Issue**: Token expiration without automatic refresh
- Access tokens expire after 30 minutes
- Frontend has no refresh logic
- After expiration, all API calls return 401
- User must re-login manually

**Secondary Issues**:
1. No error handling for 401 responses to trigger refresh
2. No retry logic after successful refresh
3. AuthContext naming confusion (`apiKey` vs JWT token)

## Proposed Fix

1. **Add Token Refresh to AuthContext**:
   - Store both access token and refresh token
   - Implement `refreshAccessToken()` function
   - Call refresh on 401 errors automatically

2. **Add Axios Interceptor**:
   - Intercept 401 responses
   - Trigger token refresh
   - Retry original request with new token
   - Handle refresh failure (logout)

3. **Update AuthContext Interface**:
   - Rename `apiKey` → `accessToken` for clarity
   - Add `refreshToken` state
   - Add `refreshAccessToken()` method

4. **Update Login Flow**:
   - Store both access and refresh tokens from `/v1/auth/login` response
   - Validate access token works before storing

## Acceptance Criteria Verification

- [x] Diagnose root cause: Token expiration without refresh
- [ ] Fix token storage: Store both access and refresh tokens
- [ ] Fix token refresh: Implement automatic refresh on 401
- [ ] Verify auth middleware: Backend expects correct Bearer format (confirmed)
- [ ] Test all endpoints: Verify dashboard works with refreshed tokens
- [ ] Manual verification: Login, wait for token expiry, verify auto-refresh works

## Files to Modify

1. `amc-frontend/src/contexts/AuthContext.tsx` - Add refresh logic
2. `amc-frontend/src/lib/api.ts` - Add axios interceptor
3. `amc-frontend/src/components/LoginForm.tsx` - Store both tokens
4. `amc-frontend/src/lib/stats-api.ts` - Use shared axios instance

## Next Steps

1. Implement axios interceptor in api.ts
2. Update AuthContext with refresh logic
3. Update LoginForm to store both tokens
4. Test with backend to verify 401 handling
5. Document token refresh flow
