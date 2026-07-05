# 预研头脑风暴：pre-test-merge-governance-lifecycle

## 背景

Freely 这次暴露出来的不是单纯的合并冲突，而是 `pre-test-merge` 的职责边界、允许用法、退出条件和批次生命周期都还不够清晰。

兼容说明：
- 本预研目录与历史 issue/path 继续保留 `pre-test-merge` 命名，避免破坏既有留痕与引用。
- 当前 canonical 语义已经改成 `test-pre-merge-*` 测试批次前缀族；下文出现的 `pre-test-merge` 都按这个前缀族理解，而不是单例长期分支。

我们已经看到几种危险信号：

- `pre-test-merge` 被当成了“临时集成批次”和“事实主线”混用
- `develop` 继续前进后，旧批次仍被拿来比较或回收
- 一些有效实现只能在旧批次里看见，但回到 `develop` 时又可能被误删、误回退或重复引入
- 验证环境、promotion gate、cleanup gate 之间没有形成完整的 machine-readable 生命周期契约

这说明问题不在某个提交，而在 `pre-test-merge` 这一治理对象本身还缺一套清晰的责任模型。

## 为什么现在必须研究

Freely 正在用 Freely 开发 Freely。

这意味着：

- 只把 `pre-test-merge` 当人工临时分支，会不断重复同类问题
- 只修单次 merge，不会解决“旧批次为什么还活着”“什么时候该退休”“什么能 promote”这些更高层问题
- 这类问题一旦不被 materialize 成 Freely 能力，未来每次复杂集成都要靠人脑重新判断

## 当前事实

### 已确认的分支事实

1. `develop` 是长期集成主线。
2. `test-pre-merge-*` 是临时预集成验证批次，不应固化为长期开发父分支。
3. 对 develop-bound 变更，正常 promote 路径已经冻结为 `feature/* -> test-pre-merge-* -> develop`；`feature/* -> develop` 不再是正常路径。
4. 单 feature 批次与 explicit multi-bundle 批次共用同一 `test-pre-merge-*` family；不再新增第二个 `test-pre-*` 前缀来表达 multi lane。
5. 复杂集成、短周期验收、冲突收敛、发布前预演可以启用 `test-pre-merge-*` 批次，但它必须有清晰的批次边界，并从当前 `develop` 新建。

### 已确认的治理缺口

1. 还没有完全冻结：
- `test-pre-merge-*` 既是临时验证批次，也是进入 `develop` 的 canonical promote family
- `develop` 仍是长期集成真相，但不再承担“先在主线上预测试”的职责

2. 还没有明确回答：
- 一个 `test-pre-merge-*` 批次什么时候 stale
- 哪些改动必须回到来源 feature worktree
- 哪些情况下当前批次仍可作为权威 promote source，哪些情况下必须 retire / rebuild fresh batch

3. 还没有形成完整的能力化输出：
- 不能自动解释当前批次归属
- 不能自动提示 stale batch
- 不能自动给出 promote / replay / retire 建议

## 当前 fleet 分类快照

### 1. active owner，必须继续

- `feature/pre-test-merge-lifecycle-management-followthrough-20260324`
  - 当前 stale-batch governance 的 canonical owner
- `feature/application-native-observability-planes-20260324`
  - 仍在 pre-brainstorm，负责 future app 观察面 contract
- `feature/manager-scheduler-capacity-candidate-replay-20260324`
  - 仍在 pre-brainstorm，唯一剩余 blocker 是 fresh `develop`-based dogfood proof
- `feature/manager-delegated-continuation-stall-materialization-20260323`
  - 仍在 pre-brainstorm / continuation research，尚无更强 owner 吸收

### 2. stale / evidence-only，不能当执行面

- `pre-test-merge`
  - stale evidence-only；可保留 replay/source evidence，但不能恢复成当前验证面
- `feature/three-loop-dogfood-flow-alignment-20260323`
  - 已被新的 three-loops canonical issue 吸收，当前只保留历史 evidence
- `feature/worker-stall-recovery-during-active-ai-20260323`
  - 仍只是 pre-brainstorm candidate evidence，尚无 issue / cleanup delete gate
- `feature/manager-primary-handoff-materialization-stall-20260324`
  - 仍只是 pre-brainstorm candidate evidence，尚无 issue / cleanup delete gate

### 3. merged-clean cleanup candidates，但还不能直接删

- `feature/delegated-continuation-prompt-consumption-visibility-20260323`
- `feature/manager-worker-launch-idempotency-queue-promotion-20260323`
- `feature/manager-worker-launch-state-relaunch-recovery-20260323`
- `feature/manager-worker-prompt-contract-and-launch-consumption-20260323`
- `feature/manager-launch-state-frozen-prompt-state-reconcile-20260324`
- `feature/manager-launch-state-frozen-queue-drift-20260324`
- `feature/manager-worker-count-fleet-truth-reconcile-20260324`

这批树都满足同一组 git-level 事实：本地 clean、分支头已被 `develop` 吸收、且未见对应远程 branch。它们可以进入 cleanup gate 候选池，但仍不能只凭这些事实判 `delete-ready`。若 canonical issue / progress / cleanup truth 没有明确给出 `verified-retirable -> delete guard -> retired`，则最多只能记为 `cleanup-candidate`。

### 4. merged 但仍 active / cleanup-pending

- `feature/global-watchdog-earliest-reset-sleep-revive-20260323`
  - 仍在 canonical `in_verification`，不能删
- `feature/manager-launch-state-consumed-truth-reconcile-20260324`
  - canonical issue/progress 明确写了 `retained-with-reason`，要等 closeout writeback 被 develop-facing path 吸收

## 当前收敛结论

- `merged + clean + ahead=0` 只足以进入 cleanup 候选池，不足以直接执行删除
- 若 delete-ready 结论需要依赖“同 family 的其他 issue 已完成，所以这些旧树大概可删”的推断，该结论必须先回到 canonical issue / progress / cleanup truth 写成显式 gate，不能直接当执行依据
- 这也是本预研线仍然 active 的原因：Freely 目前还缺把 `cleanup-candidate -> verified-retirable -> delete guard -> retired` 写成 machine-readable gate 的能力

## 问题定义

需要一条更完整的治理路线，回答：

> 当 Freely 启用 `pre-test-merge` 做预集成验证时，应该如何定义它的职责、允许的操作、失效条件、生命周期结束条件，以及它与 `develop` 的 promotion 关系，才能既保住有效实现，又不把旧批次误当成当前真相？

## 关键张力

1. `test-pre-merge-*` 是临时验证批次，不该长期承载实现真相。
2. 但多个 feature 的组合行为只能在它这里被看见，而且当前 canonical develop promote 也必须经过它，不能简单废掉它或退回 direct `feature/* -> develop`。
3. `develop` 是最终长期主线，但主线在前进时不能被旧批次的语义拖回去，也不能替代新的测试批次承担主线前预检。
4. Git 本身不能天然表达 batch 生命周期，所以 Freely 需要显式治理与状态留痕。

## 预研方向

### 方向 A：明确 `pre-test-merge` 的职责模型

- 它只负责组合验证、冲突暴露、promotion 预演
- 不负责长期保存事实真相
- 不作为新的 feature 开发父分支
- 不作为默认回收旧实现的来源
- 但它在仍然权威时，就是 develop-bound 批次的合法 promote source；lifecycle capability 不得把这条 canonical promote 路径重新改写回 replay-only 或 direct feature bypass

### 方向 B：明确 `pre-test-merge` 的生命周期模型

- 批次开始
- 批次进行中
- 批次已验证
- 批次已失效
- 批次已退休

每个阶段都需要明确：

- 谁可以推进
- 谁可以读取
- 谁可以 promote
- 谁可以 retire

### 方向 C：把治理经验能力化

Freely 后续应具备能力去判断：

- 当前 `pre-test-merge` 是否仍是有效批次
- 是否已被 `develop` 甩开到需要重建
- 是否存在未回流到来源 worktree 的 protected-env 差异
- 是否能安全 promote，还是必须 retire / rebuild fresh batch 并重新吸收来源 feature 集合

## 预期落点

- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/B1-docs/raw-**`
- `docs/milestones.md`

## 最新 dogfood 发现

### 发现 1：规则已经写了，但没有强制执行层

- `CONSTITUTION`、`LAWS`、`manager-reactivation-patrol`、`pre-test-merge-flow` 都已经要求 stale `pre-test-merge` 必须 retire / rebuild
- 真实 dogfood 里，manager 只能把它解释成 `runtime-owned` 或 `manager-owned` 的判断，却没有 machine-enforced gate 阻止旧批次继续被消费
- 结果就是：
  - `develop` 已前进
  - 旧 `pre-test-merge` 仍保留旧 runtime state / stale pid / 旧 verification 视图
  - 人和 manager 都还能继续把它当成当前观察面

### 发现 2：当前痛点不只是一条 stale-batch 检测

- 现场不是单点误判，而是三层 loop 缺少收口联动：
  - manager 能看见 stale batch，但不会强制退休
  - runtime 负责恢复进程，却不知道“这个 batch 已经不该再恢复成当前验证面”
  - worker 已进入 verification-only / continuity-refresh 自环时，也没有回交 manager 强制重判的 gate
- 所以真正缺的是一条 lifecycle capability，而不是单个 watchdog 补丁

### 发现 3：并发不足不是根因，worker 自环才是根因

- 当前默认 worker capacity 是 2，但真正堵塞新 lane 的不是数字 2 本身
- 现场两个 worker 都在占槽重复低价值动作：
  - 一个反复重跑同一套 verification，并重复补同一组三份 verification writeback
  - 一个反复刷新 continuity anchor，但没有进入 IBM / issue materialization
- 这说明 stale-batch capability 还需要同时覆盖“什么时候 worker 必须回主管重判”，否则就算把并发调大，也只是把更多槽位交给自环

### 发现 4：Freely 规范上应使用 subagent，但当前主可见实体仍是 worker lane

- 现有真源已经要求主管在可并行、写入范围不冲突的任务上使用 `subagent` 提高效率
- 但当前控制面的第一等对象仍是 `worktree / session / run / worker lane`
- `subagent` 更接近 AI 在提示词和工具能力下的内部执行安排，day-1 backend 不要求把每个 subagent 做成强实体
- 所以当前用户“看不见 subagent”不自动等于系统“不会委派”，更可能意味着：
  - 主管更多把并行工作 materialize 成 worker lane / queue / continuity
  - subagent 结果没有被单独可视化成一级对象
- 这也意味着本次预研应避免把“是否用了 subagent”与“是否产生了 machine-readable worker handoff / queue state”混成一回事

### 发现 5：`pre-tests.md` 质量是上游 gate，不只是 IBM 附件

- `doc-ibm-execution` 已明确把 `pre-tests.md` 定义为 issue-level acceptance 的主控制面，而不是附属清单
- 但 `pre-tests.md` 也不是独立自生文件；它属于 IBM 产物，必须由 milestone-owned `Issue`、issue-bound `Brainstorm` 与 `PRD` 在 `doc-ibm-execution` skill 下共同派生
- 也就是说，真正的上游缺口不是“某个 `pre-tests.md` 文件写得弱”这么简单，而是：
  - `I` 没把正式 issue scope 和 acceptance 深化稳定下来
  - `B` 没把关键比较、边界、未决问题收束成 issue-bound brainstrom
  - `PRD` 没把执行控制面写到足以自然派生 `pre-tests.md` / `tasks.md`
- `pre-tests.md` 若没有把 integration / acceptance、`pre-merge` / `post-merge acceptance`、目标验证环境与 protected branch 只做验证的边界写清，后续 dogfood 和 completion verification 就只能靠口头解释或代码阅读恢复验收标准
- 这类弱 `pre-tests.md` 会直接造成下游假推进：
  - issue 看起来已 ready for dev，但 acceptance 仍不稳定
  - worker / manager 看起来完成了 verification，但实际没有明确 target environment 与必需 evidence
  - worktree 可能被 merge / retire / cleanup，而主线 acceptance 其实还没真正被定义或完成
- 所以本次问题不能只写成 stale batch/runtime gate；还必须把 `pre-tests.md` 质量视为上游 IBM gate，并在治理 contract 中承认：
  - manager/runtime 不负责重新发明 `B` 或重写 `pre-tests.md`
  - 下游只能消费 IBM 已经写出的 acceptance contract，或明确识别“IBM contract incomplete”
  - 当 `pre-tests.md` 没有稳定 issue-level acceptance 时，后续 `completion_verification` 与 `worktree retirement` 都不应被视为 fully grounded
  - `pre-test-merge` 的 stale/replay/retire 语义必须能引用一份可恢复的 `pre-tests.md` acceptance 面，而不是靠 runtime 补推理

## 收敛后的能力拆分

### 能力线 1：stale `pre-test-merge` governance

- 这一条只处理 stale validation batch 的治理事务，不顺手解决所有 worker 自环问题
- 最小 contract 只覆盖：
  - stale machine-readable state
  - manager mandatory lifecycle decision
  - runtime consumption gate
  - replay source manifest / replay order / retire evidence
- watchdog 不负责判 stale，只负责恢复；stale 判定必须来自 manager 可追溯输出
- 但 stale 判定本身也不能脱离 IBM 真相；若 issue 的 `I + B + PRD -> pre-tests.md` 派生链没有完成，manager 只能输出“acceptance contract incomplete”，不能假装 stale/retire 已经闭环

### 能力线 2：worker self-loop exit

- 这一条是更通用的 scheduling / closeout 问题，不应绑死在 `pre-test-merge`
- 它只处理：
  - verification-only / continuity-refresh 的 machine-readable 停滞判据
  - worker 回交 manager 的阈值和证据
  - manager 释放容量、重新排队、避免同 lane 立即重占槽位
- 这条能力应单独 materialize，避免把本次 `pre-test-merge` 治理做成横跨 manager/runtime/worker 的大改造

## 能力线 1：最小可执行 contract

### A. stale state truth surface

- stale 判定本身由 manager 负责，不由 watchdog 或 runtime 自行推理
- 一旦判 stale，必须写到唯一的 machine-readable 真相面，至少能被 continuity / status surface / runtime gate 统一消费
- 这里的唯一真相面固定为：`manager continuity`
- `manager-worker-launch-state.env` 与 `live-status` 只允许做派生镜像，不得反向定义或覆盖 batch 治理语义
- stale 条件暂不扩成宽泛启发式；当前预研只冻结最小方向：
  - `develop` 已前进，当前 batch 相对其 `source_batch_base` 不再覆盖目标验证范围
  - 当前 batch 已从 `active_verification` 退化为只允许 `read_only_cleanup` 或 `rebuild_planning`
- `cleanup evidence 未齐` 或 `replay target 未明` 不自动等于“可继续普通 verification”，而是进入 manager-owned lifecycle decision

### B. manager-owned lifecycle transaction

- manager 在 stale batch 上必须继续使用既有词典输出：
  - `ownership`
  - `restart_point`
  - `next_action`
- 但要额外补齐一笔完整治理事务，而不是只打 stale 标记：
  - `replay source manifest`
  - `replay order`
  - `retire evidence`
  - `remaining cleanup requirement`
- manager 不得继续把 stale batch 路由成普通 `verification`
- manager 也不应被压成“只剩 retire 或 rebuild”二选一；允许先输出过渡动作，例如收集 cleanup 证据、标记 replay source、补齐 post-merge acceptance 结论
- 如果上游 issue 的 `I + B + PRD` 尚不足以派生出合格的 `pre-tests.md`，manager 还必须允许 `acceptance_contract_incomplete` 这一类过渡结论，阻止系统把缺失的 IBM 约束误当作 runtime 可自动补全的问题

### C. runtime consumption gate

- runtime 不负责裁决 stale，只消费 manager 已写出的 stale state / lifecycle decision
- stale batch 上允许的 runtime 行为应收窄为：
  - read-only patrol / observation
  - cleanup handoff
  - rebuild / replay handoff
- stale batch 不得被重新拉成普通 verification 会话
- 所有指向 stale batch 的旧 queued worker prompts / delegated launches 都必须被 supersede 或失效，不能继续消费旧 prompt 池

### D. 现有真源上的最小落点

- 不新增平行状态文件；优先复用现有三层状态面：
  - manager continuity：唯一治理真相面
  - `manager-worker-launch-state.env`：runtime 消费镜像
  - `live-status`：可观察镜像
- 也就是说，stale `pre-test-merge` 不是先发明“新 watchdog 状态”，而是先让 manager continuity 写出可消费字段，再由 runtime 镜像到 launch state / live-status
- 承载语法也要冻结成固定可解析块，而不是自由叙述。当前先把候选语法冻结成 `Validation batch governance:` `v1`：
  - 固定标题：`Validation batch governance:`
  - 标题下方紧跟连续的 `- key: value` 行；遇到空行即视为块结束
  - 第一行固定为 `- block_format_version: v1`
  - key 顺序固定，避免 runtime / cleanup skill 靠全文搜索或无序匹配推理
  - 缺失但必须保留的值统一写字面量 `unavailable`，而不是省略该 key
  - 多值字段先保持单行字符串：`replay_source_manifest` / `replay_order` / `superseded_worker_prompts` 用 `; ` 连接，避免与绝对路径中的 `:` 冲突
- 当前建议 specimen：

```text
Validation batch governance:
- block_format_version: v1
- validation_batch_id: pre-test-merge@20260324-001322
- validation_batch_state: stale
- validation_batch_mode: read_only_cleanup
- stale_reason: develop_advanced
- lifecycle_decision: rebuild
- integration_target: develop
- source_batch_base: refs/heads/develop@abc1234
- replay_source_manifest: /abs/feature-a;/abs/feature-b
- replay_order: feature/a -> feature/b
- retire_evidence_ref: unavailable
- remaining_cleanup_requirement: post_merge_acceptance;verified-retirable;retired
- acceptance_contract_state: incomplete
- acceptance_contract_source: /abs/docs/epics/.../pre-tests.md
- acceptance_contract_blocker: missing_post_merge_acceptance
- superseded_worker_prompts: /abs/.freely/run/worker-prompts/old-a.txt
- superseded_worker_prompts_applied_at: unavailable
```

- runtime 只解析这个块，不从普通自然语言段落推理

### F. `Validation batch governance:` `v1` contract freeze

- 当前先冻结为单一 machine-readable block，而不是继续扩散到多处自然语言说明
- `Validation batch governance:` `v1` 的最小 contract 以这 17 个 key 为准，顺序不得变化：
  1. `block_format_version`
  2. `validation_batch_id`
  3. `validation_batch_state`
  4. `validation_batch_mode`
  5. `stale_reason`
  6. `lifecycle_decision`
  7. `integration_target`
  8. `source_batch_base`
  9. `replay_source_manifest`
  10. `replay_order`
  11. `retire_evidence_ref`
  12. `remaining_cleanup_requirement`
  13. `acceptance_contract_state`
  14. `acceptance_contract_source`
  15. `acceptance_contract_blocker`
  16. `superseded_worker_prompts`
  17. `superseded_worker_prompts_applied_at`
- 其中 `retire_evidence_ref`、`remaining_cleanup_requirement`、`acceptance_contract_*`、`superseded_worker_prompts*` 都是必留 key；值未知时写 `unavailable`，不得省略
- runtime / cleanup / delete gate 只能消费这一固定块，不得退回普通段落重新推理
- 当前 freeze 的目标不是证明所有实现细节都已足够，而是证明：
  - stale-batch truth surface 已唯一化
  - delete gate 输入组合可以只靠这组字段和现有 lifecycle gate 读取
  - `specimen-S1/S2/S3` 的拒绝结论不需要再引入平行状态词

### E. IBM 到 manager continuity 的最小桥

- manager 不应自由发挥地“读完 issue 自己猜 acceptance 是否完整”
- 更稳的桥是：manager 只消费现有 IBM artifact 是否足以支撑 acceptance contract，并把结果写入自己的固定块
- 当前建议冻结为 manager continuity 固定字段：
  - `acceptance_contract_state=grounded|incomplete|not_applicable`
  - `acceptance_contract_source=<absolute pre-tests.md path|unavailable>`
  - `acceptance_contract_blocker=missing_pre_tests|missing_post_merge_acceptance|missing_integration_target|ibm_not_done|none`
- 语义约束：
  - `grounded`：存在可恢复的 issue-level acceptance 面，且 `pre-tests.md` 已把 target verification environment、`pre-merge`/`post-merge acceptance` 与 protected branch 使用边界写清
  - `incomplete`：上游 `I + B + PRD -> pre-tests.md` 派生链仍缺 acceptance 关键约束，manager 只能 freeze / reroute，不得把当前 lane 当作普通 verification 或 stale-cleanup 已可执行
  - `not_applicable`：当前 lane 不受该 acceptance contract 约束，例如纯 pre-brainstorm research
- 这意味着 runtime 不需要理解 `Issue` / `B` / `PRD` 细节；它只消费 manager continuity 里的 `acceptance_contract_*` 字段

建议冻结的最小字段：

- manager continuity 必填：
  - `ownership=manager-owned`
  - `restart_point=runtime supervision / cleanup`
  - `next_action=cleanup|freeze|delegate`
  - `validation_batch_id=<current pre-test-merge batch identity>`
  - `integration_target=develop|main|pre-test-merge`
  - `source_batch_base=<target branch sha or equivalent anchor>`
  - `validation_batch_state=stale`
  - `validation_batch_mode=read_only_cleanup|rebuild_planning`
  - `validation_batch_action=retire_only|rebuild_from_sources|collect_cleanup_evidence`
  - `replay_source_manifest=<ordered feature branches/worktrees>`
  - `replay_plan_state=pending|complete`
  - `remaining_cleanup_requirement=<evidence still missing>`
  - `acceptance_contract_state=grounded|incomplete|not_applicable`
  - `acceptance_contract_source=<absolute pre-tests.md path|unavailable>`
  - `acceptance_contract_blocker=missing_pre_tests|missing_post_merge_acceptance|missing_integration_target|ibm_not_done|none`
  - `superseded_worker_prompts=<csv absolute paths>`
- runtime launch state 镜像：
  - `LAST_MANAGER_CONTINUITY_GENERATED`
  - `LAST_MANAGER_CONTINUITY_CONSUMED`
  - `QUEUED_WORKER_PROMPTS`
  - 派生 `validation_batch_id`
  - 派生 `validation_batch_state`
  - 派生 `validation_batch_mode`
  - 派生 `validation_batch_action`
  - 派生 `acceptance_contract_state`
  - 派生 `acceptance_contract_source`
  - 派生 `acceptance_contract_blocker`
  - 派生 `superseded_worker_prompts`
  - 派生 `superseded_worker_prompts_applied_at`
- `live-status` 只负责展示，不额外裁决：
  - `validation_batch_state: stale|active|not_applicable|unavailable`
  - `validation_batch_mode: read_only_cleanup|rebuild_planning|active_verification|none`
  - `validation_batch_action: retire_only|rebuild_from_sources|collect_cleanup_evidence|none`
  - `acceptance_contract_state: grounded|incomplete|not_applicable|unavailable`
  - `acceptance_contract_blocker: missing_pre_tests|missing_post_merge_acceptance|missing_integration_target|ibm_not_done|none|unavailable`
  - `superseded_worker_prompts: <csv|none>`
  - `superseded_worker_prompts_applied_at: <timestamp|unavailable>`

约束：

- runtime gate 只读这些 machine-readable 字段，不自行重新推理 stale
- watchdog 不读取 prompt 自己做 stale 判断
- `validation_batch_action` 是 manager continuity 的补充语义，不替代既有 `next_action`
- stale batch 若仍需要 cleanup 证据，manager 可以保留 `collect_cleanup_evidence`，但必须同时把 `validation_batch_mode` 保持为 `read_only_cleanup`，不得恢复成普通 verification lane
- `superseded_worker_prompts` 只是治理真相的一部分；runtime 还必须回写 `superseded_worker_prompts_applied_at`，表示旧 prompt 已停止被调度消费
- 若 `acceptance_contract_state=incomplete`，runtime 不得把该 lane 视为“只差执行”的普通 verification；它只能消费 manager 已写出的 freeze / reroute 结论

## 能力线 2：待拆分的开放 contract

- worker self-loop exit 方向成立，但当前仍缺：
  - 什么算 phase progress
  - 连续多少轮、哪类重复 writeback 才算低价值自环
  - 回交 manager 后如何释放 worker capacity
- 在这些判据 machine-readable 之前，不应把它和 stale `pre-test-merge` gate 一起实现

建议冻结的最小字段：

## 对 IBM / `pre-tests.md` 的新增收口判断

- `pre-tests.md` 不应再被当成“实现前补一补”的软文档；它决定后续 verification 是否有可恢复的 acceptance 面
- `pre-tests.md` 的质量检查不应脱离 IBM 派生链单独进行；它必须回到：
  - milestone-owned issue 是否已稳定
  - issue-bound brainstorm 是否已完成 acceptance deepening
  - `prd.md` 是否足以自然派生 `pre-tests.md` / `tasks.md`
- 若 `pre-tests.md` 只列代码检查点，没有 integration / acceptance、`pre-merge` / `post-merge acceptance`、target verification environment 与 protected branch 使用边界，则 IBM 不应被判 `done_ibm`
- 若 issue 在弱 `pre-tests.md` 条件下已推进到 dev / verification / cleanup，本次能力至少要能让 manager 明确识别：
  - 当前是 runtime stale/retire 问题
  - 还是 acceptance contract 本身就不完整
- 这也意味着后续 materialization 不能只改 runtime；还要检查是否需要把 `pre-tests.md` 质量 bar 更明确写回 IBM 真源或相关 issue/candidate

## 必须单独冻结的测试收尾 contract

- 不能再把“测试”写成一个泛词；至少要拆成两道门：
  - `pre-tests.md` 质量 gate：是否已经把 issue-level acceptance、integration target、以及若适用时的 `pre-merge` / `post-merge acceptance`、protected branch 只做验证的边界写清
  - testing closeout gate：这些 acceptance 是否真的被执行并留下可恢复 evidence
- testing closeout 默认优先：
  - integration / end-to-end evidence
  - application-native real-environment testing evidence
  - 最后才是局部代码级或纯单测证据
- `phase_state=completed` 是 issue 唯一的最终态，但它只说明 issue 生命周期完成；它本身不等于 worktree 已可删除
- `done_ibm`、单轮 verification 收口、单个 agent/skill 的局部完成，都不是任务最终完成
- 删除 worktree 还要继续看现有 lifecycle gate 是否凑齐：merge / cleanup evidence / `verified-retirable` / `retired`；若 `pre-tests.md` 显式声明 `post-merge acceptance`，则它是 delete eligibility chain 的附加必经 gate
- 因而完成检查顺序必须固定为两段：
  - issue completion chain：`done_ibm` -> `pre-tests.md` 质量 gate -> dev / verification -> testing closeout -> `phase_state=completed`
  - delete eligibility chain：merge -> cleanup evidence -> `verified-retirable` -> delete branch/worktree guard -> `retired`
- 若 `pre-tests.md` 显式声明 `post-merge acceptance`，则它插在 delete eligibility chain 中的 merge 之后、cleanup evidence 之前；未显式声明时，不得把它误用成默认必经项
- 还要单独承认一条 merge gate：
  - `merge gate` 只回答“当前 feature 是否可并入 `develop`”
  - 它不是 issue `completed`
  - 它也不是 worktree 已可删除
- 因此 merge 后若 closeout 未闭合，系统必须立刻进入下一跳，而不是把 merge 当作结束：
  - delegated continuation / cleanup lane
  - 或 milestone/owner queue 中的显式挂起，带 `next_action` / `revisit_trigger`
  - 不允许 merge 后因为树 clean 或 issue 已 `completed` 就静默失踪
- 其中 `completed` 只表示 issue 完成，不表示 delete-eligible；只有 delete eligibility chain 闭合后，worktree/branch 才能进入 `retired`
- “application-native real-environment testing” 指当前应用自己的真实入口、真实交互面、真实集成路径，而不是抽象脚本替身
- 在 Freely 自举场景里，它当前的具体形态才是：
  - `freely start`
  - `freely chat --project <project-root> <message>`
  - 通过 chat interruption 派发真实任务、观察 manager/worker/worktree 生命周期、检查 merge / cleanup / next-task scan 是否真的发生
- 因此，后续任何 stale governance / worker self-loop / retirement honesty 的实现，都不能只用静态文档 diff 或局部脚本测试宣布完成；至少要经过：
  - `pre-tests.md` 质量复核
  - 集成测试
  - application-native real-environment testing
- 若缺少这些 evidence，manager 不应把 lane 判成 `completion_verification done` 或允许 worktree retirement

## 三层 loop 的进入、跳出与最终结束

- 当前这条能力真正缺的，不只是“哪些 gate 组成 delete eligibility”，还缺一条稳定的 loop exit 语义：每层 loop 何时只是局部收口，何时真正跳回外层，何时才允许把整个主题当成结束
- 结合 [three-loop-capability-lifecycle](/Users/zhaoyu/Downloads/code/my-freely/freely/docs/system/workspace/three-loop-capability-lifecycle.md) 与现有 lifecycle 词典，可以把它收敛成三层：
  - doc-loop / pre-brainstorm / IBM：负责定义边界、contract、acceptance surface；其内循环结束，只表示“当前文档层可交给下一层”，不表示 issue 已完成，也不表示 worktree 可删除
  - dev-loop / completion verification：负责实现、测试、验证与 issue 级 `completed`；其内循环结束，只表示“issue 已完成或已回流到新边界”，不表示 cleanup 已完成
  - cleanup / auto-loop governance：负责 merge 后 closeout、cleanup evidence、`verified-retirable`、`retired` 与 next-task scan；只有这层闭合，当前 worktree lifecycle 才真正结束
- 因而每层 loop 的跳出条件应明确区分：
  - doc-loop 跳出：
    - `pre-brainstorm -> IBM`：candidate/materialization contract 已冻结
    - `IBM -> dev-loop`：`done_ibm` 且 `pre-tests.md` 质量 gate 通过
    - doc-loop 内部收口若只得到 `needs_research` / `blocked` / `pending://...`，说明仍停在当前 loop，不得冒充“完成”
  - dev-loop 跳出：
    - `in_dev -> in_verification`：实现与测试准备齐
    - `in_verification -> completed`：按 `pre-tests.md` 逐项完成 testing closeout，含 integration 与 application-native real-environment testing evidence
    - `in_verification -> pre_brainstorm|ibm`：若验证暴露出新边界或 acceptance contract 缺口，则不是完成，而是回到外层 doc-loop
  - cleanup / auto-loop governance 跳出：
    - `completed -> merged-not-cleaned`：issue 完成后进入 merge / closeout，不是结束
    - `merged-not-cleaned -> verified-retirable`：cleanup evidence 齐
    - `verified-retirable -> retired`：删除门通过，worktree/branch 真正退休
- 这也解释了为什么经常误删：
  - 把 doc-loop 的“研究收口”当成任务完成
  - 把 dev-loop 的 `completed` 当成 worktree 完成
  - 把 merge / clean 当成 cleanup loop 已结束
- 当前更稳的最终完成定义应是：
  - issue 完成：停在 `phase_state=completed`
  - worktree 完成：停在 `retired`
  - topic 真正结束：当前主题没有未闭合的 delegated continuation / cleanup lane，且 auto-loop 已把它从 active patrol 集合移出；之后系统才应进入 next-task scan 或新任务循环
- 因此“最外层结束”不是简单的“不再跑内循环”，而是：
  - 当前主题的 doc-loop、dev-loop、cleanup/auto-loop governance 都已各自跳出
  - 最终停在 `retired`
  - 下一轮 patrol 看到的是 closed lifecycle，而不是 retained owner / pending cleanup / queued followthrough
- 若任一内层 loop 结束后仍留下：
  - `remaining_cleanup_requirement`
  - queued/delegated continuation
  - `verified-retirable` 未达成
  - stale batch replay/source evidence 未吸收
  则说明只是局部 loop 收口，不能判“任务最终完成”
- 因此，`completed` 前要有测试门，`completed` 后仍要有删除门；两者不能混成一次判断
- 最终删除门若未来可以由 hook / guard 投影执行，应以现有状态与 evidence 组合作为输入，而不是重新发明平行状态

## 最新 field audit

这轮并行审计把一个关键事实钉死了：`merged + clean` 不是 delete gate，甚至连“接近可删”都不稳定。

## 误用根因补充

- `pre-test-merge` 的职责在 `CONSTITUTION` / `LAWS` / `pre-test-merge-flow` 中其实已经写清，但控制面默认值仍不够稳，导致它经常被误当成“高显著性的默认验证面”
- 造成滥用的根因不是缺职责定义，而是三类默认值长期漂移：
  - protected canonical worktree 很显眼，manager/supervisor 容易把它误读成“当前权威验证面”
  - `pre-tests.md` 没有先被读取时，系统容易把 `pre-test-merge` 当成默认 acceptance 环境，而不是先看 `integration_target`
  - stale 批次虽已在文档中定义为必须 retire/rebuild，但 runtime / patrol 仍缺足够硬的反向拒绝，因此旧批次会残留成“看起来还能继续消费”的 surface
- 因而后续 contract 必须补一条比“何时可以启用”更硬的默认规则：
  - develop-bound 默认 promote 路径已经是 `feature/* -> test-pre-merge-* -> develop`
  - route 决策只回答当前验证落在 dedicated feature lane、当前权威 `test-pre-merge-*`，还是 merge 后的 `develop` completion verification；不得重新打开 direct `feature/* -> develop`
  - 若验证目标不是当前权威 `test-pre-merge-*`，manager 必须有来自 `pre-tests.md` 或明确完成态 followthrough 的证据，不能因为 protected canonical worktree 显眼就把它当默认 acceptance 面
  - 若批次已 stale，默认动作是 retire/rebuild，不是继续消费旧批次
- 换句话说，`pre-test-merge` 的问题更像“反滥用 contract 不够硬”，而不是“职责从未定义”

当前最有代表性的 worktree 现状如下：

1. `pre-test-merge`
- 已确认 stale
- 已补最小 retire-evidence 文档，但仍不可 delete
- 当前 blocker 不是 dirt，而是 stale batch 里仍承载了只存在于该批次的 source payload / replay chain；它必须先被 replay/absorb 到当前 `develop`，或明确 return 到来源 feature lane，删除才安全

2. `feature/delegated-continuation-prompt-consumption-visibility-20260323`
- 已收敛成 verification-only closeout lane
- 当前可以视为 merge-ready
- 但仍不可 delete；当前 specimen 的唯一剩余 gate 是 `pre-tests.md` 已显式声明的 merge 后 `develop` post-merge acceptance，并按 `pre-tests.md` 留下 application-native real-environment testing evidence；这只是当前 specimen 的剩余 gate，不是通用默认链路

3. `feature/manager-scheduler-capacity-and-queueing-20260323`
- 仍是 active pre-brainstorm candidate
- 不但不能 delete，连 issue materialization 也还没到
- 下一门已明确：先冻结 capacity owner、queue reconcile winner、busy-worker relaunch scope，再用一轮 `develop` dogfood 证明 queue / capacity / busy-worker 行为稳定

4. `feature/manager-delegated-continuation-stall-materialization-20260323`
- 仍是 active pre-brainstorm followthrough
- 明确不可 delete
- 剩余缺口已收紧成一条 proof chain：`stalled delegated continuation intake id -> current manager prompt cycle -> consumed event anchor -> no-new-continuity/handoff stall verdict`

5. 另外 6 棵“merged + clean”的历史树也全部未过 delete gate
- 共通缺口不是 Git 状态，而是 lifecycle closeout evidence
- 它们分别仍停在 `in_verification`、`needs_research`、`pending://issue-materialization`，或缺少 explicit cleanup / retire evidence

这轮 audit 直接说明：未来 delete guard / hook 至少要能拒绝以下误删：
- 只因 `merged + clean` 就删树
- 只因 issue `completed` 或局部 loop 收口就删最后一个 owner tree
- 只因 stale batch 已停止运行就删除仍承载 replay/source evidence 的验证批次

- worker continuity 先作为真相面：
  - `lane_phase_progress=advanced|unchanged`
  - `lane_stall_reason=verification_only_repeat|continuity_refresh_repeat|none`
  - `lane_stall_streak=<int>`
- manager continuity 消费后决定：
  - `next_action=freeze|cleanup|merge|delegate`
  - 是否把当前 prompt 放入 `superseded_worker_prompts`
  - 是否释放 queue / capacity 给下一 lane
- `manager-worker-launch-state.env` 只镜像最终结果，不负责自己计算 stall

## 必须硬限制的边界

- stale `pre-test-merge` 不得继续作为当前验证真相面
- `pre-test-merge` 不得因 watchdog 恢复而自动恢复成“继续可消费的 batch”
- manager 在 stale batch 上不得继续输出普通 `verification`
- worker 在 verification-only / continuity-refresh 多轮无新阶段推进后，必须退出到 manager decision
- `cleanup / retire / rebuild / replay source feature` 只能由 manager 做生命周期决定
- 不得因为 issue 已标 `completed`、某个 loop 已收口、或某个 agent/skill 已完成单轮交付，就删除最后一个 owner worktree
- 只有当当前树已达到 cleanup gate、进入 `verified-retirable`，并最终执行到 `retired`，才算这棵树真的收口
- 若未来实现 delete guard / hook，它应兜住 branch/worktree 删除动作，只允许在 `completed`、testing closeout、cleanup gate、`verified-retirable` 都已满足时继续执行；否则只能拒绝删除并要求回到三层 loop 继续推进
- merge 后未完成的 worktree 也必须有可恢复 owner：
  - 要么有 active delegated continuation / cleanup lane
  - 要么在 milestone / issue 上显式挂起并写清下一跳
  - 否则不得删除该树，也不得宣称“任务已做完”

## 应保留 AI 自主的边界

- 在合法 lane 内先看哪个池、先补哪份文档、先跑哪组测试
- 在 pre-brainstorm / IBM / verification writeback 内如何组织证据与叙述
- 在不越过 lifecycle gate 的前提下，自主决定单轮收口顺序
- 在不阻塞 primary manager handoff 的前提下，可对二次核对、日志诊断、候选评审使用 subagent

## subagent 边界补充

- 主管应使用 subagent 的场景：
  - 不阻塞首个 manager continuity / worker handoff 的二次核对
  - 高风险 candidate 的独立 acceptance review
  - 多个互不冲突的日志诊断、文档对读、只读代码库审查
- 主管不应把以下职责外包给 subagent：
  - 首个 `ownership + restart_point + next_action` 判断
  - primary manager continuity / worker prompt 的首次落盘
  - stale batch 的最终 lifecycle decision
- 因此，当前 Freely 更像“主管先写可消费 handoff，再可选地用 subagent 加速核对”，而不是“先开很多 subagent，再等它们决定主管该做什么”

## 当前预研判断

- `C-20260322-1801-B` 不该再被理解成“给 pre-test-merge 加一个 stale 标记”
- 但它也不该继续包住 `worker self-loop exit`
- 当前更稳的路线是：
  - `C-20260322-1801-B` 收窄为 `stale pre-test-merge governance capability`
  - 新开平行 candidate 承接 `worker self-loop exit / scheduling closeout`
- 这轮还补清了一个容易误判的边界：milestone 里的 issue `completed` 不等于 worktree 已可删除；若 merge / cleanup / `verified-retirable` / `retired` 链条未闭合，仍不得删除最后一个 owner worktree
- 在 machine-readable stale state、manager lifecycle transaction、runtime consumption gate 还没冻结前，不应直接实现局部 patch，否则很容易继续出现“修了 watchdog，又退回 manager/worker 自环”的倒退

## 最新 continuation 收紧

- `20260324-001134-continuation-dogfood-watchdog-fr` 没有引入新的平行问题；它只是把 `C-20260322-1801-B` 的最小 contract 再钉实一层
- 当前 worker lane 吸收的是同一条 human continuation 之下的 superseding delegated continuations `20260324-024929`、`20260324-024942`、`20260324-025910`、`20260324-030713`；它们都没有改写 route_kind，仍然是 `continuation -> pre_brainstorm`
- 当前稳定结论不是“这个能力落在某一个组件里”，而是：
  - `manager continuity` 作为唯一 stale-batch truth surface
  - `runtime launch state` / `live-status` 只做 mirror + hard gate
  - `branch/worktree governance` 只消费已有 judgement/evidence 做 replay / retire / delete gate
- 因此，这条能力现在应被理解成一个 combined minimal contract，而不是单点 `runtime status` 补丁、单点 `manager patrol` 补丁，或单点 `branch-management` 文案增强
- 本轮 superseding delegated continuation 又把 combined minimal contract 收紧成 5 条最小语义：
  - stale `pre-test-merge` 一旦被 manager 判定，就不得再充当 active verification truth surface
  - manager patrol 必须输出 `stale_batch -> retire/rebuild` 或等价 lifecycle decision，不能静默继续普通 verification
  - runtime 只消费 manager 已写出的 stale judgement，并以 hard gate 拒绝 stale batch 按普通 active validation surface 启动
  - watchdog 仍只负责 runtime recovery，不负责裁决 validation batch legitimacy
  - 若同一能力仍需继续验证，必须 replay 来源 feature 集合到 fresh `pre-test-merge` batch，而不是复用旧 stale batch
- 因此当前问题的实现落点也继续保持为 combined minimal contract，而不是在 `runtime status`、`manager patrol`、`branch-management` 三者中单选其一：
  - `manager continuity` 负责唯一 machine-readable 真相块
  - `runtime launch state` / `live-status` 负责 mirror 与 hard gate
  - `branch/worktree governance` 负责 replay / retire / delete gate 消费
- supporting pools 也都在强化同一个结论：
  - 现有 completed issue `I-20260322-1801` 明确只负责职责定义，不负责 stale-batch capability materialization
  - 语义审计 pre-brainstorm 只把这条能力当 supporting evidence，没有把它升级成 IBM
  - 当前仓库没有专门的 `docs/recovery/**`，而 `docs/progress/**` / review / test 只提供 delete gate、`verified-retirable` 和 acceptance bridge 的 supporting evidence，没有给出足以进 IBM 的稳定 contract
  - human chat / session evidence 当前只体现为 delegated continuation intake 与当前 run 的 prompt evidence；这些证据都要求继续吸收进现有 candidate，而不是新开 lifecycle
  - 当前 `freely live-status --project <this-worktree>` 也只证明 continuation 已被当前 worker 吸收：`last_consumed_delegated_continuation_ids` 已覆盖 `20260324-024929/024942/025910/030713` 等 intake，`pending_delegated_continuation_ids=none`，而 `latest_manager_continuity_generated=unavailable` / `latest_manager_continuity_consumed=unavailable` 继续说明 manager truth artifact 仍未稳定到可直接拿来做 IBM 输入
  - handoff 要求读取的 `manager-continuity-20260324-021853.md` 在当前 worktree 中并不存在，因此本轮不能把某份缺失的 manager truth artifact 当成“已经稳定可消费”的 IBM 输入；它只能继续作为 contract freeze 的缺口记录
- 当前 handoff 的 delegated continuation judgement 仍与 runtime 事实相容，但最新 runtime 真值已经落到新的 fresh run，而不是继续停留在 handoff 中的旧轮换元数据：
  - handoff 里的 `context_compacted` / `402 deactivated_workspace` 仍应视为 runtime-owned 历史触发信号，而不是新的 canonical owner
  - 当前 `freely live-status --project <this-worktree>` 仍显示 `last_launch_kind=fresh_with_handoff`、`last_rotation_reason=context_compacted`、`current_prompt_has_delegated_continuation=1`
  - 同时 `pending_delegated_continuation_ids=none`、`last_consumed_delegated_continuation_ids` 已覆盖 `20260324-024929/024942/025910/030713` 等 superseding intake，且 `latest_manager_continuity_generated/consumed=unavailable`
  - 这说明当前 worker 的确已消费 superseding delegated continuations，但 `live-status` 仍只是当前 run 的消费镜像，而不是可替代 manager continuity 的长期 truth source
- 当前 assigned worktree 的 hygiene 复核仍不改变路由：本轮开始时 `git status --short --branch` 一度显示当前 canonical doc-loop writeback 留下的 3 个 dirty 文件（`docs/milestones.md`、`brainstorms.md`、`candidates.md`），随后经 `git update-index --refresh` 校正回 clean；`git rev-list --left-right --count develop...HEAD` 当前为 `74 27`，而 handoff 要求读取的 `.freely/run/manager-continuity-20260324-021853.md` 仍然缺失。这说明本轮无需先切 checkpoint 或分流无关改动，但它只是 doc-loop continuity evidence，不是新的 promotion 信号
- 当前 same-session continuity refresh 继续把 runtime 事实收窄为“delegated continuation 已消费，但 runtime 仍只是 mirror”：
  - `git status --short --branch` 的假脏信号已被 `git update-index --refresh` 校正，`git rev-list --left-right --count develop...HEAD` 现为 `74 27`
  - 当前 `live-status` 仍显示 `last_launch_kind=fresh_with_handoff`、`last_rotation_reason=context_compacted`，同时 `current_prompt_has_delegated_continuation=1`、`pending_delegated_continuation_ids=none` 与同一组 consumed delegated ids 保持不变
  - 因此 handoff 里的 `context_compacted` 既是历史 continuity guard 输入，也是当前 runtime run 仍在暴露的事实；这不会改变 owner，只会再次证明 runtime mirror 不能替代缺失的 manager continuity truth artifact
- 最新 supporting-pool ownership check 也没有改写 owner：
  - `I-20260322-1801` 与其 verification 只继续声明 lifecycle management capability 是后续独立 lifecycle
  - `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md` 只拥有 latest manager continuity consumption timing，不拥有 stale-batch retire/rebuild governance
  - 当前 `live-status.current_focus.prompt_file` 指向的 run prompt 继续把这条 lane 路由回 `C-20260322-1801-B`，而不是给出更强的 IBM owner
- 最新一轮独立 acceptance review 继续维持 `stay_pre_brainstorm`，并把 blocker 收窄为：当前选择“不新增 machine-readable pointer”这条路线时，必须先把“`retire_evidence_ref` + `remaining_cleanup_requirement` 就是 canonical machine-readable absorption pointer”显式冻结成 contract；冻结之后，还要再过一轮独立 acceptance review，确认 frozen minimal contract 才足以 materialize
- 当前 run 的 `current_focus.prompt_file` 与 `live-status` 一起证明 superseding delegated continuation bundle 已在当前会话被消费，而不是仍停留在 queued/pending handoff；但它依旧只证明 worker consumption，不能替代缺失的 manager continuity truth artifact
- 最新 explorer ownership scan 进一步坐实 supporting-pool 边界：
  - `docs/milestones.md` 仍把 `C-20260322-1801-B` 保留为 `candidate / in_pre_brainstorm`
  - completed issue 与其 IBM brainstorm 继续把 lifecycle management 留作后续独立 lifecycle
  - `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md` 只拥有 continuity consumption gap，不拥有 stale-batch governance owner
  - `.freely/run/session-state.env` / prompt evidence 只证明 worker consumption mirror，不足以替代 manager continuity 成为 IBM 输入
- 当前 fresh explorer canonical-owner recheck 也没有改写结论：
  - 只读复核再次确认 milestone、completed issue、semantic audit 与 progress 都没有生成新的 committed issue / IBM owner
  - 当前 `live-status` / runtime 仍只是 continuation-consumption mirror，而 `.freely/run/manager-continuity-20260324-021853.md` 继续缺失
  - 当前 worktree 只脏 2 个 canonical doc-loop 文件；这说明当前 lane 仍在进行受限 continuity writeback，但 dirty 本身仍不构成 checkpoint / reroute 或更强 owner 证据
- 当前 fresh-session supporting-pool owner recheck 继续维持同样结论：
  - `docs/milestones.md` 仍只把 `C-20260322-1801-B` 保留为 `candidate / in_pre_brainstorm`
  - completed issue、semantic audit 与 `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md` 仍只提供 supporting evidence，不吸收 stale-batch governance owner
  - `.freely/run/manager-continuity-20260324-021853.md` 仍缺失，因此本轮最新事实只说明当前 writeback 继续需要保留在 candidate truth 中，而不是升级成 IBM 输入
- 当前 latest supporting-pool independent gap check 继续把边界压回同一点：
  - supporting pools 里最强的正式 artifact 仍只是已完成的 `I-20260322-1801`，但它的 `Next` 仍明确把 lifecycle management capability 留作后续独立 lifecycle，而不是当前已 materialize 的 IBM owner
  - semantic audit 继续只承担 absorbed supporting evidence，neighboring progress doc 继续只拥有 delegated-continuation consumption timing，因此 supporting pools 仍不足以绕过 `C-20260322-1801-B` 直接升格
  - 这让最小剩余 gap 保持不变：仍需把 stale detection / retire / rebuild 如何 materialize 为 dedicated issue contract 冻结清楚，而不是从 supporting pools 反推
- 当前 post-handoff read-only subagent reconfirmation 同样没有改写 owner：
  - semantic audit 仍只作为 supporting evidence，未把这条 lane 升级成 committed issue / IBM owner
  - progress 仍只拥有 latest manager continuity consumption timing，而不拥有 stale-batch retire / rebuild governance
  - 最小 freeze gap 继续只剩 fresh-batch absorption 的 machine-readable pointer 是否需要额外落点，或“无需额外 pointer”的等价 contract 是否已足够稳定
- 最新 supporting-pool boundary check 继续把 completed issue 的 `pre-tests.md` 与 verification review 留在 supporting pool：
  - 它们只加强 `I-20260322-1801` 已完成 issue 的 acceptance / quality gate，不生成新的 stale-batch capability owner
  - 这进一步说明当前 lane 还不能靠 completed issue 的下游验收文档被吸收到 IBM；canonical owner 仍然只能是 `C-20260322-1801-B`
- 最新 fresh-session IBM-readiness check 继续维持同样结论：
  - 最强 canonical owner 仍是 `C-20260322-1801-B` 与其 matching milestone candidate entry，而不是任何 completed issue / acceptance-first supporting pool
  - freeze gap 仍未缩小到可 materialize：fresh-batch absorption 还需要额外 machine-readable pointer，或把“`retire_evidence_ref` + `remaining_cleanup_requirement` 已足够”的等价 contract 冻结并经独立 review 证实
  - `specimen-S1/S2/S3` 仍要继续证明 delete-eligibility chain 与 issue completion chain 分离，runtime/live-status 也仍只是 continuation-consumption mirror
- 仓库内没有新的 github issue 落点把该问题升级成外部已定界 issue；`PROJECT_INTENT` 只继续要求扫描这些池，而没有改写本 candidate 的 owner
- 这轮按 `lead-agent -> context-source-skill -> doc-pre-brainstorm-execution` 重放首跳后，优先级仍然先落在 milestone + supporting pools，而不是 runtime 实现面：
  - `milestones.md` 仍把 `C-20260322-1801-B` 保留在 `candidate_issues`
  - completed issue、semantic audit、progress/review/test、human continuation 与 `live-status` 都只提供 supporting evidence，没有给出新的 canonical owner
  - `tools.md` 也没有改写工具选择：当前最匹配的仍是 `codex`，因为本轮工作仍是当前 feature worktree 内的 canonical doc-loop writeback
- 因此，这轮“下一跳”虽然仍会留下 `next_prompt` 作为可追溯中间产物，但真实执行不能停在 handoff 文本：`selected_tool=codex` 与当前 `AI_TOOL=codex` 相同，必须在当前会话内继续完成 `doc-pre-brainstorm-execution` writeback

## materialization 前仍缺的验证矩阵

- manager 侧验证：
  - stale batch 一旦被判定，manager continuity 必须输出 `retire/rebuild/freeze` 一类 lifecycle decision，而不是继续普通 verification
  - `acceptance_contract_state/source/blocker` 必须能把 `pre-tests.md` 质量缺口投影出来，而不是让 runtime 自己猜
- runtime 侧验证：
  - stale batch 不能再正常 boot 成 active verification surface
  - superseded queued worker prompt 会留下 machine-readable consumed/applied evidence
- branch/worktree 侧验证：
  - 若同一能力仍需验证，必须 replay 来源 feature 到 fresh `pre-test-merge` batch
  - delete gate 必须能拒绝至少三类误删：`merged + clean`、issue `completed`、stale batch stopped 但仍承载 replay/source evidence
- 在这些验证矩阵没有冻结前，仍不应进入 IBM materialization

## combined minimal contract v0

- 这轮先冻结到字段级草案，但仍保留在 pre-brainstorm：
  - manager continuity 是唯一 stale-batch truth surface
  - runtime launch state / `live-status` 只能 mirror manager judgement，并负责 hard gate
  - branch/worktree governance 只能消费 manager 已写出的 judgement / evidence，不得自行重算 stale legitimacy
- manager continuity 最小字段块：
  - `validation_batch_id`
  - `validation_batch_state=active|stale|retired`
  - `validation_batch_mode=normal|read_only_cleanup|rebuild_planning`
  - `stale_reason=develop_advanced|protected_env_diverged|cleanup_chain_broken|superseded`
  - `lifecycle_decision=continue_verification|freeze|retire|rebuild|replay_sources`
  - `integration_target`
  - `source_batch_base`
  - `replay_source_manifest`
  - `replay_order`
  - `retire_evidence_ref`
  - `remaining_cleanup_requirement`
  - `acceptance_contract_state=grounded|incomplete|not_applicable|unavailable`
  - `acceptance_contract_source`
  - `acceptance_contract_blocker`
  - `superseded_worker_prompts`
  - `superseded_worker_prompts_applied_at`
- runtime mirror / hard gate 最小消费面：
  - 只镜像 `validation_batch_state`
  - 只镜像 `validation_batch_mode`
  - 只镜像 `lifecycle_decision`
  - 只镜像 `acceptance_contract_state`
  - 当 `validation_batch_state=stale` 且 `validation_batch_mode!=normal` 时，拒绝把该 batch 作为普通 active verification surface 启动
  - 当 `superseded_worker_prompts_applied_at` 缺失时，不得宣称旧 queued prompt 已被完全吸收
- branch/worktree governance 最小消费面：
  - `replay_source_manifest`
  - `replay_order`
  - `retire_evidence_ref`
  - `remaining_cleanup_requirement`
  - `lifecycle_decision`
  - `validation_batch_state`
  - 只在 manager 已判定 `rebuild|replay_sources|retire` 后，继续做 replay / cleanup / delete gate 判断

## delete gate refusal samples

## delete gate input combination v1

- delete gate 不看 `merged + clean` 单点，不看 issue `completed` 单点，也不看 stale batch 已 `stopped` 单点
- 当前冻结的最小输入组合只有两类：
  - issue completion chain 输入：
    - `done_ibm`
    - `pre-tests.md` 质量 gate
    - dev / verification writeback
    - testing closeout evidence
    - `phase_state=completed`
  - delete eligibility chain 输入：
    - merge evidence
    - cleanup evidence
    - `verified-retirable`
    - delete guard decision
    - `retired`
- 若 `pre-tests.md` 显式声明 `post-merge acceptance`，它才作为 delete eligibility chain 的附加必经输入；未显式声明时，不得默认要求它
- stale validation batch 还要附加读取：
  - `validation_batch_state`
  - `lifecycle_decision`
  - `replay_source_manifest`
  - `retire_evidence_ref`
  - `remaining_cleanup_requirement`
- 也就是说，当前 delete gate v1 的冻结目标是：
  - issue completion chain 证明“issue 可 completed”
  - delete eligibility chain 证明“worktree 可 delete”
  - stale-batch 证据证明“source / replay / retire 已被当前 canonical owner 吸收”
- 三者少任何一个，都只能 `delete_denied`

- `specimen-S1 merged-clean-only`
  - 最小输入：
    - worktree `merged + clean`
    - issue 可为 `completed` 或 `in_verification`
    - `retire_evidence_ref=unavailable`
    - `remaining_cleanup_requirement` 仍包含 `cleanup_evidence`、`verified-retirable` 或 `retired`
  - 必要 supporting evidence：
    - 当前 manager continuity `Validation batch governance:` `v1` 块
    - closeout / cleanup 证据中不存在 `verified-retirable` 与 `retired`
  - 期望结论：`delete_denied`
- `specimen-S2 completed-only`
  - 最小输入：
    - issue `phase_state=completed`
    - merge 已发生或已计划，但 `acceptance_contract_blocker!=none`，或 `remaining_cleanup_requirement` 仍包含 `cleanup_chain`
    - 若 `pre-tests.md` 显式声明 `post-merge acceptance`，则它也可出现在 `remaining_cleanup_requirement`
    - 没有 `verified-retirable` 或 `retired` 证据
  - 必要 supporting evidence：
    - issue / pre-tests / code-review 指针能证明 `completed` 不是 delete 放行条件
    - 当前 continuity 块能把 acceptance 缺口或 cleanup 缺口投影出来
  - 期望结论：`delete_denied`
- `specimen-S3 stale-stopped-source-not-absorbed`
  - 最小输入：
    - `validation_batch_state=stale|retired`
    - `lifecycle_decision=rebuild|replay_sources|retire`
    - `replay_source_manifest` 非空
    - `retire_evidence_ref=unavailable`，或现有 evidence 仍不能证明 fresh batch 已吸收 source manifest
  - 必要 supporting evidence：
    - stale batch continuity 块
    - fresh batch / replay closeout 证据不存在，或未能指向 manifest absorption
  - 期望结论：`delete_denied`
- 当前 delete gate specimen 不另造新状态词；它们只证明 `Validation batch governance:` `v1` 块与既有 `completed` / cleanup gate / `verified-retirable` / `retired` 组合足以拒绝三类误删
- 当前 `specimen-S1/S2/S3` 的 freeze 目标也固定为三条拒绝语义：
  - `S1` 证明 `merged + clean` 从来不是 delete-eligible
  - `S2` 证明 issue `completed` 仍不能跳过 cleanup / optional post-merge acceptance / retirement chain
  - `S3` 证明 stale batch 即使 stopped，也不能在 source manifest 未被 fresh owner 吸收时删除

## pre-IBM validation matrix draft

- manager truth surface:
  - stale 判定后 continuity 必须从 `continue_verification` 切到 `freeze|retire|rebuild|replay_sources`
  - acceptance bridge 缺失时必须输出 `acceptance_contract_state=incomplete`
- runtime gate:
  - stale batch 不能以 normal verification mode 启动
  - superseded prompt 必须留下 applied evidence
- replay / retire governance:
  - 同能力续验时必须产出 fresh batch 计划，而不是继续消费旧 batch
  - replay source manifest / replay order / retire evidence 至少可被 manager 与 cleanup skill 共读
- delete guard:
  - 三类误删样例都能被拒绝
  - `completed` 只能作为 delete gate 输入之一，不能独立放行
- acceptance bridge:
  - `Issue + Brainstorm + PRD -> pre-tests.md` 缺口可稳定投影到 `acceptance_contract_state/source/blocker`
  - testing closeout 仍与 `pre-tests.md` 质量 gate 分离，不混成单一完成态

## 当前仍未冻结的点

- `stale_reason` 与 `lifecycle_decision` 是否需要更细枚举，还是保持最小集合
- `retire_evidence_ref` 与 `remaining_cleanup_requirement` 当前不能只靠默认理解支撑 future delete guard / hook 对 fresh-batch absorption 的稳定判断；当前已选路线是不新增额外 pointer，但必须把这组等价关系冻结成明确 contract，并补上独立 review evidence，证明 worker-consumption mirror 不会被误读成 absorption proof
- 这份 v0 contract 是否已足够小到能单独 materialize 成 IBM，而不是还需再做一轮独立 acceptance review
- 当前 fresh-session 对 `constitution-guard` / `laws-enforcer` 与 `I-20260322-1801` 的再读取也继续收紧同一个结论：宪法/法律只允许当前 worker 在 assigned feature worktree 里继续维护 candidate / milestone truth，而已完成的职责定义 issue 与其 `pre-tests.md` 只提供 acceptance bridge 的 source truth，不会把 stale-batch capability 直接升级成 IBM owner

## 本轮独立 review 结论

- 最新只读 explorer IBM-readiness 复核没有推翻上一轮 writeback：supporting pools 仍只支持 `stay_pre_brainstorm`
- 当前已经有一轮 supporting-pool 独立对读，但它给出的结论仍是“继续保留 `combined minimal contract v0`，不要直接开 IBM”
- 最新 concrete supporting-pool patrol 还把证据源钉得更实：`docs/milestones.md` 继续把 `C-20260322-1801-B` 保持在 `candidate/in_pre_brainstorm`，`I-20260322-1801` 继续只作为已完成的职责定义 issue，`20260322-1802` 继续只是 supporting evidence，相邻 progress 文档只拥有 continuity/launch/cleanup-closeout lane，缺失的 `.freely/run/manager-continuity-20260324-021853.md` 仍只是 provenance gap
- 当前 fresh session 的首跳闭环复核也没有改写这个结论：重新读取治理入口、workspace agent/skills、candidate/issue/supporting pools、`git status --short --branch`、`git rev-list --left-right --count develop...HEAD` 与 `freely live-status --project ...` 后，当前 worktree 的假脏信号已被 `git update-index --refresh` 校正，`develop...HEAD` 当前为 `74 27`，runtime 仍只暴露 `fresh_with_handoff + context_compacted` 的 continuation-consumption mirror，而不是新的 canonical owner
- 最新并行 explorer 又把 completed issue 栈的边界钉得更死：`I-20260322-1801` 的 `issue + brainstorm + prd + pre-tests` 一起复核后，仍明确把 runtime/status freshness、stale-batch detection capability 与 machine-readable surfacing排除在当前 IBM scope 外，只把它们留给 follow-on lifecycle；因此这条 lane 仍不能被 completed issue 栈吸收
- 当前同轮 hygiene 预检还纠正了一个索引漂移假象：`git status --short --branch` 最初显示 3 个 canonical doc-loop 文件 dirty，但 `git update-index --refresh` 后 worktree 回到 clean，因此当前不存在需要先切 checkpoint commit 或分流无关改动的 hygiene blocker；这只收窄了“可以继续写 canonical doc-loop”的前提，不改变 route / owner 结论
- 新增的 explorer contract-freeze review 进一步收窄了顺序：应先冻结 manager continuity 固定语法与最小字段块，再用 delete gate refusal samples 证明其足以支撑 runtime gate 与 cleanup/delete 判断，而不是并行扩写更多子能力
- 最新 current-turn sufficiency-closeout explorer 也把 blocker 进一步压成单点：当前不再缺 owner 归属判断，也没有新的 IBM-ready competing owner；剩余最高价值 blocker 只剩一件事，即证明 frozen five-part proof bundle 是否已经足以把这条 combined minimal contract materialize 成单一 IBM issue
- 因此，`next_action` 不再是泛化的“先去做 review”，而是继续把 review 后仍未冻结的部分收紧成可 materialize 的 issue contract：
  - manager continuity 的 `Validation batch governance:` `v1` 固定承载语法与最小字段块
  - `specimen-S1/S2/S3` 对应的 refusal specimen / evidence 组合，用于证明这组字段已足够支撑 runtime gate 与 cleanup/delete 判断
  - `retire_evidence_ref` / `remaining_cleanup_requirement` 是否仍需额外补强，才能支撑 cleanup skill、future hook 与 fresh-batch absorption 共读
- 在这三块还没冻结前，当前 lane 仍应停在 `continuation -> pre_brainstorm`
- 本轮收口后，已冻结的是：
  - `Validation batch governance:` `v1` 固定块与 key 顺序
  - delete gate 输入组合 v1
  - `specimen-S1/S2/S3` 的最小拒绝语义
- 当前首跳工具选择也未变化：`tools.md` 继续把 `codex` 定位为同 worktree 的 repo read/write 工具，而当前任务仍是 candidate/milestone canonical doc-loop 写回，所以这轮必须在当前 `codex` 会话内继续第二跳，而不是把 `next_prompt` 当作结束信号
- 仍未冻结的只剩：
  - `Frozen equivalence: retire_evidence_ref + remaining_cleanup_requirement is the canonical machine-readable absorption pointer for fresh-batch followthrough, and no extra machine-readable pointer is required.` 已经写定并被当前 candidate 与 milestone 真源吸收；当前不再把它当成开放问题
  - 冻结后的最小 contract 是否已再过一轮独立 acceptance review，足以 materialize

## 需要冻结的开放问题

1. `pre-test-merge` 的唯一职责是什么。
2. `pre-test-merge` 哪些操作允许，哪些绝对禁止。
3. stale 的最低 machine-readable 判据是什么，以及由 manager 写到哪个真相面。
4. manager 的 lifecycle transaction 至少要包含哪些 manifest / evidence，才允许 retire 或 rebuild。
5. runtime gate 消费哪个字段，以及旧 queued prompt 如何 supersede。
6. `worker self-loop exit` 是否应单开 candidate，并用什么 phase-progress 规则定义停滞。
7. 哪些现有状态与证据组合才表示“继续推进三层 loop”，哪些组合才表示“可以进入 delete worktree”。
8. 最终 delete worktree / delete branch 门禁若要由 hook / guard 兜底，应该投影到哪一层，以及最小拒绝语义是什么。
9. combined minimal contract 的边界是否已经足够稳定，可以作为单一 issue materialization，而不是继续分散在 manager/runtime/cleanup 三处叙述里。
10. 独立 acceptance review 是否已经足够证明 supporting pools 都只支持 `stay pre_brainstorm`，而不是隐含要求现在就开 IBM。

## 当前 fleet 分类快照

- 这轮再次按当前仓库事实核对后，`develop` 根 runtime 仍显示 `activity_state=stalled_without_runtime`、`active_processes=none`；因此当前问题不是“没有剩余任务”，而是“剩余任务尚未被 runtime 继续消费”。
- 当前 worktree 不能再按 `merged + clean` 或 issue `completed` 直接判完成，必须继续按 canonical owner、issue completion chain、delete eligibility chain 三层分类。

### active owner，必须继续

- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-pre-test-merge-lifecycle-management-followthrough`
  - canonical owner: `C-20260322-1801-B`
  - loop: `doc-loop`
  - current state: `in_pre_brainstorm`
  - reason to continue: stale batch governance、delete gate、fresh-batch absorption 仍未冻结到可 IBM
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-application-native-observability-planes`
  - canonical owner: `C-20260324-0415-A`
  - loop: `doc-loop`
  - current state: `in_pre_brainstorm`
  - reason to continue: acceptance-evidence schema canonical home、shared deep-ref compatibility rules 仍未冻结
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-scheduler-capacity-candidate-replay`
  - canonical owner: scheduler capacity replay candidate
  - loop: `doc-loop`
  - current state: `in_pre_brainstorm`
  - reason to continue: fresh `develop`-based dogfood proof 仍未做完，不能直接 IBM
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-manager-delegated-continuation-stall-materialization`
  - canonical owner: stalled continuation candidate
  - loop: `doc-loop`
  - current state: `in_pre_brainstorm`
  - reason to continue: explicit stalled specimen -> prompt cycle -> consumed anchor 证明链仍未冻结

### completed issue / in-verification，但还不能删树

- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-delegated-continuation-prompt-consumption-visibility`
  - canonical issue: `I-20260322-0445`
  - issue state: `completed`
  - delete state: not delete-eligible
  - reason: cleanup followthrough 仍未闭合；`completed` 只代表 issue completion，不代表 `verified-retirable` / `retired`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-global-watchdog-earliest-reset-sleep-revive`
  - canonical issue: `I-20260318-1630`
  - issue state: `in_verification`
  - delete state: not delete-eligible
  - reason: manager merge review / verification closeout 仍是当前 canonical next action

### evidence-only / stale batch，不再作为执行面

- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/pre-test-merge`
  - lifecycle role: stale evidence-only validation batch
  - allowed role: replay/source/retire evidence
  - forbidden role: active verification surface
  - reason not to delete: stale source manifest / replay evidence 仍未被 fresh owner 明确吸收
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-manager-scheduler-capacity-and-queueing`
  - lifecycle role: replay source / historical evidence
  - reason not to treat as active: replay 已转到 `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-scheduler-capacity-candidate-replay`

### merged to develop，但只进入 cleanup-pending pool

- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-manager-worker-launch-idempotency-queue-promotion`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-manager-worker-launch-state-relaunch-recovery`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-manager-worker-prompt-contract-and-launch-consumption`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-three-loop-dogfood-flow-alignment`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-worker-stall-recovery-during-active-ai`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-launch-state-consumed-truth-reconcile`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-launch-state-frozen-prompt-state-reconcile`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-launch-state-frozen-queue-drift`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-primary-handoff-materialization-stall`
- `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-worker-count-fleet-truth-reconcile`
- rule:
  - 这些树已被 `develop` 吸收，但当前只可进入 cleanup-pending / evidence-only pool
  - 未经 `cleanup evidence`、`verified-retirable`、delete guard、`retired` 组合校验前，不得删除
