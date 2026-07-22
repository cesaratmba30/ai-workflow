---
name: to-issues
description: Decompose a spec or plan into dependency-ordered, tracer-bullet board issues. Use when a PRD/spec/plan is approved and needs to become work items — "break this into issues", "populate the board", "create the user stories". Produces vertical-slice issues with explicit blocked-by dependencies. Do NOT use before the spec is approved (grill first) or to sync existing cards (board-sync).
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: recommended
  concurrency: single
  atomic: true
---

# /to-issues — spec → dependency-ordered board issues

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: recommended
>
> **Concurrency:** Single-thread: the dependency graph must be built whole; parallelism is for EXECUTING the issues, and is declared per issue.

The board is the live plan; each card carries its own rationale. This skill turns an approved spec into pickup-ready issues a future session (or a parallel agent) can execute without re-deriving context.

## Method

1. **Read the spec/PRD** (and the glossary, for canonical terms).
2. **Slice vertically — tracer bullets.** Each issue is a thin end-to-end slice that produces observable behaviour, NOT a horizontal layer ("build the data model" is wrong; "user can see X for one case, end to end" is right). Check your own output: if an issue can't be demoed or tested on its own, re-slice it. First-pass slicing drifts horizontal — self-review for this explicitly.
3. **Size to the sharp zone.** An issue should be buildable well within ~100k tokens of working context. Bigger → split.
4. **Order by dependency.** For each issue, name what blocks it and what it blocks. The dependency graph tells the execution stage what can run in parallel (disjoint, unblocked issues) and what must be sequential.
5. **Each card body carries its own rationale:** what + why (2–5 lines), acceptance criteria (testable, behavioural), the interfaces/files it's expected to touch, its dependencies, and its autonomy tier if not "supervised" (tripwire-seam issues are marked gated + plan-first).
6. **Every issue declares a `Traces:` field** naming the durable AC ID(s) it implements (see /traceability). No task without a trace; if the spec has no IDs yet, mint them first (atomic — one testable assertion per AC, split compounds before slicing).

## Destination

- **A real board** (GitHub Projects or equivalent) when available: create the issues, set dependency links, put them in Options/Ready.
- **Markdown fallback:** one file per issue (or a single BOARD.md) with the same fields.

## Output

The ordered issue list with the dependency graph (mermaid or indented text), a note on which issues are parallelizable, and any spec ambiguities discovered while slicing (those go back to `/grill`, not into guesses).
