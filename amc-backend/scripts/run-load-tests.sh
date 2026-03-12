#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
LOADTEST_DIR="${BACKEND_DIR}/load_tests"
ENV_FILE="${LOADTEST_DIR}/.env.loadtest"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

HOST="${AMC_LOADTEST_HOST:-http://localhost:8000}"
API_KEY="${AMC_LOADTEST_API_KEY:-test-api-key-load-test}"
USERS="${AMC_LOADTEST_USERS:-10}"
SPAWN_RATE="${AMC_LOADTEST_SPAWN_RATE:-10}"
DURATION="${AMC_LOADTEST_DURATION:-60s}"
HTML_REPORT="${AMC_LOADTEST_HTML_REPORT:-reports/loadtest-report.html}"
SCENARIO="${1:-smoke}"

mkdir -p "${LOADTEST_DIR}/reports"
cd "${LOADTEST_DIR}"

LOCUST_BIN="${LOCUST_BIN:-}"
if [[ -z "${LOCUST_BIN}" ]]; then
  if command -v locust >/dev/null 2>&1; then
    LOCUST_BIN="$(command -v locust)"
  else
    echo "locust binary not found in PATH. Install requirements-test.txt into the active environment or set LOCUST_BIN explicitly." >&2
    exit 1
  fi
fi

case "${SCENARIO}" in
  smoke)
    USERS="${AMC_LOADTEST_USERS:-10}"
    SPAWN_RATE="${AMC_LOADTEST_SPAWN_RATE:-10}"
    DURATION="${AMC_LOADTEST_DURATION:-60s}"
    ;;
  full)
    USERS="${AMC_LOADTEST_USERS:-100}"
    SPAWN_RATE="${AMC_LOADTEST_SPAWN_RATE:-10}"
    DURATION="${AMC_LOADTEST_DURATION:-300s}"
    ;;
  custom)
    ;;
  *)
    echo "Unknown scenario: ${SCENARIO}. Use smoke | full | custom" >&2
    exit 1
    ;;
esac

export AMC_LOADTEST_API_KEY="${API_KEY}"

echo "Running ${SCENARIO} load test against ${HOST} with ${USERS} users for ${DURATION}"
exec "${LOCUST_BIN}" -f locustfile.py --headless \
  -u "${USERS}" \
  -r "${SPAWN_RATE}" \
  -t "${DURATION}" \
  --host "${HOST}" \
  --html "${HTML_REPORT}"
