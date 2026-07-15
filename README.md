# ai-workflow

19 skills implementing the AI-agent software workflow (deterministic rails braided
around model judgment). Reconstructed from Zain's Flowgauge kit docs and walkthrough.

Outer lifecycle: /roast -> /storm-research -> /prototype -> /grill -> spec -> /to-issues.
Inner loop: /resume -> plan -> build (/tdd) -> /code-review-pass -> /simplify -> /verify -> /handoff.
Design & maintenance: /codebase-design, /domain-modeling, /improve-codebase-architecture,
/diagnosing-bugs, /doc-audit, /harness-audit, /writing-great-skills, /teach.

Companion Claude Code kit (agents, hooks, CLAUDE.md template): see ai-workflow-kit.zip.

## Install

This repo is private — you need read access (ask Cesar for an invite), plus git authenticated with GitHub on your machine.

```
claude plugin marketplace add cesaratmba30/ai-workflow
claude plugin install ai-workflow@cesaridrovo-plugins
```

## Using with Codex CLI

Codex supports the same SKILL.md format — no plugin install needed. Clone and copy the skills to your Codex skills directory:
git clone https://github.com/cesaratmba30/ai-workflow.git
cp -r ai-workflow/skills/* ~/.codex/skills/

Or for a single project, copy them into `.agents/skills/` at the repo root — Codex discovers them automatically.
