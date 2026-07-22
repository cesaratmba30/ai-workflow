---
name: bug-repro
description: Capture a bug precisely and build the smallest deterministic red-capable reproduction BEFORE any fix attempt. Use as phases 1-2 of diagnosing-bugs, or standalone ("reproduce this bug", "build a repro", "make it fail reliably"). Do NOT use to fix the bug — no fixes happen here.
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: recommended
  concurrency: single
  atomic: true
---

# /bug-repro — no fix until it fails on demand

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: recommended
>
> **Concurrency:** Sequential pipeline stage: complete (repro goes red) before bug-localize starts.

A fix without a red-capable repro is a guess. This skill's only deliverable is a reproduction that reliably goes red.

## Phase 1 — Capture

Write down: observed behaviour, expected behaviour, exact conditions (input, environment, frequency — always/sometimes?). Verbatim error output, no paraphrase.

## Phase 2 — Reproduce

Build the smallest deterministic reproduction that shows the bug — a failing test if possible, a script otherwise. **No fix attempts until the repro reliably goes red.** If it can't be reproduced, that's the work: add instrumentation/logging and gather data; do not "fix" what you can't see fail.

## Why red-capable matters

The repro that can go red is what later proves the fix (it must go green) and what makes the regression test mutation-proven.

## Output

The capture record + the repro artifact (test or script) + evidence of it going red (verbatim output). Hands off to `/bug-localize`.
