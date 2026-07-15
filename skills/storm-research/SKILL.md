---
name: storm-research
description: Adaptive expert-panel research briefing with citation verification. Use for substantial research questions — "research X", "deep dive on Y", "storm research", "what's the state of Z". Multiple expert perspectives research in parallel, findings are synthesized into a briefing, and every citation is verified before delivery.
---

# /storm-research — the expert-panel research harness

Based on the STORM method (Stanford): single-perspective research converges on the obvious; a panel of distinct perspectives, each asking its own questions, surfaces what one angle misses. Citation verification is non-negotiable — an unverified citation is a silent-wrongness bug in a briefing.

## Phase 1 — Frame

State the research question, what decision it feeds, and what "enough" looks like. Pick 4–6 perspectives suited to the question. Defaults:

- **The Researcher** — primary sources, papers, official docs.
- **The Skeptic** — counter-evidence, failed attempts, known criticisms.
- **The Historian** — how this evolved; what was tried before and why it died.
- **The Practitioner** — how people actually use/do this today; real-world friction.
- **The Competitor Analyst** — who else solves this, how, at what price. (Swap in domain-fit perspectives — e.g. The Economist, The Regulator — when the question warrants.)

## Phase 2 — Parallel research

Each perspective generates its own questions, searches for answers, and produces findings **with source URL + a one-line quote/basis per claim.** Perspectives don't share notes until synthesis (independence is the point).

## Phase 3 — Synthesis

Merge into one briefing: where perspectives agree (high confidence), where they conflict (name the conflict — do not paper over it), and what remains unknown. Structure: Executive summary → Key findings (each cited) → Disagreements & uncertainties → Implications for the decision at hand → Source list.

## Phase 4 — Citation verification (gate, not garnish)

Before delivery, re-check each load-bearing citation: the source exists, actually says what's claimed, and is current. A claim whose citation fails is downgraded to "unverified" or cut — never silently kept. Report the verification pass ("N citations checked, M verified, K cut").

## Output

The briefing document (markdown; HTML report template if the project has one). Feeds `/roast` verdicts, canon checks, and specs.
