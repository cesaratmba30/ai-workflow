---
name: zoom-out
description: Explain an unfamiliar section of code in whole-system context. Use when the user says "zoom out", "give me the big picture here", "how does this fit in", or is lost in a part of the codebase.
---

# /zoom-out — go up a layer

The user doesn't know this area of code well. Go up a layer of abstraction: give a map of the relevant modules, their responsibilities, and their callers, using the project's domain vocabulary (CONTEXT.md). Explain what the area is *for* in the system before explaining what any line does. No code changes.

## Attribution

Ported from [`zoom-out`](https://github.com/mattpocock/skills/tree/main/skills/engineering/zoom-out) in Matt Pocock's [Skills for Real Engineers](https://github.com/mattpocock/skills) (MIT). Adapted for this kit.
