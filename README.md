# ai-workflow

**v0.3.0** — 38 skills implementing the AI-agent software workflow (deterministic rails braided around model judgment), now atomic, evaluated, and platform-agnostic.

Originally reconstructed from Zain's Flowgauge kit; v0.2 added golden-thread traceability (Rik Dryfoos / HomeFlow) plus ported skills (triage, zoom-out, test-stabilizer, skill-portfolio-audit — see [CREDITS.md](CREDITS.md)); v0.3 adds the eval discipline from Philipp Schmid's "Don't Ship Skills Without Evals" (Google DeepMind), atomic sub-skills for subagent delegation, and vendor-agnostic model/effort/concurrency routing.

## The lifecycle

Outer lifecycle: `/roast` → `/storm-research` → `/prototype` → `/grill` → spec → `/to-issues`.
Inner loop: `/resume` → plan → build (`/tdd`) → `/code-review-pass` → `/simplify` → `/verify` → `/handoff`.
Issue flow: `/triage` — evaluates incoming issues before `/resume` routes them.
Design & maintenance: `/codebase-design`, `/domain-modeling`, `/improve-codebase-architecture`, `/diagnosing-bugs`, `/doc-audit`, `/harness-audit`, `/test-stabilizer`, `/zoom-out`, `/teach`.
Skill lifecycle: `/writing-great-skills`, `/skill-eval`, `/skill-adopt`, `/skill-portfolio-audit`.

New or third-party skills enter ONLY through `/skill-adopt` — the intake pipeline that enforces atomicity, metadata (model/effort/concurrency), and evals regardless of where a skill came from.

## Orchestrators and atomic sub-skills

Big multi-step skills are now **thin orchestrators** that compose **atomic sub-skills**, each independently invocable (directly or via a subagent) and each carrying its own model/effort recommendation:

| Orchestrator | Atomic sub-skills it composes |
|---|---|
| `resume` | `session-state-load`, `work-routing`, `board-sync` (+ `tdd`, `code-review-pass`, `simplify`, `verify` in the build cycle) |
| `handoff` | `board-sync` |
| `storm-research` | `perspective-research` (×N, parallel), `research-synthesis`, `citation-check` |
| `roast` | `persona-attack` (×N, parallel), `roast-judge` |
| `improve-codebase-architecture` | `architecture-survey`, then `grill` per candidate |
| `diagnosing-bugs` | `bug-repro`, `bug-localize`, `bug-fix-regression` |

Everything from v0.2 is preserved: the orchestrators carry the same rules and output contracts; the phases just live in files you can also call on their own.

## Model & effort routing (vendor-agnostic)

Every skill's frontmatter carries a `metadata` block naming its engine tier, the concrete Claude and OpenAI/Codex model + reasoning effort best suited to its atomic task, its subagent stance, and its **concurrency mode** — whether to fan out parallel subagents (`parallel-fanout`/`parallel-ok`) or single-thread and wait (`single`/`single-wait`/`interactive`). See [MODELS.md](MODELS.md) for the tier table and concurrency vocabulary. Platforms that don't parse the metadata still see the same recommendations as `> Engine:` and `> Concurrency:` notes at the top of each skill body.

## Evals

`evals/` contains a lightweight harness (per Schmid's workflow): per-skill prompt sets with positive, negative (must-NOT-trigger), and edge cases; deterministic regex/section checks; and a runner that works through both `claude` and `codex` CLIs. See [evals/README.md](evals/README.md). Don't ship a skill change without running its eval.

## Install

**Claude Code / Cowork (as a plugin):**

```
claude plugin marketplace add cesaratmba30/ai-workflow
claude plugin install ai-workflow@cesaridrovo-plugins
```

Or copy `skills/*` into `~/.claude/skills/` (personal) or `.claude/skills/` (project).

**OpenAI Codex CLI:** skills follow the Agent Skills open standard. Copy or symlink `skills/*` into `~/.codex/skills/` (personal) or `.codex/skills/` (project), or run `scripts/install.sh codex`. `AGENTS.md` in this repo gives Codex the lifecycle map and routing rules.

**Any other Agent-Skills-compatible tool** (Gemini CLI, Cursor, …): same `SKILL.md` format; install into that tool's skills directory. Run `scripts/install.sh --help` for options.

## Repo layout

```
ai-workflow/
├── README.md            ← you are here
├── AGENTS.md            ← Codex/other-agent entry point (lifecycle + routing)
├── MODELS.md            ← engine tiers → concrete model/effort mapping
├── .claude-plugin/plugin.json
├── CREDITS.md           ← upstream attribution (Pocock, Dryfoos, Schmid, Forward Future, STORM)
├── skills/<name>/SKILL.md   (38 skills: 25 lifecycle + 13 atomic sub-skills)
├── evals/
│   ├── README.md
│   ├── run_evals.py     ← harness (claude + codex adapters)
│   ├── checks.py        ← deterministic check registry
│   └── prompts/<skill>.json
└── scripts/install.sh
```
