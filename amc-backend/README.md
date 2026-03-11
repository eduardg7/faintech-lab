# Agent Memory Cloud API

FastAPI backend for the Agent Memory Cloud MVP.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Access the API:
   - API Documentation: http://localhost:8000/v1/docs
   - Health Check: http://localhost:8000/health

## Docker

Build and run with Docker:
```bash
docker build -t amc-backend .
docker run -p 8000:8000 amc-backend
```

## Production Setup (Neon PostgreSQL + pgvector)

The AMC backend uses SQLite + JSON embeddings for development. Production requires
PostgreSQL + pgvector for efficient vector similarity search.

### Environment Variables

| Variable | Dev default | Production |
|----------|-------------|------------|
| `DATABASE_TYPE` | `sqlite` | `postgres` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./amc.db` | `postgresql+asyncpg://...` |

### Production Deployment Steps

1. **Install production dependencies:**
   ```bash
   pip install pgvector asyncpg
   ```

2. **Set environment variables:**
   ```bash
   export DATABASE_TYPE=postgres
   export DATABASE_URL=postgresql+asyncpg://user:pass@host.neon.tech/dbname
   ```

3. **Enable pgvector on your PostgreSQL instance** (Neon: Dashboard → Extensions → vector):
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

4. **Run migrations** (installs pgvector extension and creates vector column automatically):
   ```bash
   alembic upgrade head
   ```

5. **Verify:**
   ```sql
   SELECT column_name, data_type FROM information_schema.columns
   WHERE table_name = 'memories' AND column_name = 'embedding';
   -- Should return: embedding | USER-DEFINED (vector type)
   ```

### How Dual-Mode Works

- `DATABASE_TYPE=sqlite` (default) → `embedding` column is `JSON` (array of floats)
- `DATABASE_TYPE=postgres` + `pgvector` installed → `embedding` column is `Vector(1536)`

This allows zero-config local development while production uses native vector operations.

See `data/ops/PGVECTOR-MIGRATION-PLAN.md` for the full migration plan (TD-015).

## Project Structure

```
amc-backend/
├── config.py                    # Application configuration (DATABASE_TYPE setting)
├── main.py                      # FastAPI app factory and entry point
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── alembic/
│   └── versions/
│       └── b2c3d4e5f6g7_add_pgvector_embedding.py  # pgvector migration (TD-015)
└── README.md                    # This file
```
