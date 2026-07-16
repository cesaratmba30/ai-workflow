---
name: codebase-design
description: Shared vocabulary and rules for designing deep modules. Use when designing or restructuring modules, discussing architecture, or when terms like "deep module", "seam", "adapter", "interface design" come up. A reference skill — it defines the design bar every substantial change is held to.
---

# /codebase-design — the deep-module vocabulary

From John Ousterhout's *A Philosophy of Software Design*. AI compounds software entropy: every change made without regard for the whole system degrades it, and AI makes changes fast. The counter is keeping the codebase *easy to change* — a good codebase is exactly where AI performs well; a ball of mud is where it drowns.

## The vocabulary (use these terms, precisely)

- **Deep module** — a lot of behaviour behind a small interface. **Depth = behaviour per unit of interface a caller must learn.** The goal state for every module.
- **Shallow module** — interface nearly as large as its implementation (a class that's just getters, a function that wraps one call). Complexity with no hiding. Merge or eliminate.
- **Seam** — the boundary where a module meets the rest of the system; where behaviour is specified and where you test. A clean seam = testable through the interface without reaching inside.
- **Adapter** (hexagonal architecture) — the thin translation layer between your domain logic and an external system (UI, DB, API). Domain logic never imports the external system directly.
- **Gray box** — you own the *interface* and verify at the seam; the implementation inside can be delegated (to the AI) without reading every line. "Design the interface, delegate the implementation."
- **Locality** — a change should touch one place. **Leverage** — a good abstraction pays rent on every future change. The two payoffs of depth.

## The rules

1. **Design the interface first.** Before building, name the seam: what does the caller see, what is hidden? An interface decided mid-build is an interface nobody designed.
2. **Test at the seam.** If a module needs its internals inspected to test it, the interface is wrong.
3. **Information hiding.** A caller should not need to know the implementation's choices (formats, ordering, caching) — if it does, the abstraction leaks.
4. **Pull complexity downward.** It's better for the module to be internally complex and simple to use than the reverse.
5. **Single source of truth per behaviour.** One function/file owns each load-bearing computation; everything else calls it. Duplicated logic is drift waiting to happen.
6. **Somewhat general-purpose.** Design the interface for the class of need, implement only today's case.

## When actively designing

State: the module's one-sentence purpose, its public interface (signatures), what it hides, its seam/tests, and what would make it shallower vs deeper. Prefer merging shallow modules into a deep one over adding another layer.

## Attribution

Distilled from John Ousterhout, *A Philosophy of Software Design* (deep modules, information hiding, complexity as the enemy). See also [agent-rules-books](https://github.com/mattpocock/agent-rules-books) (MIT) for comparable book-distilled rule sets.
