---
name: diagnosing-bugs
description: Disciplined 6-phase loop for hard bugs and performance regressions. Use when a bug has resisted a first fix attempt, when the user says "this is a hard bug", "still broken", "diagnose this", or for any perf regression. Orchestrates repro-first, mechanism confirmation, and regression-test-first fixing. Do NOT use for a fresh trivial bug a single fix attempt hasn't failed on yet.
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: no
  concurrency: orchestrator
  atomic: false
  composes: [bug-repro, bug-localize, bug-fix-regression]
---

# /diagnosing-bugs — the 6-phase hard-bug loop

> **Engine:** balanced orchestrator. Phases delegate: `bug-repro` (balanced) → `bug-localize` (deep; escalate to frontier if stalled twice) → `bug-fix-regression` (balanced).
>
> **Concurrency:** Strictly sequential phases — never parallelize repro/localize/fix; each stage waits for the previous.

For hard bugs, the failure mode is guess-and-patch: plausible fixes stacked on an undiagnosed cause. This loop forbids fixing before reproducing, and forbids shipping without a regression test that would have caught the bug.

## The loop

1. **Phases 1–2 — `/bug-repro`:** capture verbatim, build the smallest deterministic red-capable repro. No fix attempts until it reliably goes red.
2. **Phases 3–4 — `/bug-localize`:** bisect/differential/read-the-code to a falsifiable claim; confirm the mechanism with a probe that flips the behaviour. Stalls twice → escalate to a stronger reasoning pass, don't loop.
3. **Phases 5–6 — `/bug-fix-regression`:** regression test red → minimal mechanism-level fix green → full suite → sibling sweep → lessons land as code.

## Output

The final report: cause → mechanism → fix → regression test, in that order, with each phase's evidence attached.
