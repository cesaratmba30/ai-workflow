---
name: test-stabilizer
description: Find flaky tests, fix their root causes, and prove stability with repeated full-suite runs. Use when tests pass sometimes and fail others — "flaky test", "CI is red again but it passes locally", "stabilize the suite". Never fixes a flake with a sleep or a retry.
---

# /test-stabilizer — kill flakes at the root

A flaky test is worse than a missing test: it trains everyone to ignore red. Blind sleeps and retries hide the root cause and slow the suite; this skill forbids them.

## The loop

1. **Detect.** Run the suite N times (default 5) under identical conditions. List every test whose result changes across runs, with failure frequency.
2. **Diagnose the most frequent flake.** Root causes are almost always one of: shared mutable state between tests, timing/race conditions, test-order dependence, or an unmocked external dependency (network, clock, filesystem, randomness). Find which — read the test and the code under test; reproduce the failure deterministically if possible (forced ordering, seeded randomness, frozen clock).
3. **Fix the root cause.** Isolate state, inject the clock/seed, mock the dependency, or remove the order dependence. NEVER add a sleep, a retry wrapper, or a widened timeout as the fix.
4. **Prove.** Run the fixed test N times, then the full suite. Repeat from step 2 for the next flake.

## Terminal states

Stop when N consecutive full-suite runs pass, when progress stalls for two rounds, or when a fix needs approval (e.g. test infrastructure change). A quarantine (skip + tracking issue) is allowed only with explicit owner approval and a stated re-entry condition. Output: each flake, root cause, fix, run evidence, and any justified quarantines.

## Attribution

Inspired by "The test stabilizer loop" (hungtv27) from Forward Future's [Loop Library](https://signals.forwardfuture.com/loop-library/). Original text for this kit.
