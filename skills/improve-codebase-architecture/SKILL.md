---
name: improve-codebase-architecture
description: Periodic architecture-deepening pass. Use when the codebase feels sloppy or hard to change, after a stretch of fast building, or when the user says "improve the architecture", "clean up the codebase structure", "modularize this". Orchestrates a read-only survey, then a human-in-the-loop grilling per accepted candidate. Do NOT use for a single known refactor (just plan and build it) or for bug hunting.
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: no
  concurrency: orchestrator
  atomic: false
  composes: [architecture-survey, grill]
---

# /improve-codebase-architecture — the deepening loop

> **Engine:** balanced orchestrator. The survey delegates to `architecture-survey` (deep, subagent); per-candidate grilling uses `grill` (interactive).
>
> **Concurrency:** Survey may shard in parallel; grilling and refactors are sequential, one candidate at a time.

Run periodically, not every session. Restructured into deep modules at clean seams, a codebase becomes easier to test, cheaper in tokens for agents to work in, and more maintainable.

## Method

1. **Survey + rank:** run `/architecture-survey` (read-only) for the ranked opportunity report.
2. **Grill per accepted candidate (human-in-the-loop):** no refactor executes from the survey alone. Each accepted candidate gets a short `/grill`: confirm the intended interface, what callers change, what must not change (behaviour-preserving contract), and the test evidence that will prove preservation.
3. **Land as normal work:** each grilled candidate becomes a board item — planned, built (tests green before and after), reviewed like any change. Behaviour-preserving means the suite is the referee: green before, green after, no test semantics weakened.

## Output

The ranked report, and board issues for accepted candidates. Never a big-bang rewrite — deepening lands as a sequence of small, verified refactors.
