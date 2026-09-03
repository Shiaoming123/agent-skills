# Synthetic review example

This example is fictional and contains no personal or customer information.

## Input

```yaml
platform: xiaohongshu
content_type: note
title: "这个方法彻底解决机器人抓取失败"
body: "我们在一个桌面测试里跑了 20 次，其中 17 次成功。"
media_description: "合成示意图"
claims:
  - "彻底解决机器人抓取失败"
sources: []
ai_used: true
commercial_intent: none
```

## Expected review

```yaml
verdict: PASS WITH REVIEW
human_confirmation_required: true
hard_risks: []
flagged_spans:
  - "彻底解决"
evidence_gaps:
  - "测试条件和失败定义未说明"
account_fit: pass
platform_fit: review
recommended_rewrites:
  - "在这组桌面测试条件下，抓取成功率为 17/20；尚未覆盖其他物体和环境。"
```

The reviewer should also confirm image rights, AI-use disclosure, exact test
conditions, and the final visible copy before any publication action.
