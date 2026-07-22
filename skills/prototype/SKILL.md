---
name: prototype
description: Throwaway code to answer one design question. Use before writing a spec, when a design question can't be settled by argument — "prototype this", "mock this up", "let's see it before we decide". Deliberately before the spec; keep only the answer, throw away the code. Do NOT use to build production features or anything that will be kept.
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: recommended
  concurrency: parallel-ok
  atomic: true
---

# /prototype — something concrete before the spec

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: recommended (isolated scratch context)
>
> **Concurrency:** Independent questions may prototype in parallel subagents; one question per prototype still holds.

Prototype-before-spec is the "packaging first" instinct: react to something concrete rather than to abstract prose. A prototype surfaces the real design questions the grill then sharpens, so the spec is grounded in an artifact, not a guess.

## Rules

1. **One design question per prototype.** State it up front: "Does the timeline read better as rows-per-epic or as a single lane with color?" Two questions = two prototypes.
2. **Throwaway by contract.** The code is disposable — no tests, no error handling beyond what the question needs, no production dependencies. Say so in the file header.
3. **Cheapest medium that answers the question.** A static HTML mock, a script that prints numbers, a single React file — never a mini-app.
4. **Timebox.** If the prototype grows past the point of answering its question, stop; that's the spec's job.
5. **Keep only the answer.** Write the answer down (1–5 lines: what was tried, learned, decided) in the research/spec doc. Then DELETE the prototype code — or park it clearly marked `prototype/` and gitignored. Prototype code never migrates into production by "cleaning it up"; production code is rebuilt properly through plan → build → review.

## Two flavors

- **LOGIC prototype** — validates an algorithm/data question. Output: numbers, comparisons, a table.
- **UI prototype** — validates a layout/interaction question. Output: something rendered you can look at and react to.

## Output

The stated question, the artifact, and the written answer. The answer feeds `/grill` or the spec.
