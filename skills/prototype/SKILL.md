---
name: prototype
description: Throwaway code to answer one design question. Use before writing a spec, when a design question can't be settled by argument — "prototype this", "mock this up", "let's see it before we decide". Deliberately before the spec; keep only the answer, throw away the code.
---

# /prototype — something concrete before the spec

Prototype-before-spec is the "packaging first" instinct: react to something concrete rather than to abstract prose. A prototype surfaces the real design questions the grill then sharpens, so the spec is grounded in an artifact, not a guess.

## Rules

1. **One design question per prototype.** State it up front: "Does the timeline read better as rows-per-epic or as a single lane with color?" If there are two questions, that's two prototypes.
2. **Throwaway by contract.** The code is disposable — no tests, no error handling beyond what the question needs, no production dependencies. Say so in the file header.
3. **Cheapest medium that answers the question.** A static HTML mock, a script that prints numbers, a single React file — never a mini-app.
4. **Timebox.** If the prototype grows past the point of answering its question, stop; that's the spec's job.
5. **Keep only the answer.** When the question is answered, write the answer down (1–5 lines: what was tried, what was learned, what the decision is) in the research/spec doc. Then DELETE the prototype code — or park it clearly marked `prototype/` and gitignored. Prototype code never migrates into production by "cleaning it up"; production code is rebuilt properly through the plan → build → review cycle.

## Two flavors

- **LOGIC prototype** — validates an algorithm/data question. Output: numbers, comparisons, a table.
- **UI prototype** — validates a layout/interaction question. Output: something rendered you can look at and react to.

## Output

The stated question, the artifact, and the written answer. The answer feeds `/grill` or the spec.

## Attribution

Derived from [`prototype`](https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype) in Matt Pocock's [Skills for Real Engineers](https://github.com/mattpocock/skills) (MIT). Evolved for this kit.
