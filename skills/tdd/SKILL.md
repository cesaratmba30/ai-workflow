---
name: tdd
description: Test-first build method for agents. Use whenever building a non-trivial behaviour change — red-green in vertical slices, mutation-proven, deterministic, non-tautological. Trigger on "TDD", "test-first", or automatically as the build method inside any build cycle. Do NOT use for throwaway prototypes (prototype) or pure refactors with no behaviour change.
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: recommended
  concurrency: single
  atomic: true
---

# /tdd — test-first at our bar

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: recommended (a builder lane runs this)
>
> **Concurrency:** Single-thread within a lane: slices are sequential (red then green). Parallel lanes only for disjoint file areas.

Kent Beck's TDD, adapted for agents. Agents left alone write poor tests that are easy to pass; forcing a *failing* test first, then making it pass, produces materially better tests and better code. The feedback-loop argument (The Pragmatic Programmer): "the rate of feedback is your speed limit"; don't outrun your headlights.

## The loop (per vertical slice)

1. **Slice vertically.** One thin end-to-end behaviour per slice, not a horizontal layer. Size each slice so the working context stays in the model's sharp zone (~first 100k tokens).
2. **RED** — write the test for the slice's behaviour FIRST and run it. It must fail, for the right reason. A test that passes before the code exists is testing nothing.
3. **GREEN** — write the minimum code to pass. Run the suite.
4. **Repeat** for the next slice. Refactor only on green.

## The bar every test must meet

- **Mutation-proven:** the test goes red if the fix/feature is reverted. No test that stays green when the feature breaks. Spot-check by mentally (or actually) reverting the change.
- **Non-tautological:** expected values come from an independent source of truth — a hand-computed literal, a worked example, the spec — NEVER recomputed the way the code computes them.
- **Deterministic:** seed randomness, pin dates and fixtures, no wall-clock or network in an assertion. `expect(ms < 50)` is flaky and banned — assert behaviour or invariants, not timing.
- **Real interface:** test through the module's public seam, not its internals. Prefer interaction-based assertions (act → observe result) over static-render checks.
- **Same change:** a behaviour change lands with its test in the SAME commit/change, never "tests later".
- **Requirement-shaped:** when the work traces to an AC ID (see /traceability), the test NAME encodes it (`test_AC_USER_04_edit_role_can_modify`) and the implementing source carries `@covers AC-USER-04`. A test named after the AC must prove that AC's specific semantics — this catches the requirement-shaped hole a generic test misses.

## Done means

Suite green, stated explicitly ("Tests: N pass, M new"). Then the change proceeds to review — green tests are necessary, not sufficient (they prove logic, not that it renders/runs; that's `/verify`).
