---
name: skill-adopt
description: Intake pipeline for NEW skills — whether authored from scratch or adopted from a third party (a repo, a marketplace, a colleague's zip). Use when adding any skill to this collection — "add this skill", "adopt this skill from GitHub", "incorporate this skill", "create a new skill for the repo". Ensures every skill enters with the same rigor - atomicity, metadata, evals - regardless of origin. Do NOT use for revising an existing in-repo skill (writing-great-skills + skill-eval).
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: optional
  concurrency: single
  atomic: false
  composes: [writing-great-skills, skill-eval]
---

# /skill-adopt — same rigor, any origin

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: optional
>
> **Concurrency:** Single-thread pipeline per skill; multiple candidate skills may be adopted in parallel subagents, one pipeline each.

A collection stays trustworthy only if every entrant clears the same bar. Skills written in-house get discipline from `/writing-great-skills`; skills pulled from the ecosystem (47k+ exist, almost none tested) get none — unless this pipeline runs. No skill lands in `skills/` without completing ALL steps.

## The pipeline (in order, no skips)

1. **Provenance & safety read.** Read the ENTIRE skill — body, scripts, references. Flag anything that executes code, fetches URLs, or writes outside the workspace; a skill is a prompt-injection surface. Record origin (URL/author/license) in the frontmatter or a `PROVENANCE` note.
2. **Fit check.** Does it overlap an existing skill? Overlap → merge into the existing skill or reject; never ship two skills that trigger on the same prompts (they'll fight). Check the lifecycle map in README for where it belongs.
3. **Atomicity check.** Multi-phase skill? Split into atomic sub-skills + a thin orchestrator (see the resume/storm-research pattern). Each atomic piece must be independently invocable.
4. **Rewrite to house style** via `/writing-great-skills`: description with triggers AND negative triggers, one-paragraph why, directive rules, output contract, under 500 lines, sidecar heavy material.
5. **Add the metadata block** (see MODELS.md): `engine` tier, `claude:`/`openai:` model+effort, `subagent:` stance, `concurrency:` (parallel-fanout / parallel-ok / single / single-wait / interactive / orchestrator), `atomic:`/`composes:`. Mirror it in the body `> Engine:` / `> Concurrency:` lines.
6. **Eval before ship** via `/skill-eval`: prompt set in `evals/prompts/<name>.json` (positives, negatives, edges), checks registered in `evals/checks.py`, 3–5 trials, run on BOTH platforms (claude + codex). No eval, no merge.
7. **Register:** add to README's skill table/lifecycle map and bump `plugin.json`. Update AGENTS.md if the skill needs a translation note.

## Output

The landed skill directory, its eval artifacts, the registry diffs (README/plugin.json/AGENTS.md), and a one-line adoption record: origin → what changed in intake → eval pass rate.
