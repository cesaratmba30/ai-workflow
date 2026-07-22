---
name: simplify
description: Quality-only cleanup pass over a settled diff. Use after review findings are resolved and before final verification — "simplify this diff", "clean up the change". Hunts reuse, dead code, duplication, and over-complication, and APPLIES the fixes. Do NOT use to hunt bugs (code-review-pass) or restyle/rename for taste.
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: recommended
  concurrency: single-wait
  atomic: true
---

# /simplify — clean the shape of the settled diff

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: recommended
>
> **Concurrency:** Single-thread gate on the settled diff; wait for review findings to resolve first.

Separating "find the bugs" (code review) from "clean the shape" (this pass) keeps each pass focused. Simplify runs on the *settled* diff — after review findings resolve — so it isn't cleaning code the review is still changing. Skipped for a trivial one-liner.

## What to hunt (in the diff and its immediate blast radius)

1. **Missed reuse** — the change reimplements something an existing helper/module already does. Call the existing one.
2. **Dead code the change created** — now-unused imports, variables, functions, branches orphaned by the change. Remove them. (Pre-existing dead code: flag it; remove only when verifiably unused and safe; escalate risky removals.)
3. **Duplication** — the same logic landed in two places; extract or point both at the single source of truth.
4. **Redundant guards** — conditions already guaranteed by the caller or an earlier check.
5. **Over-complication** — needless indirection, premature abstraction, a config knob nothing sets, a class where a function does.
6. **Scaffolding remnants** — debug prints, commented-out code, TODO husks from the build.

## Rules

- **Behaviour-preserving only.** Every edit must leave observable behaviour identical; the suite is the referee — re-run it after applying.
- **Applies its fixes** (that's the point), but edits are shown for reading before acceptance; on a tripwire seam, each edit is individually verified behaviour-preserving and the suite re-run.
- Not a restyle pass: no renames-for-taste, no reformatting beyond the changed lines.
- A true quality finding with zero runtime impact still gets fixed — "cosmetic" is not a dismissal.

## Output

The applied cleanup diff, a one-line-per-edit summary (what + why), and the fresh suite result.
