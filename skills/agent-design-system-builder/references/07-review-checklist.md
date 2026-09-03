# Adversarial design review checklist

## Contract
- Is the task mode explicitly LOCKED / EXISTING / EXPLORE?
- Are approved visual references named?
- Did any implementation decision silently alter a non-negotiable?

## Tokens
- New hardcoded colors that should be semantic tokens?
- New spacing/radius/font values outside the system?
- Do light/dark themes map semantics rather than fork components?

## Components
- Was an existing component duplicated?
- Are states and variants complete?
- Did a page-specific visual quirk leak into a global primitive?

## Visual hierarchy
- Does the same thing dominate the viewport as in the reference?
- Are major proportions, density, and whitespace relationships preserved?
- Did the agent add generic cards, pills, gradients, or shadows absent from the contract?

## Typography
- Correct family/character, scale, weight, line height, and measure?
- Did a fallback font materially alter wrapping or hierarchy?

## Interaction
- Hover/pressed/focus/disabled/loading/error states present?
- Motion supports hierarchy rather than decoration?

## Responsive
- No accidental overflow or clipped content?
- Mobile/tablet preserves hierarchy and visual grammar?
- Dense desktop surfaces adapt intentionally rather than collapse into generic stacks?

## Accessibility
- Semantic elements and labels?
- Keyboard/focus?
- Contrast/non-color cues?
- Reduced motion?
- Pointer targets?

## Visual QA
- Rendered at agreed target viewport(s)?
- P0/P1 mismatch log resolved?
- Screenshots or equivalent evidence retained when the workflow supports it?

## Completion statement

The agent should report:
- references checked
- files/tokens/components changed
- known deviations and why
- viewports/states tested
- remaining visual uncertainty
