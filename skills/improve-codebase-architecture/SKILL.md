---
name: improve-codebase-architecture
description: Periodic architecture-deepening survey. Use when the codebase feels sloppy or hard to change, after a stretch of fast building, or when the user says "improve the architecture", "clean up the codebase structure", "modularize this". Finds deepening opportunities, then runs a human-in-the-loop review per candidate.
---

# /improve-codebase-architecture — the deepening survey

Ousterhout applied as a periodic sweep. A codebase built fast (especially by agents) accretes shallow modules, duplicated logic, and tangled seams. Restructured into deep modules at clean seams, it becomes easier to test, cheaper in tokens for agents to work in, and generally more maintainable. Run periodically, not every session.

## Phase 1 — Survey (read-only)

Explore the codebase for **deepening opportunities**, using the `/codebase-design` vocabulary:

- **Shallow modules** — interfaces nearly as large as their implementations; pass-through layers; utility grab-bags. Candidates for merging into a deep module.
- **Duplicated logic** — the same computation living in 2+ places; nominate the single source of truth.
- **Leaky seams** — callers reaching into module internals; tests that need private state; domain logic importing external systems without an adapter.
- **Missing seams** — god-files where several responsibilities tangle, making tests slow and agents confused about where things live.
- **Test friction** — behaviour testable only through heavy setup, a symptom of the wrong interface.

## Phase 2 — Rank

For each candidate: the problem, the proposed deepening (merge X+Y behind interface Z; extract seam W), estimated blast radius, and payoff (locality/leverage/test-speed/token-cost). Rank by payoff ÷ risk. Quick wins first.

## Phase 3 — Grill per candidate (human-in-the-loop)

No refactor executes from the survey alone. Each accepted candidate gets a short grilling: confirm the intended interface, what callers change, what must not change (behaviour-preserving contract), and the test evidence that will prove preservation. Then it becomes a normal board item — planned, built (tests green before and after), reviewed like any change. Behaviour-preserving means the suite is the referee: green before, green after, no test semantics weakened.

## Output

The ranked opportunity report (a doc/HTML report for anything substantial), and board issues for accepted candidates. Never a big-bang rewrite — deepening lands as a sequence of small, verified refactors.

## Attribution

Derived from [`improve-codebase-architecture`](https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture) in Matt Pocock's [Skills for Real Engineers](https://github.com/mattpocock/skills) (MIT). Design vocabulary: John Ousterhout, *A Philosophy of Software Design*. Evolved for this kit.
