# Issue: launch-time-verification-contract-hard-gate-governance

- issue_id: `I-20260411-1414-A`
- title: Launch-time verification contract hard gate governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `launch-time-verification-contract-hard-gate-governance`
- issue-name: `launch-time-verification-contract-hard-gate-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260411T141600Z/candidates.md#c-20260411-1414-a`
- source_brainstorm: `docs/B1-docs/raw-20260411T141600Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
  - `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

现有验证真相已经要求 manager / worker handoff 带完整 verification metadata，但 runtime launch 仍只记录缺字段，不阻断 worker 启动。这使测试契约的第一道硬门禁落后于实际执行边界。

## Scope

1. 冻结 launch-time 必填 verification metadata
2. 在 runtime launch 边界拒绝缺字段 handoff
3. 保留 machine-readable missing-fields / blocked-state 诊断
4. 明确 branch-only / 自然语言 prompt 的受限策略
5. 用 focused regressions 锁住 blocked path 与 success path

## Non-Goals

1. 不扩 adequacy schema v2
2. 不补 cleanup / retirement enforcement
3. 不新增 `tests.md`
4. 不把本 owner 扩成全链 testing orchestration

## IBM Handoff

- implementation_scope_summary:
  - 本 owner 只补 launch-time hard gate，不重做 merge/completion gate。
  - 对 branch-only / 自然语言 prompt，要么拒绝并给 remediation，要么通过显式升级路径补全 contract，不能继续保留默认宽松。
- required_doc_refs:
  - `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/prd.md`
  - `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/pre-tests.md`
  - `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/tasks.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/agents/worker-agent.md`
  - `docs/system/workspace/scripts/start-lead-agent.sh`

## Completion

- `docs/B1-docs/raw-20260411T141600Z/candidates.md`
- `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/issues/launch-time-verification-contract-hard-gate-governance.md`
- `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/brainstorms/b-launch-time-verification-contract-hard-gate-governance.md`
- `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/prd.md`
- `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/pre-tests.md`
- `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/tasks.md`
- `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/code-reviews/20260411-launch-time-verification-contract-hard-gate-verification.md`
- `docs/progress/workspace-routing-foundation/p-launch-time-verification-contract-hard-gate-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-partial-verification-metadata`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-unresolved-worktree-blocked`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-worker-partial-metadata-keeps-running-state`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-missing-prompt-blocked`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-partial-verification-metadata`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-unresolved-worktree-blocked`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-worker-partial-metadata-keeps-running-state`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-missing-prompt-blocked`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`
- `./bin/test-lane premerge-integration -- ./bin/governance-check`
- `./bin/governance-check`
- `docs/B2-docs/ibm/launch-time-verification-contract-hard-gate-governance/code-reviews/20260411-launch-time-verification-contract-hard-gate-verification.md`

## Next

1. next_action: `completed on canonical develop; the guarded premerge replay, develop promotion, and dedicated-lane retirement are already closed and this issue now remains only as canonical delivered truth.`
2. revisit_trigger: Re-open only if guarded premerge replay still shows the launch-time hard gate or its absorbed adequacy dependency can cross into develop without explicit develop-merge proof, or if incomplete verification metadata again crosses the dispatch boundary.
