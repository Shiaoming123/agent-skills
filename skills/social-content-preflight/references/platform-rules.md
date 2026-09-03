# Platform rules and evidence boundary

Research baseline: 2026-08-04. Platform rules and enforcement change; open the official page again when a post is commercially sensitive, controversial, or close to a policy boundary.

## Official starting points

- Xiaohongshu subject/community rules: https://top.xiaohongshu.com/fe/toph5/rules/subject
- Xiaohongshu creator center: https://creator.xiaohongshu.com/
- Xiaohongshu help center: https://pgy.xiaohongshu.com/faq
- Douyin user agreement: https://www.douyin.com/draft/douyin_agreement/douyin_agreement_user.html?id=6773906068725565448
- Douyin open-platform operation rules: https://open.douyin.com/platform/resource/docs/operation-standard/agreement-protocol
- Bilibili open-platform documents: https://open.bilibili.com/doc
- Bilibili developer service agreement: https://open.bilibili.com/agreement/developer-service

## Interpretation

There is no reliable, complete, permanent public list of “all prohibited words”. Official rules are the authority; third-party lexicons and moderation models are triage aids. `content-compliance-checker` is a useful high-recall detector but may flag ordinary words and is not an official XHS/Douyin/Bilibili checker. General safety models such as Qwen3Guard can be considered for a later semantic triage experiment, but they are not installed by this skill and do not replace platform review or human judgment.

Treat the following as review triggers: absolute/exclusive/guaranteed claims, medical/financial/employment promises, unsupported authority or ranking, fabricated experience, privacy exposure, copyright uncertainty, competitor attacks, off-platform diversion, forced engagement, and attempts to evade detection. A review trigger is not automatically a violation; inspect the surrounding claim and evidence.
