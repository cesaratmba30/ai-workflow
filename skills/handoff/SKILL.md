---
name: handoff
description: Session-end bookend. Use when wrapping up a work session, when the user says "handoff", "wrap up", "close the session", or "we're done for now". Lands or parks work (never silently), cleans remnants, syncs the board and memory, and leaves the project resumable from durable artifacts alone — the chat is disposable.
---

# /handoff — session-end bookend

The bookend to `/resume`. The next session must resume from durable artifacts, not this chat's memory. A session that just stops leaves stale boards, stale memory, and orphaned work — the exact rot this skill prevents.

## Steps (in order)

1. **Land or park — never silently.** Every piece of in-flight work is either landed (committed/merged per the project's git discipline) or explicitly parked with a note. Nothing is left half-done without a written trace.
2. **Clean remnants.** Remove scratch files, dead experiments, orphaned worktrees (only ones both clean AND fully landed on main), stray branches the owner agreed to drop.
3. **Sync the board.** Move every card to the column matching reality (built → In review / Shipped; abandoned → back to Options with a reason). Run a drift check: any card whose column contradicts git reality is flagged loudly, not silently fixed. Report coverage using `/traceability`'s three-state model — never binary done/not-done, and never a silent gap (an untested AC must exist as an unchecked task before the session ends).
4. **Sync memory + docs.** Update only what changed: durable rulings to the decisions log, sharpened terms to the glossary, stale pointers in CLAUDE.md/README. Replace old wording, never append caveats. Do NOT write status into docs — status lives in git and the board.
5. **In-flight note.** Only if genuinely mid-task: ONE line saying where things stand and the next action. Not a diary.
6. **Report.** Tell the owner what was landed, parked, cleaned, and synced — and the one-line note if any.

## Rules

- Never claim "done" for anything not verified green.
- The test of a good handoff: could a zero-context session `/resume` tomorrow and continue without reading this chat? If not, something is missing from the durable stores.
