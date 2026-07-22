# evals — don't ship skills without them

Lightweight harness per Philipp Schmid's workflow ("Don't Ship Skills Without Evals", Google DeepMind; philschmid.de/testing-skills). Deterministic checks first, LLM-as-judge only where quality is qualitative, multiple trials because agents are nondeterministic, clean environment per case, both platforms.

## Layout

- `prompts/<skill>.json` — the prompt set for one skill. Each case: `id`, `prompt`, `should_trigger`, `expected_checks` (ids from `checks.py`), optional `notes`.
- `checks.py` — the deterministic check registry (regex/section functions).
- `run_evals.py` — the runner. Adapters for `claude` and `codex` CLIs.

## Running

```bash
# All cases for one skill, 3 trials each, via Claude Code CLI
python evals/run_evals.py --agent claude --skill roast --trials 3

# Same set through Codex CLI (cross-harness check — same skill can behave differently)
python evals/run_evals.py --agent codex --skill roast --trials 3

# Everything (slow; use in CI nightly, not per-commit)
python evals/run_evals.py --agent claude --all

# Retirement test: run with skills NOT installed; if pass rate holds, retire the skill
python evals/run_evals.py --agent claude --skill tdd --no-skill

# LLM-as-judge for cases with a "judge_criteria" list (qualitative grading,
# extra CLI call per such case -- used selectively, not on every case)
python evals/run_evals.py --agent claude --skill roast --judge
```

The runner executes each prompt in an isolated temp workspace (context bleed masks failures), captures the agent's final output, checks the CLI's exit code (a nonzero exit is always a hard error and is never scored as pass or fail, even if stdout looks plausible), runs the case's deterministic checks, optionally runs the LLM judge on any case carrying `judge_criteria`, and reports pass rate per check across trials — read the distribution, not one run.

### LLM-as-judge

Deterministic regex/section checks (`checks.py`) are the default and the fast path. A case can additionally declare a `judge_criteria` list — natural-language statements that are true only if the output is actually good, not just shaped right (e.g. "the objection raised is specific to this idea, not generic boilerplate"). Judging only runs when `--judge` is passed, and only for cases that declare criteria; it fails closed (all criteria FAIL) on a judge-call error, timeout, or missing CLI, so a broken judge can never silently pass a case.

## Ground rules (from the talk)

1. Grade outcomes, not paths — don't penalize creative routes to the right answer.
2. Always include negative cases (`should_trigger: false`) — a skill that fires on everything is broken.
3. Start with 10–20 prompts drawn from real usage; every user-reported failure becomes a new case.
4. 3–5 trials per case; look at the distribution.
5. Fix the description first — most failures are trigger failures.
6. Graduate: capability evals that reach ~100% become regression evals in CI.
7. Retire: if evals pass with the skill unloaded (`--no-skill`), the model absorbed it.

## Starter sets

Each skill ships with a ~6-case starter set (3–4 positive, 2 negative, 1 edge). They are a floor, not a ceiling — extend from real usage per rule 3. Trigger detection is marker-based: each prompt file declares `trigger_markers` (regexes that appear in output only when the skill's method is actually followed).
