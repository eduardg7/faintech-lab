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

## Project Structure

```
amc-backend/
├── config.py          # Application configuration
├── main.py            # FastAPI app factory and entry point
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker configuration
└── README.md          # This file
```
