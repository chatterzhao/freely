# Issue: verification-contract-and-premerge-adequacy-governance

- issue_id: `I-20260408-1205-A`
- title: Verification contract and premerge adequacy governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `verification-contract-and-premerge-adequacy-governance`
- issue-name: `verification-contract-and-premerge-adequacy-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260408/candidates.md#c-20260408-1205-a`
- source_brainstorm: `docs/B1-docs/raw-20260408/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/test-lane-routing-and-enforcement-governance/issues/test-lane-routing-and-enforcement-governance.md`
  - `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/issues/pre-tests-evidence-binding-and-completion-gate-governance.md`
  - `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 现在已经有测试真源，但没有形成闭环：

- `pre-tests.md` 定义 acceptance contract
- `test-lane` 定义测试应在哪条 lane 合法执行
- `pretests-gate` 只卡 issue `completed`
- `governance-merge-gate` / `pre-merge-commit` 只卡 develop-bound owner materialization
- manager / worker handoff 只传调度信息，不传测试义务

因此系统目前还不能稳定区分：

1. `pre-tests.md` 根本没写当前修改需要的测试任务
2. 任务写了，但没有从任务派生测试用例 / acceptance items
3. 测试项定义了，但根本没执行
4. 测了，但没有把完成状态、artifact、`not_applicable` 理由正确回写

这不是“测试理念缺失”，而是 issue-bound verification contract 没有被 handoff 与 merge gate 强消费。

## Scope

1. 冻结 manager / worker handoff 必须携带的最小 verification metadata：
   - `Owner-Issue`
   - `Pre-Tests-Path`
   - `Verification-Artifact-Dir`
   - `Required-Test-Lanes`
   - `Required-Acceptance-Item-Ids`
   - `Minimum-Evidence-Level`
   - `Target-Environment`
   - `Closeout-Gate`
2. 冻结 `pre-tests.md` item-level contract，使系统能 machine-readably 判断：
   - 四个必备章节始终存在：`Unit`、`Integration`、`End-to-End`、`Real-Environment`
   - `Unit`、`Integration`、`End-to-End` 章节若不适用，必须写有限枚举的 `not_applicable_reason`
   - `Real-Environment` 固定写 `real_environment_status` 与 `real_environment_reason`
   - 测试项属于哪类 surface / lane / environment
   - 是否属于 promote 必跑项
   - 它来自哪些任务 / acceptance target
   - 测试用例是否真的被设计出来
3. 冻结 `test-pre-merge-* -> develop` 的 fallback adequacy gate：
   - gate 不猜 changed paths
   - gate 只消费 owner issue 绑定的 `pre-tests.md`
   - gate 失败时必须区分：
     - `pre_tests_missing`
     - `testcase_derivation_missing`
     - `execution_missing`
     - `verification_state_missing`
4. 保留 post-merge integration / real-environment / dogfood surface 的独立性，不把它们误压成单一 premerge smoke。

## Non-Goals

1. 不在本 owner 内自动生成全部测试命令。
2. 不在本 owner 内对全仓历史 issue 做回填改写。
3. 不在本 owner 内靠 changed paths、关键词或全仓扫描猜相关测试。
4. 不在本 owner 内引入新的测试编排 DSL 或全自动 orchestration。

## Acceptance

1. Freely 真源明确：`pre-tests.md` 仍是 issue-bound verification 的唯一 canonical truth。
2. Freely 真源明确：worker handoff 不能只写调度 metadata，必须带最小 verification contract 索引。
3. Freely 真源明确：`test-pre-merge-* -> develop` 的 gate 是最后兜底，不代替测试设计，但必须能提示失败具体落在哪一层。
4. Freely 真源明确：gate 至少能区分“没写测试任务”“没按任务设计测试用例”“没测”“没标记完成情况”这四类失败面。
5. Freely 真源明确：`pre-tests.md` 必须显式包含 `Unit`、`Integration`、`End-to-End`、`Real-Environment` 四章；前三章不适用只能使用有限 reason type 加短解释，`Real-Environment` 固定写最终审查结论。
6. Freely 真源明确：premerge adequacy 不等于覆盖所有 post-merge surface；real-environment / dogfood 仍保留为独立 acceptance 面。

## IBM Handoff

- implementation_scope_summary:
  - `I-20260408-1205-A` 先冻结单一 verification contract，再决定实现阶段是否把 prompt/runtime 改动与 gate 改动拆成两个 dev-loop lane。
  - 第一阶段优先改真源与 prompt/gate contract，不要求一次性完成所有 wrapper adoption。
  - merge gate 的职责是兜底并给可操作诊断，不是替代 manager / worker 设计测试。
- required_doc_refs:
  - `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
  - `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/brainstorms/b-verification-contract-and-premerge-adequacy-governance.md`
  - `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/tasks.md`
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/agents/worker-agent.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/quality/pretests-gate`
  - `docs/system/workspace/scripts/quality/governance-merge-gate`
  - `docs/system/workspace/hooks/pre-merge-commit.sh`

## Next

1. next_action: `completed`
2. revisit_trigger: 若后续发现 manager handoff、worker recovery、或 develop-bound adequacy gate 仍出现“contract 已写但 runtime state / review 无法恢复”的漏口，再开 follow-on issue 继续收紧 launch 恢复与 merge followthrough。
3. absorbed_follow_ons:
   - `C-20260411-1417-B` from `docs/B1-docs/raw-20260411/candidates.md`, because the stale-truth audit confirmed this canonical owner already closed the verification-contract / premerge-adequacy chain and no separate runtime owner should be reopened.

## Completion

- `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/code-reviews/20260408-verification-contract-and-premerge-adequacy-verification.md`
- `docs/progress/workspace-routing-foundation/p-verification-contract-and-premerge-adequacy-governance.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `./bin/governance-check`
