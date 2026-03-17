# SDK Authentication Header Fix

**Date:** 2026-03-17 23:30
**Priority:** P0 (Blocking SDK usability)
**Owner:** faintech-backend
**Status:** In Progress

## Problem

SDKs (Python and TypeScript) are sending `X-API-Key` header, but backend uses `HTTPBearer` security which expects `Authorization: Bearer <token>`.

### Current State

**Backend (auth.py):**
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_auth_context(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> AuthContext:
    token = credentials.credentials
    if token.startswith(API_KEY_PREFIX):
        auth_context = await _get_api_key_context(token, db)
        ...
```

**Python SDK (client.py, line 108):**
```python
def _headers(self) -> Dict[str, str]:
    return {
        "X-API-Key": self.api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
```

**TypeScript SDK (http-client.ts):**
```typescript
const headers = {
  'X-API-Key': this.apiKey,
  'Content-Type': 'application/json',
  Accept: 'application/json',
};
```

### Root Cause

Backend changed to use HTTPBearer (standard OAuth 2.0 pattern) but SDKs weren't updated to match.

## Solution

Update both SDKs to send `Authorization: Bearer <api_key>` instead of `X-API-Key: <api_key>`.

### Python SDK Changes

File: `sdks/python/agentmemory/client.py`

```python
def _headers(self) -> Dict[str, str]:
    """Build request headers."""
    return {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
```

### TypeScript SDK Changes

File: `sdks/typescript/src/http-client.ts`

```typescript
const headers = {
  'Authorization': `Bearer ${this.apiKey}`,
  'Content-Type': 'application/json',
  Accept: 'application/json',
};
```

## Testing

After fix, test both SDKs:

**Python:**
```bash
cd sdks/python
python -c "
from agentmemory import MemoryClient
client = MemoryClient(api_key='amc_live_test_key')
# Try a simple API call
print('SDK connected successfully')
"
```

**TypeScript:**
```bash
cd sdks/typescript
npm test
# Or manual test:
node -e "
const { MemoryClient } = require('@agentmemory/sdk');
const client = new MemoryClient({ apiKey: 'amc_live_test_key' });
console.log('SDK connected successfully');
"
```

## Impact

- **Blocker:** Without this fix, SDKs cannot authenticate with the backend
- **Beta launch impact:** SDK users cannot use AMC for beta testing
- **Documentation impact:** Example code in READMEs uses incorrect header

## Related

- AMC-FEAT-002: API Key Generation (completed, backend endpoints exist)
- PUBLISHING.md: SDK publishing guide
- Beta launch target: March 24, 2026

## Evidence

- Discovery: Code inspection of auth.py and SDK client files
- Root cause: Header mismatch between SDK and backend
- Proposed fix: Update SDK headers to use Authorization: Bearer pattern
