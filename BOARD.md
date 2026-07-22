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

## Shipped

| Card | Traces | Evidence |
|---|---|---|
| [#2 Restore marketplace.json](https://github.com/cesaratmba30/ai-workflow/issues/2) | FR-MKTP-01 | commit `6a0752f` |
| [#3 Fix eval runner correctness](https://github.com/cesaratmba30/ai-workflow/issues/3) | FR-EVAL-01 | commit `6a0752f`, live smoke-tested |
| [#4 Diversify negative test cases](https://github.com/cesaratmba30/ai-workflow/issues/4) | FR-EVAL-02 | commit `6a0752f` |
| [#5 Fix documentation/metadata drift](https://github.com/cesaratmba30/ai-workflow/issues/5) | FR-DOCS-01 | commit `6a0752f` |
| [#6 Make installer non-destructive](https://github.com/cesaratmba30/ai-workflow/issues/6) | FR-INST-01 | commit `6a0752f`, live smoke-tested |
| [#7 Add MIT LICENSE](https://github.com/cesaratmba30/ai-workflow/issues/7) | FR-LIC-01 | commit `6a0752f` |
| [#8 Add lightweight CI workflows](https://github.com/cesaratmba30/ai-workflow/issues/8) | FR-CI-01 | commit `6a0752f` |

## Building

| Card | Traces | Route | Note |
|---|---|---|---|
| [#9 Commit full Claude multi-trial eval results](https://github.com/cesaratmba30/ai-workflow/issues/9) | AC-EVAL-06 | inline | live run in progress, background process, logging to `evals/results/claude-v0.3.1-raw.txt` |

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

None as of this sync — first sync, board and git created from the same
retrofit pass, so nothing has had a chance to drift yet. Future syncs should
flag any card whose column contradicts git/CI/issue-state reality.

## Coverage (three honest states, per `/traceability`)

- **Verified:** 9/18 ACs
- **Implemented — test pending:** 6/18 ACs
- **Tracked debt / planned:** 3/18 ACs
- **Silent gaps:** 0

Full per-AC breakdown: [`docs/PRD-v0.3.1.md`](docs/PRD-v0.3.1.md).
