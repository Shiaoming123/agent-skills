---
name: social-content-preflight
description: Preflight Chinese social-media content for Xiaohongshu, Douyin, and Bilibili. Use when creating, reviewing, rewriting, or deciding whether a post, script, caption, carousel, subtitle, image description, or source-backed claim is ready to publish; combine platform rules, account tone, factual boundaries, copyright/privacy checks, and a pass/review/block decision.
version: 0.1.0
---

# Social Content Preflight

## Purpose

Act as the gate between content generation and browser publishing. Review the complete draft, its claims, media, audience fit, and platform-specific risks. This skill can reduce avoidable risk; it cannot guarantee approval, reach, or the absence of every newly changing rule.

Read these references when relevant:

- `references/account-profile-template.md` to create a private account profile when the user provides one. Do not invent or publish personal profile details.
- `references/platform-rules.md` for official rule links and the limits of third-party detectors.
- `references/review-output.md` for the input fields and compact report format.

## Workflow

1. Normalize the submission into platform, content type, title, body/script, subtitles, media description, claims, sources, AI-use disclosure, and commercial intent. If a required field is missing, mark it as unknown rather than inventing it.
2. Run a hard-risk review before stylistic editing. Block or escalate content involving illegal activity, sexual exploitation, graphic violence, fraud, gambling, privacy or personal data, minors at risk, credentials, internal or unreleased information, unlicensed media, fabricated identities/results/testimonials/metrics, engagement manipulation, or instructions to evade review.
3. If `content-compliance-checker` is installed and available, use it as an optional high-recall warning layer for advertising absolutes, guarantees, medical/financial claims, authority claims, platform-sensitive terms, and other sensitive categories. A hit is a review signal, not proof of a violation; ordinary words can false-positive. If it is unavailable, continue the manual category and evidence review, and disclose that the optional detector was not run. Do not invent a complete platform blacklist and do not recommend homophone, pinyin, split-character, or image-text evasion.
4. Separate claims by evidence class:
   - public fact: retain a source and date;
   - personal experience: identify it as personal, remove private details, and avoid generalizing;
   - inference: label it as an inference;
   - unverified or confidential claim: do not publish until verified or removed.
5. Check account fit against the private profile supplied by the user. If no profile is available, mark account fit as unknown and apply only the general audience and evidence boundaries. Prefer concrete experience, reproducible methods, evidence or clearly stated limitations, and a useful takeaway. Reject invented workplace stories, motivational marketing, unsupported “industry first” language, and aggressive controversy that does not serve the stated audience.
6. Rewrite risky phrasing without changing meaning. For example:
   - “行业最强” -> “在这个任务和测试条件下表现较好”；
   - “彻底解决” -> “尝试解决其中一个具体环节，但仍有这些边界”；
   - “一定会进入家庭” -> “是否进入家庭取决于成本、可靠性、隐私和使用习惯”；
   - “评论区扣1发资料” -> put the useful checklist in the post and remove forced engagement;
   - “内部消息” -> replace with a public source or label it as an unverified claim and remove it.
7. Adapt the final version to the platform without weakening safety: Xiaohongshu should be experience-led, useful, concrete, and non-spammy; Douyin should make the spoken claim and AI-use status clear; Bilibili should preserve source context, attribution, and long-form explanation.
8. Return one of `PASS`, `PASS WITH REVIEW`, `REVIEW`, or `BLOCK`, with reasons, flagged spans, evidence gaps, proposed rewrites, and a final checklist. Always set `human_confirmation_required: true` for any publication action.

## Publication Boundary

Never publish, like, follow, comment, send private messages, or batch-operate on the user's behalf from this skill. Before using the visible Edge browser, show the exact final title, body/script, tags, and media set; confirm privacy, rights, factual boundaries, and user approval. Publish at most one confirmed item, then verify the visible result. Stop on login challenges, CAPTCHA, risk control, browser disconnection, or uncertain submission status.

## Output Standard

Use the schema in `references/review-output.md`. Be specific and conservative: quote the risky span, explain the category, distinguish official rules from third-party heuristics, and never claim “绝对安全”“保证过审” or “完整违禁词库”.
