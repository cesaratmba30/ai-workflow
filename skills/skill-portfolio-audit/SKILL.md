---
name: skill-portfolio-audit
description: Govern the skill portfolio itself — decide what recurring work deserves a new skill, and audit existing skills for retirement. Use periodically or when the kit feels bloated or gappy — "audit the skills", "do we need a skill for this", "which skills earn their place". Recommends only; never installs or deletes without approval. Do NOT use to eval one skill's behaviour (skill-eval), author a skill (writing-great-skills), or intake a specific skill (skill-adopt).
metadata:
  engine: deep
  claude: claude-opus-4-8 (high)
  openai: gpt-5.6-sol (high)
  subagent: optional
  concurrency: single
  atomic: true
---

# /skill-portfolio-audit — hire and fire skills

> **Engine:** deep — Claude `opus-4.8` (high) · OpenAI `gpt-5.6-sol` (high) · Subagent: optional
>
> **Concurrency:** Single-thread governance pass; one verdict set, evidence gathering may be delegated read-only.

Skills are automation, and automation must prove its value or be removed. /harness-audit asks "do the guards still fire?"; this asks "does each skill still earn its place, and what recurring work has no owner?" Two passes, both evidence-only.

## Pass 1 — hiring (what's missing)

Review the project's goals, repeated failures, recurring chores, and existing skills. Find recurring outcomes that lack reliable ownership, a repeatable process, or proof of completion. For the strongest gaps (max 3 candidates), prefer adapting an existing skill; design new only when nothing fits. For each candidate define: trigger, inputs, authority, success check, budget, terminal states, trial plan, and retirement rule. Reject speculative, generic, duplicate, or lower-value candidates. Recommend at most one manual trial. A hired candidate enters through `/skill-adopt`, and `/skill-eval`'s `--no-skill` retirement runs feed Pass 2 evidence.

## Pass 2 — auditing (what should go)

For each existing skill, inspect its purpose, success criteria, and usage evidence (session transcripts, git history, board activity). Assign exactly one status, evidence-backed:

- **KEEP** — used, and its runs demonstrably changed outcomes.
- **PIVOT** — the need is real but the skill misses it; state the reshape.
- **RETIRE** — need has lapsed or is absorbed by another skill (or the model — see skill-eval's unloaded-eval test).
- **KILL** — actively harmful: misfires, wastes budget, or contradicts current practice.
- **INSUFFICIENT EVIDENCE** — no usage data; say what evidence would decide it.

## Terminal states

Stop when every skill has one status and the candidate shortlist is justified, or report blocked if usage evidence is unavailable. Output: portfolio scorecard, hire shortlist with evidence, KILL/RETIRE candidates with rationale. Do not install, modify, or delete anything without explicit approval.

## Attribution

Inspired by "The Loop Hiring Manager" (Eric Lott) and "The loop-auditor loop" (quigleyBits) from Forward Future's [Loop Library](https://signals.forwardfuture.com/loop-library/). Original text for this kit.
