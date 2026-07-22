---
name: resume
description: Session-start bookend. Use at the start of any work session, or when the user says "resume", "what's next", "pick up where we left off", or "start a session". Orchestrates state loading, work routing, and the per-item build cycle after the owner picks. Do NOT use mid-session or to close a session (handoff).
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: no
  concurrency: interactive
  atomic: false
  composes: [session-state-load, work-routing, tdd, code-review-pass, simplify, verify]
---

# /resume — session-start bookend

> **Engine:** balanced orchestrator, interactive (main thread). State load delegates to `session-state-load` (fast); routing to `work-routing` (balanced); the build cycle composes `tdd`/`code-review-pass`/`simplify`/`verify` at their own tiers.
>
> **Concurrency:** Main thread, owner in the loop. Build-cycle steps run sequentially; parallel builder lanes only for disjoint file areas, owner opt-in.

The single entry point for a work session. One ritualised entry point means state-loading happens the same way every time, so nothing is skipped. Prose lies; `git log` + the test suite don't — never trust a "done/next" claim from a doc or a previous chat.

## Step 1 — Load state

Run `/session-state-load` (board → git → memory, drift flagged loudly).

## Step 2 — Propose work

Run `/work-routing`: 2–4 candidates × route / autonomy tier / plan-first. The owner picks; the pick is the first board move (Options → Ready).

## Step 3 — Per-item build cycle (one pass, in order)

1. **Triage** — routing reflex as a gated step. Tripwire seam ⇒ plan-first + a named anti-regression test. User-facing ⇒ canon check (ground in prior art; state the match-or-exceed call in 1–3 lines).
2. **Plan** — for plan-first items: a file-level plan (approach, canon check, tripwire assessment, exact files) approved *before* a line is written. The plan IS the research step and must be airtight before any handoff to a builder — no mid-build course-correction.
3. **Build + tests in one change** — vertical slices sized to the model's sharp zone (~first 100k tokens); quality degrades past that. Test-first per `/tdd` (balanced tier).
4. **Suite green + lint** — state the result ("Tests: N pass"). Never claim done without it.
5. **Adversarial review** — `/code-review-pass` (deep tier). The deciding question on any finding: "is it TRUE?", never "does it change runtime?".
6. **Simplify** — `/simplify` on the settled diff (balanced tier).
7. **Verify by RUNNING it** — `/verify`. Green tests prove logic, not that it renders/runs.
8. **Decision packet** — one screen: 2–4 line diff summary + seam touched, test delta, verification evidence. The owner steers; they never read diffs.

## Rules

- Parallel builder lanes only when the backlog splits into disjoint file areas; solo is first-class.
- Commit/push only when the owner asks. Batch a coherent chunk into ONE PR.
- End the session with `/handoff`, never by just stopping.
