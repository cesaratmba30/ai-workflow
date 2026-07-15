---
name: resume
description: Session-start bookend. Use at the start of any work session, or when the user says "resume", "what's next", "pick up where we left off", or "start a session". Loads state from the board, git, and memory the same way every time, proposes work items with a routing recommendation, and runs the per-item build cycle after the owner picks.
---

# /resume — session-start bookend

The single entry point for a work session. One ritualised entry point means state-loading (board, git, memory) happens the same way every time, so nothing is skipped. Prose lies; `git log` + the test suite don't — never trust a "done/next" claim from a doc or a previous chat.

## Step 1 — Load state (always, in this order)

1. **The board** (issue tracker / project board / ROADMAP file — whichever single owner this project uses). Read the candidate items in Ready/Options.
2. **`git log`** (last ~10 commits) + current branch + `git status`. This is the only truthful "what's shipped".
3. **Persistent memory / CLAUDE.md pointers** — durable rulings, in-flight notes from the last `/handoff`.
4. Flag any drift loudly: a card whose column contradicts reality (e.g. closed issue still "Building") is reported, not silently fixed.

## Step 2 — Propose work

Present 2–4 candidate items from the board. For each, include a one-line **routing recommendation**:

- **Route:** `inline` | `one subagent` | `architect → builder → reviewer` | `parallel lanes / workflow (owner opt-in)`
- **Autonomy tier:** autonomous / supervised / controlled / gated (by blast radius; tripwire seams are always gated + plan-first)
- **Plan-first?** yes for anything with blast radius; a trivial one-liner may skip straight to build.

The owner picks. The pick is the first board move (Options → Ready).

## Step 3 — Per-item build cycle (one pass, in order)

1. **Triage** — run the routing reflex above as a gated step. Tripwire seam ⇒ plan-first + a named anti-regression test. User-facing ⇒ re-run the canon check (ground in prior art; state the match-or-exceed call in 1–3 lines).
2. **Plan** — for plan-first items: a file-level plan (approach, canon check, tripwire assessment, exact files) approved *before* a line is written. The plan IS the research step. The plan must be airtight before any handoff to a builder — there is no mid-build course-correction.
3. **Build + tests in one change** — vertical slices sized to stay in the model's sharp zone (~first 100k tokens of context); quality degrades past that and collapses past ~400k. Test-first per `/tdd`.
4. **Suite green + lint** — state the result ("Tests: N pass"). Never claim done without it.
5. **Adversarial review** — re-validate any risky part. The deciding question on any finding: "is it TRUE?", not "does it change runtime?". True quality findings get fixed; false ones dismissed with a one-line reason.
6. **Simplify** — quality-only cleanup of the *settled* diff (reuse, dead code, duplication).
7. **Verify by RUNNING it** — drive the real artifact and look at the result. Green tests prove logic, not that it renders/runs. Screenshot for visual changes.
8. **Hand back a decision packet** — one screen: 2–4 line diff summary + seam touched, test delta, verification evidence. The owner steers; they never read diffs.

## Rules

- Fan out to parallel builder lanes only when the backlog splits cleanly into disjoint file areas; solo is the common, first-class case.
- Commit/push only when the owner asks. Batch a coherent chunk into ONE PR.
- End the session with `/handoff`, never by just stopping.
