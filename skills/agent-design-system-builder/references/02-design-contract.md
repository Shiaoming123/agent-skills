# DESIGN.md contract

`DESIGN.md` is the living design-language contract for humans and agents. It should be short enough to be read before UI work and specific enough to prevent “reasonable” but unauthorized redesign.

## Required sections

### 1. Status and evidence
- Mode: LOCKED / EXISTING / EXPLORE
- Approved references: exact file/Figma node/screenshot paths
- Last approved date or revision
- Product/surface scope

### 2. Visual thesis
One sentence describing the intended mood, material quality, density, and energy.

Bad: “modern clean SaaS.”
Good: “dense professional analysis workspace with matte neutral surfaces, sharp typography, restrained blue action accents, and almost no decorative elevation.”

### 3. Non-negotiables
Name 5–10 properties that must not drift, e.g.:
- one accent family per surface
- compact 40px data rows
- square-to-small-radius controls, not pill-heavy UI
- left rail remains visually subordinate to the canvas
- no gradients except data visualization

Budgets are easier for agents to follow than vague adjectives.

### 4. Foundations
Document sources, not duplicated values:
- token file path
- typefaces and scale
- spacing/grid
- color roles
- radius scale
- elevation/border strategy
- motion durations/easing
- icon/image language

### 5. Layout grammar
- max widths / shell behavior
- grid and gutters
- page hierarchy
- preferred alignment rules
- breakpoint behavior
- density rules

### 6. Component grammar
For each high-frequency component, name:
- source component path
- variants
- sizes
- states
- content constraints
- accessibility notes
- when not to use it

### 7. Platform/responsive adaptation
State what may change and what must remain recognizable.

### 8. Anti-patterns
Write concrete prohibited patterns:
- no arbitrary cards around every section
- no hardcoded hex colors in feature components
- no new spacing values outside the scale
- no replacing distinctive display type with generic system font
- no extra shadows to “improve separation” unless the contract permits them

### 9. Visual QA
- target routes/screens
- exact viewports
- approved screenshots
- known tolerances
- interactive states to verify

## Governance rule

A deliberate design change should update `DESIGN.md`, tokens, and affected shared components in the same change. If code differs from `DESIGN.md`, the mismatch is a defect until one source is explicitly approved as canonical.
