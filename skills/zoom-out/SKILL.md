---
name: zoom-out
description: Explain an unfamiliar section of code in whole-system context. Use when the user says "zoom out", "give me the big picture here", "how does this fit in", or is lost in a part of the codebase. Do NOT use to modify code, hunt refactor candidates (architecture-survey), or teach a topic over time (teach).
metadata:
  engine: balanced
  claude: claude-sonnet-5 (medium)
  openai: gpt-5.6-terra (medium)
  subagent: optional
  concurrency: single
  atomic: true
---

# /zoom-out — go up a layer

> **Engine:** balanced — Claude `sonnet-5` (medium) · OpenAI `gpt-5.6-terra` (medium) · Subagent: optional (read-only exploration)
>
> **Concurrency:** Single-thread, read-only; no writes to interleave with.

The user doesn't know this area of code well. Go up a layer of abstraction: give a map of the relevant modules, their responsibilities, and their callers, using the project's domain vocabulary (CONTEXT.md). Explain what the area is *for* in the system before explaining what any line does. No code changes.

## Attribution

Ported from [`zoom-out`](https://github.com/mattpocock/skills/tree/main/skills/engineering/zoom-out) in Matt Pocock's [Skills for Real Engineers](https://github.com/mattpocock/skills) (MIT). Adapted for this kit.
