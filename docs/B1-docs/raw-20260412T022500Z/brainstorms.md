# 预研头脑风暴：structured closeout gate and fresh review evidence

## 背景与问题

这轮 worktree 收口审查再次证明，`test-pre-merge-* -> develop` 的测试门禁并没有缺席；真正反复出问题的是“门禁前置真相”仍然分裂：

- worker/runtime state 只把 `Closeout-Gate` 记录成一段弱 free-text 命令串
- owner `pre-tests.md` 已能 machine-readably 声明 `target_lane=premerge-integration` 与 `promotion_gate=develop_merge`
- `governance-merge-gate` / `pretests-gate` 在 develop-bound promote 时又额外要求 fresh staged review artifact

结果就是：

1. runtime/cleanup replay 无法仅靠结构化 state 恢复 adequacy replay 所需的 lane/gate 上下文
2. owner closeout-only 文档改动虽然不改变 `pre-tests.md` 的 lane/gate 声明，但 develop promote 仍要求同批 staged review artifact
3. 操作者容易误判为“hook 没触发”或“tests 设计没接住”，实际上 gate 已 fail-close，只是 closeout contract 没有把完整充分条件提前说清

## 已确认事实

1. `verification-contract-and-premerge-adequacy-governance` 已把 manager/worker handoff 的最小 verification contract 冻结到 machine-readable 字段，但 `Closeout-Gate` 仍是单一字符串字段：
- `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- `docs/progress/workspace-routing-foundation/p-verification-contract-and-premerge-adequacy-governance.md`
- `docs/system/workspace/scripts/runtime/freely`

2. `pretests-retirement-gate` 已经暴露这个缺口，并明确 residual risk 是“recorded closeout gate 还没捕获 full lane/gate context”：
- `docs/system/workspace/scripts/quality/pretests-retirement-gate`
- `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/code-reviews/20260411-pre-tests-cleanup-and-retirement-enforcement-verification.md`

3. `implementation-decision-notes-in-issue-review-artifacts-governance` 已冻结 develop-bound implementation-bearing diff 需要 staged review artifact，但没有把“closeout-truth only diff 何时也必须 refresh review artifact”上升为更显式的 contract：
- `docs/B2-docs/ibm/implementation-decision-notes-in-issue-review-artifacts-governance/issues/implementation-decision-notes-in-issue-review-artifacts-governance.md`
- `docs/system/workspace/scripts/quality/governance-merge-gate`

4. 本轮真实 develop merge 失败证据说明 gate 工作正常，失败点是 owner `pre-tests.md` 虽声明了 `premerge-integration:develop_merge`，但 develop-bound staged diff 里没有 fresh staged review artifact：
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/scripts/quality/pretests-gate`

## 结论

这不是宪法、法律或 `AGENTS.md` 提示不足导致的首要问题；首要问题是 closeout contract 的 machine-readable 真相仍然不完整。

更具体地说，当前系统把 develop-bound adequacy 的充分条件拆散在三处：

1. runtime state 里的 `Closeout-Gate`
2. owner `pre-tests.md` 的 lane/gate adequacy item
3. merge gate 对 fresh staged review artifact 的额外要求

只要这三者没有在一个可恢复 contract 中同时出现，门禁就会“工作但总像突然出现”，并持续诱发以下误解：

- 误以为是 branch/test-pre-merge 命名问题
- 误以为是 hook 没启用
- 误以为只要 `pre-tests.md` 有 `develop_merge` adequacy item 就够了

## 最小正确设计

目标不是放松 gate，而是把现有 fail-closed 规则前移成更可恢复、更可提示的 contract。

### 1. 结构化 closeout gate context

在 worker prompt、delegated intake、runtime verification contract、workcell state 中，把下列字段从弱 free-text 拆成显式结构：

- `closeout_gate_command`
- `closeout_target_lane`
- `closeout_promotion_gate`
- `closeout_requires_adequacy`
- `closeout_review_artifact_policy`

其中 `closeout_review_artifact_policy` 第一阶段至少能表达：

- `staged_owner_review_required_for_develop_merge`

### 2. closeout replay 与 merge gate 对齐

cleanup followthrough / retirement replay 不再从 `LAST_WORKER_CLOSEOUT_GATE` 里解析隐含参数，而是直接消费结构化字段。

`governance-merge-gate` / `pretests-gate` 仍保持 fail-close，但错误输出与 worker guidance 应统一引用同一组结构化字段，明确告诉操作者：

- 这次 replay 目标 lane 是什么
- 目标 promotion gate 是什么
- 是否要求 adequacy
- 是否要求 fresh staged owner review artifact

### 3. owner / IBM 真源前置提示

对承担 `test-pre-merge-* -> develop` promote 的 owner，IBM 与 dev-loop guidance 应显式教会两件事：

- `pre-tests.md` 里的 `premerge-integration:develop_merge` adequacy item 只是必要条件，不是充分条件
- 若 develop-bound diff 触及 owner truth 或 implementation-bearing surface，必须在 owner `verification_artifact_dir` 下 staged 一份 fresh review artifact

### 4. 不做平行设计

不新增 `tests.md`，不新增第二套 closeout ledger，也不把 fresh review artifact 变成与 owner issue 无关的仓库级散落约定。

## 推荐吸收边界

首选把这条 follow-on 吸收到 `verification-contract-and-premerge-adequacy-governance` 的 follow-on owner，而不是重开 launch-time 或 cleanup owner：

- 结构化 closeout gate context 的真源主要在 verification contract
- fresh staged review artifact requirement 的“为什么”和“何时需要”要和 adequacy contract 一起解释
- cleanup owner 只应消费这套 contract，不应再次定义它

同时需要引用 `implementation-decision-notes-in-issue-review-artifacts-governance` 作为 staged review artifact policy 的上游依赖，但不应把 runtime/closeout state 结构化职责塞回那个 owner。

## 非目标

1. 不放宽 develop merge gate 对 fresh staged review artifact 的要求
2. 不把 closeout truth drift 一律当作纯文档改动从 gate 中豁免
3. 不在本批次重写所有历史 owner 的 `pre-tests.md`
4. 不在本批次新增新的测试编排 DSL

## Landing Zones

- runtime contract / state: `docs/system/workspace/scripts/runtime/freely`
- runtime regressions: `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-*`
- cleanup replay consumer: `docs/system/workspace/scripts/quality/pretests-retirement-gate`
- merge / adequacy gate messaging: `docs/system/workspace/scripts/quality/pretests-gate`
- worker / manager guidance: `docs/system/workspace/agents/worker-agent.md`, `docs/system/workspace/agents/manager-agent.md`
- owner / follow-on docs: `docs/B2-docs/git-worktree/<new-owner>/`

## 建议的后续 owner

- `structured-closeout-gate-context-and-review-evidence-governance`

第一阶段验收建议：

1. runtime verification contract 与 workcell state 记录结构化 closeout lane/gate/evidence policy，而不是只存 `Closeout-Gate` free-text
2. cleanup/retirement replay 直接消费结构化字段，不再依赖命令串解析
3. worker guidance 与 gate 诊断能明确指出 develop-bound promote 还缺哪类 review evidence
4. 不放松现有 develop merge gate，且不引入功能回退
