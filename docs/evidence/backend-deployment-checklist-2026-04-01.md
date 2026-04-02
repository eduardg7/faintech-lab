# Backend Deployment Checklist - P0 Priority

**Created:** 2026-04-01T14:52:00+02:00
**Owner:** DevOps
**Urgency:** P0 - Must complete before HN launch (17:00 EET, ~2h remaining)
**Estimated Time:** 2-4 hours

## Prerequisites

- [ ] Docker installed and running
- [ ] Cloud provider account (Railway, Render, Fly.io, or VPS)
- [ ] Domain name (optional, can use provider's subdomain)
- [ ] Stripe account with API keys
- [ ] Postgres database (can use provider's managed DB)

## Step 1: Database Setup (30 min)

- [ ] Create Postgres database with pgvector extension
  - Railway: `railway run postgresql:15`
  - Render: Create managed PostgreSQL
  - Fly.io: `fly postgres create`

- [ ] Enable pgvector extension:
  ```sql
  CREATE EXTENSION IF NOT EXISTS vector;
  ```

- [ ] Save database connection string for Step 2

## Step 2: Environment Configuration (15 min)

- [ ] Copy `.env.production.example` to `.env.production`
- [ ] Set required values:
  ```bash
  # Database
  DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname

  # Security (generate new secrets)
  JWT_SECRET_KEY=<generate 32+ char random string>

  # Stripe (from Stripe dashboard)
  STRIPE_SECRET_KEY=sk_live_xxx
  STRIPE_WEBHOOK_SECRET=whsec_xxx
  STRIPE_STARTER_PRICE_ID=price_xxx
  STRIPE_PRO_PRICE_ID=price_xxx

  # Frontend URL
  FRONTEND_URL=https://amc-frontend-weld.vercel.app
  ```

- [ ] Test configuration locally:
  ```bash
  cd /Users/eduardgridan/faintech-lab/amc-backend
  docker-compose -f docker-compose.production.yml up -d
  curl http://localhost:8000/health
  ```

## Step 3: Deploy to Cloud (1-2 hours)

### Option A: Railway (Fastest - Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add --plugin postgresql

# Deploy
railway up

# Set environment variables
railway variables set JWT_SECRET_KEY=<value>
railway variables set STRIPE_SECRET_KEY=<value>
# ... (set all variables from .env.production)

# Get deployment URL
railway domain
```

### Option B: Render (Free tier available)

1. Create new Web Service on render.com
2. Connect GitHub repo: `eduardg7/faintech-lab`
3. Set:
   - Root Directory: `amc-backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env.production`
5. Deploy

### Option C: Fly.io (More control)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
fly launch --path amc-backend

# Set secrets
fly secrets set JWT_SECRET_KEY=<value>
fly secrets set STRIPE_SECRET_KEY=<value>
# ... (set all variables from .env.production)

# Deploy
fly deploy
```

## Step 4: Configure Frontend (5 min)

- [ ] Get backend deployment URL from Step 3
- [ ] Go to Vercel project settings: https://vercel.com/eduardg7/amc-frontend
- [ ] Add environment variable:
  - Name: `NEXT_PUBLIC_API_URL`
  - Value: `https://<your-backend-url>/v1`
- [ ] Trigger redeploy in Vercel

## Step 5: Run Database Migrations (10 min)

- [ ] Connect to deployed backend:
  ```bash
  # For Railway
  railway connect

  # For other providers, SSH into container
  ```

- [ ] Run migrations:
  ```bash
  alembic upgrade head
  ```

- [ ] Verify migrations:
  ```bash
  alembic current
  ```

## Step 6: Verification (15 min)

### Backend Health Check
```bash
curl https://<your-backend-url>/health
# Expected: {"status": "healthy"}
```

### Frontend-Backend Integration
```bash
# Test signup endpoint
curl -X POST https://<your-backend-url>/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test"}'
# Expected: {"email":"test@example.com","full_name":"Test",...}
```

### Full User Flow
1. Visit https://amc-frontend-weld.vercel.app
2. Click "Get Started"
3. Fill signup form
4. Submit → should create account (no errors)
5. Login → should redirect to dashboard
6. Create memory → should save successfully
7. Search memories → should return results

## Step 7: Configure Webhooks (10 min)

- [ ] Get backend URL for webhook endpoint
- [ ] In Stripe dashboard, add webhook endpoint:
  - URL: `https://<your-backend-url>/v1/webhooks/stripe`
  - Events: `checkout.session.completed`, `customer.subscription.*`
- [ ] Update `STRIPE_WEBHOOK_SECRET` in backend environment
- [ ] Test webhook with Stripe CLI:
  ```bash
  stripe trigger payment_intent.succeeded
  ```

## Step 8: Monitoring Setup (Optional - 30 min)

The docker-compose.production.yml includes Prometheus + Grafana. For cloud deployment:

- [ ] Set up monitoring alerts for:
  - Health check failures
  - High response times (>2s)
  - Database connection errors
  - Stripe webhook failures

## Rollback Plan

If deployment fails:
1. Revert Vercel `NEXT_PUBLIC_API_URL` to empty (disables API calls)
2. Display maintenance message on frontend
3. Postpone HN launch to April 2
4. Resume deployment troubleshooting

## Success Criteria

- [ ] Backend health check returns 200
- [ ] User can signup and login
- [ ] Memory creation and search work
- [ ] Stripe webhooks received
- [ ] No errors in backend logs
- [ ] Frontend successfully communicates with backend

## Contacts

- **DevOps Owner:** @devops (ClawTeam)
- **Backend Expert:** @faintech-backend
- **Architecture:** @cto
- **Escalation:** Post to c-suite-chat.jsonl

## Time Estimates

- Database setup: 30 min
- Environment config: 15 min
- Cloud deployment: 1-2 hours
- Frontend config: 5 min
- Migrations: 10 min
- Verification: 15 min
- Webhooks: 10 min
- **Total: 2-4 hours**

---

**URGENCY:** HN launch scheduled for 17:00 EET (~2h from now). Backend MUST be deployed and verified by 16:30 EET to allow for final testing.

**Next Action:** DevOps to choose deployment option (Railway/Render/Fly.io) and begin Step 1 immediately.
