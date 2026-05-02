# Code Review: worktree-fleet-governance-closure
- issue_id: `I-20260321-0257`

## Scope Reviewed

- `docs/system/workspace/skills/worktree-maintenance-governance/**`
- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- 当前仓库 active worktree inventory

## Findings

- No blocking findings.

## Fleet Inventory

- current snapshot: `./bin/wt-status-all => Summary: total=9, dirty=0`

### Protected / Control Trees

- `develop`
  - disposition: `protected manager environment`
  - reason: clean；只承担监督、集成扫描与 post-merge acceptance，不承担 feature 开发
- `test-pre-merge-*`
  - disposition: `protected integration buffer family`
  - reason: 历史记录中的 `pre-test-merge` 现按 `test-pre-merge-*` 测试批次前缀族解释；clean 时只作为受保护验证环境保留

### Retained Integration / Verification Owners

- `feature/manager-family-integration-20260325`
  - disposition: `retained-with-reason`
  - reason: same-family source/companion retirement 已收口，但 integration owner 仍等待 develop-facing absorption 与 cleanup followthrough
- `feature/watchdog-family-replay-20260325`
  - disposition: `in-verification-owner`
  - reason: strict probe-gating / slot-first replay 已通过 focused verification，仍待 manager merge review
- `feature/testing-evidence-ladder-and-real-environment-gates-20260325`
  - disposition: `verification/materialization-owner`
  - reason: `I-20260325-0410` 仍在 `in_verification`，umbrella candidate `C-20260325-0333-A` 也仍 active；不能退休
- `feature/pre-test-merge-lifecycle-management-followthrough-20260324`
  - disposition: `runtime-owned-followthrough`
  - reason: 当前树继续承担 pre-test-merge completion/delete gate 与 fleet closure 最新真相写回

### Active Research / Replay Owners

- `feature/manager-scheduler-capacity-candidate-replay-20260324`
  - disposition: `needs-research replay owner`
  - reason: `C-20260323-2045-A` 仍缺一次真实 `develop` supervisor dogfood 证明 direct dispatch / queue retention / no-duplicate-launch contract
- `feature/manager-delegated-continuation-stall-materialization-20260323`
  - disposition: `needs-research candidate owner`
  - reason: `C-20260323-1705-A` 仍未冻结 stalled intake id -> prompt cycle -> consumed anchor -> no-new-continuity/handoff 的 specimen-chain
- `feature/worker-stall-recovery-during-active-ai-20260323`
  - disposition: `needs-research candidate owner`
  - reason: `C-20260323-1835-A` 仍未决定是 materialize 成独立 issue 还是并入既有 recovery owner；真实 dogfood acceptance 仍未冻结

## Actions Executed This Round

- 更新 `fleet_closure` evidence，使其从旧的 `dirty=3` snapshot 对齐到当前 `Summary: total=9, dirty=0`
- 记录本轮已完成的 superseded companion/source retirements，并明确剩余 9 棵当前没有新的 `retire-now` 对象
- 将剩余树按 protected / integration owner / runtime-owned followthrough / research-replay owner 四类重新分层，避免 manager/runtime 继续消费旧 fleet 真相

## Verification

- `./bin/governance-check`
- `./bin/wt-status-all`

## Residual Risks

- 当前 fleet 虽已 clean，但剩余 9 棵树里的大多数不是 cleanup 尾巴，而是仍在 `in_verification` 或 `needs_research` 的 owner 树；若继续按旧 closeout 思路扫，会误删生命周期 owner。
- `feature/manager-family-integration-20260325` 与 `feature/watchdog-family-replay-20260325` 仍待 manager merge / replay judgement；在被上游吸收前不能 cleanup。
- `feature/manager-scheduler-capacity-candidate-replay-20260324`、`feature/manager-delegated-continuation-stall-materialization-20260323`、`feature/worker-stall-recovery-during-active-ai-20260323` 仍缺真实 dogfood / evidence freeze，不能跳过 research owner 直接删除。
