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

## Full multi-trial suite: not yet run

The full `python evals/run_evals.py --agent claude --all --trials 3` run has
**not** been executed against a live, authenticated `claude` CLI yet. The
sandbox this v0.3.1 pass was done in has the `claude` CLI on PATH but not
logged in (no `ANTHROPIC_API_KEY`, no OAuth session reachable by a spawned
subprocess), so live trials aren't possible from there.

To produce the real numbers this section should hold:

```bash
export ANTHROPIC_API_KEY=...   # or `claude /login` interactively
python evals/run_evals.py --agent claude --all --trials 3 | tee evals/RESULTS-claude.txt
```

`.github/workflows/nightly-evals.yml` runs exactly this nightly once an
`ANTHROPIC_API_KEY` repo secret is added, and its output should be pasted
into (or linked from) this file after the first green run.

## Codex results: not yet run

The `codex` CLI is not installed in the environment this v0.3.1 pass was done
in, so no Codex-side trials could be run either. The runner's `--agent codex`
path is implemented and was exercised for its error path (missing CLI); it
has not been exercised against a live Codex CLI. `nightly-evals.yml` does not
yet have a Codex job — add one (install the codex CLI, pass `--agent codex`,
gate on an appropriate secret) once Codex CI access is available.

## Static validation: passing

`python scripts/validate.py` passes for all 38 skills (frontmatter shape,
metadata fields, compose-link integrity, eval-prompt wiring, negative-case
minimums). This is necessary but not sufficient evidence of "eval-ready" —
it checks that the harness is wired correctly, not that skills actually
behave correctly under it. Treat it as the fast CI gate, and the live runs
above as the actual behavioral evidence.
