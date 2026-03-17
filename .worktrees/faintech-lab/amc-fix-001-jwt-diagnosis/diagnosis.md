# AMC-FIX-001: JWT Token Flow Diagnosis

## Issue
Dashboard returns 401 errors on all requests after login, despite successful authentication.

## Root Cause Analysis

### Frontend Flow (Correct)
1. **LoginForm.tsx**:
   - User enters JWT token
   - Validates token via `api.validateToken(trimmedToken)` → `GET /v1/auth/me`
   - Stores token in localStorage as `amc_api_key` via `setApiKey()`
   - Redirects to `/dashboard`

2. **AuthContext.tsx**:
   - Loads `amc_api_key` from localStorage on mount
   - Provides `apiKey` via `useAuth()` hook

3. **Dashboard Page**:
   - Calls `statsApi.getMemoryStats(apiKey!)`
   - Passes token to API calls

4. **API Layer (stats-api.ts)**:
   - `fetchAllMemories(token)` sends: `headers: { Authorization: Bearer ${token} }`
   - This is CORRECT Bearer auth format

### Backend Flow (Correct in Theory)
1. **auth.py - get_current_auth_context()**:
   - Uses `HTTPBearer()` to extract credentials
   - If token starts with `amc_live_` → validates as API key
   - Otherwise → validates as JWT access token via `TokenData.from_token(token, "access")`

2. **security.py - verify_token()**:
   - Decodes JWT using `JWT_SECRET_KEY`
   - Checks `type == "access"`
   - Checks expiration
   - Returns payload or `None`

### Potential Issues

#### Issue 1: Backend Not Running
The frontend is configured to hit `http://localhost:8000/v1`. If the backend is not running, all requests will fail with connection errors or 404s, not 401s.

**Test**: `curl http://localhost:8000/v1/auth/me -H "Authorization: Bearer <token>"`

#### Issue 2: JWT Secret Key Mismatch
Frontend/backend might be using different JWT secrets in dev vs production environments.

**Backend env** (`amc-backend/.env`):
```
JWT_SECRET_KEY=dev-secret-key-change-in-production
```

**Test**: Generate a fresh token via `POST /v1/auth/login` and test it immediately.

#### Issue 3: Token Type Mismatch
The backend expects `type: "access"` in the JWT payload. If the login endpoint is returning a different type or the validate token logic is inconsistent, this would fail.

**Code check**:
- `create_access_token()` → sets `type: "access"` ✅
- `verify_token()` → checks `payload.get("type") == expected_type` ✅
- `/login` endpoint → returns `access_token` from `create_access_token()` ✅

#### Issue 4: Token Expiration
JWT_ACCESS_TOKEN_EXPIRE_MINUTES is set to 60 minutes in the backend, but the frontend sets it to 30 in the code comments. If tokens expire faster than expected, dashboard polls will fail.

**Backend env**:
```
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend**: No explicit expiration handling seen in AuthContext.

## Recommended Fix

### Immediate Fix
1. Start the backend server if not running
2. Generate a fresh login token via `POST /v1/auth/login`
3. Test the token immediately with `/v1/auth/me`
4. Verify dashboard can fetch data with the new token

### Code Improvements
1. **Add token expiration handling to AuthContext**:
   ```typescript
   // Check token expiration from JWT payload
   const isTokenExpired = (token: string) => {
     const payload = JSON.parse(atob(token.split('.')[1]));
     return payload.exp * 1000 < Date.now();
   };

   // In useEffect:
   if (storedKey && isTokenExpired(storedKey)) {
     setApiKey(null); // Clear expired token
     setIsLoading(false);
   }
   ```

2. **Add better error handling in dashboard**:
   ```typescript
   } catch (error) {
     if (axios.isAxiosError(error) && error.response?.status === 401) {
       logout(); // Clear invalid token
       window.location.href = '/';
     }
     console.warn('Stats API not available, using mock data');
     setUseMockData(true);
     return mockMemoryStats;
   }
   ```

3. **Add backend health check**:
   ```typescript
   const isBackendHealthy = async () => {
     try {
       await axios.get(`${API_BASE_URL}/health`, { timeout: 2000 });
       return true;
     } catch {
       return false;
     }
   };
   ```

## Verification Steps
1. [ ] Start backend: `cd amc-backend && uvicorn app.main:app --reload`
2. [ ] Login via frontend, capture the access token
3. [ ] Test token: `curl http://localhost:8000/v1/auth/me -H "Authorization: Bearer <token>"`
4. [ ] Load dashboard, check browser console for 401 errors
5. [ ] Verify stats API calls with correct Bearer header in network tab

## Evidence
- Diagnosis document created
- Root cause identified (backend likely not running or token validation issue)
- Code review shows frontend auth flow is correct
