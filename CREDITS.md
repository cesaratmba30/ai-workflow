# Credits & Attribution

This kit stands on prior work. Each skill's SKILL.md carries its own Attribution section where applicable; this file is the roll-up. All derived material has been adapted and evolved — errors are ours, not the sources'.

## Primary sources

### Matt Pocock — Skills for Real Engineers (MIT)
https://github.com/mattpocock/skills — © Matt Pocock, MIT License.

Direct ancestors of: **grill** (grill-me, grill-with-docs), **tdd**, **diagnosing-bugs** (diagnose; now split into bug-repro / bug-localize / bug-fix-regression), **to-issues**, **improve-codebase-architecture** (now split with architecture-survey), **prototype**, **handoff**, **writing-great-skills** (write-a-skill), and the CONTEXT.md + ADR discipline in **domain-modeling** (grill-with-docs). Ported from the same source: **triage**, **zoom-out**.

### Rik Dryfoos — HomeFlow
https://github.com/rdryfoos/HomeFlow — © Rik Dryfoos.

Source of the **traceability** method: durable requirement IDs carried PRD → spec → tasks → code → tests, rooted in GE Healthcare design-controls practice, composed with GitHub Spec Kit. Also prior art for this kit's glossary discipline (glossary.md).

### Philipp Schmid — "Don't Ship Skills Without Evals" (Google DeepMind)
Talk: https://www.youtube.com/watch?v=0vphxNt4wyk · Written guides: https://www.philschmid.de/testing-skills, https://www.philschmid.de/agent-skills-tips

Source of the v0.3 eval discipline: **skill-eval**, the `evals/` harness (prompt sets with negative cases, deterministic checks, multi-trial isolated runs, description-first iteration, graduation and retirement), the authoring upgrades folded into **writing-great-skills**, and the intake bar enforced by **skill-adopt**.

### Forward Future — Loop Library
https://signals.forwardfuture.com/loop-library/

Inspiration (concepts, not text) for: **skill-portfolio-audit** — from "The Loop Hiring Manager" (Eric Lott) and "The loop-auditor loop" (quigleyBits) — and **test-stabilizer** — from "The test stabilizer loop" (hungtv27). The library's design pattern of explicit stopping conditions and budgets informs this kit's loop-shaped skills.

### Stanford OVAL — STORM (MIT)
https://github.com/stanford-oval/storm — Shao et al., 2024.

Method basis for **storm-research** (multi-perspective research synthesis; now split into perspective-research / research-synthesis / citation-check), adapted from article generation to decision-support briefings.

## Books and papers

- John Ousterhout, *A Philosophy of Software Design* — **codebase-design**, **improve-codebase-architecture**, **architecture-survey**
- Kent Beck, *Test-Driven Development: By Example* — **tdd**
- David Thomas & Andrew Hunt, *The Pragmatic Programmer* — feedback-loop framing in **tdd**
- Eric Evans, *Domain-Driven Design* (ubiquitous language) — **domain-modeling**
- Michael Nygard, Architecture Decision Records — **domain-modeling**
- Frederick Brooks, *The Design of Design* (the "design concept") — **grill**
- Roediger & Karpicke (retrieval practice), Cepeda et al. (spacing), Sweller (worked examples) — **teach**

## Also consulted

- [agent-rules-books](https://github.com/mattpocock/agent-rules-books) (MIT) — book-distilled rule sets, companion reference to **codebase-design**
- [GitHub Spec Kit](https://github.com/github/spec-kit) — spec → plan → tasks pipeline that **traceability** composes with
- [Agent Skills open standard](https://agentskills.io) — the cross-platform SKILL.md format this repo targets

## Pending / to chase down

The following skills currently have no external attribution and trace only to Zain's Flowgauge kit (see README): **resume**, **roast**, **verify**, **code-review-pass**, **simplify**, **doc-audit**, **harness-audit**. If upstream sources exist for these, they belong here.
