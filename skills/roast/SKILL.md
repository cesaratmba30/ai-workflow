---
name: roast
description: Idea-validation council. Use when the user has a new product/feature idea and wants it stress-tested before committing to build — "roast this idea", "is this worth building", "poke holes in this". Orchestrates parallel persona attacks and a Judge verdict (GO / RESHAPE / KILL) plus the cheapest de-risking test. Do NOT use for reviewing code (code-review-pass) or eliciting requirements (grill).
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: no
  concurrency: orchestrator
  atomic: false
  composes: [persona-attack, roast-judge]
---

# /roast — GO / RESHAPE / KILL before any spend

> **Engine:** balanced orchestrator — attacks run `persona-attack` (balanced, parallel subagents); the verdict runs `roast-judge` (deep).
>
> **Concurrency:** Fan out the council in parallel; WAIT for all attacks; the Judge runs once, after.

An AI agent's default is to agree with you; `/roast` is the deliberate opposite, so a bad idea dies *before* it draws research or build spend. It decides **whether** to build (the grill, later, decides **what**).

## Method

1. **Input:** the owner's brain-dump — a paragraph or a page. Do quick online research first if market/competitor claims are checkable.
2. **Fan out the council:** spawn one `/persona-attack` per persona (Skeptical Customer, Competitor Analyst, Builder, Economist, Operator, Devil's Advocate — swap for domain-fit personas when warranted), parallel and isolated, each with the idea + its angle.
3. **Judge:** hand all attacks to `/roast-judge` (deep tier) for exactly one verdict + the cheapest de-risking test.

## Output

The council transcript (compact), the verdict, and the cheapest de-risking test. A GO/RESHAPE survivor lands in the board's Options column — the skill returns the verdict; a human moves the card.
