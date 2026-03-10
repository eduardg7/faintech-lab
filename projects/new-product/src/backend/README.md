# Agent Memory Cloud Backend

FastAPI backend for Agent Memory Cloud - a memory system for AI agents.

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL (for production) or SQLite (for development)

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export DATABASE_URL="postgresql://user:password@localhost/amc"
# Or use .env file
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up -d
```

2. View logs:
```bash
docker-compose logs -f
```

3. Stop services:
```bash
docker-compose down
```

## API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Configuration and database
│   ├── middleware/    # Auth and rate limiting
│   ├── models/        # SQLAlchemy models
│   └── main.py        # FastAPI application
├── tests/             # Test suite
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker configuration
└── docker-compose.yml # Docker Compose setup
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection URL | `sqlite:///./amc.db` |
| `DEBUG` | Enable debug mode | `False` |
| `RATE_LIMIT_PER_MINUTE` | API rate limit | `60` |
| `API_KEY_HEADER` | Header name for API keys | `X-API-Key` |

## License

MIT
