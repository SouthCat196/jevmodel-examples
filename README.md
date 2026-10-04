# JevModel API examples

JevModel provides a hosted playground and API for structured AI decisions using Choice, Score, and Noul.

Run small examples for support classification, lead scoring, and human review. **The default mode is an offline demonstration.** Add `--live` to make one real API request, which may consume free quota or tokens.

[中文说明](README.zh-CN.md) · [Try JevModel](https://jevmodel.app/workbench?utm_source=github&utm_medium=referral&utm_campaign=jevmodel-examples) · [API guide](https://jevmodel.app/guides/api) · [Usage and pricing](https://jevmodel.app/pricing)

JevModel is an independent hosted service and is **not affiliated with TypeSafe AI**. TypeSafe AI develops Jev; this repository contains JevModel integration examples, not model weights, the official TypeSafe SDK, or the website source. A JevModel key is for `jevmodel.app`, not the TypeSafe API.

## Start with an offline demo

Requirements: Git and either **Node.js 22+**, **Python 3.10+**, or **Bash with curl 7.76+**. No npm or pip dependencies are required.

```sh
git clone https://github.com/SouthCat196/jevmodel-examples.git
cd jevmodel-examples
node quickstart/node.mjs
# Or:
python quickstart/python.py
# Or, in Bash / Git Bash:
bash quickstart/curl.sh
```

The output is labeled `OFFLINE DEMO`. Every `response.example.json` is a fabricated illustration, including usage, quota, request ID, scores, and probabilities. None is a recorded model response or a performance result.

## Make one live request

1. [Create an account](https://jevmodel.app/sign-up), verify your email, then [create an API key in Console](https://jevmodel.app/console/keys).
2. Set the key in your terminal session. Keep it out of browser code, screenshots, commits, and issue reports. The examples do not load `.env` automatically.
3. Add `--live` to the command. Each invocation sends one request; it performs no external business action.

Bash / Git Bash:

```sh
export JEVMODEL_API_KEY='your-key-here'
node quickstart/node.mjs human-review --live
# Alternatives (each makes a separate request):
python quickstart/python.py human-review --live
bash quickstart/curl.sh human-review --live
```

PowerShell:

```powershell
$env:JEVMODEL_API_KEY = 'your-key-here'
node quickstart/node.mjs human-review --live
# Or:
python quickstart/python.py human-review --live
```

As documented on October 4, 2026, verified accounts share ten daily free units per UTC day across the playground and API, subject to site capacity. Additional usage may consume tokens. Check the [current pricing and usage rules](https://jevmodel.app/pricing) before running.

## Choose a scenario

Replace `human-review` in any command with one of these names. Each directory includes the request, illustrative response, and a short interpretation guide.

| Scenario | Question | Run offline | Website tutorial |
| --- | --- | --- | --- |
| [Support triage](examples/support-triage) | Choice: billing, technical, or review | `node quickstart/node.mjs support-triage` | [Support routing](https://jevmodel.app/guides/support-triage) |
| [Lead scoring](examples/lead-scoring) | Score: ordered follow-up rubric | `node quickstart/node.mjs lead-scoring` | [Lead scoring](https://jevmodel.app/guides/lead-scoring) |
| [Human review](examples/human-review) | Noul: probability that review is needed | `node quickstart/node.mjs human-review` | [Review queues](https://jevmodel.app/guides/content-moderation) |

## Understand the API contract

All clients send `POST https://jevmodel.app/api/v1/systemone` with `Authorization: Bearer <JEVMODEL_API_KEY>` and `Content-Type: application/json`.

Requests contain `state` (text, JSON object, or nonempty array) and `questions` (1–8 named questions). Do not send a `model` field. Choice criteria are named options; Score criteria are ordered levels; Noul criteria have `true` and `false` descriptions. See the [API guide](https://jevmodel.app/guides/api) for character limits and validation rules.

Successful responses have `{ "code": 0, "message": "ok", "data": { "request_id": "...", "answers": {}, "usage": {}, "quota": {} } }`. Node.js and Python unwrap `data`; curl prints the original envelope and HTTP status. Preserve the raw answers and probabilities when assessing results.

- **Choice** selects a named option. Its probabilities and any returned confidence describe the model output, not a guaranteed correctness rate.
- **Score** may be fractional on an ordered rubric. It is not inherently a 0–1 score or a conversion probability.
- **Noul** returns a 0–1 probability of the proposition being true, with no separate confidence field.

Thresholds and permissions belong in your application. Evaluate them with representative labeled cases. These examples only print data; they do not refund payments, email leads, or create tickets.

## Errors and retries

Check both HTTP status and JSON `code`. Node.js and Python fail with a nonzero exit code for HTTP errors, application errors, malformed responses, missing keys, and timeouts.

| Status | Meaning / next step |
| --- | --- |
| 400 | Invalid JSON or question fields; fix the request. |
| 401 | Missing or invalid JevModel API key. |
| 403 | Verify the account email. |
| 413 | Reduce request size. |
| 429 | Check daily capacity and token balance. |
| 502 / 503 | Upstream result or connection unavailable; inspect history before deciding to retry. |

There are **no automatic retries**. The API does not support idempotency keys: a timeout or lost response can happen after a successful charged run. Check [Console history](https://jevmodel.app/console) and balance before retrying. curl exits nonzero on HTTP failures but does not parse application-level `code`; inspect its printed JSON too. Do not use verbose HTTP logging with a real key.

## Verify locally

```sh
node --test tests/client.test.mjs
python -m unittest discover -s tests -p 'test_*.py'
```

Tests use fake HTTP responses and never call the model or require a key. Contributions should include reproducible steps and sanitized inputs. Please do not post secrets or customer data in issues.

## License and sources

The original example code and documentation are [MIT licensed](LICENSE). This does not grant rights to Jev weights, upstream software, or the hosted service.

- [JevModel API documentation](https://jevmodel.app/guides/api)
- [What is Jev?](https://jevmodel.app/guides/what-is-jev)
- [TypeSafe AI documentation](https://docs.typesafe.ai/)
- [TypeSafe confidence explanation](https://docs.typesafe.ai/confidence)
