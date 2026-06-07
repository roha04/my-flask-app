#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-}"
if [ -z "$BASE_URL" ]; then
  echo "Usage: smoke_test.sh <base_url>"
  exit 1
fi

BASE_URL="${BASE_URL%/}"
ATTEMPTS="${SMOKE_ATTEMPTS:-5}"
RETRY_SLEEP="${SMOKE_RETRY_SLEEP:-5}"

echo "Running smoke tests against ${BASE_URL}"

for attempt in $(seq 1 "$ATTEMPTS"); do
  echo "Attempt ${attempt}/${ATTEMPTS}"
  response="$(curl -fsS "${BASE_URL}/health")"
  echo "Health response: ${response}"
  echo "${response}" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"(ok|degraded)"'
  echo "${response}" | grep -Eq '"db"[[:space:]]*:[[:space:]]*"ok"'
  sleep "$RETRY_SLEEP"
done

curl -fsS "${BASE_URL}/version" | grep -Eq '"version"'
curl -fsS "${BASE_URL}/docs" | grep -qi "swagger"

echo "Smoke tests passed."
