# MODELS.md — engine tiers and vendor mapping

Skills declare an abstract **engine tier**; this file maps tiers to concrete models per vendor. When model generations change, update THIS file (and the frontmatter `claude:`/`openai:` hints if you want them literal) — the tier semantics don't change.

Current mapping (July 2026):

| Tier | Use for | Claude | OpenAI / Codex |
|---|---|---|---|
| `fast` | Mechanical, well-specified, high-volume: state loading, grep-shaped checks, extraction, formatting | `claude-haiku-4-5`, effort low | `gpt-5.6-luna`, reasoning low |
| `balanced` | Everyday build work: TDD slices, issue slicing, drafting, single-perspective research | `claude-sonnet-5`, effort medium | `gpt-5.6-terra`, reasoning medium |
| `deep` | Judgment work: adversarial review, synthesis, architecture, diagnosis, verdicts | `claude-opus-4-8`, effort high | `gpt-5.6-sol`, reasoning high |
| `frontier` | The hardest single problems; escalation when `deep` stalls twice | `claude-fable-5`, effort high | `gpt-5.6-sol`, reasoning xhigh (or Max mode) |

Reasoning-effort names differ per surface: Claude Code uses low/medium/high; Codex CLI uses low/medium/high/xhigh (plus Max/Ultra modes in the ChatGPT app). Map to the nearest available.

## Frontmatter schema

Every skill carries:

```yaml
metadata:
  engine: deep                # fast | balanced | deep | frontier
  claude: claude-opus-4-8 (high)
  openai: gpt-5.6-sol (high)
  subagent: recommended       # recommended | optional | no (needs the user / main thread)
  concurrency: parallel-fanout
  atomic: true                # false for orchestrators
  composes: [a, b]            # orchestrators only
```

### Concurrency vocabulary

| Value | Meaning |
|---|---|
| `parallel-fanout` | Spawn N isolated subagent instances concurrently (lanes/personas/citations); the caller MUST join — wait for every instance — before the next phase. |
| `parallel-ok` | May shard across subagents for scale (by directory, file group, test case); join before any write/scoring phase. Single-threaded is also fine. |
| `single` | One thread, run to completion; do not interleave with writers of the same resource. |
| `single-wait` | One thread AND a blocking gate: downstream steps wait for this skill's output (reviews, verdicts, syntheses, verification). |
| `interactive` | Main thread only, human in the loop; WAIT for the human at each step. Never delegate to a subagent. |
| `orchestrator` | Composes other skills; its body states which phases fan out and which are sequential gates. |

Platforms that ignore unknown frontmatter keys (all current ones do) lose nothing; the same info is repeated as a `> Engine:` line in the body.

## Routing rules

1. Run each atomic skill on its declared tier — don't run everything on the biggest model, and never run judgment skills (`code-review-pass`, `roast-judge`, `research-synthesis`, `architecture-survey`, `bug-localize`) below `deep`.
2. `subagent: recommended` means the skill benefits from a clean, isolated context (parallel fan-out or context economy). `no` means it is interactive or session-bound (e.g. `grill`, `resume`) — keep it in the main thread.
3. Escalation: if a `deep` diagnosis or review stalls twice, escalate to `frontier` rather than looping.
4. Orchestrators themselves run `balanced` — their job is composition, not judgment; the judgment happens inside the sub-skills they spawn. Exception: a *fixed-order, zero-decision* composition — one that never reasons about which path to take, like `checkpoint` (always: push, board-sync, note, in that order) — runs at its composed piece's own tier instead. The `balanced` default is for orchestrators that decide something; `checkpoint` doesn't.
