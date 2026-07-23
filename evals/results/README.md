# Raw eval run logs — not final results

These are raw, unprocessed logs from two live eval attempts on 2026-07-22,
preserved here (rather than left only on the machine that ran them) because
part of the data is genuinely valid and the failure pattern itself is
diagnostic. **Neither file is a clean pass-rate report** — see
`evals/RESULTS.md` for the honest, current summary. Do not cite numbers
from these files directly without reading the context below.

## `claude-v0.3.1-raw.txt`

Full `--agent claude --all --trials 3 --judge` run, started ~12:56pm PT.

- **Valid**: every case in `architecture-survey.json` through
  `domain-modeling.json` (alphabetically, the first ~13 of 39 prompt sets) —
  clean run, real signal, only 4 isolated errors total.
- **Not valid**: everything from `harness-audit.json` onward — a clean
  cutover into ~100% `nonzero exit (1)` errors for the rest of the run, with
  empty stderr. Root cause not confirmed but ruled out a broken prompt/model
  (see below); do not read a "0/3" in this range as the skill failing.

## `claude-v0.3.1-retry-tail.txt`

Retry of just the 25 files broken above, using a corrected runner
(per-skill model/effort routing — the first run had also been squandering
tokens by running every skill on `sonnet-5`/`high` regardless of its own
declared tier; fixed in PR #18). **Also broke**, same shape: clean for the
first 5 files, then 100% errored from `research-synthesis.json` onward.

## What's actually been ruled in/out

- Not a broken prompt or a runner bug in the model-routing sense — a single
  isolated retry of an exact case that failed 100% of the time in both runs
  succeeds immediately when run alone.
- Not a simple request-rate limit — 12 rapid, cheap haiku-tier calls in a
  row didn't reproduce it.
- Most likely a token/cost-based usage cap that clears after some window,
  tripped once sustained sonnet/opus multi-turn calls accumulate enough
  volume. Not confirmed with certainty — the CLI exposes no direct
  quota-status command, and reproducing it costs real money, so this wasn't
  chased further. `evals/run_evals.py` now retries a bare nonzero exit
  (3 attempts, backoff) and captures stdout on error too (was empty-stderr
  before), so the next attempt should either recover on its own for short
  blips, or at least log the CLI's actual stated reason instead of nothing.

## Next step

Re-run `python evals/run_evals.py --agent claude --only <broken-list> --trials 3 --judge`
on a machine/account where the cap (if that's what it is) isn't already hit,
or after enough time has passed. See `docs/PRD-v0.3.1.md` AC-EVAL-06 and
GitHub issue #9 for the up-to-date status.
