---
name: writing-great-skills
description: How to author new skills well. Use when creating or revising any skill/slash command — "write a skill for X", "improve this skill", "why isn't this skill triggering". Covers context-vs-cognitive load, progressive disclosure, trigger design with negative cases, model/effort declaration, and the known failure modes of skill prose. Do NOT ship the result without skill-eval.
metadata:
  engine: deep
  claude: claude-opus-4-8 (high)
  openai: gpt-5.6-sol (high)
  subagent: optional
  concurrency: single
  atomic: true
---

# /writing-great-skills — authoring discipline

> **Engine:** deep — Claude `opus-4.8` (high) · OpenAI `gpt-5.6-sol` (high) · Subagent: optional
>
> **Concurrency:** Single-thread authoring; eval runs may parallelize via skill-eval.

A skill is a reusable, versioned "play". Badly written skills either never trigger, bloat every session's context, or rot into stacked caveats. These rules prevent that. (Incorporates Philipp Schmid's authoring tips.)

## Context economics (the governing constraint)

- **The description is always-loaded; the body loads on trigger.** Spend the description budget on WHEN to trigger (verbs, trigger phrases, situations) — the what AND the when. A description rewrite alone can fix most trigger failures (~50% improvements observed).
- **Progressive disclosure:** main SKILL.md holds the method (keep under 500 lines); heavy reference material goes in sidecar files (`references/`, `scripts/`, `assets/`) read only when needed. A reference file over 500 lines gets a table of contents with line hints.
- **Short beats complete.** Every line costs attention on every invocation. If a section wouldn't change the agent's behaviour, cut it.

## Structure that works

1. **Frontmatter:** `name` + a description that starts with what it does, then explicit trigger conditions ("Use when…", the exact phrases users say), then **negative triggers** ("Do NOT use for…" — without them the skill hijacks adjacent requests). Add the `metadata` block: engine tier, claude/openai model+effort, subagent stance (see MODELS.md).
2. **One-paragraph WHY** at the top — the failure the skill exists to prevent. An agent that knows why complies better than one following steps blindly.
3. **Numbered method** — steps in execution order, each starting with a verb. But **set the right level of freedom**: describe what to achieve and the constraints, not every keystroke — if exact steps are fragile, that's a script's job, not prose ("if step 3 before step 2 breaks everything, write a script").
4. **The bar / rules** — non-negotiables as testable assertions ("the test goes red if the fix is reverted"), not vibes ("write good tests"). Use directives, not information: "Always use X" works; "X is the recommended approach" is trivia the agent won't act on. When a rule matters, say why — the why helps the agent generalize.
5. **Output contract** — what the skill returns, so the caller knows when it's done.

## Failure modes to design against

- **Trigger miss:** description describes the domain, not the situations. Fix: name user phrasings and moments.
- **Trigger hijack:** description too broad; fires on adjacent requests. Fix: negative triggers + negative eval cases.
- **Cognitive overload:** the skill tries to teach everything; the agent skims and misses the load-bearing rule. Fix: one method per skill; split into atomic sub-skills or sidecar the rest.
- **Caveat accretion:** lessons appended as exceptions until nothing is load-bearing. Fix: REPLACE wording when a lesson lands.
- **Tautological instructions:** "ensure quality", "be careful". If it can't fail a test, it isn't an instruction.
- **Prose doing a tool's job:** if the rule can be a script/hook/CI check, make it one and let the skill point at it (tool > test > prose).
- **Overfitting:** fiddly wording that only passes your three test prompts. Write for millions of invocations.

## Ship discipline

Never ship without `/skill-eval` (10–20 prompts, negatives included, 3–5 trials, both platforms). When revising an existing skill: diagnose which failure mode occurred, fix by rewriting the smallest section, state what changed — never silently rewrite a standing instruction. Periodically test for retirement: if evals pass with the skill unloaded, the model absorbed it.
