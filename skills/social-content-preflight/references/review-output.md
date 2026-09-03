# Review contract

## Input fields

```yaml
platform: xiaohongshu
content_type: note
title: ""
body: ""
script: ""
subtitles: ""
media_description: ""
tags: []
claims: []
sources: []
ai_used: false
commercial_intent: none
```

## Output fields

```yaml
verdict: REVIEW
human_confirmation_required: true
hard_risks: []
flagged_spans: []
evidence_gaps: []
account_fit: pass
platform_fit: review
recommended_rewrites: []
final_checklist:
  - factual boundaries checked
  - privacy and copyright checked
  - exact final media and copy shown to user
  - user confirmed before browser publishing
```

The accompanying Markdown should briefly explain each non-empty field. Use `BLOCK` for a hard red line, `REVIEW` when a human decision or evidence is needed, `PASS WITH REVIEW` when the draft is usable after named edits, and `PASS` only when no known issue remains while still retaining the human confirmation gate.
