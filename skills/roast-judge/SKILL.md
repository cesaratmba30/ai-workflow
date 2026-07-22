---
name: roast-judge
description: Weigh a set of persona attacks on an idea and return exactly one verdict — GO / RESHAPE / KILL — plus the cheapest de-risking test. Use as the final step of a roast, or when handed existing critiques to adjudicate ("what's the verdict", "judge these attacks"). Do NOT use to generate the attacks themselves.
metadata:
  engine: deep
  claude: claude-opus-4-8 (high)
  openai: gpt-5.6-sol (high)
  subagent: optional
  concurrency: single-wait
  atomic: true
---

# /roast-judge — one verdict, no hedging

> **Engine:** deep — Claude `opus-4.8` (high) · OpenAI `gpt-5.6-sol` (high) · Subagent: optional
>
> **Concurrency:** Single-thread: requires ALL attacks complete; one judge, one verdict.

The council attacks; the Judge decides. A judgment that hedges between verdicts is a non-verdict.

## Method

1. Weigh the attacks: which are load-bearing (kill-capable) vs survivable friction. Discount attacks the idea's own evidence already answers.
2. Return **exactly one** verdict:
   - **GO** — the idea survives; note the 1–2 attacks worth monitoring.
   - **RESHAPE** — the core survives but a stated change is required; name the reshape precisely.
   - **KILL** — the idea should not be built; state the decisive reason plainly.
3. Always append **the cheapest de-risking test**: the smallest, fastest, cheapest experiment that would confirm or refute the biggest open risk (a landing page, five customer conversations, a spreadsheet model, a throwaway prototype).

## Output

The verdict line (`Verdict: GO|RESHAPE|KILL — <one-sentence reason>`), the reasoning (compact, referencing specific attacks), and the cheapest de-risking test. A GO/RESHAPE survivor lands in the board's Options column — the skill returns the verdict; a human moves the card.
