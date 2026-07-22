# Eval results

Status as of v0.3.1. This file is the committed record the v0.3.0 review asked
for: real run output, not just "the harness exists."

## Harness fixes verified live

`evals/run_evals.py` was fixed and smoke-tested against a real `claude` CLI
in this environment:

- **Exit-code handling**: confirmed live. A `claude -p` subprocess that exits
  nonzero (observed here: an unauthenticated CLI returning `Not logged in`,
  exit 1) is now reported as `ERROR nonzero exit (1)` and excluded from the
  pass/fail tally, instead of the previous behavior of scoring whatever
  partial stdout came back.
- **Missing CLI handling**: confirmed live against `--agent codex` (codex CLI
  not installed here) — reported cleanly as `codex CLI not found on PATH`,
  no misclassification.
- **`--judge`**: implemented (`run_judge` in `run_evals.py`); three prompt
  sets (`roast`, `code-review-pass`, `grill`) carry real `judge_criteria` as
  a working example. Not yet exercised end-to-end against a live model (see
  below).

## Full multi-trial suite: in progress

The `claude` CLI was authenticated (`claude /login`) after this pass started.
`python evals/run_evals.py --agent claude --all --trials 3 --judge` is now
running in the background (logging to `evals/results/claude-v0.3.1-raw.txt`)
against the repo state *after* the code-review-pass fixes below — an earlier
run was deliberately killed and restarted once those fixes landed, since it
had started reading `evals/prompts/*.json` before the negative-case fix was
applied and would have produced results for a stale prompt set. Real
multi-trial pass rates will be committed here once it completes (see
[BOARD.md](../BOARD.md) card `#9`, [GitHub issue #9](https://github.com/cesaratmba30/ai-workflow/issues/9)).

**Known open question, not yet verified either way:** `build_cmd` passes
`--max-turns 12`. It is not yet confirmed whether the `claude` CLI returns a
nonzero exit code on hitting that turn limit (as opposed to a clean
truncated-but-successful response). If it does, the new exit-code check
would misclassify a legitimately-triggered-but-truncated run as a hard
error rather than a scoreable case. Watch the live run's error rate for
cases that plausibly needed >12 turns; if errors cluster there, the fix is
either raising `--max-turns` or distinguishing that specific exit condition.

## Codex results: not yet run

The `codex` CLI is not installed in the environment this v0.3.1 pass was done
in, so no Codex-side trials could be run either. The runner's `--agent codex`
path is implemented and was exercised for its error path (missing CLI); it
has not been exercised against a live Codex CLI. `nightly-evals.yml` does not
yet have a Codex job — add one (install the codex CLI, pass `--agent codex`,
gate on an appropriate secret) once Codex CI access is available.

## code-review-pass on commit 6a0752f

Run per this repo's own `/code-review-pass` method (fresh subagent, adversarial,
two axes, "is it TRUE?" triage) against the full v0.3.1 diff. All 4 findings
were independently re-verified before being accepted, then fixed:

- **should-fix**: `install.ps1`'s already-correct check compared destination
  files by *filename only* (`Compare-Object -Property Name`), so a skill
  whose content changed but kept the same filenames would be silently
  reported as already up to date and skipped. Fixed to hash file contents
  (SHA-256, relative path + hash) like `install.sh`'s `diff -rq` already did.
- **should-fix**: 8 of the 38 negative-case fixes (`architecture-survey`,
  `citation-check`, `domain-modeling`, `persona-attack`, `roast-judge`,
  `skill-eval`, `test-stabilizer`, `work-routing`) still paired the exact
  original CSV-script + vendor-email prompts verbatim — a bug in the
  rotation formula (`(2·idx, 2·idx+1) mod 10` landed on pool positions
  `(0,1)`, which *were* the original pair, whenever `idx mod 5 == 0`). Fixed
  by reordering the prompt pool so those two items are never adjacent, then
  regenerating and verifying no file pairs them together.
- **nit**: both installers reported `Installed N skill(s)` under `--dry-run`
  even though nothing was written. Fixed to say `Would install N` in dry-run
  mode.
- **nit**: `nightly-evals.yml` interpolated `${{ secrets.ANTHROPIC_API_KEY }}`
  directly into an inline `run:` shell test rather than passing it via `env:`
  — low blast radius (the value is owner-controlled, not attacker-controlled)
  but not the safe pattern GitHub recommends. Fixed to route through `env:`.

All 4 fixes verified: negative-case fix confirmed programmatically (no file
pairs the original prompts), `install.sh` dry-run relabeling re-verified live,
`install.ps1` and the workflow YAML changes verified by manual review only
(no `pwsh`/`actionlint` in this environment — same limitation as the original
v0.3.1 pass).

## simplify pass on the settled diff

Ran per `/simplify`'s method (reuse / dead code / duplication / over-
complication, behaviour-preserving only) after the review findings above were
resolved. No fixes applied: `build_cmd`'s claude/codex branches in
`evals/run_evals.py` duplicate a few lines (skill-copying, agent dispatch),
but that duplication is pre-existing and outside this diff's blast radius —
flagged, not fixed, per simplify's own rule for pre-existing issues.
`build_judge_cmd` has a structurally similar but not identical claude/codex
branch; extracting a shared helper was considered and rejected — the actual
differences (skill-copying, `--max-turns`, `--skip-git-repo-check`) would
make a shared abstraction more indirection than the two call sites it saves.
No dead code, no missed reuse, no redundant guards found in the diff itself.

## Static validation: passing

`python scripts/validate.py` passes for all 38 skills (frontmatter shape,
metadata fields, compose-link integrity, eval-prompt wiring, negative-case
minimums). This is necessary but not sufficient evidence of "eval-ready" —
it checks that the harness is wired correctly, not that skills actually
behave correctly under it. Treat it as the fast CI gate, and the live runs
above as the actual behavioral evidence.
