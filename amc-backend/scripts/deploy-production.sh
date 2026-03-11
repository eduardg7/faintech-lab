#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f .env.production ]]; then
  echo "Missing .env.production. Copy .env.production.example and fill in production secrets." >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required" >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "docker compose plugin is required" >&2
  exit 1
fi

echo "[deploy] Building and starting AMC production stack"
docker compose -f docker-compose.production.yml up -d --build

echo "[deploy] Waiting for healthy container"
for attempt in {1..20}; do
  status=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}unknown{{end}}' amc-backend 2>/dev/null || true)
  if [[ "$status" == "healthy" ]]; then
    echo "[deploy] Container is healthy"
    break
  fi
  echo "[deploy] Attempt $attempt/20 status=$status"
  sleep 3
done

curl --fail --silent http://127.0.0.1:8000/health | python3 -m json.tool

echo "[deploy] Done"
