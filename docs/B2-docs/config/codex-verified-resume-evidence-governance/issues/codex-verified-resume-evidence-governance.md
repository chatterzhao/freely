# Issue: codex-verified-resume-evidence-governance

- issue_id: `I-20260328-2105-A`
- title: Codex verified resume evidence governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-verified-resume-evidence-governance`
- issue-name: `codex-verified-resume-evidence-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260328/candidates.md#c-20260328-2105-a`
- source_brainstorm: `docs/B1-docs/raw-20260328/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md`
  - `docs/B2-docs/ibm/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- pre_tests_path: `docs/B2-docs/config/codex-verified-resume-evidence-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-verified-resume-evidence-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/codex-verified-resume-evidence-governance/code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
  - {tool: codex, session_id: "019d374c-6743-7020-a420-14573edb41cd", jsonl_path: "unavailable://no-rollout-found-for-thread-id", role: "reproduced-invalid-resume-target"}

## Why

Freely 已经把 `codex` 的 canonical continuity model 收敛为显式 session-addressed resume，但 `2026-03-28` 的 dogfood 现场证明当前恢复证据判定仍然过弱：

- `fresh` 首轮失败后，runtime 从 cycle log 观察到一个 `session_id`
- 同一轮又已经确认 `jsonl_path=unavailable`
- supervisor 仍把该 id 持久化为下轮 `resume_target`
- 后续连续对同一个不可恢复 thread id 执行 `resume`
- 直到进入 `restart_storm_pause`

隔离工位里直接执行 `codex exec resume 019d374c-6743-7020-a420-14573edb41cd ...` 也稳定报：

- `thread/resume failed: no rollout found for thread id ...`

这说明当前缺口不是“resume 不可用”，而是 runtime 把弱观察信号误升格成了可恢复证据。

## Scope

1. 冻结 `codex` 这条链上的恢复证据边界，区分：
   - `observed`
   - `persistable`
   - `resumable`
2. 明确 `observed session id + missing rollout/jsonl` 不得进入下一轮 `resume`
3. 为该场景定义 runtime 的合法降级面：
   - `fresh_with_handoff`
   - 或等价的 `missing_resume_evidence`
4. 补足 focused regression，覆盖：
   - 有 session id 但无 rollout/jsonl 的假阳性 resume evidence
   - 健康 explicit `resume` 不退化
5. 只在本 issue 内修复已证实的 `codex` 链；其他显式 session-addressed tool 是否共享同类抽象，留待后续审计决定

## Non-Goals

1. 不把本 issue 扩成账号池 / watchdog / slot governance 总修复。
2. 不回退 `explicit session-addressed resume` 到 `resume --last` 或 PTY-first 模型。
3. 不把 `live-status` 空白或 fleet observability 不一致并入同一 owner issue。
4. 不在本 issue 内直接宣称所有显式 session-addressed tool 都已证实存在同类问题。

## Acceptance

1. `codex` resume evidence 的 runtime 判定强于 `resume_target != empty`。
2. `observed session id + missing rollout/jsonl` 不再触发下一轮 `resume`。
3. runtime 对该场景会给出明确降级原因，而不是重复无效 `resume` 到 restart storm。
4. 带真实 rollout/jsonl evidence 的健康 `resume` 继续可用。
5. `auth_failure` / watchdog slot recovery 语义不被本 issue 误伤。

## Verification

- `./bin/governance-check`
- focused reproduction for invalid `codex` resume target in isolated worktree
- focused regression for false-positive session-id-only resume evidence
- focused regression proving valid rollout-backed `codex` resume still works

## Implementation References

- `docs/B2-docs/config/codex-verified-resume-evidence-governance/prd.md`
- `docs/B2-docs/config/codex-verified-resume-evidence-governance/pre-tests.md`
- `docs/B2-docs/config/codex-verified-resume-evidence-governance/tasks.md`
- `docs/system/workspace/scripts/runtime/freely`

## Next

- IBM, dev-loop, and verification are complete; this owner is closed.
- Current implementation stays deliberately narrow: verified rollout/jsonl evidence is now required before the `codex` path can reuse explicit `resume`.
- Develop already contains the repair in commit `20574fa`; the earlier merge-prep lane is provenance only, not an active owner.
- Verification truth remains in `docs/B2-docs/config/codex-verified-resume-evidence-governance/code-reviews/20260330-codex-verified-resume-evidence-feature-verification.md`.
