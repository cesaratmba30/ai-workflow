---
name: writing-great-skills
description: How to author new skills well. Use when creating or revising any skill/slash command — "write a skill for X", "improve this skill", "why isn't this skill triggering". Covers context-vs-cognitive load, progressive disclosure, and the known failure modes of skill prose.
---

# /writing-great-skills — authoring discipline

A skill is a reusable, versioned "play". Badly written skills either never trigger, bloat every session's context, or rot into stacked caveats. These rules prevent that.

## Context economics (the governing constraint)

- **The description is always-loaded; the body loads on trigger.** Spend the description budget on WHEN to trigger (verbs, trigger phrases, situations), not on how the skill works.
- **Progressive disclosure:** main SKILL.md holds the method; heavy reference material (format templates, long checklists, report skeletons) goes in sidecar files the skill points to, read only when needed.
- **Short beats complete.** Every line costs attention on every invocation. If a section wouldn't change the agent's behaviour, cut it.

## Structure that works

1. **Frontmatter:** `name` + a description that starts with what it does, then explicit trigger conditions ("Use when…", including the exact phrases users say).
2. **One-paragraph WHY** at the top — the failure the skill exists to prevent. An agent that knows why complies better than one following steps blindly.
3. **Numbered method** — steps in execution order, each starting with a verb.
4. **The bar / rules** — the non-negotiables, stated as testable assertions ("the test goes red if the fix is reverted"), not vibes ("write good tests").
5. **Output contract** — what the skill returns, so the caller knows when it's done.

## Failure modes to design against

- **Trigger miss:** description describes the domain, not the situations. Fix: name user phrasings and moments.
- **Cognitive overload:** the skill tries to teach everything; the agent skims and misses the load-bearing rule. Fix: one method per skill; split or sidecar the rest.
- **Caveat accretion:** lessons appended as exceptions until nothing is load-bearing. Fix: REPLACE wording when a lesson lands; rewrite the step, don't annotate it.
- **Tautological instructions:** "ensure quality", "be careful". If it can't fail a test, it isn't an instruction.
- **Prose doing a tool's job:** if the rule can be a script/hook/CI check, make it one and let the skill point at it (tool > test > prose).

## When revising an existing skill

Diagnose which failure mode occurred, fix by rewriting the smallest section, and state what changed — never silently rewrite a standing instruction.
