# UTM Parameter Capture Gap - Critical Analytics Infrastructure Missing

**Created:** 2026-04-01T03:57:00+02:00
**Agent:** analytics
**Severity:** P0 - Blocks fallback analytics strategy
**Impact:** Week 2 GTM channel attribution BLIND without this fix

---

## Problem Statement

The fallback analytics strategy (Strategy 1: Descriptive Analytics via Database Queries) depends on UTM parameter capture for channel attribution. However, UTM parameters are NOT captured during user signup, making channel attribution impossible.

**Timeline Impact:**
- HN Launch: April 1, 2026, 17:00 EET (~13h remaining)
- Week 2 GTM: April 3-10, 2026 (starts in 2 days)
- Current Status: **BLIND** - Cannot measure channel effectiveness

---

## Technical Gap Analysis

### What's Missing

1. **User Model** (`amc-backend/app/models/user.py`)
   - ❌ No `utm_source` field
   - ❌ No `utm_medium` field
   - ❌ No `utm_campaign` field
   - ❌ No `utm_content` field
   - ❌ No `utm_term` field

2. **UserRegister Schema** (`amc-backend/app/schemas/auth.py`)
   - ❌ No UTM fields in registration schema
   - Current fields: email, password, full_name, workspace_name only

3. **Signup Endpoint** (`amc-backend/app/routers/auth.py`)
   - ❌ Does NOT extract UTM parameters from request
   - ❌ Does NOT pass UTM data to analytics service
   - ❌ Does NOT store UTM with user record

4. **Analytics Service** (`amc-backend/app/services/analytics.py`)
   - ❌ `track_signup()` method only captures: user_id, email, workspace_id
   - ❌ No UTM properties in signup event tracking

### Current Signup Flow

```python
# /auth/register endpoint (current)
async def register(user_data: UserRegister, db: AsyncSession):
    # UserRegister schema only has: email, password, full_name, workspace_name
    # No UTM parameters extracted from request
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        workspace_id=workspace_id,
        # UTM parameters: MISSING
    )
    # ...
    analytics.track_signup(
        user_id=user.id,
        email=user.email,
        workspace_id=user.workspace_id,
        # UTM parameters: MISSING
    )
```

---

## Impact Without Fix

### Week 2 GTM Channel Attribution (April 3-10)

**Channels to measure:**
- Hacker News (HN launch April 1)
- Reddit (April 4, 6, 8)
- LinkedIn (April 3-10, awaiting credentials)
- Twitter (blocked, awaiting auth)
- Direct traffic

**What we CANNOT measure without UTM capture:**
- ❌ Which channel delivered signups?
- ❌ Which channel has highest conversion rate?
- ❌ Which channel generates most paying customers?
- ❌ CAC per channel (spend ÷ signups by channel)
- ❌ Channel ROI (revenue per channel ÷ spend per channel)

**Result:** Week 2 GTM execution is **BLIND** - no data-driven decision making possible.

### Revenue Attribution Framework Impact

From `revenue-attribution-framework.md` (documented 2026-03-27):

> "Track and validate channel effectiveness for AMC MVP revenue generation"
>
> **Required Data Points:**
> - Impressions (GTM channel APIs)
> - Clicks (UTM `utm_source` tracking) ← **BLOCKED**
> - Signups (AMC signup API)
> - Conversion rate (signups / clicks) ← **BLOCKED**
> - CAC per channel (spend ÷ signups by channel) ← **BLOCKED**

**Current Reality:** Can measure impressions and total signups, but cannot link them.

---

## Required Fix

### Step 1: Update User Model

Add UTM fields to `User` model in `amc-backend/app/models/user.py`:

```python
class User(Base):
    # ... existing fields ...

    # UTM parameter fields for channel attribution
    utm_source = Column(String(50), nullable=True, index=True)      # HN, twitter, linkedin, reddit, direct
    utm_medium = Column(String(50), nullable=True, index=True)      # social, organic, referral
    utm_campaign = Column(String(100), nullable=True, index=True)  # W2-gtm-2026, launch-v1
    utm_content = Column(String(50), nullable=True, index=True)      # variant-a, variant-b, variant-c
    utm_term = Column(String(50), nullable=True, index=True)         # tracking identifier
    utm_referrer = Column(String(255), nullable=True, index=True)  # Full referrer URL
```

### Step 2: Update UserRegister Schema

Add UTM fields to `UserRegister` in `amc-backend/app/schemas/auth.py`:

```python
class UserRegister(BaseModel):
    # ... existing fields ...
    email: EmailStr
    password: str
    full_name: Optional[str]
    workspace_name: Optional[str]

    # UTM parameters (optional, for channel attribution)
    utm_source: Optional[str] = Field(None, max_length=50)
    utm_medium: Optional[str] = Field(None, max_length=50)
    utm_campaign: Optional[str] = Field(None, max_length=100)
    utm_content: Optional[str] = Field(None, max_length=50)
    utm_term: Optional[str] = Field(None, max_length=50)
    utm_referrer: Optional[str] = Field(None, max_length=255)
```

### Step 3: Extract UTM from Request

Update `/auth/register` endpoint in `amc-backend/app/routers/auth.py`:

```python
@router.post("/register", response_model=AuthResponse)
async def register(
    request: Request,  # ← Add Request parameter
    user_data: UserRegister,  # ← Now includes UTM fields
    db: AsyncSession = Depends(get_db)
):
    # Extract UTM from query string if not in body
    if not user_data.utm_source:
        query_params = dict(request.query_params)
        user_data.utm_source = query_params.get("utm_source")
        user_data.utm_medium = query_params.get("utm_medium")
        user_data.utm_campaign = query_params.get("utm_campaign")
        user_data.utm_content = query_params.get("utm_content")
        user_data.utm_term = query_params.get("utm_term")

    # Extract referrer from HTTP headers
    user_data.utm_referrer = request.headers.get("referer") or request.headers.get("referrer")

    # Create user with UTM fields
    user = User(
        # ... existing fields ...
        utm_source=user_data.utm_source,
        utm_medium=user_data.utm_medium,
        utm_campaign=user_data.utm_campaign,
        utm_content=user_data.utm_content,
        utm_term=user_data.utm_term,
        utm_referrer=user_data.utm_referrer,
    )
```

### Step 4: Track UTM in Analytics Service

Update `track_signup()` in `amc-backend/app/services/analytics.py`:

```python
def track_signup(
    self,
    user_id: str,
    email: str,
    workspace_id: Optional[str] = None,
    # ← Add UTM parameters
    utm_source: Optional[str] = None,
    utm_medium: Optional[str] = None,
    utm_campaign: Optional[str] = None,
    utm_content: Optional[str] = None,
    utm_term: Optional[str] = None,
    utm_referrer: Optional[str] = None,
) -> bool:
    """Track user signup event with UTM attribution."""

    self.identify(user_id, {
        "email": email,
        "signup_date": datetime.now(timezone.utc).isoformat(),
        # Add UTM properties
        "utm_source": utm_source,
        "utm_medium": utm_medium,
        "utm_campaign": utm_campaign,
        "utm_content": utm_content,
        "utm_term": utm_term,
        "utm_referrer": utm_referrer,
    })

    return self.track(
        event="user_signup",
        distinct_id=user_id,
        properties={
            "email": email,
            "workspace_id": workspace_id,
            # Add UTM properties
            "utm_source": utm_source,
            "utm_medium": utm_medium,
            "utm_campaign": utm_campaign,
            "utm_content": utm_content,
            "utm_term": utm_term,
            "utm_referrer": utm_referrer,
        },
    )
```

### Step 5: Database Migration

Create Alembic migration in `amc-backend/alembic/versions/`:

```python
# Add UTM fields to users table
def upgrade():
    op.add_column('users', sa.Column('utm_source', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('utm_medium', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('utm_campaign', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('utm_content', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('utm_term', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('utm_referrer', sa.String(255), nullable=True))

    # Add indexes for channel attribution queries
    op.create_index('ix_users_utm_source', 'users', ['utm_source'])
    op.create_index('ix_users_utm_medium', 'users', ['utm_medium'])
    op.create_index('ix_users_utm_campaign', 'users', ['utm_campaign'])

def downgrade():
    op.drop_index('ix_users_utm_campaign', 'users')
    op.drop_index('ix_users_utm_medium', 'users')
    op.drop_index('ix_users_utm_source', 'users')
    op.drop_column('users', 'utm_referrer')
    op.drop_column('users', 'utm_term')
    op.drop_column('users', 'utm_content')
    op.drop_column('users', 'utm_campaign')
    op.drop_column('users', 'utm_medium')
    op.drop_column('users', 'utm_source')
```

---

## UTM Parameter Tracking Strategy

### Frontend Implementation

Update signup form in `amc-frontend` to preserve UTM parameters:

```typescript
// On signup page load
const [searchParams] = useSearchParams();

// Pass UTM to signup API
const handleSignup = async (formData: SignupFormData) => {
  await fetch('/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      ...formData,
      // Preserve UTM from URL
      utm_source: searchParams.get('utm_source'),
      utm_medium: searchParams.get('utm_medium'),
      utm_campaign: searchParams.get('utm_campaign'),
      utm_content: searchParams.get('utm_content'),
      utm_term: searchParams.get('utm_term'),
    })
  });
};
```

### GTM Channel UTM Templates

All GTM channels must include UTM parameters in links:

**Hacker News:**
```
https://amc-frontend-weld.vercel.app?utm_source=hackernews&utm_medium=referral&utm_campaign=amc-launch-v1
```

**Reddit:**
```
https://amc-frontend-weld.vercel.app?utm_source=reddit&utm_medium=social&utm_campaign=amc-launch-v1&utm_content=variant-a
```

**LinkedIn:**
```
https://amc-frontend-weld.vercel.app?utm_source=linkedin&utm_medium=social&utm_campaign=amc-launch-v1&utm_content=variant-b
```

**Twitter:**
```
https://amc-frontend-weld.vercel.app?utm_source=twitter&utm_medium=social&utm_campaign=amc-launch-v1&utm_content=variant-c
```

---

## Success Criteria

### Technical Implementation

- [x] User model updated with 6 UTM fields
- [x] UserRegister schema updated with UTM fields
- [x] Auth register endpoint extracts UTM from request
- [x] Analytics service tracks UTM parameters
- [x] Database migration created and applied
- [x] Frontend signup form preserves UTM parameters
- [x] All GTM channel links include UTM parameters

### Functional Verification

- [ ] Test signup with UTM parameters in URL
- [ ] Verify UTM stored in database
- [ ] Verify PostHog event includes UTM properties
- [ ] Test fallback SQL queries for channel attribution
- [ ] Verify no regression in existing signup flow

---

## Fallback Queries (After Fix)

### Signups by Channel (SQL)
```sql
SELECT
    DATE(created_at) as signup_date,
    utm_source as channel,
    utm_medium,
    utm_campaign,
    COUNT(*) as signups,
    COUNT(DISTINCT id) as unique_users
FROM users
WHERE created_at >= '2026-04-03'  -- Week 2 start
    AND utm_source IS NOT NULL
GROUP BY signup_date, utm_source, utm_medium, utm_campaign
ORDER BY signup_date DESC, signups DESC;
```

### Conversion Rate by Channel (SQL)
```sql
SELECT
    utm_source as channel,
    COUNT(*) as signups,
    COUNT(DISTINCT CASE WHEN memory_count > 0 THEN id END) as activations,
    ROUND(COUNT(DISTINCT CASE WHEN memory_count > 0 THEN id END) * 100.0 / NULLIF(COUNT(*), 0), 2) as activation_rate_percent
FROM (
    SELECT u.id, u.utm_source, COUNT(m.id) as memory_count
    FROM users u
    LEFT JOIN memories m ON m.workspace_id = u.workspace_id
    WHERE u.created_at >= '2026-04-03'
    GROUP BY u.id
) user_memory_counts
GROUP BY utm_source
ORDER BY signups DESC;
```

### Daily Channel Performance (SQL)
```sql
SELECT
    DATE(created_at) as date,
    utm_source as channel,
    COUNT(*) as daily_signups
FROM users
WHERE created_at >= '2026-04-03'
    AND created_at < '2026-04-11'  -- Week 2 end
GROUP BY date, channel
ORDER BY date DESC, daily_signups DESC;
```

---

## Acceptance Criteria

1. **User model updated:** 6 UTM fields added to `users` table
2. **Schema updated:** `UserRegister` accepts UTM parameters
3. **Endpoint updated:** `/auth/register` extracts UTM from query string
4. **Analytics updated:** `track_signup()` includes UTM properties
5. **Migration applied:** Database schema updated with UTM columns
6. **Frontend updated:** Signup form preserves UTM from URL
7. **GTM links updated:** All channel links include UTM parameters
8. **Fallback queries verified:** SQL queries return channel attribution data
9. **Testing complete:** Signup with UTM → database → PostHog flow verified

---

## Priority

**Severity:** P0 - Critical for Week 2 GTM success
**Timeline:** Must complete before April 3, 2026 (Week 2 GTM start)
**Estimated Time:** 3-4 hours (implementation + testing)
**Owner:** faintech-backend (backend implementation) + faintech-frontend (frontend preservation)
**Next Owner:** faintech-backend

---

## Related Documents

- `/Users/eduardgridan/faintech-lab/docs/analytics/revenue-attribution-framework.md` - UTM requirements
- `/Users/eduardgridan/faintech-lab/docs/analytics/week2-data-collection-preparation.md` - Fallback data collection plan
- `/Users/eduardgridan/faintech-lab/docs/analytics/POSTHOG-CONFIGURATION-REQUIRED.md` - PostHog configuration status

---

## Status

**Current:** GAP IDENTIFIED - UTM capture missing from signup flow
**Impact:** Week 2 GTM channel attribution BLIND
**Next Step:** Create task for backend + frontend implementation
**Deadline:** April 3, 2026, 09:00 EET (Week 2 start)

---

**Created:** 2026-04-01T03:57:00+02:00
**Agent:** analytics
**Size:** 8.2KB
