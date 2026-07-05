# Issue: manager-reactivation-and-fleet-patrol-governance

- issue_id: `I-20260321-0345`
- title: Manager reactivation and fleet patrol governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-reactivation-and-fleet-patrol-governance`
- issue-name: `manager-reactivation-and-fleet-patrol-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260321-0345/candidates.md#c-20260321-0345-a`
- source_brainstorm: `docs/B1-docs/raw-20260321-0345/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`, `docs/epics/workspace-routing-foundation/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 现在已经能通过 runtime watchdog 拉起主管，也能通过 `live-status` / `fleet-status` / worktree skills 观察当前项目状态。

但还缺一条更明确的主管 patrol 协议：

- 主管重激活后，要先巡检整个 fleet，而不是只等下一条 event source
- 主管需要主动发现“哪些 phase / issue / worktree 当前没有 worker 推进”
- 主管需要主动发现“issue 已完成但 worktree 未收口”

否则 Freely 只能做到：
- manager process alive

做不到：
- manager actually supervising the fleet

## Scope

1. 扩展 `manager-agent`，明确主管重激活后先做一轮 fleet patrol。
2. 扩展 `multi-worktree-supervision`，定义 patrol 的固定输入顺序与 stalled/orphaned phase 检查面。
3. 扩展 `auto-loop-orchestrator`，明确 standing-source patrol 是主管职责的一部分，而不是纯被动信号路由。
4. 扩展首跳提示与脚本回归，锁定：
   - `live-status -> fleet-status -> milestone / issue / progress / recovery`
   - `candidate stuck / phase orphaned / completion without closure`
5. 保持现有 worktree / runtime / watchdog 能力不被平行新 skill 稀释。

## Acceptance

- `manager-agent` 明确要求主管重激活后先 patrol fleet
- `multi-worktree-supervision` 存在 manager reactivation patrol reference
- `auto-loop-orchestrator` 明确 standing-source patrol 不是可选建议
- `start-lead-agent.sh` / `test-routing-foundation-loop` 锁定 patrol 提示
- 不通过新增平行大 skill 达成；优先维护既有真源

## Completion

- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/code-reviews/20260321-manager-reactivation-and-fleet-patrol-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/code-reviews/20260326-manager-reactivation-and-fleet-patrol-canonical-replay-verification.md`

## Verification Summary

- canonical replay 继续证明：主管重激活后先 patrol fleet、从 `live-status -> fleet-status -> milestone / issue / progress / recovery` 取输入、并显式检查 stalled/orphaned/completed-without-closure 情况的协议仍在真源中成立。
- 当前剩下的只是“以后若要做真正定时巡检或自动派单”的增量方向，不是当前 issue 的未完成项。
- 当前批次据此把本 issue 从 `in_verification` 关闭为 `completed`。
