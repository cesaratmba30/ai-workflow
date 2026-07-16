# ai-workflow

24 skills implementing the AI-agent software workflow (deterministic rails braided
around model judgment). Reconstructed from Zain's Flowgauge kit docs and walkthrough;
see [CREDITS.md](CREDITS.md) for upstream sources.

Outer lifecycle: /roast -> /storm-research -> /prototype -> /grill -> spec -> /to-issues.
Inner loop: /resume -> plan -> build (/tdd) -> /code-review-pass -> /simplify -> /verify -> /handoff.
Design & maintenance: /codebase-design, /domain-modeling, /improve-codebase-architecture,
/diagnosing-bugs, /doc-audit, /harness-audit, /writing-great-skills, /teach,
/zoom-out, /test-stabilizer, /skill-portfolio-audit.
Issue flow: /triage — evaluates incoming issues before /resume routes them.
Traceability: /traceability — durable AC IDs carried from spec through tasks, code, and tests.

## Install

Anyone can install:

```
claude plugin marketplace add cesaratmba30/ai-workflow
claude plugin install ai-workflow@cesaridrovo-plugins
```

## Using with Codex CLI

Codex supports the same SKILL.md format — no plugin install needed. Clone and copy the skills to your Codex skills directory.

macOS / Linux:
```
git clone https://github.com/cesaratmba30/ai-workflow.git
cp -r ai-workflow/skills/* ~/.codex/skills/
```

Windows (PowerShell):
```
git clone https://github.com/cesaratmba30/ai-workflow.git
Copy-Item -Recurse ai-workflow\skills\* $env:USERPROFILE\.codex\skills\
```

Or for a single project, copy them into `.agents/skills/` at the repo root — Codex discovers them automatically.

## Credits

This kit is derived from and inspired by prior work — most directly Matt Pocock's
[Skills for Real Engineers](https://github.com/mattpocock/skills) (MIT) and Rik Dryfoos'
[HomeFlow](https://github.com/rdryfoos/HomeFlow) traceability method. Full per-skill
attribution in [CREDITS.md](CREDITS.md) and in each skill's Attribution section.
