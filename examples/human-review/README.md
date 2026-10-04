# Human review / 人工复核

Noul asks whether a human billing specialist should review a synthetic duplicate-charge request now. It outputs a signal; the calling application decides what happens next.

```sh
node quickstart/node.mjs human-review
python quickstart/python.py human-review
bash quickstart/curl.sh human-review
```

Run from the repository root. Set `JEVMODEL_API_KEY` and add `--live` to opt into one real request per command.

Inspect `data.answers.escalate.noul`, a 0–1 probability of the declared proposition being true. Noul has no separate confidence field. The offline `0.94` is illustrative, not a recorded result or a correctness guarantee. Set review rules using representative labeled cases and the cost of missed escalations. This example never approves a refund or sends a notification.

Noul 返回“当前是否需要账单专员复核”命题为真的 0–1 概率，无独立 confidence 字段。离线 `0.94` 仅示意。用代表性标注样本和漏报代价确定复核规则。示例不批准退款、不发送通知。

[Review queue design](https://jevmodel.app/guides/content-moderation) · [中文教程](https://jevmodel.app/zh/guides/content-moderation) · [Billing triage](https://jevmodel.app/guides/support-triage)
