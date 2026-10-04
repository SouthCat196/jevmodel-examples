# Lead scoring / 销售线索评分

Score evaluates observable follow-up signals using four ordered levels: no stated need, some fit, a demo request, and active procurement. Input describes a synthetic lead.

```sh
node quickstart/node.mjs lead-scoring
python quickstart/python.py lead-scoring
bash quickstart/curl.sh lead-scoring
```

Run from the repository root. Set `JEVMODEL_API_KEY` and add `--live` to opt into one real request per command.

Inspect `data.answers.priority.score`. The offline `2.7` is an illustrative rubric score, not a conversion probability, a 0–1 score, or an observed result. Check the returned scale before choosing bands. Compare score bands with labeled leads and actual follow-up outcomes; revisit them as business conditions change. The example sends no emails and updates no CRM.

Score 按可观察的跟进行为评分。离线 `2.7` 是示意量表分数，不是转化概率，也非天然 0–1 值。设置分数区间前确认实际返回尺度，并与标注线索和跟进结果对照。示例不发邮件、不更新 CRM。

[Rubric and evaluation guidance](https://jevmodel.app/guides/lead-scoring) · [中文教程](https://jevmodel.app/zh/guides/lead-scoring)
