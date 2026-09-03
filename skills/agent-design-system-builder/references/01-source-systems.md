# Source systems: what to borrow, not what to clone

This skill synthesizes reusable principles from major public design systems. It does **not** copy their visual identities or proprietary assets.

## Material Design 3 / M3 Expressive
Source: https://m3.material.io/

Borrow:
- Design as a coherent system of foundations, components, motion, and adaptive behavior.
- Use tokens so visual decisions can change coherently rather than through one-off values.
- Treat motion, shape, typography, and color as coordinated parts of the product personality.
- Build for adaptive layouts rather than only one fixed viewport.

Do not automatically make every product “Material.” The system architecture is more reusable than its specific look.

## Apple Human Interface Guidelines
Sources:
- https://developer.apple.com/design/human-interface-guidelines/
- https://developer.apple.com/design/human-interface-guidelines/design-principles

Borrow:
- Strong hierarchy: interface chrome should clarify content and action priority.
- Harmony with the target platform and device.
- Consistency with learned platform conventions.
- Accessibility, typography, layout, materials, motion, privacy, and writing are part of the design system—not afterthoughts.
- Prefer platform-native behavior when it materially improves familiarity and usability.

## Ant Design
Source: https://ant.design/docs/spec/values/

Borrow:
- “Certainty” for enterprise products: reduce subjective one-off decisions through reusable rules.
- Modular design: encapsulate common patterns and expose a small, predictable interface.
- Restraint: spend visual complexity only where it creates user value.
- Consistency across products and workflows lowers learning and coordination costs.

## IBM Carbon
Sources:
- https://carbondesignsystem.com/
- https://carbondesignsystem.com/all-about-carbon/what-is-carbon/

Borrow:
- A design system includes guidance, working code, reusable components, patterns, and design resources.
- Accessibility and inclusion are system-level requirements.
- Modularity and composability are preferable to bespoke page-specific styling.
- Design patterns should emerge from proven product usage and feed back into the shared system.
- Layering and contextual tokens are useful for theming complex surfaces.

## Microsoft Fluent 2
Sources:
- https://fluent2.microsoft.design/
- https://fluent2.microsoft.design/design-tokens
- https://fluent2.microsoft.design/layout

Borrow:
- Separate raw/global values from semantic/alias tokens.
- Naming should communicate role, not merely appearance.
- Spacing establishes grouping and hierarchy; empty space is an active design element.
- Cross-platform systems should respect platform conventions while preserving a shared identity.
- Figma variables and code tokens should map cleanly to reduce design-development drift.

## DTCG Design Tokens 2025.10
Sources:
- https://www.designtokens.org/TR/2025.10/format/
- https://www.w3.org/community/design-tokens/

Borrow:
- Use a vendor-neutral token vocabulary when starting a new system.
- Represent design decisions as named values with explicit types and aliases.
- Keep tokens interoperable across design and development tools when practical.

## Synthesis used by this skill

The shared architecture is:

**Principles → foundations/tokens → components → patterns → surfaces → QA/governance**

For AI coding agents, add one more layer:

**Approved visual reference + project contract + render/compare loop**

That final layer is essential because LLMs otherwise tend to treat a design reference as inspiration and silently normalize it toward familiar frontend patterns.
