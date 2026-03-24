# 预研头脑风暴：pre-test-merge-governance-lifecycle

## 背景

Freely 这次暴露出来的不是单纯的合并冲突，而是 `pre-test-merge` 的职责边界、允许用法、退出条件和批次生命周期都还不够清晰。

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
2. `pre-test-merge` 是临时预集成验证分支，不应固化为长期开发父分支。
3. 复杂集成、短周期验收、冲突收敛、发布前预演可以启用 `pre-test-merge`，但它必须有清晰的批次边界。

### 已确认的治理缺口

1. 还没有明确区分：
- `pre-test-merge` 只做验证
- `develop` 才是最终集成真相

2. 还没有明确回答：
- 一个 `pre-test-merge` 批次什么时候 stale
- 哪些改动必须回到来源 feature worktree
- 哪些改动可以直接推进到 `develop`

3. 还没有形成完整的能力化输出：
- 不能自动解释当前批次归属
- 不能自动提示 stale batch
- 不能自动给出 promote / replay / retire 建议

## 问题定义

需要一条更完整的治理路线，回答：

> 当 Freely 启用 `pre-test-merge` 做预集成验证时，应该如何定义它的职责、允许的操作、失效条件、生命周期结束条件，以及它与 `develop` 的 promotion 关系，才能既保住有效实现，又不把旧批次误当成当前真相？

## 关键张力

1. `pre-test-merge` 是临时验证批次，不该长期承载实现真相。
2. 但多个 feature 的组合行为只能在它这里被看见，不能简单废掉它。
3. `develop` 是最终集成主线，但主线在前进时不能被旧批次的语义拖回去。
4. Git 本身不能天然表达 batch 生命周期，所以 Freely 需要显式治理与状态留痕。

## 预研方向

### 方向 A：明确 `pre-test-merge` 的职责模型

- 它只负责组合验证、冲突暴露、promotion 预演
- 不负责长期保存事实真相
- 不作为新的 feature 开发父分支
- 不作为默认回收旧实现的来源

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
- 是否能安全 promote，还是只能 replay 来源 feature

## 预期落点

- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/pre-brainstorms/**`
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
- 承载语法也要冻结成固定可解析块，而不是自由叙述。当前建议在 manager continuity 内加入固定标题块：
  - `Validation batch governance:`
  - 后续每行固定 `- key: value`
- runtime 只解析这个块，不从普通自然语言段落推理

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
  - `pre-tests.md` 质量 gate：是否已经把 issue-level acceptance、integration target、`pre-merge` / `post-merge acceptance`、protected branch 只做验证的边界写清
  - testing closeout gate：这些 acceptance 是否真的被执行并留下可恢复 evidence
- testing closeout 默认优先：
  - integration / end-to-end evidence
  - application-native real-environment testing evidence
  - 最后才是局部代码级或纯单测证据
- `phase_state=completed` 只能表达 issue-level completion；它不等于 worker/agent/skill lane 已完全收口，也不等于 branch/worktree/topic 已 fully closed
- 内循环完成、外循环完成、单个 agent/skill 的局部完成，都不能直接当作“任务做完”
- 真正的 topic closeout 还要继续经过：merge / post-merge acceptance / cleanup evidence / owner continuity 全部闭合
- “application-native real-environment testing” 指当前应用自己的真实入口、真实交互面、真实集成路径，而不是抽象脚本替身
- 在 Freely 自举场景里，它当前的具体形态才是：
  - `./bin/freely start`
  - `./bin/freely chat --project <project-root> <message>`
  - 通过 chat interruption 派发真实任务、观察 manager/worker/worktree 生命周期、检查 merge / cleanup / next-task scan 是否真的发生
- 因此，后续任何 stale governance / worker self-loop / retirement honesty 的实现，都不能只用静态文档 diff 或局部脚本测试宣布完成；至少要经过：
  - `pre-tests.md` 质量复核
  - 集成测试
  - application-native real-environment testing
- 若缺少这些 evidence，manager 不应把 lane 判成 `completion_verification done` 或允许 worktree retirement

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
- 这轮还补清了一个容易误判的边界：milestone 里的 issue `completed` 不等于 topic 已 fully closed；若 merge / cleanup / next owner continuity 未闭合，仍不得删除最后一个 owner worktree
- 在 machine-readable stale state、manager lifecycle transaction、runtime consumption gate 还没冻结前，不应直接实现局部 patch，否则很容易继续出现“修了 watchdog，又退回 manager/worker 自环”的倒退

## 需要冻结的开放问题

1. `pre-test-merge` 的唯一职责是什么。
2. `pre-test-merge` 哪些操作允许，哪些绝对禁止。
3. stale 的最低 machine-readable 判据是什么，以及由 manager 写到哪个真相面。
4. manager 的 lifecycle transaction 至少要包含哪些 manifest / evidence，才允许 retire 或 rebuild。
5. runtime gate 消费哪个字段，以及旧 queued prompt 如何 supersede。
6. `worker self-loop exit` 是否应单开 candidate，并用什么 phase-progress 规则定义停滞。
7. `issue completed`、`loop closed`、`topic fully closed` 三层完成语义，分别由哪些 artifact 和 gate 支撑。
