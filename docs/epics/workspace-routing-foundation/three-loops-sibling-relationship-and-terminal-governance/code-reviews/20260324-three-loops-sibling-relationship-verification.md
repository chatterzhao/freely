# Code Review: three-loops-sibling-relationship-and-terminal-governance
- issue_id: `I-20260324-0405`

## Result

- verification passed
- active truth now consistently treats `auto-loop` as the outer orchestration/governance loop and `doc-loop` / `dev-loop` as sibling execution loops
- verification / cleanup / recovery are consistently described as route, phase, or governance path rather than extra loops
- supervisor-owned completion, cleanup, retirement, and dead-loop judgement now match the loop model across docs, agent prompts, and script-facing contracts

## Evidence

- `./bin/governance-check`
- `rg -n "三层循环|三层 loop|三层职责边界|第二层 auto-loop" docs/CONSTITUTION.md docs/PROJECT_INTENT.md docs/system/workspace/three-loop-capability-lifecycle.md docs/system/workspace/agents/manager-agent.md docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md docs/system/workspace/scripts/compose-context-source-prompt.sh docs/system/workspace/scripts/README.md docs/LAWS.md`
- `bash docs/system/workspace/scripts/tests/test-human-chat-routing`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- manual read-through of the updated active truth set, including manager/worker/lead/context-source/watchdog docs and script entrypoints

## What Changed

1. high-level constitutional and intent documents now describe “三个 loop” instead of layered containment
2. `three-loop-capability-lifecycle.md` now distinguishes loop, route, phase, verification, cleanup, and terminal retirement more precisely
3. agent/skill contracts now make `auto-loop` the owner of completion, verification, cleanup, retirement, and supervision judgement
4. script prompt truth no longer describes `auto-loop` as a “second layer” or implies local loop exit equals terminal completion
5. restart storm / process churn is now framed as a watchdog supervision signal judged by manager `auto-loop`, not by worker self-declaration

## Remaining Lifecycle

- the issue is complete for this batch
- this worktree is not delete-ready until merge, cleanup evidence, and retirement gating are finished
