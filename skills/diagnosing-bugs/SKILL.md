---
name: diagnosing-bugs
description: Disciplined 6-phase loop for hard bugs and performance regressions. Use when a bug has resisted a first fix attempt, when the user says "this is a hard bug", "still broken", "diagnose this", or for any perf regression. Builds a red-capable repro FIRST and lands a regression test before the fix.
---

# /diagnosing-bugs — the 6-phase hard-bug loop

For hard bugs, the failure mode is guess-and-patch: plausible fixes stacked on an undiagnosed cause. This loop forbids fixing before reproducing, and forbids shipping without a regression test that would have caught the bug.

## Phase 1 — Capture

Write down: observed behaviour, expected behaviour, exact conditions (input, environment, frequency — always/sometimes?). Verbatim error output, no paraphrase.

## Phase 2 — Reproduce (red-capable repro FIRST)

Build the smallest deterministic reproduction that shows the bug — a failing test if possible, a script otherwise. **No fix attempts until the repro reliably goes red.** If it can't be reproduced, that's the work: add instrumentation/logging and gather data; do not "fix" what you can't see fail. A repro that can go red is what later proves the fix (it must go green) and what makes the regression test mutation-proven.

## Phase 3 — Localize

Narrow the cause: bisect (git bisect, input bisection, config bisection), differential comparison (working vs broken case), read the actual code path — never reason from memory of what the code "should" do. State the suspected cause as a falsifiable claim.

## Phase 4 — Confirm the mechanism

Prove the suspected cause *is* the cause: a targeted probe that flips the behaviour (toggle the suspect condition → bug appears/disappears). A fix based on an unconfirmed mechanism is a guess. If confirmation fails, return to Phase 3 — and if the diagnosis stalls twice, escalate to a stronger reasoning pass rather than looping.

## Phase 5 — Fix, regression test first

Turn the repro into a permanent regression test (red), then apply the minimal fix (test goes green), then run the full suite. The fix addresses the mechanism, not the symptom — no `if (weirdCase) return hack;` unless that genuinely is the mechanism.

## Phase 6 — Sweep and learn

- Search for sibling instances of the same mechanism elsewhere in the codebase.
- Lessons land as code: if a ritual or guard would have caught this earlier, add it in the SAME session (tool > test > prose).
- Report: cause → mechanism → fix → regression test, in that order.
