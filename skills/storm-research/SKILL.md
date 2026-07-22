---
name: storm-research
description: Adaptive expert-panel research briefing with citation verification. Use for substantial research questions — "research X", "deep dive on Y", "storm research", "what's the state of Z". Orchestrates parallel perspective lanes, synthesis, and citation verification. Do NOT use for a quick single-fact lookup or a single-angle question (use perspective-research).
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: no
  concurrency: orchestrator
  atomic: false
  composes: [perspective-research, research-synthesis, citation-check]
---

# /storm-research — the expert-panel orchestrator

> **Engine:** balanced orchestrator — lanes run `perspective-research` (balanced, parallel subagents), synthesis runs `research-synthesis` (deep), verification runs `citation-check` (fast). Claude `sonnet-5`/`gpt-5.6-terra` for the orchestration itself.
>
> **Concurrency:** Fan out Phase 2 in parallel; WAIT for all lanes; Phases 3-4 are sequential gates.

Based on the STORM method (Stanford): single-perspective research converges on the obvious; a panel of distinct perspectives, each asking its own questions, surfaces what one angle misses.

## Phase 1 — Frame (here, in the main thread)

State the research question, what decision it feeds, and what "enough" looks like. Pick 4–6 perspectives suited to the question. Defaults: **The Researcher** (primary sources), **The Skeptic** (counter-evidence), **The Historian** (what was tried and died), **The Practitioner** (real-world friction), **The Competitor Analyst** (who else, how, at what price). Swap in domain-fit perspectives (The Economist, The Regulator) when warranted.

## Phase 2 — Fan out

Spawn one `/perspective-research` per perspective — **parallel, isolated subagents** at the `balanced` tier. Pass each: the question, its perspective, the decision context. Lanes don't share notes (independence is the point).

## Phase 3 — Synthesize

Hand all lane outputs to `/research-synthesis` at the `deep` tier. Conflicts are named, never averaged.

## Phase 4 — Verify (gate, not garnish)

Run `/citation-check` on the briefing. A claim whose citation fails is downgraded or cut — never silently kept. Report the pass ("N checked, M verified, K cut").

## Output

The briefing document (markdown; HTML report template if the project has one). Feeds `/roast` verdicts, canon checks, and specs.
