# PRD — v0.3.1 release-blocker fixes

Retroactive spec, minted after the fact. The v0.3.1 work (commit `6a0752f`)
shipped before this document existed — this repo has never dogfooded its own
`traceability`/`to-issues`/`board-sync` discipline on itself before now. This
PRD exists to close that gap: it mints the IDs the shipped work should have
traced to, and gives the outstanding follow-ups a durable home instead of
living only in chat. See `BOARD.md` for card state and `evals/RESULTS.md` for
live eval evidence.

Source: an external assessment of v0.3.0 (24→38 skill upgrade), delivered as
an unstructured list of 8 release blockers, never itself broken into issues
before implementation started.

ID grammar per `/traceability`: `<TYPE>-<DOMAIN>-<NN>`, minted once here,
inherited everywhere downstream (issues, commits, tests). Never repointed;
retired IDs are tombstoned, not reused.

---

## FR-MKTP-01 — Marketplace install path is restored and accurate

The documented `claude plugin marketplace add cesaratmba30/ai-workflow` path
must actually work.

- **AC-MKTP-01** — `.claude-plugin/marketplace.json` exists at repo root and
  is valid, parseable JSON. **Verified** — `python -m json.tool` check in
  `validate.yml` (CI, every push/PR).
- **AC-MKTP-02** — the marketplace entry's `description` states the current
  skill count. **Verified** — matches `skills/` directory count (38); no
  automated check ties this to the directory count yet, so treat as
  **implemented — test pending** if the skill count changes again before a
  check is added (see AC-DOCS-01 for the sibling case that already has one).

## FR-EVAL-01 — Eval harness produces real evidence, not just static shape

- **AC-EVAL-01** — a nonzero CLI exit code in `run_evals.py` is reported as a
  hard error and is never scored as a pass or a fail. **Verified** — live
  smoke test this session: an unauthenticated `claude` CLI (exit 1) and a
  missing `codex` CLI were both caught correctly, not silently misclassified.
- **AC-EVAL-02** — a `--judge` flag exists, is documented, and scores
  declared `judge_criteria` per case. **Implemented — test pending**: the
  code path is real (fails closed on error) and wired into 3 prompt sets
  (`roast`, `code-review-pass`, `grill`), but has not yet been exercised
  end-to-end against a live judged case (the background run in progress at
  commit time covers this — see AC-EVAL-06).
- **AC-EVAL-03** — `evals/RESULTS.md` states, per agent, exactly what has and
  has not been run, with no unqualified "evaluated" claims elsewhere in the
  repo. **Verified** — README's "evaluated" claim softened to
  "eval-harnessed" with a link to RESULTS.md.

## FR-EVAL-02 — Negative test cases are diverse, not duplicated

- **AC-EVAL-04** — no single generic-negative pair is shared by all 38 skills
  (the pre-fix state). **Verified** — 5 rotating pairs now in use, no pair
  shared by more than 8 of 38 skills (see `evals/prompts/*.json`).
- **AC-EVAL-05** — at least half of the 38 skills carry an explicit
  neighboring-skill collision negative case naming the confused skill.
  **Verified** — 18 of 38 already had one via their `edge_*` case or gained
  one (`neg_collision_*`); the other 20 already had a same-family collision
  case pre-existing (e.g. `edge_not_code_review`, `edge_close`).

## FR-EVAL-03 — Live multi-trial results are committed (tracked debt at spec time)

- **AC-EVAL-06** — a full `--agent claude --all --trials 3 --judge` run
  completes and its output is committed to `evals/results/`.
  **Tracked debt at PRD-mint time** — running in the background as of this
  writing; promotes to Verified once committed (see BOARD.md card
  `EVAL-CLAUDE-RUN`).
- **AC-EVAL-07** — an equivalent Codex run is committed. **Tracked debt,
  blocked**: the `codex` CLI is not installed in the environment this work
  was done in (see BOARD.md card `EVAL-CODEX-RUN`, blocked-by: codex CLI
  access).

## FR-DOCS-01 — Documentation and metadata are internally consistent

- **AC-DOCS-01** — every skill's declared skill count in prose (AGENTS.md,
  README) matches the actual `skills/` directory count. **Verified** —
  AGENTS.md 34→38; `scripts/validate.py` does not yet assert this specific
  cross-file count match (it only validates per-skill frontmatter shape),
  so this AC is **implemented — test pending** for regression purposes.
- **AC-DOCS-02** — every skill's `composes:` metadata list matches every
  `/skillname` invocation actually present in that skill's own body.
  **Verified** for `resume` specifically (added `board-sync` to both the
  metadata list and the body's Step 2). Not swept across all 38 skills —
  only the one instance flagged by the external review was checked and
  fixed; a full sweep is tracked debt (see BOARD.md card `DOCS-COMPOSE-SWEEP`).
- **AC-DOCS-03** — no skill declares `atomic: true` while also declaring a
  non-empty `composes:` list. **Verified** for `triage` (flagged instance,
  now `atomic: false`). `scripts/validate.py` does not assert this rule
  generally, so a regression elsewhere would not be caught — tracked debt
  (see BOARD.md card `VALIDATE-ATOMIC-COMPOSES-RULE`).

## FR-INST-01 — Installer is non-destructive and cross-platform

- **AC-INST-01** — `install.sh` never deletes an existing destination
  directory without first moving its contents to a backup path.
  **Implemented — test pending**: verified live in this session (dry-run,
  real run with a pre-seeded conflicting skill, backup content confirmed
  preserved, idempotent re-run confirmed) — but there is no committed,
  repeatable regression test asserting this, so a future edit could
  silently reintroduce the old `rm -rf` behavior undetected. Tracked debt
  (see BOARD.md card `INST-SMOKE-TEST`).
- **AC-INST-02** — `install.ps1` provides the same non-destructive contract
  for Windows/PowerShell. **Implemented — test pending**: written and
  manually reviewed (one real scoping bug found and fixed: `$script:`
  prefix on counters inside `ForEach-Object` would have silently reported
  0 installed skills), but never executed — no `pwsh` available in this
  environment. Tracked debt, blocked (see BOARD.md card `INST-PS1-VERIFY`).

## FR-LIC-01 — Repository has an explicit license

- **AC-LIC-01** — a `LICENSE` file exists at repo root naming a specific
  license and copyright holder. **Verified** — MIT, Cesar Idrovo, cross-
  referenced from CREDITS.md for upstream attributions.

## FR-CI-01 — CI validates the repo and the release is correctly tagged

- **AC-CI-01** — a CI workflow runs the static self-check on every push/PR.
  **Verified** — `.github/workflows/validate.yml`.
- **AC-CI-02** — a CI workflow can run the full multi-trial eval suite on a
  schedule, degrading gracefully without a configured secret.
  **Implemented — test pending**: workflow YAML is written and manually
  reviewed (no `pwsh`-style linter run against it — no `actionlint`
  available in this environment), but has never actually fired in GitHub
  Actions. Tracked debt (see BOARD.md card `CI-NIGHTLY-FIRST-RUN`).
- **AC-CI-03** — the release is tagged `v0.3.1` only after real eval results
  are committed. **Tracked debt by design** — tag intentionally held per
  owner instruction until AC-EVAL-06 lands (see BOARD.md card `TAG-V0.3.1`).

---

## Coverage summary (three honest states, per /traceability)

- **Verified:** AC-MKTP-01, AC-EVAL-01, AC-EVAL-03, AC-EVAL-04, AC-EVAL-05,
  AC-DOCS-02 (resume only), AC-DOCS-03 (triage only), AC-LIC-01, AC-CI-01 —
  **9**
- **Implemented — test pending:** AC-MKTP-02, AC-EVAL-02, AC-DOCS-01,
  AC-INST-01, AC-INST-02, AC-CI-02 — **6**
- **Tracked debt / planned:** AC-EVAL-06, AC-EVAL-07, AC-CI-03 — **3**
- **Silent gaps:** 0

18 ACs total. See `BOARD.md` for the card-level breakdown and
`evals/RESULTS.md` for live eval evidence as it lands.
