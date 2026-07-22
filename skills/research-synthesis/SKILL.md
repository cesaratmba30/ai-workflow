---
name: research-synthesis
description: Merge multiple independent research lanes into one decision-ready briefing, preserving disagreements. Use when handed 2+ perspective findings to synthesize ("synthesize these findings", "merge the research"), typically as phase 3 of storm-research. Do NOT use to do new research — lanes must already exist.
metadata:
  engine: deep
  claude: claude-opus-4-8 (high)
  openai: gpt-5.6-sol (high)
  subagent: optional
  concurrency: single-wait
  atomic: true
---

# /research-synthesis — merge without papering over

> **Engine:** deep — Claude `opus-4.8` (high) · OpenAI `gpt-5.6-sol` (high) · Subagent: optional
>
> **Concurrency:** Single-thread: requires ALL lanes complete; never start on partial inputs.

Synthesis is judgment work: the value is in the conflicts, and the cheap failure is averaging them away.

## Method

1. Map agreements: where 2+ independent lanes converge → high confidence, say so.
2. Name every conflict explicitly ("The Practitioner reports X in production; The Researcher's benchmarks show Y") — never blend conflicting claims into a hedge.
3. List what remains unknown, distinguishing "no lane looked" from "looked and found nothing".
4. Tie back to the decision the research feeds: what the findings imply, and what would change the conclusion.

## Output structure (fixed)

Executive summary → Key findings (each cited, carrying the lane's source) → Disagreements & uncertainties → Implications for the decision at hand → Source list.

Citations pass through untouched — verification is `/citation-check`'s job, and it runs AFTER synthesis, before delivery.
