---
name: architecture-survey
description: Read-only survey of a codebase for deepening opportunities — shallow modules, duplicated logic, leaky/missing seams, test friction — ranked by payoff over risk. Use as phase 1-2 of improve-codebase-architecture, or standalone ("survey the architecture", "where is the codebase shallow", "find refactor candidates"). Do NOT execute any refactor — this pass changes nothing.
metadata:
  engine: deep
  claude: claude-opus-4-8 (high)
  openai: gpt-5.6-sol (high)
  subagent: recommended
  concurrency: parallel-ok
  atomic: true
---

# /architecture-survey — find the deepening opportunities

> **Engine:** deep — Claude `opus-4.8` (high) · OpenAI `gpt-5.6-sol` (high) · Subagent: recommended (read-only, context-heavy)
>
> **Concurrency:** May shard the read-only survey across subagents by directory; join before ranking.

Ousterhout applied as a sweep. A codebase built fast (especially by agents) accretes shallow modules, duplicated logic, and tangled seams. This pass finds and ranks — it never edits.

## What to hunt (using /codebase-design vocabulary)

- **Shallow modules** — interfaces nearly as large as their implementations; pass-through layers; utility grab-bags. Candidates for merging into a deep module.
- **Duplicated logic** — the same computation living in 2+ places; nominate the single source of truth.
- **Leaky seams** — callers reaching into module internals; tests that need private state; domain logic importing external systems without an adapter.
- **Missing seams** — god-files where several responsibilities tangle, making tests slow and agents confused about where things live.
- **Test friction** — behaviour testable only through heavy setup, a symptom of the wrong interface.

## Rank

For each candidate: the problem, the proposed deepening (merge X+Y behind interface Z; extract seam W), estimated blast radius, and payoff (locality / leverage / test-speed / token-cost). Rank by **payoff ÷ risk**. Quick wins first.

## Output

The ranked opportunity report (a doc/HTML report for anything substantial). No refactor executes from the survey alone — each accepted candidate goes through `/grill` and lands as a normal board item.
