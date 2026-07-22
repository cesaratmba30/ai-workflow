---
name: skill-eval
description: Build and run an eval harness for an agent skill — success criteria, 10-20 prompt set with negative cases, deterministic checks, multi-trial runs, iterate on failures. Use when creating or changing any skill ("eval this skill", "test the skill", "why isn't this skill triggering", "is this skill still needed"), before shipping it. Do NOT use for evaluating application code (tdd/verify) or model choice.
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: optional
  concurrency: parallel-ok
  atomic: true
---

# /skill-eval — don't ship skills without evals

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: optional. Judge passes (LLM-as-judge) run `deep`.
>
> **Concurrency:** Cases and trials may run as parallel isolated subagents; join before scoring. Iteration on the skill text is single-threaded.

From Philipp Schmid's workflow (Google DeepMind). Skills get vibe-checked with two manual runs and shipped; you wouldn't merge code without tests. This repo's harness lives in `evals/` — extend it, don't rebuild it.

## Method

1. **Manual first.** Trigger the skill a few times with explicit invocations; watch where it breaks. Every manual fix becomes an automatable check. These runs surface hidden assumptions, not scores.
2. **Define success measurably, outcomes not paths:** *Outcome* (usable result), *Style/Instructions* (follows the skill's directives and conventions), *Efficiency* (no retries/thrashing; token cost — the most undervalued dimension). Agents find creative routes; don't penalize an unexpected route to the right answer.
3. **Prompt set (10–20):** each case declares `id`, `prompt`, `should_trigger`, `expected_checks`. Mix core capabilities, guardrails, edge cases, and **negative controls** — prompts the skill must NOT fire on. A too-broad description hijacks every request; without negatives you optimize in one direction only.
4. **Deterministic checks:** small regex/section/file-existence functions in a check registry, dispatched by `check_id`. Fast and free — prefer them.
5. **LLM-as-judge only for qualitative dimensions** (design quality, naming, structure): structured-output schema (pass/notes per dimension + score), `deep` tier, used selectively — it adds cost and latency.
6. **Run it right:** clean environment per case (context bleed masks failures); **3–5 trials per case** (nondeterminism — read the distribution, not one result); test in each harness the skill ships to (claude AND codex — same skill behaves differently per runner).
7. **Iterate description-first.** Most failures are trigger failures. Rewrite the description to match user intent (not domain terminology) and convert passive information to directives ("Always use X", not "X is recommended") before touching the body. Schmid: the description change alone fixed 5 of 7 failures (66.7% → 100%).
8. **Graduate and retire.** Capability evals that hit ~100% become regression evals. Periodically run the evals with the skill **unloaded**: if they still pass, the model has absorbed the skill — retire it.

## Output

The prompt set (`evals/prompts/<skill>.json`), any new checks in `evals/checks.py`, the run report (pass rate per check, per trial), and the iteration log (what changed, what it fixed).
