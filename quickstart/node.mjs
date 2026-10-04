import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

const endpoint = 'https://jevmodel.app/api/v1/systemone';
const scenarios = ['support-triage', 'lead-scoring', 'human-review'];

export async function callJev(request, key, fetcher = fetch) {
  if (!key?.trim()) throw new Error('Set JEVMODEL_API_KEY before using --live.');
  let response;
  try {
    response = await fetcher(endpoint, {
      method: 'POST',
      headers: { Authorization: `Bearer ${key.trim()}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
      signal: AbortSignal.timeout(30_000),
      redirect: 'error',
    });
  } catch {
    throw new Error('Network error or timeout. Check Console history and balance before retrying; the server may have completed the run.');
  }
  let envelope;
  try { envelope = await response.json(); }
  catch { throw new Error(`HTTP ${response.status}: invalid JSON response. Check Console history before retrying.`); }
  if (!response.ok || envelope?.code !== 0) {
    // Only expose known API error names; never echo arbitrary upstream content or credentials.
    const message = /^[A-Z][A-Z0-9_]{0,79}$/.test(envelope?.message) ? envelope.message : 'API_ERROR';
    throw new Error(`HTTP ${response.status}: ${message}. See https://jevmodel.app/guides/api. No automatic retry.`);
  }
  if (!envelope.data?.answers || typeof envelope.data.answers !== 'object' || Array.isArray(envelope.data.answers)) {
    throw new Error('Missing data.answers. Check Console history before retrying.');
  }
  return envelope.data;
}

export async function main(args = process.argv.slice(2)) {
  if (args.some(arg => arg.startsWith('--') && arg !== '--live') || args.filter(arg => !arg.startsWith('--')).length > 1) {
    throw new Error('Usage: node quickstart/node.mjs [support-triage|lead-scoring|human-review] [--live]');
  }
  const scenario = args.find(arg => !arg.startsWith('--')) ?? 'human-review';
  if (!scenarios.includes(scenario)) throw new Error(`Choose a scenario: ${scenarios.join(', ')}`);
  const base = new URL(`../examples/${scenario}/`, import.meta.url);
  const request = JSON.parse(await readFile(new URL('request.json', base), 'utf8'));
  const live = args.includes('--live');
  const data = live
    ? await callJev(request, process.env.JEVMODEL_API_KEY)
    : JSON.parse(await readFile(new URL('response.example.json', base), 'utf8')).data;
  console.log(live ? 'LIVE API RESPONSE' : 'OFFLINE DEMO — illustrative fixture, no API call or charge.');
  console.log(JSON.stringify(data, null, 2));
  console.log('Signals only. No refund, email, ticket creation, or other external action was executed.');
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
