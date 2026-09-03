# Pressure scenarios for validating the skill

These scenarios are designed to detect common AI design drift. Run them with and without the skill and compare behavior.

## Scenario 1 — Approved screenshot vs easier implementation
Prompt: “This screenshot is approved. Implement it. You may use the current component library.”
Failure signal: Agent changes a 3-column shell to 2 columns, replaces distinctive controls with generic cards, or says the result is “inspired by” the screenshot.
Expected with skill: LOCKED mode, evidence extraction, reuse where compatible, render/compare, mismatch reporting.

## Scenario 2 — Existing design system with missing component
Prompt: “Add a bulk-action toolbar to this product.”
Failure signal: Agent invents colors/spacing and a bespoke toolbar without checking tokens/components.
Expected: EXISTING mode, audit current system, extend minimally, document reusable variant if justified.

## Scenario 3 — Vague greenfield brief
Prompt: “Build a premium analytics dashboard.”
Failure signal: Agent immediately codes generic cards without deciding a visual direction.
Expected: EXPLORE mode, 2–3 directions, lock an approved direction before broad implementation.

## Scenario 4 — Responsive temptation
Prompt: “Make the approved desktop design mobile responsive.”
Failure signal: Mobile becomes a generic default stack that loses information/action hierarchy and visual identity.
Expected: explicit responsive behavior matrix preserving hierarchy and grammar.

## Scenario 5 — Accessibility conflict
Prompt: “Match this low-contrast reference exactly.”
Failure signal: blindly reproduces inaccessible contrast or completely redesigns the page.
Expected: identify the accessibility conflict, preserve layout/aesthetic while making the smallest justified semantic-token correction and document the deviation.
