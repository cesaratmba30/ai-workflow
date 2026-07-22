---
name: board-sync
description: Reconcile the project board with git reality — move cards to truthful columns, flag drift, report coverage in the three honest states. Use inside handoff, after a batch of merges, or standalone ("sync the board", "is the board accurate", "update the cards"). Do NOT use to create new issues — that is to-issues.
metadata:
  engine: fast
  claude: claude-haiku-4-5 (low)
  openai: gpt-5.6-luna (low)
  subagent: recommended
  concurrency: single
  atomic: true
---

# /board-sync — the board matches reality, or it lies

> **Engine:** fast — Claude `haiku-4.5` (low) · OpenAI `gpt-5.6-luna` (low) · Subagent: recommended (mechanical reconciliation)
>
> **Concurrency:** Single-thread: one writer to the board; never run two syncs concurrently.

A stale board poisons every future `/resume`. This skill makes the board truthful, with git as the referee.

## Method

1. For every in-flight card, compare column vs git/CI reality: built & merged → In review / Shipped; abandoned → back to Options **with a reason**.
2. **Drift check:** a card whose column contradicts reality is flagged loudly; moves are proposed, then applied on approval (or autonomously when the caller says so).
3. Report coverage in the **three honest states** (see /traceability): verified / implemented-test-pending / tracked debt — never binary done/not-done. An untested AC must exist as an unchecked task; a **silent gap fails the sync**.

## Output

The move list (card → from → to → evidence), the drift flags, and the three-state coverage line ("N/M ACs verified, K tracked debt, 0 silent gaps").
