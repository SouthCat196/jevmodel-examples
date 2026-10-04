# JevModel API 示例

JevModel 提供托管工作台与 API，通过 Choice、Score、Noul 输出结构化 AI 判断。

本仓库包含客服分类、销售线索评分和人工复核三个可运行示例。**默认离线运行，不调用模型、不扣额度。** 只有添加 `--live` 才发送一次真实请求，可能使用免费额度或 Token。

[English](README.md) · [试用工作台](https://jevmodel.app/zh/workbench?utm_source=github&utm_medium=referral&utm_campaign=jevmodel-examples) · [API 文档](https://jevmodel.app/zh/guides/api) · [价格与使用规则](https://jevmodel.app/zh/pricing)

JevModel 是独立托管服务，**与 TypeSafe AI 无关联**。Jev 由 TypeSafe AI 开发；本仓库只提供本站接入示例，不包含模型权重、官方 TypeSafe SDK 或网站源码。本站 API Key 不能用于 TypeSafe 官方 API。

## 离线运行

需要 Git，以及 Node.js 22+、Python 3.10+ 或带 curl 7.76+ 的 Bash / Git Bash。无需安装 npm 或 pip 依赖。

```sh
git clone https://github.com/SouthCat196/jevmodel-examples.git
cd jevmodel-examples
node quickstart/node.mjs
# 或：
python quickstart/python.py
# Bash / Git Bash：
bash quickstart/curl.sh
```

输出标为 `OFFLINE DEMO`。所有 `response.example.json` 均为人工编写的示意数据，其中分数、概率、请求 ID、用量和额度都不是真实调用记录，也不能作为性能证明。

## 真实调用

先[注册](https://jevmodel.app/zh/sign-up)并验证邮箱，再在 [Console → API keys](https://jevmodel.app/zh/console/keys) 创建本站密钥。密钥只放在终端或服务端，不放进浏览器代码、截图、提交或 Issue。示例不会自动加载 `.env`。

PowerShell：

```powershell
$env:JEVMODEL_API_KEY = 'your-key-here'
node quickstart/node.mjs human-review --live
# 或（另一次调用）：
python quickstart/python.py human-review --live
```

Bash / Git Bash：

```sh
export JEVMODEL_API_KEY='your-key-here'
node quickstart/node.mjs human-review --live
# 或，每条命令分别发起一次请求：
python quickstart/python.py human-review --live
bash quickstart/curl.sh human-review --live
```

截至 2026-10-04，已验证邮箱的账号每个 UTC 日共享十次免费单位，工作台与 API 共用，仍受全站容量限制；额外使用可能消耗 Token。运行前查看[当前规则](https://jevmodel.app/zh/pricing)。

## 三个场景

将命令中的 `human-review` 换成其他场景名即可；不加 `--live` 就是离线演示。每个目录均含输入、示意响应和中英文解读。

| 场景 | 输出 | 网站教程 |
| --- | --- | --- |
| [support-triage](examples/support-triage) | Choice：账单、技术或人工分流 | [客服分流](https://jevmodel.app/zh/guides/support-triage) |
| [lead-scoring](examples/lead-scoring) | Score：按有序量表评估跟进优先级 | [线索评分](https://jevmodel.app/zh/guides/lead-scoring) |
| [human-review](examples/human-review) | Noul：是否需要人工复核的概率 | [审核队列](https://jevmodel.app/zh/guides/content-moderation) |

## 请求、响应与解释

接口为 `POST https://jevmodel.app/api/v1/systemone`，请求头包含 `Authorization: Bearer <JEVMODEL_API_KEY>` 与 `Content-Type: application/json`。请求包含 `state` 和 1–8 个具名 `questions`，不要发送 `model`。字段限制见 [API 文档](https://jevmodel.app/zh/guides/api)。

成功响应包装为 `{code: 0, message: "ok", data: {request_id, answers, usage, quota}}`。Node.js 和 Python 输出解包后的 `data`，curl 输出完整包装与 HTTP 状态。

- Choice 返回选项；概率分布与可能返回的 confidence 都不是正确率保证。
- Score 可以带小数，并非天然的 0–1 分数或转化概率。
- Noul 是命题为真的 0–1 概率，没有单独的 confidence 字段。

阈值和权限由调用应用决定，应使用代表性标注样本评估。所有示例只输出数据，不执行退款、发邮件或创建工单。

## 错误处理

同时检查 HTTP 状态与 JSON `code`：400 修正输入；401 检查密钥；403 验证邮箱；413 缩小输入；429 检查容量和余额；502/503 检查上游状态与运行历史。Node.js / Python 在缺少密钥、API 错误、响应格式错误和超时时以非零状态退出。curl 对 HTTP 错误非零退出，但不解析应用层 `code`，需检查输出 JSON。

**不自动重试。** 接口不支持幂等键，超时可能发生在成功扣费之后。再次请求前先检查 [Console 历史](https://jevmodel.app/zh/console)和余额。使用真实密钥时不要开启详细 HTTP 日志。

## 本地检查与许可

```sh
node --test tests/client.test.mjs
python -m unittest discover -s tests -p 'test_*.py'
```

测试使用模拟 HTTP 响应，不调用模型。Issue 请提供脱敏输入与复现步骤，勿包含密钥和客户资料。

自有示例代码和文档采用 [MIT](LICENSE)，不涉及模型权重、上游软件或托管服务的许可。参考：[Jev 是什么](https://jevmodel.app/zh/guides/what-is-jev)、[TypeSafe 文档](https://docs.typesafe.ai/)、[confidence 说明](https://docs.typesafe.ai/confidence)。
