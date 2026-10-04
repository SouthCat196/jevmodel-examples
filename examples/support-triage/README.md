# Support triage / 客服分类

Choice selects a support queue from `billing`, `technical`, and `review`. The request is a synthetic duplicate-charge complaint; it contains no customer record.

```sh
node quickstart/node.mjs support-triage
python quickstart/python.py support-triage
bash quickstart/curl.sh support-triage
```

Run from the repository root. Add `--live` only after setting `JEVMODEL_API_KEY`; each command then sends one separate request. See the [quickstart](../../README.md#make-one-live-request).

Inspect `data.answers.queue.choice` and any returned `probabilities` / `confidence`. The offline `billing: 0.86` is illustrative, not a measured 86% correctness rate. Preserve the input and use labeled tickets to evaluate queue assignments. Close probabilities, unfamiliar categories, or risk signals should prompt human triage. No ticket or refund is created.

客服 Choice 从账单、技术和人工分流中选一项。离线概率是示意数据，不代表准确率；相近概率、不熟悉的类别或风险信号应交人工。示例不创建工单、不退款。以上命令在仓库根目录运行，加 `--live` 才真实调用。

[Workflow and fallback design](https://jevmodel.app/guides/support-triage) · [中文教程](https://jevmodel.app/zh/guides/support-triage)
