#!/usr/bin/env bash
set -eu
scenario="${1:-human-review}"
case "$scenario" in support-triage|lead-scoring|human-review) ;; *) echo 'Choose support-triage, lead-scoring, or human-review.' >&2; exit 1 ;; esac
root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
if [ "${2:-}" != '--live' ]; then
  if [ "$#" -gt 1 ]; then echo 'Usage: bash quickstart/curl.sh [scenario] [--live]' >&2; exit 1; fi
  echo 'OFFLINE DEMO — illustrative fixture, no API call or charge.'
  cat "$root/examples/$scenario/response.example.json"
  exit 0
fi
if [ "$#" -gt 2 ]; then echo 'Too many arguments.' >&2; exit 1; fi
: "${JEVMODEL_API_KEY:?Set JEVMODEL_API_KEY before using --live.}"
echo 'LIVE REQUEST — check both HTTP status and JSON code; no automatic retry.' >&2
# Keep the authorization header off the process argument list.
printf 'Authorization: Bearer %s\n' "$JEVMODEL_API_KEY" | curl --silent --show-error --fail-with-body \
  --max-time 30 --proto '=https' \
  --request POST 'https://jevmodel.app/api/v1/systemone' \
  --header @- --header 'Content-Type: application/json' \
  --data-binary "@$root/examples/$scenario/request.json" \
  --write-out '\nHTTP %{http_code}\n'
# If the response is lost, check Console history and balance before repeating.
