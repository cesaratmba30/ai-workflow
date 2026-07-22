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
  composes: [board-sync]
---

# /handoff — session-end bookend

> **Engine:** balanced, interactive (main thread); board reconciliation delegates to `board-sync` (fast).
>
> **Concurrency:** Main thread, sequential steps; land/park decisions need the owner.

The bookend to `/resume`. The next session must resume from durable artifacts, not this chat's memory. A session that just stops leaves stale boards, stale memory, and orphaned work — the exact rot this skill prevents.

## Steps (in order)

1. **Land or park — never silently.** Every piece of in-flight work is either landed (committed/merged per the project's git discipline) or explicitly parked with a note. Nothing left half-done without a written trace.
2. **Clean remnants.** Scratch files, dead experiments, orphaned worktrees (only ones both clean AND fully landed on main), stray branches the owner agreed to drop.
3. **Sync the board.** Run `/board-sync`: truthful columns, loud drift flags, three-state coverage — an untested AC must exist as an unchecked task before the session ends.
4. **Sync memory + docs.** Update only what changed: durable rulings → decisions log, sharpened terms → glossary, stale pointers → CLAUDE.md/AGENTS.md/README. Replace old wording, never append caveats. Do NOT write status into docs — status lives in git and the board.
5. **In-flight note.** Only if genuinely mid-task: ONE line — where things stand, next action. Not a diary.
6. **Report.** What was landed, parked, cleaned, synced — and the one-line note if any.

## Rules

- Never claim "done" for anything not verified green.
- The test of a good handoff: could a zero-context session `/resume` tomorrow and continue without reading this chat? If not, something is missing from the durable stores.
