# Token architecture

## Default three-layer model

### 1. Primitive tokens
Raw values without product meaning.
Examples:
- `color.blue.600`
- `space.300`
- `radius.200`
- `font.size.400`

### 2. Semantic tokens
Role-based aliases that express intent.
Examples:
- `color.text.primary`
- `color.surface.canvas`
- `color.border.subtle`
- `space.content.gap`
- `radius.control`

### 3. Component tokens
Use only when a component needs a stable semantic contract beyond shared aliases.
Examples:
- `button.primary.background.default`
- `input.border.focus`

Prefer semantic tokens over component tokens when the same role is shared across components.

## Naming rules

Names should answer “what role does this value serve?” rather than “what value is it?”

Prefer:
- `color.text.muted`
- `color.action.primary.hover`

Avoid:
- `gray-500-text`
- `blue-button-hover`

## Theme rules

Themes change mappings, not token names. A component should usually reference `color.text.primary`, not branch on light/dark mode itself.

## DTCG-compatible template

The asset `assets/tokens-dtcg-template.json` uses `$type`, `$value`, and aliases. Use it when starting a new cross-tool token source. If the project already has a mature token format, do not migrate solely for theoretical purity.

## Agent enforcement

Before adding a raw value:
1. Search for an existing semantic token.
2. Search for a primitive token.
3. If neither exists, determine whether the new value is genuinely system-level or a one-off.
4. If system-level, add it at the correct layer and document the reason.
5. If one-off geometry is truly necessary (for an illustration, chart, etc.), keep it local and annotate why it is exempt.

## Minimum token families

- color: text, icon, surface, border, action, status, data visualization
- spacing: micro → section/page spacing
- typography: family, size, weight, line height, letter spacing
- radius
- border/stroke width
- elevation/shadow when used
- motion: duration and easing
- size: common control/icon dimensions where consistency matters

## Common failure

A token system is not a palette dump. If component code still selects raw “blue 600” everywhere, the agent can drift by swapping visually similar values. Semantic roles provide the behavioral contract.
