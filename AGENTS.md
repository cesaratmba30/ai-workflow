# AGENTS.md — ai-workflow for Codex (and any Agent-Skills-compatible agent)

This repo ships 34 skills implementing a full software-agent workflow. Skills live in `skills/<name>/SKILL.md` (Agent Skills open standard). Install into `~/.codex/skills/` or `.codex/skills/` (see `scripts/install.sh`). This file is the platform-neutral equivalent of the plugin manifest: the lifecycle map, routing rules, and translation notes.

## Lifecycle

- Outer (idea → work items): `roast` → `storm-research` → `prototype` → `grill` → spec → `to-issues`
- Inner (session loop): `resume` → plan → build (`tdd`) → `code-review-pass` → `simplify` → `verify` → `handoff`
- Design & maintenance: `codebase-design`, `domain-modeling`, `improve-codebase-architecture`, `diagnosing-bugs`, `doc-audit`, `harness-audit`, `writing-great-skills`, `teach`, `skill-eval`

## Model & effort routing

Each skill's frontmatter declares `metadata.engine` (fast / balanced / deep / frontier) plus concrete `claude:` and `openai:` hints. On Codex, map tiers per `MODELS.md`: fast → `gpt-5.6-luna` low · balanced → `gpt-5.6-terra` medium · deep → `gpt-5.6-sol` high · frontier → `gpt-5.6-sol` xhigh/Max. Never run judgment skills below `deep`.

`metadata.concurrency` tells you when to parallelize: `parallel-fanout` = spawn concurrent subagents and JOIN before the next phase (research lanes, roast personas, citation checks — Codex Ultra/cloud tasks fit here); `parallel-ok` = may shard, join before writes; `single`/`single-wait` = one thread, downstream WAITS for the result (reviews, verdicts, syntheses, verification gates); `interactive` = main conversation only, wait for the human each step (grill, teach, resume, handoff); `orchestrator` = the body states which phases fan out and which are gates. When in doubt, single-thread — parallelism is an optimization, correctness gates are not.

New skills (authored or third-party) enter only via `skill-adopt`, which enforces this metadata plus evals before anything lands in `skills/`.

## Translation notes (Claude ⇄ Codex, nothing lost)

- Where a skill says **CLAUDE.md**, read/write **AGENTS.md** (this standard) instead. Same role: always-loaded project rules + pointers.
- Where a skill says **hooks / `.claude/hooks`**, use the platform's equivalent guardrails (git hooks and CI work everywhere; `harness-audit` covers whichever you have).
- Skill invocation: Claude uses `/name` or auto-trigger; Codex auto-triggers on description match, or use `$name` / "use the <name> skill". The bodies use `/name` notation — treat it as "invoke the skill named *name*".
- The "sharp zone" (~100k tokens) sizing guidance applies to any frontier model; keep slices small regardless of vendor.
- Persistent memory: Claude Cowork memory ⇄ Codex session notes — either way, durable state belongs in the board, git, the glossary (CONTEXT.md), and the decisions log, per `handoff`.

## Evals

Before shipping any skill change: `python evals/run_evals.py --agent codex --skill <name>` (or `--agent claude`). See `evals/README.md`. Prompt sets include negative cases — a skill that triggers on everything is broken.
