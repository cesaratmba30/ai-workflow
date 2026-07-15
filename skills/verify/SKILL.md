---
name: verify
description: Run the real thing and look at the result — never trust green tests alone. Use before declaring any change done or pushing — "verify it", "prove it works", "did you actually run it". For visual changes, drive the UI and capture a screenshot; for non-visual changes, exercise the real path.
---

# /verify — run it, don't trust green

Tests prove the *logic*; they don't prove it *renders* or *runs* — a UI/mount bug passes the suite and paints wrong. And agents will claim "done" without looking ("AI lies"); verification must be forced, structurally. A change isn't done until the real result has been driven and LOOKED at.

## Method by change type

- **Visible/UI change:** build/serve the artifact, load real (or realistic) data, drive the changed surface (click the path, not just the happy render), capture a screenshot (e.g. via Playwright), and **view the screenshot** — confirm what's on screen matches intent: right data, right state, no blank panels, no misleading zeros.
- **CLI/script/backend change:** execute through the real entry point (run the CLI, call the API, import the module) with real-shaped input; capture the actual output verbatim.
- **Generated artifact:** rebuild from source and confirm the shipped artifact byte-matches (no stale/hand-edited copy).
- **Honesty spot-check:** feed one bad/empty input; the failure must be loud and explanatory, never a silent blank or plausible-looking zero.

## Rules

1. Verification comes AFTER suite-green, not instead of it.
2. Evidence or it didn't happen: the claim "verified" must be accompanied by the artifact — screenshot, pasted output, or byte-match result. Re-reading the diff is not verification.
3. Report outcomes straight: show failing output if it failed; never say "done" on inference.

## Output

The evidence bundle (screenshot/output + one line of interpretation), which feeds the decision packet handed back to the owner.
