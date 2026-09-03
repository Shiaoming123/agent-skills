---
name: agent-design-system-builder
description: Use when an AI coding agent must create, document, preserve, or implement a product UI from an approved image, Figma design, existing codebase, or emerging design language without visual drift.
version: 0.1.0
---

# Agent Design System Builder

## Core principle

Treat approved design decisions as a **contract**, not inspiration. Separate design exploration from implementation. Once a design is approved, implementation may adapt only for explicit responsive, accessibility, or platform constraints; it must not silently restyle the product.

## First classify the task

Choose exactly one mode before editing UI:

1. **LOCKED** — an approved screenshot, image, Figma frame, prototype, or explicit visual spec exists. Preserve it.
2. **EXISTING** — a codebase already has tokens/components/patterns. Audit and document before extending.
3. **EXPLORE** — no approved direction exists. Propose 2–3 coherent directions, get approval, then lock one.

If uncertain, prefer EXISTING over inventing a new language.

## Required project artifacts

Before broad UI implementation, create or update:

- `DESIGN.md` — product-level visual and interaction contract.
- a token source of truth — existing token file, or a DTCG-compatible token file when starting fresh.
- `VISUAL_QA.md` — approved references, target viewports, and acceptance checks.
- project agent rules (`AGENTS.md`, `CLAUDE.md`, or equivalent) that link to `DESIGN.md` in one hop.

Use `assets/DESIGN-template.md`, `assets/tokens-dtcg-template.json`,
`assets/VISUAL-QA-template.md`, and the agent-rules snippet in `assets/`.

## Mandatory workflow

1. **Audit evidence first.** Read existing UI, token files, component library, screenshots/Figma, and agent rules. Never describe invented rules as existing facts.
2. **Extract the contract.** Capture visual thesis, layout/grid, spacing, typography, color roles, radii, elevation, motion, imagery, responsive behavior, component states, content density, and accessibility constraints.
3. **Tokenize decisions.** Prefer primitive → semantic → component tokens. No new hardcoded color/spacing/type values when an appropriate token exists.
4. **Reuse before creating.** Search existing components and variants before adding new primitives.
5. **Implement one surface at a time.** Preserve hierarchy, geometry, density, typography, asset framing, states, and interaction model.
6. **Render and compare.** Use available browser/render/screenshot tools at the target viewport. Compare against the approved reference; fix the largest visual mismatches first.
7. **Run adversarial QA.** Check responsive behavior, keyboard/focus, contrast, states, loading/empty/error, overflow, and consistency with neighboring surfaces.
8. **Update the contract.** If an approved change intentionally alters the system, update tokens/components/`DESIGN.md`; do not leave one-off CSS as hidden drift.

## Hard rules for LOCKED mode

- Do not redesign, “improve,” simplify, modernize, or substitute a different aesthetic unless requested.
- Do not change copy hierarchy, section order, dominant proportions, key colors, typography character, radii, or visual density just because another implementation is easier.
- Responsive adaptation must preserve the same visual grammar, not become a new design.
- If the reference is ambiguous, list the ambiguity and choose the smallest plausible deviation.
- Do not declare completion from code inspection alone when rendering is available.

## Read next

- System synthesis: `references/01-source-systems.md`
- Design contract: `references/02-design-contract.md`
- Tokens: `references/03-token-architecture.md`
- Components: `references/04-component-contract.md`
- Image/Figma → code fidelity: `references/05-visual-fidelity-workflow.md`
- Accessibility/responsive: `references/06-accessibility-responsive.md`
- Review checklist: `references/07-review-checklist.md`
