---
name: grill
description: Intent-elicitation interview. Use before planning any ambiguous or substantial feature, when the user says "grill me", "interview me about this idea", or hands over a rough idea/markdown brain-dump. Asks one question at a time until user and agent share one design concept, then optionally writes the glossary and decision log ("grill with docs" mode).
---

# /grill — one question at a time, until intent is truly shared

Based on Frederick Brooks' *design concept* (The Design of Design) — the shared, un-writable-down idea two designers hold — and popularized as a skill by Matt Pocock. Plan mode is "eager to create an asset": it writes a detailed plan against a *wrong assumption* and everything downstream inherits the error. Grilling closes the intent gap through dialogue FIRST. This is the hinge of the outer lifecycle: its output is the raw material for the spec.

## When

- Owner-invoked, ahead of the plan, for ambiguous or substantial work only. Skip for trivial or fully-specified changes.
- Input: whatever the owner has — a sentence, a brain-dump markdown, a prototype.

## Method

1. **Read context first.** The domain glossary (CONTEXT.md) if it exists, plus any research/prototype artifacts. Use the project's canonical terms; never invent synonyms.
2. **Interview one question at a time.** Never a questionnaire. Each question:
   - walks one branch of the design tree (scope → behaviour → edge cases → interfaces → non-goals),
   - resolves dependencies between decisions (if answer A forces choice B, surface that),
   - offers concrete options with trade-offs when the owner seems unsure.
3. **Keep going until the concept is shared.** For an ambitious feature this can be dozens of questions. Stop only when you can state the design back in the owner's own vocabulary and they confirm nothing is missing.
4. **Play back.** A compact statement of: what we're building, what we're NOT building, the key decisions and why, open risks.

## Two modes

- **grill (plain)** — the interview only; writes nothing. For a quick intent check or a non-code decision.
- **grill with docs** — additionally writes back as it goes:
  - sharpened/new terms → the domain glossary (one canonical term per concept, plus *Avoid* synonyms),
  - durable rulings → the decisions log as ADR-style entries (decision, context, trade-off).
  
  This gives future sessions the same shared language instead of the LLM inventing new abbreviations for the same thing.

## Output

The play-back summary (and in docs mode, the glossary/ADR diffs). This feeds the spec/PRD or, for small changes, goes straight to `/to-issues`.
