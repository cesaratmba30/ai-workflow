---
name: harness-audit
description: Guard smoke-test — red-team your own guardrails. Use periodically or after changing hooks/scripts/CI — "audit the harness", "are the guards still firing", "test the hooks". Re-tests every hook, git hook, gate, and script and reports any guard that has silently stopped firing. Do NOT use for prose rot (doc-audit) or application tests (tdd).
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: recommended
  concurrency: single
  atomic: true
---

# /harness-audit — the self-improvement loop pointed at itself

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: recommended
>
> **Concurrency:** Single-thread: guard tests can interfere with each other; run sequentially.

A guard that silently stops firing is the exact failure mode this catches. Rule of thumb: prose adherence is ~80%, a hook is 100% — but only while it actually fires. Run periodically, not every session, and after any change to the harness itself.

## Method: red-team, don't inspect

For each guard, don't just read its code — **feed it the bad case it exists to block** and verify it blocks, loudly (non-zero exit / visible refusal). A guard test that never goes red proves nothing.

## The inventory to test (adapt to the project's actual harness)

1. **Agent-harness hooks** (Claude: `.claude/hooks/` + settings wiring; other platforms: their equivalent):
   - *block-unsafe-git* — attempt (dry-run/simulated) a `--no-verify` commit and a force-push; both must be blocked. `--force-with-lease` must pass.
   - *spawn guards* — attempt a builder spawn with no checkpoint file / no completion sentinel in the handoff; must be blocked.
   - *stop/verify-green guards* — introduce a deliberate lint error or artifact byte-drift in a scratch copy; the stop must be blocked.
2. **Git hooks** (`.githooks/`): pre-commit fires on a staged bad case (malformed frontmatter, script change without its tests, hand-edited generated artifact); verify `core.hooksPath` is actually configured — an unwired hook is a dead guard.
3. **CI gates**: required merge-gate present and required on the branch protection; post-merge gate publishes only on green; draft-guard skips CI on drafts.
4. **Scripts** (board moves, CI-wait, findings-pull): run each against a known input; verify real exit codes (the hand-rolled CI-wait that hung for 7 hours matching the wrong check name is the canonical failure).
5. **Wiring drift**: hooks present on disk but absent from settings; renamed scripts still referenced by old names; guards disabled "temporarily" and forgotten.

## Output

A table: guard → test performed → FIRING / DEAD / MISSING → fix. Dead guards are fixed in the SAME session (lessons land as code), and the fix itself is re-tested. Report ends with the date, so `/doc-audit` can catch a stale audit claim later.
