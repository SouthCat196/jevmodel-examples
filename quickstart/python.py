"""Standard-library example. Offline by default; --live opts into one API call."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ENDPOINT = 'https://jevmodel.app/api/v1/systemone'
SCENARIOS = ('support-triage', 'lead-scoring', 'human-review')

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def call_jev(payload, key, opener=None):
    if not key or not key.strip():
        raise ValueError('Set JEVMODEL_API_KEY before using --live.')
    request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(), method='POST',
        headers={'Authorization': 'Bearer ' + key.strip(), 'Content-Type': 'application/json'})
    open_request = opener or urllib.request.build_opener(NoRedirect()).open
    try:
        with open_request(request, timeout=30) as response:
            status = response.status
            raw = response.read()
    except urllib.error.HTTPError as error:
        status = error.code
        with error:
            raw = error.read()
    except (urllib.error.URLError, TimeoutError, OSError):
        raise ValueError('Network error or timeout. Check Console history and balance before retrying; the server may have completed the run.') from None
    try:
        envelope = json.loads(raw)
    except (ValueError, UnicodeError):
        raise ValueError(f'HTTP {status}: invalid JSON response. Check Console history before retrying.') from None
    if not isinstance(envelope, dict) or not 200 <= status < 300 or envelope.get('code') != 0:
        message = envelope.get('message') if isinstance(envelope, dict) else None
        message = message if isinstance(message, str) and re.fullmatch(r'[A-Z][A-Z0-9_]{0,79}', message) else 'API_ERROR'
        raise ValueError(f'HTTP {status}: {message}. See https://jevmodel.app/guides/api. No automatic retry.')
    data = envelope.get('data')
    if not isinstance(data, dict) or not isinstance(data.get('answers'), dict):
        raise ValueError('Missing data.answers. Check Console history before retrying.')
    return data

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario', nargs='?', choices=SCENARIOS, default='human-review')
    parser.add_argument('--live', action='store_true', help='Make one authenticated API call; quota or tokens may be consumed.')
    args = parser.parse_args()
    base = Path(__file__).resolve().parent.parent / 'examples' / args.scenario
    payload = json.loads((base / 'request.json').read_text(encoding='utf-8'))
    data = call_jev(payload, os.getenv('JEVMODEL_API_KEY')) if args.live else json.loads((base / 'response.example.json').read_text(encoding='utf-8'))['data']
    print('LIVE API RESPONSE' if args.live else 'OFFLINE DEMO — illustrative fixture, no API call or charge.')
    print(json.dumps(data, indent=2))
    print('Signals only. No refund, email, ticket creation, or other external action was executed.')

if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
