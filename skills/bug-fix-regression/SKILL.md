---
name: bug-fix-regression
description: Land the regression test first (red), apply the minimal mechanism-level fix (green), then sweep for siblings and land the lesson. Use as phases 5-6 of diagnosing-bugs once the mechanism is confirmed, or standalone ("fix it with a regression test", "land the fix"). Do NOT use before the mechanism is confirmed (bug-localize).
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: recommended
  concurrency: single
  atomic: true
---

# /bug-fix-regression — regression test first, then the fix

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: recommended
>
> **Concurrency:** Sequential pipeline stage: needs the confirmed mechanism; test-red before fix.

Shipping a fix without a regression test re-opens the door the bug walked through.

## Phase 5 — Fix, regression test first

Turn the repro into a permanent regression test (red), then apply the minimal fix (test goes green), then run the full suite. The fix addresses the **mechanism, not the symptom** — no `if (weirdCase) return hack;` unless that genuinely is the mechanism.

## Phase 6 — Sweep and learn

- Search for sibling instances of the same mechanism elsewhere in the codebase.
- Lessons land as code: if a ritual or guard would have caught this earlier, add it in the SAME session (tool > test > prose).

## Output

Report in this order: cause → mechanism → fix → regression test. Plus the suite result and any sibling findings/guards added.
