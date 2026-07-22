---
name: perspective-research
description: Atomic research pass from ONE named expert perspective (e.g. The Skeptic, The Historian, The Practitioner). Use when running one lane of a storm-research fan-out, or when the user asks for a single-angle deep dive ("what would a skeptic say about X", "research the history of Y"). Do NOT use for multi-angle synthesis — that is storm-research.
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: recommended
  concurrency: parallel-fanout
  atomic: true
---

# /perspective-research — one lane of the panel

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: recommended (run lanes in parallel, isolated — independence is the point)
>
> **Concurrency:** Parallelize: run all lanes as concurrent subagents; the caller JOINS (waits for every lane) before synthesis.

Single-perspective research converges on the obvious; this skill exists to hold ONE assigned angle rigorously, without contaminating or being contaminated by other lanes.

## Input contract

The caller supplies: the research question, the assigned perspective (name + one-line stance), and what decision the research feeds.

## Method

1. Generate 3–6 questions this perspective — and only this perspective — would ask.
2. Search for answers. Prefer primary sources for The Researcher, counter-evidence and post-mortems for The Skeptic, prior art and dead ends for The Historian, real-world usage and friction for The Practitioner, competing offerings and pricing for The Competitor Analyst (or the domain-fit stance assigned).
3. For every claim, record **source URL + a one-line quote/basis**. A claim without a source is marked "unsourced" inline, never silently asserted.

## Rules

- Stay in character: report what THIS angle finds, including "nothing found" — a lane that pads with generic findings poisons the synthesis.
- No cross-lane peeking; don't anticipate the synthesis.

## Output

`## Findings — <Perspective>`: the questions asked, then findings as bullets, each with source + basis line, ending with `Open questions:` for what the lane couldn't resolve.
