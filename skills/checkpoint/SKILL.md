---
name: checkpoint
description: Lightweight durability pass — push what's landed, sync the board, note where things stand. No land-or-park ceremony, no glossary/decisions-log sweep. Use after each landed build-cycle item, immediately after launching any long-running background process, or whenever interruption risk is elevated (approaching a context ceiling, a long external wait ahead). Composed by resume (per item) and handoff (as its board+status step). Do NOT use for a full session-end wrap-up (handoff) or to create new issues (to-issues).
metadata:
  engine: fast
  claude: claude-haiku-4-5 (low)
  openai: gpt-5.6-luna (low)
  subagent: recommended
  concurrency: single
  atomic: false
  composes: [board-sync]
---

# /checkpoint — durability, not ceremony

> **Engine:** fast — Claude `haiku-4.5` (low) · OpenAI `gpt-5.6-luna` (low) · Subagent: recommended (mechanical). This is a fixed-order, zero-decision composition — unlike `resume`/`handoff`/`triage`, it never reasons about which path to take, so it runs at its composed piece's own tier rather than `balanced` (see MODELS.md routing rule 4).
>
> **Concurrency:** Single-thread, strictly sequential: push, then board-sync, then note. No fan-out, nothing to join.

`/session-state-load` reads the truth in a fixed order so nothing is skipped; this is its write-side counterpart. The moment of highest risk is exactly the one you don't see coming — a usage limit, a killed process, a power cut. Waiting for a deliberate "wrap up" to make state durable means the loss window is however long the session happened to run. Checkpoint exists to make that window small, by being cheap enough to run often.

**This is a durability action, not a quality gate.** It doesn't run tests, review anything, or decide if work is good — it preserves whatever has already been decided to be good. If nothing has landed since the last checkpoint, that's a fine, common result.

## Method (always, in this order)

1. **Push what's landed.** If there is a complete, coherent, already-decided chunk sitting uncommitted (not mid-edit, not broken), commit it first — small and honest, never a forced or partial commit just to have something to push. Work still genuinely in progress is left exactly as it is; checkpoint does not rush it to a decision.
   - **On a dedicated working/feature branch** (not the repo's shared default branch): commit and push freely, no need to ask each time. Nobody else is affected, nothing merges, and it's exactly the durability job this skill exists for.
   - **On the shared default branch directly** (no feature branch in use): commit locally — that alone protects against losing uncommitted work — but do not push without the owner's go-ahead. Note it instead ("N commits ready to push, waiting on you").
   - Opening or merging a PR into the default branch is never checkpoint's call, on either branch — that's still the owner's, same as before.
2. **Sync the board.** Run `/board-sync`.
3. **Note where things stand.** Only if genuinely mid-task: ONE line — where things stand, next action. Not a diary. Skip this line entirely when there's nothing usefully different from the last note.

## Rules

- **Bias toward running it.** It's cheap enough that an unnecessary run costs almost nothing; the failure mode this exists to prevent — losing real work to an unannounced cutoff — is worse than one extra no-op pass.
- **Never the land-or-park ceremony.** That question ("is this done or abandoned?") belongs to `/handoff` at a genuine stopping point. Checkpoint never asks it.
- **Never the glossary/decisions-log sweep.** Durable-ruling and vocabulary work is judgment work with its own cadence (`/domain-modeling`), not something to force on every pass. `/handoff` still owns that step for real session ends.
- **No new judgment calls.** If something surfaces that genuinely needs one (a synonym drifted, a real decision got made), name it in the note and leave it — that's `/domain-modeling` or `/handoff`'s job, not checkpoint's.

## Output

What got pushed (or "nothing to push"), `/board-sync`'s move list + drift flags, and the one-line note if there was one.
