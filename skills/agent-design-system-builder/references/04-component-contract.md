# Component contract

A reusable component is more than JSX plus styling. Document its anatomy, variants, states, behavior, and constraints.

## Required component specification

### Purpose
What task does it solve? When should it not be used?

### Anatomy
Named parts: container, label, leading icon, trailing action, helper text, etc.

### Variants
Variants should represent meaningful behavior or hierarchy—not every random visual combination.

### Sizes
Use the shared size/spacing scale. State content-density intent.

### States
At minimum where relevant:
- default
- hover
- pressed/active
- focus-visible
- disabled
- selected
- loading
- error/success/warning
- empty

### Content constraints
- label length
- truncation/wrapping behavior
- icon rules
- allowed nested content

### Responsive behavior
What reflows, hides, collapses, scrolls, or becomes a different interaction pattern?

### Accessibility
- semantic element/role
- accessible name
- keyboard behavior
- focus treatment
- announcements for async/status changes
- touch/pointer target requirements

### Tokens
List semantic/component tokens. Avoid raw style values in the component contract.

### Implementation source
Point to the canonical component path and stories/examples. An agent must search and reuse before creating another component with overlapping purpose.

## Variant discipline

When a new use case appears:
1. Can existing composition solve it?
2. Can an existing variant cover it without semantic confusion?
3. Is a new variant reusable across multiple surfaces?
4. Only then extend the shared component.

Do not encode one page’s accidental styling as a global component variant.
