---
name: citation-check
description: Verify every load-bearing citation in a briefing or document — the source exists, says what is claimed, and is current. Use before delivering any research output ("verify the citations", "check the sources"), as the final gate of storm-research. Do NOT use for code review or fact-free documents.
metadata:
  engine: fast
  claude: claude-haiku-4-5 (low)
  openai: gpt-5.6-luna (low)
  subagent: recommended
  concurrency: parallel-fanout
  atomic: true
---

# /citation-check — gate, not garnish

> **Engine:** fast — Claude `haiku-4.5` (low) · OpenAI `gpt-5.6-luna` (low) · Subagent: recommended (mechanical, parallelizable)
>
> **Concurrency:** Parallelize: citations can be checked concurrently; join before editing the document.

An unverified citation is a silent-wrongness bug in a briefing. This is a mechanical pass: fetch, compare, report.

## Method (per load-bearing citation)

1. Fetch the source. Dead link / paywall with no cached copy → **failed**.
2. Confirm the source actually supports the specific claim it backs — not just the topic. Supports-topic-but-not-claim → **failed**.
3. Check currency: if the claim is time-sensitive, confirm the source isn't superseded.

## Rules

- A claim whose citation fails is **downgraded to "unverified" or cut — never silently kept.**
- Only load-bearing citations gate delivery; decorative ones get a best-effort pass.
- Escalate to the caller only genuine judgment calls (e.g. source contradicts itself); everything mechanical is decided here.

## Output

`Citations: N checked, M verified, K failed (downgraded/cut)` plus a per-failure line: claim → source → what went wrong. The edited document with downgrades applied.
