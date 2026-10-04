import importlib.util
import io
import json
from pathlib import Path
import unittest
import urllib.error

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('jev_client', ROOT / 'quickstart/python.py')
client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(client)

class Response(io.BytesIO):
    status = 200

class ClientTests(unittest.TestCase):
    def test_scenarios(self):
        for scenario in client.SCENARIOS:
            base = ROOT / 'examples' / scenario
            payload = json.loads((base / 'request.json').read_text())
            envelope = json.loads((base / 'response.example.json').read_text())
            calls = []
            def opener(request, timeout):
                calls.append(request)
                self.assertEqual(request.full_url, client.ENDPOINT)
                self.assertEqual(json.loads(request.data), payload)
                self.assertEqual(timeout, 30)
                return Response(json.dumps(envelope).encode())
            self.assertEqual(client.call_jev(payload, 'your-key-here', opener), envelope['data'])
            self.assertEqual(len(calls), 1)

    def test_missing_key(self):
        with self.assertRaisesRegex(ValueError, 'Set JEVMODEL_API_KEY'):
            client.call_jev({}, '')

    def test_http_and_application_errors(self):
        for status in (400, 401, 403, 413, 429, 502, 503, 200):
            calls = []
            def opener(request, timeout):
                calls.append(request)
                raw = json.dumps({'code': -1, 'message': 'UNAUTHORIZED'}).encode()
                if status == 200: return Response(raw)
                raise urllib.error.HTTPError(client.ENDPOINT, status, 'error', {}, io.BytesIO(raw))
            with self.assertRaisesRegex(ValueError, 'UNAUTHORIZED'):
                client.call_jev({}, 'your-key-here', opener)
            self.assertEqual(len(calls), 1)

    def test_bad_and_lost_responses(self):
        for raw in (b'not json', b'{"code":0,"data":{}}', b'null'):
            with self.assertRaises(ValueError):
                client.call_jev({}, 'your-key-here', lambda request, timeout: Response(raw))
        def timeout(request, timeout): raise TimeoutError()
        with self.assertRaisesRegex(ValueError, 'history'):
            client.call_jev({}, 'your-key-here', timeout)

    def test_redirect_is_not_followed(self):
        self.assertIsNone(client.NoRedirect().redirect_request(None, None, 302, 'redirect', {}, 'https://example.com'))

if __name__ == '__main__': unittest.main()
