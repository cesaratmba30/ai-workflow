# BOARD

Markdown fallback per `/to-issues`' documented destination rule (the repo's
`gh` token lacks `project`/`read:project` scope, so no GitHub Projects v2
board is attached — cards below are the real GitHub issues at
[cesaratmba30/ai-workflow/issues](https://github.com/cesaratmba30/ai-workflow/issues)).
Columns: **Options → Ready → Building → In review → Shipped**, plus
**Blocked** for gated cards per `/board-sync`'s convention. This file is the
board of record; keep it synced with git/issue reality via `/board-sync`,
never let it silently drift.

First sync: 2026-07-22. This is the first time this repo has had a board —
see `docs/PRD-v0.3.1.md` for why (retrofit after the fact, per owner request).

Second sync: 2026-07-22, same day — [PR #16](https://github.com/cesaratmba30/ai-workflow/pull/16)
opened (`v0.3-atomic-skills-evals` → `main`). Per `/board-sync`'s own rule
("built & merged → Shipped"), these cards are **built, not yet merged** —
moved from Shipped to In review. Flagging this as the drift it is, not
silently correcting it: the first BOARD.md draft called them Shipped before
a PR existed to merge, which was premature.

Third sync: 2026-07-22, same day — PR #16 **merged** by @cesaratmba30
(merge commit `75ca2c1`). Cards #2–#8 move to Shipped for real this time.

## Shipped

| Card | Traces | Evidence |
|---|---|---|
| [#2 Restore marketplace.json](https://github.com/cesaratmba30/ai-workflow/issues/2) | FR-MKTP-01 | merged `75ca2c1` via [PR #16](https://github.com/cesaratmba30/ai-workflow/pull/16) |
| [#3 Fix eval runner correctness](https://github.com/cesaratmba30/ai-workflow/issues/3) | FR-EVAL-01 | merged `75ca2c1`, live smoke-tested |
| [#4 Diversify negative test cases](https://github.com/cesaratmba30/ai-workflow/issues/4) | FR-EVAL-02 | merged `75ca2c1` |
| [#5 Fix documentation/metadata drift](https://github.com/cesaratmba30/ai-workflow/issues/5) | FR-DOCS-01 | merged `75ca2c1` |
| [#6 Make installer non-destructive](https://github.com/cesaratmba30/ai-workflow/issues/6) | FR-INST-01 | merged `75ca2c1`, live smoke-tested |
| [#7 Add MIT LICENSE](https://github.com/cesaratmba30/ai-workflow/issues/7) | FR-LIC-01 | merged `75ca2c1` |
| [#8 Add lightweight CI workflows](https://github.com/cesaratmba30/ai-workflow/issues/8) | FR-CI-01 | merged `75ca2c1` |

## Building

| Card | Traces | Route | Note |
|---|---|---|---|
| [#9 Commit full Claude multi-trial eval results](https://github.com/cesaratmba30/ai-workflow/issues/9) | AC-EVAL-06 | inline | live run in progress (background PID, local machine), logging to `evals/results/claude-v0.3.1-raw.txt` in the working tree; will land in a follow-up PR off current `main` once done |

## Blocked

| Card | Traces | Blocked by | Autonomy |
|---|---|---|---|
| [#13 Tag and push v0.3.1](https://github.com/cesaratmba30/ai-workflow/issues/13) | AC-CI-03 | #9 | gated (owner confirms) |
| [#10 Publish Codex multi-trial results](https://github.com/cesaratmba30/ai-workflow/issues/10) | AC-EVAL-07 | codex CLI access (owner) | gated |
| [#11 Verify install.ps1 live](https://github.com/cesaratmba30/ai-workflow/issues/11) | AC-INST-02 | a `pwsh` runtime (owner) | supervised |
| [#12 Trigger nightly-evals.yml](https://github.com/cesaratmba30/ai-workflow/issues/12) | AC-CI-02 | `ANTHROPIC_API_KEY` repo secret (owner) | gated |

## Ready

| Card | Traces | Route | Autonomy |
|---|---|---|---|
| [#14 Add installer regression test](https://github.com/cesaratmba30/ai-workflow/issues/14) | AC-INST-01 | inline | supervised |
| [#15 Generalize doc/metadata checks into validate.py](https://github.com/cesaratmba30/ai-workflow/issues/15) | AC-DOCS-01, AC-DOCS-02, AC-DOCS-03 | inline | supervised |

## Options

_(empty — nothing proposed and not yet accepted onto Ready)_

---

## Drift flags

- **2026-07-22, second sync:** cards #2–#8 were placed in Shipped on first
  sync, before any PR existed. Corrected to In review (see above). Root
  cause: the retrofit pass wrote the board from commit evidence alone
  without checking merge state — a real instance of the exact drift
  `/board-sync` exists to catch, caught on the very first re-sync.

## Coverage (three honest states, per `/traceability`)

- **Verified:** 9/18 ACs
- **Implemented — test pending:** 6/18 ACs
- **Tracked debt / planned:** 3/18 ACs
- **Silent gaps:** 0

Full per-AC breakdown: [`docs/PRD-v0.3.1.md`](docs/PRD-v0.3.1.md).
