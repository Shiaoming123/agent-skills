# Agent Design System Builder — v0.1.1

A portable Agent Skill for keeping AI-generated frontend work aligned with approved prototypes and a durable design system.

## Why this exists

Coding agents often interpret screenshots or image-generated prototypes as inspiration rather than a hard implementation contract. This skill adds a project-level design contract, token/component discipline, and a render/compare QA loop.

## Suggested Codex setup

Copy the `agent-design-system-builder` folder into your Codex skills directory or install it as part of your own skill-only plugin. Keep the reusable skill global, but copy the templates into each project as `DESIGN.md`, `VISUAL_QA.md`, and an `AGENTS.md` section.

Recommended companion capabilities:
- OpenAI `build-web-apps` plugin / `frontend-app-builder` skill for concept-to-implementation + browser QA.
- Compatible Figma design-to-code and library-generation capabilities may be used when available. Their exact names and availability depend on the current agent environment.

## Included templates

- `assets/DESIGN-template.md`
- `assets/VISUAL-QA-template.md`
- `assets/tokens-dtcg-template.json`
- `assets/AGENTS.design-system.snippet.md`

## Sources synthesized

- Google Material Design 3: https://m3.material.io/
- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Ant Design values: https://ant.design/docs/spec/values/
- IBM Carbon Design System: https://carbondesignsystem.com/
- Microsoft Fluent 2: https://fluent2.microsoft.design/
- Design Tokens Community Group 2025.10: https://www.designtokens.org/TR/2025.10/format/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

The material in this package is an original synthesis. It does not bundle or reproduce the upstream design-system documentation or proprietary assets.

## License and provenance

Copyright (c) 2026 Shiaoming123. Licensed under MIT; see `LICENSE.md`.
See `AUTHORS.md` and `PROVENANCE.md` for authorship and source boundaries.
