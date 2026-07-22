---
name: bug-localize
description: Narrow a reproduced bug to its cause and prove the mechanism with a targeted probe. Use as phases 3-4 of diagnosing-bugs, or standalone when a red repro exists ("localize this", "find the root cause", "why does this fail"). Do NOT use without a reliable repro (bug-repro first), and NOT to apply the fix.
metadata:
  engine: deep
  claude: claude-opus-4-8 (high)
  openai: gpt-5.6-sol (high)
  subagent: recommended
  concurrency: single
  atomic: true
---

# /bug-localize — from symptom to confirmed mechanism

> **Engine:** deep — Claude `opus-4.8` (high) · OpenAI `gpt-5.6-sol` (high) · Subagent: recommended. If the diagnosis stalls twice, escalate to `frontier` (fable-5 / sol xhigh) rather than looping.
>
> **Concurrency:** Sequential pipeline stage: needs the red repro; complete (mechanism confirmed) before any fix.

Localization is the judgment-heavy phase; guess-and-patch happens when it's skipped.

## Phase 3 — Localize

Narrow the cause: bisect (git bisect, input bisection, config bisection), differential comparison (working vs broken case), read the actual code path — never reason from memory of what the code "should" do. State the suspected cause as a **falsifiable claim**.

## Phase 4 — Confirm the mechanism

Prove the suspected cause *is* the cause: a targeted probe that flips the behaviour (toggle the suspect condition → bug appears/disappears). A fix based on an unconfirmed mechanism is a guess. If confirmation fails, return to Phase 3.

## Output

The confirmed mechanism (cause → why it produces the symptom), the probe evidence, and the falsifiable claim trail. Hands off to `/bug-fix-regression`.
