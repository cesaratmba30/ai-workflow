---
name: work-routing
description: Propose 2-4 candidate work items with a routing recommendation each — route, autonomy tier, plan-first — for the owner to pick. Use inside resume after state is loaded, or standalone when asked "what should we work on", "route this backlog", "which of these next". Do NOT use to execute the work.
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: optional
  concurrency: single-wait
  atomic: true
---

# /work-routing — the routing reflex

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: optional
>
> **Concurrency:** Single-thread: present the menu, then WAIT for the owner's pick — never start building.

The owner steers; this skill turns a loaded state packet into a small, decidable menu.

## Method

Present 2–4 candidate items from the board. For each, one line per dimension:

- **Route:** `inline` | `one subagent` | `architect → builder → reviewer` | `parallel lanes / workflow (owner opt-in)`
- **Autonomy tier:** autonomous / supervised / controlled / gated — by blast radius; tripwire seams are always gated + plan-first.
- **Plan-first?** yes for anything with blast radius; a trivial one-liner may skip straight to build.

## Rules

- Fan out to parallel lanes only when the backlog splits cleanly into disjoint file areas; solo is the common, first-class case.
- The owner picks; the pick is the first board move (Options → Ready). Never start building from this skill.

## Output

The candidate menu (2–4 items × route/autonomy/plan-first + a one-line why), and a stated recommendation.
