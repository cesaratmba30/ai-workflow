---
name: domain-modeling
description: Active glossary and ADR discipline. Use when domain terms are drifting or ambiguous, when the user says "define our terms", "update the glossary", "record this decision", or when starting a project that needs a shared vocabulary. Owns CONTEXT.md (ubiquitous language) and the decisions log (ADRs).
---

# /domain-modeling — one canonical term per concept

From Eric Evans' Domain-Driven Design: the **ubiquitous language** — developers, the code, and domain experts share ONE vocabulary. LLMs left alone invent their own synonyms and abbreviations for the same concept ("paragraph 31"), and every synonym is a future misunderstanding. The glossary kills that; the decisions log (ADRs) stops settled rulings being re-litigated.

## The glossary (CONTEXT.md)

- **One canonical name per concept** + a one-line definition of what the term IS (never the formula — formulas live in code).
- **An *Avoid* list per term:** the synonyms that must not be used, so drift is caught rather than accreted.
- Created lazily — the first time a term matters — and sharpened continuously (by this skill and by grill-with-docs).
- Format per entry:

  ```
  ### <Canonical Term>
  <One-line definition — what it IS.>
  _Avoid:_ <synonym1>, <synonym2>
  ```

- General design/engineering vocabulary (deep module, seam, adapter) does NOT go here — that lives in `/codebase-design`. CONTEXT.md is domain terms only.

## The decisions log (ADRs)

A slot is earned only by a decision a future session would otherwise re-open or re-derive: a real fork (genuine alternatives chosen for stated reasons), costly to reverse, not obvious from the code. Each entry 1–3 sentences: **the decision, the context, the trade-off accepted.** Durable rulings ("don't re-propose X") belong here, not in chat memory.

## The pass (when invoked)

1. Sweep recent specs/plans/diffs/conversation for: new concepts without a canonical name, synonym drift, formula-in-glossary violations, decisions made but not recorded.
2. Propose glossary adds/sharpenings and ADR entries; apply on approval.
3. Replace stale wording — never append caveats to an old definition.

## Rule for every other session

Before naming any new concept, check CONTEXT.md. Use the canonical term or propose a new entry — never coin a synonym silently.

## Attribution

Ubiquitous language: Eric Evans, *Domain-Driven Design*. ADRs: Michael Nygard. Skill shape derived from [`grill-with-docs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs) in Matt Pocock's [Skills for Real Engineers](https://github.com/mattpocock/skills) (MIT). Evolved for this kit.
