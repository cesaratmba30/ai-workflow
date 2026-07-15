---
name: doc-audit
description: Periodic prose-drift sweep. Use every few weeks or after a heavy stretch of changes — "audit the docs", "check for stale docs", "doc cleanup". Sweeps CLAUDE.md, the memory index, and every SPEC/PLAN/RESEARCH/REVIEW doc for stale facts, redundancy, and dangling references.
---

# /doc-audit — the prose counterpart to the guard audit

The self-improvement loop only fires on loud failures; stale docs fail silently. Prose accretes and rots: one copy of a duplicated fact gets updated, the other quietly lies. This skill is the periodic sweep that catches what the loop can't.

## What to sweep

CLAUDE.md, README, the memory index + memory files, CONTEXT.md (glossary), the decisions log, every SPEC-/PLAN-/RESEARCH-/REVIEW- doc, and skill/command prose.

## What to hunt

1. **Stale facts** — claims contradicted by the code, git log, or current config (old commands, renamed files, dead feature descriptions). Verify against the source of truth, don't trust the prose.
2. **Status leakage** — "done/next" claims living in docs. Status belongs to git + the board; docs hold rationale. Delete or move.
3. **Date-stamped rot** — "as of March", "currently", "new" markers that have expired.
4. **Redundancy / single-owner violations** — the same fact or procedure owned by two files. Keep the one owner, replace the copy with a pointer.
5. **Dangling references** — links/paths to files that moved or died; pointers to sections that no longer exist.
6. **Accreted caveats** — instructions amended with stacked exceptions instead of rewritten. Rewrite clean.
7. **Bloat in always-loaded files** — CLAUDE.md carrying narrative that belongs in ARCHITECTURE.md or a path-scoped rule (target: core under ~200 lines, rules + pointers only).
8. **Consumed REVIEW docs** — point-in-time audit findings already acted on: archive them (they're finished work, never current status).

## Discipline

- Every fix REPLACES old wording; never append another caveat.
- Fixes are proposed as a batch with evidence (the contradicting source), applied on approval.
- Same cadence and spirit as `/harness-audit` (guards) and the suite-health sweep (tests): the three self-audits that keep the system honest.

## Output

A findings list grouped by file (stale / redundant / dangling / bloat), the proposed edit per finding, and the applied diff once approved.
