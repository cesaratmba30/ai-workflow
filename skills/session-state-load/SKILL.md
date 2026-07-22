---
name: session-state-load
description: Load session state the same way every time — board, git log/status, persistent memory/project rules — and flag drift. Use at the start of resume, or standalone when asked "what's the current state", "load the project state", "where are we". Do NOT use to pick or plan work — that is work-routing.
metadata:
  engine: fast
  claude: claude-haiku-4-5 (low)
  openai: gpt-5.6-luna (low)
  subagent: recommended
  concurrency: single
  atomic: true
---

# /session-state-load — read the truth, in order

> **Engine:** fast — Claude `haiku-4.5` (low) · OpenAI `gpt-5.6-luna` (low) · Subagent: recommended (mechanical read-only sweep)
>
> **Concurrency:** Single-thread: read stores in the fixed order; do not interleave with writes.

Prose lies; `git log` + the test suite don't. This skill loads state from the durable stores in a fixed order so nothing is skipped, and reports — it never fixes.

## Method (always, in this order)

1. **The board** (issue tracker / project board / ROADMAP file — whichever single owner this project uses). Read the candidate items in Ready/Options.
2. **`git log`** (last ~10 commits) + current branch + `git status`. This is the only truthful "what's shipped".
3. **Persistent memory / always-loaded project rules** (CLAUDE.md or AGENTS.md, per platform) — durable rulings, in-flight notes from the last `/handoff`.
4. **Drift check:** any card whose column contradicts git reality (e.g. closed issue still "Building") is reported loudly, never silently fixed.

## Output

A state packet: board candidates (id + one line each), git summary (branch, last commits, dirty files), memory highlights (rulings + in-flight note), and a `Drift:` list (or `Drift: none`).
