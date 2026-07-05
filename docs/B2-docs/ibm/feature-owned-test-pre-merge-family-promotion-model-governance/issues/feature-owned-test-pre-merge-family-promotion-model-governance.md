# Issue: feature-owned-test-pre-merge-family-promotion-model-governance

- issue_id: `I-20260405-1615-A`
- title: Feature-owned test-pre-merge family promotion model governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `feature-owned-test-pre-merge-family-promotion-model-governance`
- issue-name: `feature-owned-test-pre-merge-family-promotion-model-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260405/candidates.md#c-20260405-1615-a`
- source_brainstorm: `docs/B1-docs/raw-20260405/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/pre-tests.md`
- progress_path: `pending://progress-created-on-dev-loop`
- verification_artifact_dir: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
  - `docs/B2-docs/ibm/develop-guarded-merge-entrypoint-enforcement-governance/issues/develop-guarded-merge-entrypoint-enforcement-governance.md`
  - `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
  - `docs/B1-docs/raw-20260405/brainstorms.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

当前仓库对 `test-pre-merge-*` 仍停留在旧模型：

1. `feature/*` 仍被描述为可直接 merge 到 `develop` 的默认 promote 单位。
2. `test-pre-merge-*` 仍主要被描述为 shadow batch / replay 证据面。
3. multi-feature 组合测试是否只是验证证据、还是能成为 bundle promote 单位，没有被冻结。

这已经不只是命名或流程提示问题，而是 develop promotion model 本身没有冻结：

- 如果 `feature/*` 仍能直接进 `develop`，就始终存在“忘记先过 develop-like 预集成 lane”的制度逃逸面。
- 如果多个 feature 要并行做集成验证，又没有统一的 single-feature / multi-bundle 语义，就会让 `pr-merge-guarded`、hook、`governance-check`、runtime/status 在不同地方各自发明自己的模型。
- 如果在 owner issue 之前就直接改 `CONSTITUTION` / `LAWS` / gate 实现，后续很容易出现“脚本已经固化，治理模型却还没定”的反向耦合。

因此这条 owner 的职责是先冻结 promote model，再把 gate enforcement、lifecycle automation、tooling UX 留给后续 issue。

## Scope

1. 冻结 `test-pre-merge-*` family 的 canonical promote model，包括 single-feature lane 与 explicit multi-bundle lane 的角色。
2. 冻结 `feature/*`、`test-pre-merge-*`、`develop` 三者的职责边界：
   - 谁是 source-of-truth 开发单位
   - 谁是 develop-like 预集成验证环境
   - 谁是 canonical protected integration line
3. 冻结 `multi` 语义只能存在于 `test-pre-merge-*` family 内，不再发明第二个前缀。
4. 冻结 explicit multi-bundle 最小可追溯概念：
   - source features
   - feature shas
   - merge order
   - base develop sha
   - stale / rebuild trigger
5. 冻结哪些约束属于后续必须 machine-enforced 的治理面，但不在本 owner 内承诺具体 hook/script/CLI 落点。

## Non-Goals

1. 不在本 owner 内直接修改 `CONSTITUTION`、`LAWS`、`pr-merge-guarded`、hook 或 `governance-check`。
2. 不在本 owner 内承诺具体 wrapper、命令名、manifest 文件格式或 test runner 接口。
3. 不在本 owner 内把所有测试 lane 直接做成 executable enforcement。
4. 不把 `test-pre-merge-*` 升级为长期开发主线或长期真相面。
5. 不把 stale detection、family cleanup、paired create、bundle automation 一次性实现。

## Acceptance

1. IBM 文档能明确回答三类问题：
   - develop-bound feature 的默认 promote 路径是什么
   - single-feature lane 与 explicit multi-bundle lane 分别承担什么职责
   - `develop`、`test-pre-merge-*`、`feature/*` 各自不是谁
2. 文档明确 canonical 前缀只保留 `test-pre-merge-*`，multi 不再单独发明 `test-pre-multi-merge-*`。
3. 文档明确冻结 multi-bundle 需要的最小可追溯概念，但不提前锁死具体实现介质。
4. issue / brainstorm / `prd.md` / `pre-tests.md` / `tasks.md` 一致表达：
   - promote model 先冻结
   - gate enforcement 后开新 owner
   - lifecycle automation 后开新 owner
5. `docs/milestones.md` 与 candidate 写回后，后续执行 authority 以本 owner 为准，而不是继续从 pre-brainstorm 直接驱动实现。

## IBM Handoff

- implementation_scope_summary:
  - `I-20260405-1615-A` 先冻结 `test-pre-merge` family 的 promote model，不提前做 enforcement implementation。
  - 后续只允许基于本 owner 的结论，分别开出 gate enforcement 与 lifecycle automation follow-on。
  - 若本 owner 尚未明确某个 multi-bundle promote 结论，执行层不得提前在脚本中单方面固化。
- required_doc_refs:
  - `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`
  - `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/brainstorms/b-feature-owned-test-pre-merge-family-promotion-model-governance.md`
  - `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/prd.md`
  - `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/pre-tests.md`
  - `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/tasks.md`
  - `docs/B1-docs/raw-20260405/brainstorms.md`

## Verification

- `./bin/governance-check`
- review `docs/B1-docs/raw-20260405/brainstorms.md`
- confirm this owner does not itself claim hook/script enforcement has already landed

## Completion

- `docs/B1-docs/raw-20260405/brainstorms.md`
- `docs/B1-docs/raw-20260405/candidates.md`
- `docs/B1-docs/raw-INDEX.md`
- `docs/milestones.md`
- `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`
- `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/brainstorms/b-feature-owned-test-pre-merge-family-promotion-model-governance.md`
- `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/prd.md`
- `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/pre-tests.md`
- `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/tasks.md`
- `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/code-reviews/20260405-feature-owned-test-pre-merge-family-promotion-model-implementation-decision.md`
- `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/code-reviews/20260405-feature-owned-test-pre-merge-family-promotion-model-verification.md`

## Next

1. `2026-04-05` closeout: canonical promote model has been frozen into the new owner package and consumed by the follow-on promotion-gate and test-lane owners in this same governance transaction.
2. Future work should reopen only for lifecycle automation, paired create UX, or manifest/runtime surfaces that were explicitly excluded here.
3. Do not reopen this owner to change hook/script behavior directly unless the frozen model itself is proven inconsistent.
