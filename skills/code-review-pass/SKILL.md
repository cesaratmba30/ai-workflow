---
name: code-review-pass
description: Two-axis adversarial code review of a diff or change set. Use before merging any non-trivial change — "review this diff", "code review", "check this PR". Axis 1 is standards and code smells; axis 2 is spec-vs-implementation. Every finding is triaged by "is it TRUE?", never by "does it change runtime?".
---

# /code-review-pass — the two-axis reviewer

The default reviewer for a project. Complementary to a simplify pass: this hunts bugs and defects; simplify cleans shape. Reviews are judgment work — run them at high effort, never delegate to the cheapest model.

## Axis 1 — Standards + smells (the code on its own terms)

Walk the diff hunting, in order of severity:

1. **Correctness** — logic errors, off-by-ones, unhandled edge cases, race conditions, wrong error handling.
2. **Honesty invariants** — silent empty outputs, misleading zeros/placeholders, silently narrowed input handling. These are bugs, not style.
3. **Security** — if the change touches the trust surface (input parsing, auth, secrets, egress, injection/escaping), flag for a dedicated security review; don't wave it through.
4. **Tests** — is the behaviour change covered by a test in the same change? Is the test mutation-proven and non-tautological, or theater?
5. **Fowler-style smells** — duplication, dead code, redundant guards, long methods doing several things, feature envy, leaky abstractions, shallow modules that should be deep.

## Axis 2 — Spec-vs-implementation

Read the issue/spec/plan the change claims to implement. Verify: everything promised is present; nothing unrequested snuck in (scope creep is a finding); the interface built matches the interface specified.

## Triage discipline (the deciding rule)

For every finding, the question is **"is it TRUE?"** — never "does it change runtime?":

- **True** → it gets fixed, including pure code-quality findings with zero runtime impact. "Cosmetic" is not a dismissal.
- **False** → dismissed with a one-line reason, on the record.
- **Clean** = every finding is a verified false-positive or a deliberate, stated by-design choice.

## Output

Findings grouped by severity (blocker / should-fix / nit), each with file:line, the claim, and the evidence. End with the verdict: merge-clean, or the blocker list.
