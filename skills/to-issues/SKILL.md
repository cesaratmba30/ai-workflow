---
name: to-issues
description: Decompose a spec or plan into dependency-ordered, tracer-bullet board issues. Use when a PRD/spec/plan is approved and needs to become work items — "break this into issues", "populate the board", "create the user stories". Produces vertical-slice issues with explicit blocked-by dependencies.
---

# /to-issues — spec → dependency-ordered board issues

The board is the live plan; each card carries its own rationale. This skill turns an approved spec into pickup-ready issues a future session (or a parallel agent) can execute without re-deriving context.

## Method

1. **Read the spec/PRD** (and the glossary, for canonical terms).
2. **Slice vertically — tracer bullets.** Each issue is a thin end-to-end slice that produces observable behaviour, NOT a horizontal layer ("build the data model" is wrong; "user can see X for one case, end to end" is right). Check your own output: if an issue can't be demoed or tested on its own, re-slice it. It's known that first-pass slicing drifts horizontal — self-review for this explicitly.
3. **Size to the sharp zone.** An issue should be comfortably buildable in one pass — as a rough guide, well within ~100k tokens of working context. Judge this by observable shape, not a token count: if the issue spans more than a handful of files or reads more like an epic than a task, split it; the builder will further slice internally, but the issue boundary should already be small.
4. **Order by dependency.** For each issue, name what blocks it and what it blocks. The dependency graph tells the execution stage what can run in parallel (disjoint, unblocked issues) and what must be sequential.
5. **Each card body carries its own rationale:** what + why (2–5 lines), acceptance criteria (testable, behavioural), the interfaces/files it's expected to touch, its dependencies, and its autonomy tier if not "supervised" (tripwire-seam issues are marked gated + plan-first).
6. **Every issue declares a `Traces:` field** naming the durable AC ID(s) it implements (see /traceability). No task without a trace; if the spec has no IDs yet, mint them first (atomic — one testable assertion per AC, split compounds before slicing). This is what lets a gate later refuse "done" without a test naming that AC.

## Destination

- **A real board** (GitHub Projects or equivalent) when available: create the issues, set the dependency links, put them in Options/Ready.
- **Markdown fallback:** one file per issue (or a single BOARD.md) with the same fields, if no tracker is connected.

## Output

The ordered issue list with the dependency graph (mermaid or indented text), a note on which issues are parallelizable, and any spec ambiguities discovered while slicing (those go back to `/grill`, not into guesses).

## Attribution

Derived from [`to-issues`](https://github.com/mattpocock/skills/tree/main/skills/engineering/to-issues) in Matt Pocock's [Skills for Real Engineers](https://github.com/mattpocock/skills) (MIT). Evolved for this kit.
