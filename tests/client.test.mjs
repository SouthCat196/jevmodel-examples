import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { callJev } from '../quickstart/node.mjs';

test('all scenario fixtures unwrap without a live request', async () => {
  for (const scenario of ['support-triage', 'lead-scoring', 'human-review']) {
    const base = new URL(`../examples/${scenario}/`, import.meta.url);
    const request = JSON.parse(await readFile(new URL('request.json', base), 'utf8'));
    const envelope = JSON.parse(await readFile(new URL('response.example.json', base), 'utf8'));
    let count = 0;
    const data = await callJev(request, 'your-key-here', async (url, options) => {
      count++;
      assert.equal(url, 'https://jevmodel.app/api/v1/systemone');
      assert.equal(options.method, 'POST');
      assert.equal(options.redirect, 'error');
      assert.equal(options.headers.Authorization, 'Bearer your-key-here');
      assert.deepEqual(JSON.parse(options.body), request);
      return Response.json(envelope);
    });
    assert.deepEqual(data, envelope.data);
    assert.equal(count, 1);
    for (const [id, question] of Object.entries(request.questions)) assert.equal(data.answers[id].type, question.type);
  }
});

test('missing key makes no HTTP request', async () => {
  await assert.rejects(callJev({}, '', () => { throw new Error('must not call'); }), /Set JEVMODEL_API_KEY/);
});

test('HTTP and application errors fail without retry or leaking response content', async () => {
  for (const status of [400, 401, 403, 413, 429, 502, 503, 200]) {
    let calls = 0;
    await assert.rejects(callJev({}, 'your-key-here', async () => {
      calls++;
      return Response.json({ code: -1, message: 'UNAUTHORIZED' }, { status });
    }), /UNAUTHORIZED/);
    assert.equal(calls, 1);
  }
  await assert.rejects(callJev({}, 'your-key-here', async () => Response.json({ code: -1, message: 'secret-user-data' }, { status: 502 })), /API_ERROR/);
});

test('malformed, missing-data, and network responses advise checking history', async () => {
  const fetchers = [
    async () => new Response('<html>error</html>'),
    async () => Response.json({ code: 0, data: {} }),
    async () => { throw new Error('timeout'); },
  ];
  for (const fetcher of fetchers) await assert.rejects(callJev({}, 'your-key-here', fetcher), /[Hh]istory/);
});
