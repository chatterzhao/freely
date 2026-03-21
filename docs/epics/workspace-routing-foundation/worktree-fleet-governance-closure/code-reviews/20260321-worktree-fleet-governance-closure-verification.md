# Code Review: worktree-fleet-governance-closure

## Scope Reviewed

- `docs/system/workspace/skills/worktree-maintenance-governance/**`
- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- 当前仓库 active worktree inventory

## Findings

- No blocking findings.

## First-pass Fleet Inventory

- `feature/worktree-maintenance-merge-chain-governance-20260321-1045`
  - disposition: `merge-up`
  - reason: develop 派生、tests 与治理文档齐备，已可向上并入 develop-facing integration branch
- `feature/merge-prep-cc-codex-runtime-20260321-1005`
  - disposition: `merge-prep-to-develop`
  - reason: 已完成 `child -> parent -> merge-prep-from-develop`，当前保留为正式 develop-facing 集成工位
- `feature/research-codex-in-cc-mcp`
  - disposition: `merge-up`
  - reason: 已被上游 merge-prep 工位吸收；后续待 develop-facing 分支提升后再进入 retirement handoff
- `feature/cc-runtime-codex-mcp-20260320-2017`
  - disposition: `merge-up`
  - reason: 子分支内容已被父 research 分支吸收；后续沿上层链完成 promote 后再 cleanup
- `feature/cc-codex-mcp-runtime-governance-20260320-2235`
  - disposition: `blocked`
  - reason: branch 已在 develop 祖先内，但 worktree 仍 dirty；必须先判断未提交差异是否已被 newer cc chain 吸收，不能直接删
- `feature/governance-batch-merge-20260320-2235`
  - disposition: `blocked`
  - reason: 属于历史 merge batch companion；需做 anti-retrogression 与 salvage 判断，当前不应直接 promote 或 cleanup
- docs-only / research-heavy worktrees
  - disposition: `continue-dev` 或 `research-writeback-then-retire`
  - reason: 这批工位大多未进入 develop，且 diff 主要是 docs/candidate 研究；应继续按 candidate / milestone 生命周期推进，而不是在本轮强行清空

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `./bin/wt-status-all`

## Residual Risks

- 当前 inventory 仍是首轮分类，不等于所有 worktree 已完成 promote / cleanup。
- `feature/cc-codex-mcp-runtime-governance-20260320-2235` 与 `feature/governance-batch-merge-20260320-2235` 仍需后续 salvage_then_retire 判断。
