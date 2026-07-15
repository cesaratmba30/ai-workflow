---
name: traceability
description: The golden thread — durable requirement IDs machine-checked from PRD to spec to task to code to test. Use when writing a spec/PRD (mint IDs), when checking coverage ("are all ACs tested?", "traceability check", "any silent gaps?"), or when setting up the traceability gate in a project. Fails loud on gaps AND untraced scope.
---

# /traceability — the golden thread

From Rik Dryfoos' HomeFlow method (GE Healthcare design controls, adapted). Code is cheap; **proof is the constraint**. A generic "must have a test" rule accepts any test; requirement-shaped enforcement demands a test naming the specific AC — so the test must prove that AC's semantics. The gate's job isn't intelligence; it's stubbornness: it doesn't find bugs, it makes missing proof impossible to ignore.

## The ID scheme

- **Grammar:** `<TYPE>-<DOMAIN>-<NN>` — `US` story, `FR` functional, `NFR` non-functional, `AC` acceptance criterion (e.g. `AC-SYNC-03`). Regex: `^(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?$`.
- **Minted ONCE, at the PRD/spec level.** Downstream artifacts inherit IDs, never mint their own. Immutable: reword text freely, never repoint an ID; retire (tombstone), never reuse.
- **Atomic ACs:** one independently testable assertion per AC. Split compound criteria (`AC-OFFL-03a/b/c/d`) BEFORE decomposition — compound ACs turn 1:1 mapping into 1:N and make the coverage report lie.

## The chain (the ID is a literal string at every hop — the matrix is a grep, not a spreadsheet)

```
PRD requirement (FR-OFFL-02)
  └─ AC (AC-OFFL-03) → spec carries it → task "Traces: AC-OFFL-03"
       → commit references it → source "@covers AC-OFFL-03"
       → test_AC_OFFL_03_no_silent_regression
```

## The check (run before merge/release; script it in CI where possible)

Bidirectional, fail-loud on either direction:

1. **Gap:** an AC in the registry with no test naming it AND no unchecked (tracked-debt) task → FAIL.
2. **Untraced scope:** a test name or `@covers` annotation referencing an ID not in the registry → FAIL (the scope-creep tripwire).
3. **Registry drift:** spec/tasks referencing IDs the PRD doesn't have, or vice versa → FAIL.
4. **Tasks without a `Traces:` field** → FAIL.

## The three honest states (never binary done/not-done)

- **Verified** — a named test passes in the suite.
- **Implemented — test pending** — code exists, test is an unchecked tracked task.
- **Tracked debt / planned** — visible on the board.

A fourth state, **silent gap**, is the only forbidden one. Debt is fine; silent debt is not. Report coverage as "N/M ACs verified, K tracked debt, 0 silent gaps."

## Spec extras that feed the thread

- **Risk & failure modes** per spec (3–8 rows: failure, user impact, mitigation traced to an AC ID).
- **Verification vs validation:** unit tests verify (built it right); E2E/manual sessions validate (built the right thing). Validation work is tracked debt, not optional polish.
- **Release checklist** before any ship: gates green, known validation gaps documented, rollback plan noted.

## Output

When minting: the ID registry. When checking: the gap/untraced-scope list (each a FAIL line) or "golden thread intact," plus the three-state summary. The kit's `check-traceability.template.sh` is the deterministic version — prefer wiring it into CI over re-running this skill by hand.
