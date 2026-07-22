---
name: handoff
description: Session-end bookend. Use when wrapping up a work session, when the user says "handoff", "wrap up", "close the session", or "we're done for now". Lands or parks work (never silently), cleans remnants, syncs the board and memory, and leaves the project resumable from durable artifacts alone. Do NOT use to start a session (resume).
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: no
  concurrency: interactive
  atomic: false
  composes: [checkpoint]
---

# /handoff — session-end bookend

> **Engine:** balanced, interactive (main thread); housekeeping delegates to `checkpoint` (fast), which itself composes `board-sync`.
>
> **Concurrency:** Main thread, sequential steps; land/park decisions need the owner.

The bookend to `/resume`. The next session must resume from durable artifacts, not this chat's memory. A session that just stops leaves stale boards, stale memory, and orphaned work — the exact rot this skill prevents. `/checkpoint` covers the routine housekeeping (push, board, one-line note) that this skill would otherwise duplicate; handoff adds the parts that are genuinely session-end-only: the land-or-park decision, cleanup, and the heavier docs sweep.

## Steps (in order)

1. **Land or park — never silently.** Every piece of in-flight work is either landed (committed/merged per the project's git discipline) or explicitly parked with a note. Nothing left half-done without a written trace.
2. **Clean remnants.** Scratch files, dead experiments, orphaned worktrees (only ones both clean AND fully landed on main), stray branches the owner agreed to drop. **Background processes are a remnant only if abandoned** — if one is intentionally still running past session end (a long eval, a build), don't kill it: confirm it's actually detached (won't die with this session — check its parent isn't this session's own process tree) and that where it logs and how to check on it is written down somewhere durable (the board, the in-flight note). An intentionally-running process nobody can find again on resume is the same rot as an orphaned worktree.
3. **Checkpoint.** Run `/checkpoint`: push what's landed, sync the board, one-line note if genuinely mid-task. Covers what used to be this skill's own board-sync and in-flight-note steps.
4. **Sync heavier docs.** Update only what changed: durable rulings → decisions log, sharpened terms → glossary, stale pointers → CLAUDE.md/AGENTS.md/README. Replace old wording, never append caveats. Do NOT write status into docs — status lives in git and the board. (This is the judgment-heavy sweep `/checkpoint` deliberately doesn't do on every pass — it belongs here, at a genuine session end.)
5. **Report.** What was landed, parked, cleaned, and synced — including `/checkpoint`'s note, if it wrote one.

## Rules

- Never claim "done" for anything not verified green.
- The test of a good handoff: could a zero-context session `/resume` tomorrow and continue without reading this chat? If not, something is missing from the durable stores.
