# Approved image / Figma → code fidelity workflow

This is the critical workflow for preventing the “I approved the prototype, but the agent built something else” failure mode.

## A. Lock the reference

Record in `VISUAL_QA.md`:
- reference file/Figma node
- exact viewport/aspect ratio
- approved revision
- elements intentionally outside scope

Do not start broad implementation until the reference is unambiguous enough to compare.

## B. Extract a measurable spec

Before coding, inspect and record:
- shell dimensions and major regions
- grid, gutters, alignment anchors
- approximate spacing scale
- typography hierarchy and line lengths
- color roles and surface relationships
- radii/borders/elevation
- dominant image crop/framing
- component states visible in the reference
- density (row height, control height, information per viewport)
- motion/interaction implied by the prototype

Avoid pretending every pixel is known. Mark uncertain items as inferred.

## C. Map to reusable implementation

Create or identify:
- tokens
- shared primitives
- feature components
- layout primitives

Do not translate a reference into hundreds of unrelated magic numbers. High fidelity should come from a coherent system.

## D. Implement in descending visual importance

1. overall canvas and page geometry
2. dominant visual/content block
3. typography hierarchy
4. major component geometry
5. color/surface/border relationships
6. fine spacing
7. states and motion

This ordering prevents polishing details on a fundamentally wrong composition.

## E. Render at the target viewport

Use the strongest available visual path:
- browser screenshot for web
- simulator/preview for native UI
- Figma screenshot/context for Figma-driven work

Do not rely on source-code inspection as proof of fidelity.

## F. Compare and repair

Use a mismatch log:

| Priority | Region | Reference | Current | Fix |
|---|---|---|---|---|
| P0 | page shell | 3-column | 2-column | restore secondary rail |
| P0 | hero | 46% viewport | 30% | increase visual block |
| P1 | title | condensed display | generic sans | restore specified family |
| P2 | radius | 8px | 16px | token correction |

Fix P0 composition errors before P2 polish.

## G. Cross-viewport verification

The desktop reference is not permission to improvise mobile. Define responsive rules that preserve:
- hierarchy
- component identity
- action priority
- visual personality

## H. Completion gate

A LOCKED design is complete only when:
- target viewport comparison has no known P0 mismatch
- component/state behavior is correct
- responsive adaptation is intentional
- accessibility checks pass
- no new undocumented design language was introduced
