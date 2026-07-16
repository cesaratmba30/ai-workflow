---
name: teach
description: Multi-session teaching workspace grounded in learning science. Use when the user wants to learn a topic over time — "teach me X", "help me learn", "continue my lessons", "quiz me". Maintains a persistent learning record so teaching resumes where it left off, with spaced retrieval and worked examples.
---

# /teach — the teaching workspace

Teaching that restarts from zero every session teaches nothing. This skill keeps a durable learning record and applies learning-science pedagogy instead of lecture-dumping.

## The learning record (the durable artifact)

A `LEARNING-<topic>.md` maintained across sessions:

- **Goal & scope** — what the learner wants to be able to DO (not just know).
- **Syllabus** — the concept sequence, each marked: not-started / introduced / practiced / solid.
- **Evidence log** — what the learner got right/wrong, misconceptions observed (verbatim), open questions.
- **Review queue** — concepts due for spaced retrieval, with last-tested date.

Update it every session (it's the teaching equivalent of the board: the record is the truth, the chat is disposable).

## Pedagogy (the method, per session)

1. **Resume from the record** — greet with a 2–3 question retrieval quiz on due items BEFORE new material (spaced retrieval practice; testing beats re-reading).
2. **One concept at a time**, connected to what's already solid; define new terms against the learner's existing vocabulary.
3. **Worked example → faded example → learner solves.** Show a full worked case, then one with gaps the learner fills, then a fresh problem solo.
4. **Elicit, don't tell:** ask the learner to predict/explain before revealing; a wrong prediction is the most teachable moment — diagnose the misconception, don't just correct the answer.
5. **Calibrate difficulty** to keep the learner in the productive-struggle band: success with effort. Too easy → advance; flailing → back up one rung.
6. **Close each session:** learner summarizes in their own words (self-explanation), record updated, next session's due-review queue set.

## Rules

- Never mark a concept "solid" without retrieval evidence from a later session.
- Honesty applies: if the learner's answer is wrong, say so plainly and kindly — a false "great job" is a silent wrongness bug.
- Real fluency is doing: bias toward exercises over exposition, roughly 1:1 time.

## Attribution

Grounded in learning-science literature: retrieval practice / testing effect (Roediger & Karpicke, 2006), spaced repetition (Ebbinghaus; Cepeda et al., 2006), worked examples (Sweller). Skill design original to this kit.
