# Accessibility and responsive behavior

Accessibility is a design-system concern. It can justify a controlled deviation from a reference, but not an unrelated redesign.

## Baseline for web

Use WCAG 2.2 AA as the default target unless the project specifies a stronger or different standard.
Source: https://www.w3.org/TR/WCAG22/

Check:
- semantic structure
- keyboard access and logical focus order
- visible focus indication
- accessible names and descriptions
- form labels and error association
- color contrast
- non-color status cues
- reduced-motion preferences
- zoom/reflow and text resizing
- pointer/touch target size and spacing
- alternatives for drag-only interactions

## Responsive system

Define behavior, not just breakpoints.

For each major region/component, specify one of:
- retain
- reflow
- stack
- collapse
- scroll
- truncate/wrap
- move to disclosure
- replace with platform-native compact pattern

## Fidelity rule

Responsive adaptation may change geometry, but should preserve:
- information priority
- recognizable component roles
- semantic color hierarchy
- typography character
- action priority
- distinctive visual language

Avoid the common agent failure where desktop becomes a unique design but mobile falls back to a generic card stack with default spacing.
