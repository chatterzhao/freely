# Issue: worker-reactivation-and-local-reentry-residual-runtime-governance

- issue_id: `I-20260401-1831-A`
- title: Worker reactivation and local reentry residual runtime governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `worker-reactivation-and-local-reentry-residual-runtime-governance`
- issue-name: `worker-reactivation-and-local-reentry-residual-runtime-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260401T224500Z/candidates.md#c-20260401-1831-a`
- source_brainstorm: `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/raw-20260401-1831/verification/pre-tests.md
- progress_path: `docs/progress/workspace-routing-foundation/p-worker-reactivation-and-local-reentry-residual-runtime-governance.md`
- verification_artifact_dir: docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/raw-20260401-1831/code-reviews
- depends_on:
  - `docs/B2-docs/human/chat-triggered-worker-runtime-reactivation-governance/raw-20260321-1706issues/chat-triggered-worker-runtime-reactivation-governance.md`
  - `docs/B2-docs/ibm/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`
  - `docs/B2-docs/ibm/manager-attach-reuse-missing-ai-repair-governance/issues/manager-attach-reuse-missing-ai-repair-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

完成 `I-20260401-1303-A-2` 的当前 materialization slice 后，当前 worktree 只剩两条红测，而且它们都不再属于 security/materialization：

1. `test-freely-chat-worker-reactivation` 仍可能在 worker `operator_stop` 后走到 attach reuse，写出 optimistic `already_running_attach`，但没有 durable `ai.pid`。
2. `test-freely-interruption-direct-answer` 暴露出 worker-side local continuation reentry 的 canonical active-worker predicate 仍未冻结，导致 completed owner 的验证口径与现行 runtime/test truth 不再完全一致。

这已经不是新的安全基线问题，而是 workspace-routing 的 worker-runtime residual。该 owner 用来承接 focused runtime/test 收口，避免当前 security lane 继续背 runtime debt，也把既有 worker reactivation / reentry owners 从过宽 closure 叙述拉回到当前 truth。

## Scope

1. 证明 worker chat/tui reactivation 失败时的真实 attach-reuse path。
2. 冻结 worker-side local continuation reentry 的 canonical active-worker predicate。
3. 明确 worker `operator_stop` 之后，何时允许 attach reuse，何时必须 repair/restart。
4. 对齐 runtime behavior、focused tests、以及旧 verification claims。
5. 将修复限定在 worker reactivation / local reentry boundary，不扩成 generic runtime orchestration redesign。

## Non-Goals

1. 不重新打开 Freely 默认自治/activation consent/materialization owner。
2. 不重做 manager-only attach repair；除非 worker residual 证明必须统一 manager/worker attach gate。
3. 不把问题扩大到 generic `live-status` redesign。
4. 不在本条里重新设计 interruption taxonomy 或 cleanup lifecycle。

## Acceptance

1. `test-freely-chat-worker-reactivation` 的 worker-side failure path 被精确绑定到明确 runtime contract gap，而不是继续停留在模糊“红测但归属不明”状态。
2. worker local continuation reentry 的 canonical active-worker predicate 被写成清晰 truth，并与 `test-freely-interruption-direct-answer` 对齐。
3. runtime 在 worker `operator_stop` 场景下，不再把“只有 supervisor、没有 durable AI child”的状态误写成成功 reactivation truth，除非新 contract 明确允许且有 bounded proof。
4. `I-20260321-1706` 与 `I-20260322-0412` 的完成性表述被 narrowed、superseded，或显式链接到本 follow-up。
5. 修复可由 focused runtime/test slice 验证，不要求同时重构多条无关 runtime 主干。

## Implemented Truth

1. worker attach-reuse 现在只在 AI pid 已确认归属当前项目且处于 running 状态时，才允许 `already_running_attach`。
2. 对于 worker `operator_stop` 后出现的“只有 supervisor、没有 durable AI child”状态，runtime 会转向 repair/restart 语义，而不是继续写 optimistic success。
3. project ownership 判定现在按 realpath 对齐，避免 `/tmp` 与 `/private/tmp` 这类路径别名导致 worker 运行时被误判成非当前项目。
4. local continuation reentry 的 worker-side fixture truth 已与 runtime contract 对齐；测试夹具使用真正归属 worker project 的模拟 AI 进程，并在 retry 场景前清掉旧 dispatcher，防止 watcher 抢先吸收 intake。

## Current Artifact Set

- `docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/issues/worker-reactivation-and-local-reentry-residual-runtime-governance.md`
- `docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/brainstorms/b-worker-reactivation-and-local-reentry-residual-runtime-governance.md`
- `docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/prd.md`
- `docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/pre-tests.md`
- `docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/tasks.md`
- `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- `docs/B1-docs/raw-20260401T224500Z/candidates.md`
- `docs/milestones.md`

## Current Evidence

- `./bin/governance-check`
- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- wording review confirming:
  - this owner clearly sits under `workspace-routing-foundation`, not the current security lane
  - worker reactivation and worker local reentry are treated as one narrow residual boundary
  - old completed owners are referenced as upstream truth, not silently overwritten

## Next

- 当前 worktree 已有 focused runtime/test evidence，并已进入这条 bounded owner 的 develop-bound verification。
- 若后续再出现新的 worker-runtime residual 漂移，应另开更窄的 residual follow-on，而不是重新扩大当前 issue。

- 记录或单独吸收旁路 repro，例如 `test-live-status-attach-false-positive-repro`，但它不再属于本 owner 的 closure 前提。

## Closeout

- canonical_merge_target: `develop`
- canonical_merge_commit: `e3cce23`
- post_merge_acceptance:
  - `bash docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
  - `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
  - `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
  - `./bin/governance-check`
- closeout_note: Focused worker-runtime residual verification now holds on canonical `develop`; any future drift should reopen as a narrower follow-on instead of keeping this owner in verification.
