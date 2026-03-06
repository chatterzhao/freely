# 研究：issue 绑定头脑风暴路由与兜底门禁

## Context

- 日期：2026-03-06 02:48 UTC
- 触发：当前治理已经区分两类头脑风暴：
  - 非 issue 前置收敛：`docs/pre-brainstorms/`
  - 基于已有 issue 的 IBM 头脑风暴：`docs/epics/{epic}/{story}/brainstorms/`
- 现状问题：规则已存在于文档，但缺少统一入口、显式元数据和提交前兜底校验，AI 与人类都可能把 brainstorm 文档放错位置。
- 附加约束：Freely 正在自举开发 Freely，必须在自己的 worktree / brainstorm / issue 治理下收敛本规则。

## 需要回答的问题

1. 如何判断一个 brainstorm 是“基于已有 issue”还是“尚未形成 issue 的前置研究”？
2. 如果当前任务是之前任务的连续开发，但没有新的 issue 文档，是否仍应留在原有 issue 路径，还是进入新的 pre-brainstorm？
3. 哪个环节最适合作为主判断入口：
   - 会话开始
   - worktree 创建后
   - brainstorm 文档创建时
   - add/commit 前
   - doc-loop 执行前
4. 兜底应该做到什么程度：
   - 只提示
   - 阻止提交
   - 自动迁移到正确路径
5. 文档元数据最小集合应该是什么，才能让 hook / script 低成本判断？

## 当前观察

### 1. 已有规则来源

- `AGENTS.md`
  - 非 issue -> `docs/pre-brainstorms/`
  - 基于 issue -> `docs/epics/{epic}/{story}/brainstorms/b-{issue-name}.md`
- `PROJECT_INTENT.md`
  - chat / review / 新问题 先进入 `pre-brainstorms`
  - issue 绑定产物进入 `epics/...`
- `doc-loop-execution`
  - `IBM` 负责 issue 接入、brainstorm、mapping

### 2. 执行缺口

- `.githooks/` 目前没有检查 brainstorm 路由是否正确
- `bin/bmad-check` 与 `bin/freely` 仍引用旧 `docs/brainstorms/` 路径，说明旧工作流残留尚未清理
- 当前没有统一的 brainstorm 元数据契约，导致脚本很难可靠判断“是否基于 issue”

### 3. 风险

- 如果只靠路径名或文件名猜测，会出现误判
- 如果在 pre-commit 做过重自动迁移，会把错误变成隐蔽状态
- 如果没有显式证据字段，AI 会继续凭上下文模糊判断，稳定性差

## 初步判断框架

### A. 默认文档落位原则（不是总任务路由）

这里先约束的是 **brainstorm 文档应该落在哪个目录**，而不是整个任务后续要走哪条执行流。

- **没有明确 issue 证据时，brainstorm 文档默认落到 `docs/pre-brainstorms/`**
- **只有有明确 issue 证据时，brainstorm 文档才允许落到 `docs/epics/.../brainstorms/`**

原因：
- 错误地把研究放进 `pre-brainstorms` 的代价较低
- 错误地把研究放进正式 issue/story 目录会污染正式执行链路

注意：
- 这条只解决“brainstorm 文件放哪里”
- **它不能单独决定总任务路由**
- 总任务路由仍要结合 `context + milestone + status + boundary + runtime`

### B. “基于 issue” 的可能证据

候选证据：
1. 文档元数据里明确存在 `source_issue_path`
2. 创建命令显式传入 `--issue <path>`
3. 当前任务上下文明确绑定某个 issue 文档路径
4. 该 brainstorm 文档位于某个 story 目录下，并引用该 story 下的 issue 文档

待决问题：
- 是否需要允许“基于 milestone、但还未形成 issue”的路径？
- “之前任务的连续开发”是否必须指回原 issue，而不是开新 pre-brainstorm？

### C. 需要区分的任务场景

这里要区分的是“当前上下文命中了什么对象、该对象当前处于什么状态”，而不是简单按“有没有 issue”二分。

1. 新问题 / 新讨论 / review 发现 / 对话中临时冒出的问题
   - 若未命中已有 issue/candidate：进入 `pre-brainstorms`
2. milestone 中已有 candidate，但尚未形成正式 issue
   - 继续研究流；通常仍由 `pre-brainstorms` 承载
3. 已有 issue，但当前仍需继续研究
   - 不一定回 `pre-brainstorms`
   - 若仍在原 issue 边界内：进入 issue-bound brainstorm（`epics/.../brainstorms/b-*.md`，属于 `IBM` 内的 `B`）
   - 若已超出原 issue 边界：新开 `pre-brainstorms`
4. 已有 issue，且已足够清晰但尚未开始
   - 不需要 pre-brainstorm
   - 应先做 milestone alignment，再进入 `doc-loop(IBM)`
5. 已有 issue，处于 `in-progress` / `done`
   - 需继续结合 runtime / completion 状态决定 continuation、recovery、completion verification 或 follow-up

### D. 触发层建议

1. **创建入口**：主判断入口
   - 最适合决定路径
   - 可以要求显式参数或上下文选择
2. **pre-commit**：兜底校验
   - 不负责主路由
   - 只阻止明显错误
3. **doc-loop / bmad-check**：一致性验收
   - 负责发现旧路径残留、元数据缺失、issue 绑定缺失

### E. 两层判断：文档落位 vs 总任务路由

当前研究需要把两个经常被混淆的判断拆开：

1. **brainstorm 文档落位**
- 看是否存在明确 issue 证据
- 决定文件放在 `pre-brainstorms` 还是 `epics/.../brainstorms/`

2. **总任务路由**
- 看 `context + milestone` 的语义命中结果
- 再结合状态、边界、运行时做 route decision
- 因此不能简化成：
  - `有 issue -> IBM`
  - `没 issue -> pre-brainstorms`

更准确的是：
- `没命中 issue/candidate` -> `pre-brainstorms`
- `命中 candidate/research-needed` -> 研究流
- `命中 issue 但仍需研究` -> issue-bound brainstorm 或新的 pre-brainstorm
- `命中 issue 且已清晰` -> `IBM`
- `命中 in-progress` -> continuation/recovery
- `命中 done` -> completion verification 或 follow-up pre-brainstorm

## 与现有工作方法的关系

当前感觉存在一个工作方法缺口：
- 已有“pre-brainstorms -> candidates -> issue-ready”
- 但“候选 issue -> 里程碑 -> 正式 issue -> IBM brainstorm”之间的操作指引还不够显式

需要进一步澄清的链路可能是：
1. `pre-brainstorms/<id>/brainstorms.md`
2. `pre-brainstorms/<id>/candidates.md`
3. 候选项晋升为正式 issue 文档
4. issue 被编入 milestone / story
5. 后续基于该 issue 的 brainstorm 才进入 `docs/epics/.../brainstorms/`

## 候选落地方向

### 方向 1：最小元数据契约 + 轻量 hook 兜底

- pre-brainstorm 禁止出现 `source_issue_path`
- issue-brainstorm 必须出现 `source_issue_path`
- `pre-commit` 只检查：路径与元数据是否匹配

优点：
- 简单
- 可解释性强
- 不需要太多自动推断

缺点：
- 仍需人工在创建时决定类型

### 方向 2：创建命令强制显式选择来源类型

例如未来统一入口：
- `freely brainstorm --pre ...`
- `freely brainstorm --issue <path> ...`

优点：
- 源头约束最强
- AI 和人类都更容易遵守

缺点：
- 需要先设计命令入口

### 方向 3：提交前基于 staged 文件做智能推断

- 如果新增了 `docs/epics/.../brainstorms/` 文件，检查是否引用 issue
- 如果新增了 `docs/pre-brainstorms/` 文件，同时出现 issue 元数据，则阻止

优点：
- 可作为兜底层

缺点：
- 单靠提交时推断，不足以作为主入口

## 测试思路（初稿）

### T1. 新 pre-brainstorm 允许
- 新增 `docs/pre-brainstorms/<id>/brainstorms.md`
- 无 `source_issue_path`
- 允许提交

### T2. issue-brainstorm 缺失 issue 绑定时阻止
- 新增 `docs/epics/.../brainstorms/b-*.md`
- 缺少 `source_issue_path`
- `pre-commit` 阻止

### T3. pre-brainstorm 错带 issue 绑定时阻止
- 新增 `docs/pre-brainstorms/.../brainstorms.md`
- 包含 `source_issue_path`
- `pre-commit` 阻止

### T4. 旧路径遗留检测
- 若新增或修改 `docs/brainstorms/**`
- `bmad-check` 或 hook 直接报错

## 暂时结论

当前更稳的路线应修正为：
1. 先定义最小元数据契约
2. 再把“创建入口”设计为显式选择 pre / issue
3. `pre-brainstorms` 结束后只产出 candidates，并原子同步进入 milestone
4. 后续所有活跃任务路由由 milestone 承担
5. 最后由 `pre-commit` 和 `bmad-check` 做兜底与验收

关键修正：
- `pre-brainstorms -> candidates -> route` 这个说法不再准确
- 更准确的是：`pre-brainstorms -> candidates -> milestone -> route decision`
- 因此 `candidates.md` 不再是调度主表，而是研究收敛产物
- milestone 才是唯一活跃任务路由面

但还需要继续收敛两件事：
- 连续开发 / recovery 如何可靠绑定原 issue
- milestone 与 issue 的状态机、默认路由和完成判定如何表达

## 新增讨论：里程碑应作为起始扫描层

### 1. 里程碑不是后置报表，而是前置扫描入口

当前更合理的理解是：
- `milestones` 不只是记录“已经决定的 issue”
- 它还应该是 AI / 人类开始扫描任务时的第一层入口之一
- 因为项目当前真正“准备做什么、尚未收敛什么、哪些问题需要继续研究”，都应该在 milestone 里有明确表达

因此扫描顺序更接近：
1. milestone
2. progress / recovery
3. issue 文档
4. pre-brainstorms candidates
5. review / test / chat / 新输入

其中 milestone 提供的是：
- 当前项目阶段
- 当前批次关注范围
- issue 是否已 ready
- issue 是否仍需研究
- issue 在里程碑内的相对顺序

### 2. pre-brainstorm 候选 issue 不应停留在“悬空状态”

当前已有规则要求 `candidates.md` 显式填写 `milestone` 字段，但这还不够。

更强的约束应该是：
- **所有非 dropped 的 candidate，都必须进入 milestone 体系**
- 不能出现 candidate 还活着，但 milestone 完全无感知的状态

但“进入 milestone”不等于“已经 fully scheduled”。
它至少可以有三种层次：

1. 已明确 milestone 归属
- 已知道属于哪个 milestone
- 已知优先级和大致顺序

2. 已进入某个 milestone 的候选池
- 说明这个 issue 不会被丢失
- 但仍需继续研究、排序或跨 issue 收敛

3. 仍是 pending milestone binding
- 只允许短暂过渡
- 不应成为长期停留状态

因此，当前 `pending://milestone-binding` 更像临时占位，而不是稳定终态。

### 3. 里程碑内部应允许“候选列表”层

你提的这个点是对的。

一个 milestone 内部不能只存“完全 ready 的 issue”，还需要容纳：
- 还要继续研究的问题
- 单个 issue 已达标，但与项目其他 issue 还未整体收敛的问题
- 已知要做，但尚未想清放在哪个阶段顺序的问题

所以 milestone 内部至少应区分两层：

1. `committed_issues`
- 已 ready
- 已具备执行条件
- 有明确顺序或阶段位置

2. `candidate_issues`
- 尚未 dropped
- 已确认属于该 milestone 关注范围
- 但可能仍需研究 / 排序 / 依赖收敛

这样可以避免两个坏结果：
- 还没 ready 的 issue 被迫伪装成 ready
- 候选 issue 因未完全收敛而在里程碑体系里消失

### 4. candidate 状态变化时，应同步写 milestone

这部分应该形成硬规则：

- 当 `candidates.md` 中某个候选项状态不是 `dropped` 时
  - 必须同步写入 milestone
- 写 milestone 时，至少要声明该 issue 当前属于：
  - committed
  - candidate
  - research-needed
  - sequencing-pending

也就是说，candidate 的状态写入不该只改 `candidates.md`，还要原子更新 milestone 映射。

### 5. milestone 开头应有元数据，解释状态语义和行动规则

这点很重要。否则同一个状态名，AI 和人会各自理解。

milestone 文档头部应该至少声明：

```md
milestone_id: <id>
milestone_status_policy_version: v1
candidate_policy:
  dropped: remove from active milestone queues
  needs_research: keep in candidate_issues; route back to pre-brainstorm or issue-brainstorm
  proposed: keep in candidate_issues; waiting for convergence
  ready: move to committed_issues when sequencing is clear
  in_progress: must exist in committed_issues and progress tracking
  blocked: keep visible with blocker and next action
sequencing_policy:
  ordered_by: dependency_then_value
  allow_unordered_candidates: true
routing_policy:
  no_issue_path: route to pre-brainstorms
  issue_path_present: enter issue-bound handling and decide between issue-bound brainstorm / IBM / continuation based on status
```

重点不是字段名字，而是 milestone 文档开头必须回答：
- issue 状态怎么标记
- 每个状态怎么理解
- AI 看到该状态后应该怎么行动

### 6. 这会反过来影响 brainstorm 路由判断

如果 milestone 成为第一扫描层，那么 brainstorm 的“是否基于 issue”判断会更稳定：

1. milestone 中已有正式 issue path
- 说明当前问题已进入“已有 issue”方向
- 后续仍需结合状态决定是 issue-bound brainstorm、IBM、continuation 还是 completion verification

2. milestone 中只有 candidate entry，没有正式 issue path
- 后续仍应先回到 pre-brainstorm / candidate 收敛

3. milestone 中标记为 research-needed
- 默认说明还没进入正式 issue 执行面
- 若已有 issue 且仍在原边界内，应继续 issue-bound brainstorm；否则回 pre-brainstorm

4. milestone 中标记为 continuation of issue
- 后续工作应绑定原 issue，而不是新开 pre-brainstorm

### 7. 当前工作方法里缺的那一跳

当前方法更像：
- pre-brainstorm -> candidates -> issue-ready

但还缺：
- candidate 写状态时，必须同步 milestone
- milestone 决定 issue 是否 ready / candidate / research-needed
- milestone 反过来决定后续 brainstorm 路由

也就是更完整的方法应该接近：
1. pre-brainstorm 产出 candidates
2. candidate 写入状态时，原子同步 milestone
3. milestone 作为主动扫描源决定下一步
4. 若已进入已有 issue 方向，则结合状态决定 issue-bound brainstorm / IBM / continuation / completion verification
5. 若仍未形成 issue 或仍处于 candidate 研究态，则继续 pre-brainstorm 收敛

## 暂时修正后的判断

### 修正 1：milestone 不是可选附属，而是核心路由层
- 不应只在 issue 成熟后才写 milestone
- candidate 进入活跃状态时就应写 milestone

### 修正 2：`pending://milestone-binding` 只能是短暂过渡态
- 长期存在说明流程没有闭环
- 后续可考虑用 hook / bmad-check 检测长期未绑定 candidate

### 修正 3：issue 路由判断应结合 milestone
- 不是单看 brainstorm 文件本身
- 还要看 milestone 是否已经承认它为正式 issue 或仅为 candidate

## 新增待收敛问题

1. candidate 的状态枚举是否需要统一升级？
   - 当前常见有：`proposed | promoted | dropped | needs_research`
   - 但 milestone 层可能需要：`candidate | research-needed | sequencing-pending | committed | in_progress | blocked`
2. `promoted` 是否足够表达“已成为正式 issue”，还是应该拆成：
   - `issue_materialized`
   - `milestone_bound`
   - `sequenced`
3. milestone 文档是否要从单一 `docs/milestones.md` 进一步结构化成：
   - 全局索引
   - 单 milestone 文档
4. milestone 与 progress/recovery 的边界如何定义，避免重复记录？

## 新增讨论：会话启动应是 `context + milestone` 路由，而不是静态扫表

### 1. 路由输入不是“有没有 issue”，而是 `input_context + milestone_path`

当前更准确的定义应是：
- 路由器输入不是单独的 issue id，也不是盲扫 milestone
- 路由器输入应是：
  - `input_context`
  - `milestone_path`

也就是：

```text
router(input_context, milestone_path)
```

其中：
- `input_context` 可以来自：
  - 用户 chat input
  - review 信号
  - test 信号
  - recovery 信号
  - AI 自治发现的问题描述
- `milestone_path` 是当前项目活跃 milestone 的语义索引与状态表

### 2. auto-loop 的职责不是替代上下文，而是组装上下文

对于 Freely 自举和未来产品化后的运行方式：
- 人类会话：chat input 就是 context
- AI 自治：auto-loop 负责把发现的问题组织成 context，再传给路由器

例如概念上应接近：

```bash
iflow -p "<context>"
```

这里的 `<context>` 不是普通提示词补充，而是本次任务发现的标准化输入。

因此 auto-loop 不应“无上下文盲扫项目”，而应：
1. 收集触发信号
2. 组装 `input_context`
3. 调用统一路由器

### 3. milestone 是被 context 检索的，不是固定优先级队列

这意味着：
- milestone 不是“先看 in_progress，再看别的”的死板扫描顺序
- milestone 是“当前项目任务语义索引 + 状态路由表”
- 必须先用 `input_context` 在 milestone 中做语义命中，再根据命中结果看状态

也就是说，第一步是：
- 根据当前上下文，在 milestone 中找最相关的 issue / candidate / follow-up 项

第二步才是：
- 根据该项状态决定是否进入 pre-brainstorm、IBM、continuation 或 completion verification

### 4. 会话启动的正确顺序

会话启动时应是：
1. 获取 `input_context`
2. 用 `input_context` 检索 milestone 中的相关 issue / candidate
3. 若命中，再检查状态与边界
4. 最终决定路由

而不是：
- 先静态看 milestone 里谁是 `in_progress`
- 然后不考虑本次上下文就默认继续

### 5. “没有明确指令”不等于没有上下文

这点需要显式写清。

对于 AI 自治：
- 用户没有显式下指令
- 但 auto-loop 发现的问题、review 结果、test 失败、会话恢复信号，本身都构成 `input_context`

因此：
- `no explicit user intent` != `no context`
- 路由依然要由 context 驱动

## 新增讨论：基于命中状态的分流

### 1. 未命中任何已有 issue / candidate

若 `input_context` 在当前 milestone 中未命中任何已有 issue 或 candidate：
- 路由到 `pre-brainstorms`
- 产出新的 candidate issue
- 并同步写入 milestone candidate 区，不能悬空

### 2. 命中 candidate 或 research-needed

若命中项当前状态仍属于研究态，例如：
- `candidate`
- `research-needed`
- `sequencing-pending`

则默认进入研究流，而不是直接执行。

分流细化：
- 若命中的是 milestone candidate：通常继续 `pre-brainstorms` 研究链
- 若命中的是已有 issue 但仍在研究态：进入 issue-bound brainstorm（`IBM/B`）
- 若语义已明显超出原边界：新开 pre-brainstorm

### 3. 命中已有 issue，状态为 not-started，但已足够清晰

若命中已有正式 issue，且：
- 当前不需要重新研究
- 问题边界清晰
- 只是尚未开始文档接入/推进

则进入 `doc-loop(IBM)`，而不是回 pre-brainstorm。

但在进入 `IBM` 前，应先检查 milestone 内该 issue 的位置是否需要调整：
- 同 milestone 内顺序是否需要调整
- 是否需要跨 milestone 挪动
- 是否需要从 candidate 区移动到 committed 区

### 4. 命中已有 issue，状态为 in-progress

此时默认不是“重新 intake”，而是先检查运行时状态：

1. 相关 AI 进程是否存在
2. 若不存在，是否需要重启
3. 是否存在 recovery / progress 记录
4. 是否存在对应的会话 jsonl 地址
5. 观察 jsonl 结尾状态，判断：
   - attach
   - resume
   - restart
   - failure recovery

所以：
- `in-progress` 默认路由是 `continuation_or_recovery`
- 不是默认重新进入 pre-brainstorm 或 IBM

### 5. 命中已有 issue，状态为 done

命中 done 也不能直接视为结束。
还应检查：
- 完成状态标记是否达标
- 是否缺 closing evidence
- 必需产物是否齐全

若未达标：
- 不应保持 done
- 应回到 `IBM` 补文档或进入 recovery/closure flow

若已达标，但当前 context 语义是一个 follow-up 新问题：
- 不应强行挂回已完成 issue
- 应新开 pre-brainstorm，产出 follow-up candidate

## 新增讨论：里程碑需要承载可执行状态语义

仅有 `todo/doing/done` 之类标签是不够的。
里程碑中的每个 issue/candidate，至少应能表达：
- 当前状态
- 默认路由
- 是否仍在原边界内可继续
- 完成判定如何检查
- recovery 时应看哪些记录

因此 milestone 元数据或条目结构中，后续可能需要：
- `default_route`
- `boundary_note`
- `recovery_hint`
- `completion_check`

## 修正后的总路由逻辑

当前更准确的总逻辑应是：

```text
brainstorm_doc_placement = issue_evidence_check
route = context_match(milestone, issue, candidate)
      x item_status
      x boundary_check
      x runtime_state
```

其中：
- `brainstorm_doc_placement` 解决文件放在 `pre-brainstorms` 还是 `epics/.../brainstorms/`
- `route` 解决这次任务进入 `pre-brainstorms`、`IBM/B`、`IBM`、continuation/recovery 还是 completion verification

其中：
- `context_match`：先决定当前上下文命中了哪个任务实体
- `item_status`：决定它是研究态、未开始、进行中还是已完成
- `boundary_check`：判断当前语义是否仍在原 issue/candidate 边界内
- `runtime_state`：在 `in-progress` 时决定 attach / resume / restart / recovery

## 当前进一步收敛出的工作方法

会话启动时更完整的方法应接近：
1. 获取 `input_context`
2. 在当前 milestone 中做语义命中
3. 若未命中：进入 pre-brainstorm，产出 candidate issue
4. 若命中研究态：继续研究流
5. 若命中 not-started 且已清晰：先做 milestone alignment，再进入 `doc-loop(IBM)`
6. 若命中 in-progress：检查进程、recovery、jsonl 结尾状态，再 continuation/recovery
7. 若命中 done：先做完成达标检查；若是新 follow-up，再新开 pre-brainstorm

## 新增待收敛问题

1. `input_context` 的最小标准化结构是什么？
2. milestone 条目是否必须增加 `default_route`、`boundary_note`、`recovery_hint`、`completion_check`？
3. `in-progress` 的 jsonl 结尾状态应该有哪些枚举值，才能稳定决定 attach / resume / restart？
4. “完成状态标记达标”最小需要哪些证据？


## 新增讨论：`pre-brainstorms -> candidates -> route` 应改为 `pre-brainstorms -> candidates -> milestone -> route`

### 1. `pre-brainstorms` 不应再承担最终路由职责

如果 pre-brainstorm 已经完成研究并产出 candidate issue：
- 它的结束动作应是把 candidate 写入 milestone
- 而不是自己直接决定进入 `doc-loop` 或 `dev-loop`

也就是说：
- `pre-brainstorms` 负责前置研究收敛
- `candidates.md` 负责记录候选 issue 结果
- milestone 负责后续活跃任务路由

### 2. `candidates.md` 是研究层，不是调度层

这意味着 `candidates.md` 的角色需要收缩为：
- 研究过程的候选 issue 记录
- 候选状态记录
- issue-ready 证据沉淀

而不应继续承担：
- 后续会话启动时的主调度入口
- 最终由谁进入 IBM / continuation / recovery 的直接判断

这些职责都应转移给 milestone。

### 3. milestone 才是唯一活跃任务路由面

只要某个 candidate/issue 仍是活跃任务：
- 它就必须能在 milestone 中被扫描到
- 后续所有 `context + milestone` 路由都以 milestone 为准

因此：
- 非 dropped 的 candidate，必须进入 milestone candidate 区
- 已成熟的 issue，必须进入 milestone committed 区
- `in-progress` / `done` / `blocked` 等状态也必须在 milestone 中可见

### 4. 这意味着流程图也要改

如果这个职责修正成立，那么现有流程图里：
- `pre-brainstorms -> candidates -> route`

应改成：
- `pre-brainstorms -> candidates -> milestone`
- `milestone + input_context -> route decision`

即：
- pre-brainstorm 的结束出口是 milestone
- 真正的路由器在 milestone 层发生

### 5. 当前研究产出的候选 issue 也应包含“流程图路由修正”

本次研究本身已经形成一个新的候选问题：
- 现有统一循环图中，pre-brainstorms 与 route 的关系表述不准确
- 需要把流程图和文字说明一起修正为 milestone-centered routing


## 新增讨论：受影响 guidance/skills 范围需要同步修正

在当前收敛出 `milestone-centered routing` 之后，仓库内已有多处 guidance/skills 仍在表达旧职责，即：
- `pre-brainstorms -> candidates -> route`
- 或把 `candidates.md` 当成后续调度主表

这些位置需要纳入同一批次修正范围。

### 当前命中的主要位置

1. `docs/PROJECT_INTENT.md`
- `A2 分流决策` 仍把 `raw problem / candidate` 直接送入 doc-loop/dev-loop
- 仍写有“更新 candidates.md 的 route/status”
- mermaid 图仍把 `pre-brainstorms/candidates` 放在直接路由入口
- 仍写“在 candidates.md 的 session_refs 留痕并进入 A2 路由”

2. `docs/system/workspace/skills/doc-loop-execution/SKILL.md`
- 仍写“更新 pre-brainstorms 候选项路由/状态”
- 后续应改为：更新候选研究状态 + milestone 绑定，而不是直接承担路由

3. `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- 仍写“更新候选项路由/状态记录”
- 后续应改为：产出 candidate，并同步 milestone，由 milestone 承担活跃任务路由

4. `docs/pre-brainstorms/README.md`
- 当前虽然要求 `milestone` 字段显式填写
- 但尚未明确：
  - 非 dropped candidate 必须进入 milestone 活跃面
  - `candidates.md` 不再是调度主表

### 修正目标

这些 guidance/skills 应统一到如下表述：
- `pre-brainstorms -> candidates -> milestone -> route decision`
- `candidates.md` 是研究收敛层，不是活跃任务调度层
- milestone 是唯一活跃任务路由面
- 会话启动和 auto-loop 使用 `input_context + milestone` 做语义命中与状态分流

### 为什么这必须形成独立 issue

如果只在当前预研文档里改认知，而不同步修改指导文档：
- AI 仍会从旧 guidance 学到错误流程
- 之后的实现与规范会再次分叉
- pre-brainstorm 的方法指导会继续教错人/错 AI

因此，这部分应形成独立候选 issue，并与流程图路由修正一起进入后续落地。


## 新增收敛：一旦确定进入 `doc-loop(IBM)`，先落正式 story 目录

### 1. `doc-loop(IBM)` 的起点是 milestone 命中的 issue

当 `context + milestone` 的判断结果已经明确：
- 不再走 `pre-brainstorms`
- 而是进入 `doc-loop(IBM)`

则应视为：
- 当前问题已经绑定到某个正式 issue
- 接下来应进入该 issue 所属的正式 story 文档空间

### 2. 先确认 `epic-name/story-name`，再开始 `IBM`

在这种情况下，更合理的操作顺序不是先随手写 brainstorm，再回头想归属；
而是：

1. 先确认当前 issue 的 `epic-name`
2. 先确认当前 issue 的 `story-name`
3. 先建立或进入正式目录：

```text
docs/epics/{epic-name}/{story-name}/
```

然后再继续 `IBM`。

### 3. 除 milestone 外，`IBM` 的产出物都沉淀到该 story 目录

一旦进入 `doc-loop(IBM)`，则除 milestone 外的相关产出，都应优先沉淀到该 story 目录：

- `issues/{issue-name}.md`
- `brainstorms/b-{issue-name}.md`
- `prd.md`
- `pre-tests.md`
- `tasks.md`

这意味着：
- `B` 阶段的 brainstorm，不再留在 `pre-brainstorms`
- 而是写入该 issue 对应的 story 目录

### 4. milestone 仍是独立收敛面，由 `M` 单独回写

即使已经进入 `doc-loop(IBM)`：
- milestone 仍不属于 story 目录内部文件
- milestone 仍是项目级活跃路由面与收敛面
- `M` 的职责，是把 `I/B` 产生的顺序、归属、状态变化正式回写到 milestone

因此应明确区分：
- story 目录：保存 issue 相关正式文档产物
- milestone：保存项目级顺序、状态、路由面

### 5. `B` 与 `M` 的关系

当前更准确的理解应是：
- `B` 不只是“写 brainstorm 文件”
- `B` 是围绕该 issue 继续收敛问题、补边界、补验收、补方案
- 在这个过程中，可能发现：
  - 同 milestone 内顺序要调整
  - issue 需要跨 milestone 移动
  - candidate 要进入 committed
  - issue 还需进一步收敛才能满足落地

这些变化需求，由 `M` 正式写回 milestone。

### 6. 对当前整体方法的进一步收敛

因此当前更清晰的方法链应是：

1. `context + milestone` 做语义命中与状态判断
2. 若仍未形成 issue 或超出原 issue 边界：进入 `pre-brainstorms`
3. 若确定进入 `doc-loop(IBM)`：
   - 先确认 `epic/story`
   - 先进入正式 story 目录
   - 再执行 `I/B/M`
4. 除 milestone 外，正式产物都沉淀到 story 目录
5. milestone 由 `M` 单独回写

### 7. 这会影响后续流程图和 guidance 修正

后续如果修流程图和 guidance，需补上这条：
- `doc-loop(IBM)` 一旦启动，就不再把产物留在 `pre-brainstorms`
- 正式产物进入 `docs/epics/{epic}/{story}/`
- milestone 继续保持独立


## 新增收敛：顶层可收敛为少量 skill，但不能把状态分流抹平

### 1. 顶层“两个 skill”方向是可行的，且更适合作为最终产品落地抽象

从 Freely 的产品实现角度，当前可以收敛出一个更明确的方向：
- 前面讨论的复杂路由逻辑，不必全部暴露给 AI 当作显式流程图去记忆
- 最终落地到 Freely 系统时，应由 auto-loop 负责：
  - 组装标准化输入/提示词
  - 调用 AI CLI 的无交互自治模式
- 对 AI 工具暴露的顶层工作入口，可以尽量收敛为两个 skill

概念上可接近：

```bash
iflow -p -y "<normalized-input>,<milestone-path>"
```

然后在提示词里明确：
- 由 AI 根据输入分析意图，并在 milestone 中判断是否有 **可用 issue**
- 若判断为 `no-usable-issue`：读取 `no-usable-issue-skill.md`
- 若判断为 `has-usable-issue`：读取 `has-usable-issue-skill.md`

也就是说：
- 前面讨论的大量路由逻辑，最终在产品里并不要求 AI 记住一长串分支
- 而是由 auto-loop 先收敛判断，再通过提示词把 AI 引导到两个 skill 中对应的一个

这条方向在“降低 AI 需要记忆的流程面”上是合理的。

### 2. 但“两个 skill”不能把判断简化成“有没有 issue”

这里必须强调：
- 给 AI 的判断条件不是“是否存在 issue”
- 而是“**是否有可用 issue**”

因为现实中会出现：
- milestone 里存在 issue，但与当前输入语义不匹配 -> 对当前任务来说等于没有可用 issue
- milestone 里存在 issue，但仍处于研究态或边界不适配 -> 不一定能直接作为当前执行入口
- milestone 里存在 issue，且当前正好命中并可继续推进 -> 才算有可用 issue

因此：
- `no-usable-issue` -> `no-usable-issue-skill.md`
- `has-usable-issue` -> `has-usable-issue-skill.md`

这仍然不能被进一步粗暴理解成：
- has issue -> 直接进入单一路径

因为前面已经收敛出：
- 有可用 issue，不一定直接进入 `IBM` 的同一子路径
- 有可用 issue 但仍在研究态，进入的是 `doc-loop(IBM)` 中的 `B`
- 有可用 issue 且 `in-progress` 时，首先要做 runtime / recovery 判断
- 有可用 issue 且 `done` 时，首先要做 completion verification

因此更准确的说法是：
- 顶层可以只有少量 **入口 skill**
- 但入口 skill 内部仍必须执行状态分流，而不能把所有 “has issue” 都当成同一种情况

### 3. 更合理的顶层模型

当前更稳的实现模型应接近：

1. `auto-loop/router` 负责：
   - 来源适配
   - 上下文归一化
   - milestone 命中
   - 决定进入哪个顶层 skill

2. `no-usable-issue-skill` 负责：
   - 未命中 issue/candidate 或超出原 issue 边界时的前置研究
   - 产出 candidates
   - 同步 milestone

3. `has-usable-issue-skill` 负责：
   - 已绑定 issue 的 doc-loop 路径
   - 其中内部仍要区分：
     - `I`：确认 milestone 命中的 issue
     - `B`：围绕 issue 继续 brainstorm / 收敛
     - `M`：回写 milestone / mapping / 顺序 / 状态

### 4. `has-usable-issue-skill` 是否还要兜住 `in-progress/done`

这里需要更谨慎。
当前更合理的收敛是：
- `has-usable-issue-skill` 可以覆盖“已有可用 issue 的文档型推进”，包括 `I/B/M`
- 但如果命中 `in-progress`：
  - 首先不是无条件读取 `has-usable-issue-skill`
  - 而是先做 runtime / recovery 判断
- 如果命中 `done`：
  - 首先不是无条件读取 `has-usable-issue-skill`
  - 而是先做 completion verification

因此：
- 若只保留两个顶层 skill，`in-progress` / `done` 的前置门禁必须由 router 先做
- 不能让 `has-usable-issue-skill` 成为“所有 has-usable-issue 的直接入口”

### 5. 所以更准确的落地方式

若产品层确实想把 AI 主流程收敛为极少数 skill，较合理的落地是：

- router 层：
  - `context + milestone` 命中
  - `runtime/completion` 前置检查
- skill 层：
  - `no-usable-issue-skill`
  - `has-usable-issue-skill`

即：
- `no-usable-issue-skill` 与 `has-usable-issue-skill` 负责主要内容工作流
- router 负责更细的状态门控

这样既能保持：
- AI 入口简单

又不会破坏：
- `in-progress`
- `done`
- `runtime_state`
- `completion_verification`
这些必要分流

### 6. 对当前预研的进一步收敛

因此本次研究可以收敛成：
- 顶层 skill 面可以极简化
- 但前提是 router 仍保留：
  - milestone 命中
  - 状态判断
  - runtime/completion gate
- skill 本身不负责替代全部路由器职责

一句更准确的话是：
- **产品可将 AI 工作流最终落地为“auto-loop 组装提示词 + 2 main skills”模型，而不是“2 skills 直接替代路由器”。**


### 7. 作为产品落地视角的最终表述

这里需要明确 auto-loop 的真实调用形态。

- auto-loop 总是负责发送统一结构的顶层提示词
- 这不是人类手工输入，而是 Freely 自治编排时，由一个 AI CLI 发给另一个 AI CLI 的执行输入
- 被调用的 AI CLI 可以继续在自己的内部终端环境中调用自己或其他 CLI 工具

概念形态应接近：

```text
iflow -p -y "<user-input>or<other input>,<milestone-path>；根据输入，分析意图，在里程碑里查询是否有 issue 可用；无：阅读 path/no-usable-issue-skill.md，严格按指南工作；有：阅读 path/has-usable-issue-skill.md"
```

其中：
- auto-loop 外层并不负责替 AI 直接得出 has/no 结论
- auto-loop 外层只根据“上下文来源-skill”决定刚才这条提示词中的 `input` 如何组装
- 被调用的 AI 在执行提示词时，自己根据输入分析意图，并在 milestone 中判断是否有**可用 issue**

如果从 Freely 系统实现角度总结本次研究，可以收敛成一句更落地的话：

- **Freely 最终通过 auto-loop 组装提示词给 AI 工具；提示词只需要把 AI 引导到两个 skill 之一，就能完成这部分工作。**

即：
- 前面大量研究出来的 milestone-centered routing、状态机、runtime/completion gate
- 在产品层并不要求 AI 人工记忆所有分支
- 它们应先由 auto-loop / router 逻辑消化
- 最后只把“你现在应读取哪个 skill”暴露给 AI 工具

因此本次研究在产品层的最终抽象可以是：
1. auto-loop 负责来源适配、上下文归一化、milestone 命中与状态判定
2. auto-loop 组装最终提示词
3. 提示词要求 AI：
   - 先根据输入分析意图
   - 在 milestone 中判断是否有**可用 issue**
   - 再读取：
     - `no-usable-issue-skill.md`，或
     - `has-usable-issue-skill.md`
4. AI 按该 skill 完成当前工作流

这条表述比直接要求 AI 理解完整内部状态机，更适合自治 CLI 场景。


## 新增收敛：顶层 skill 文件名应体现 `usable issue` 判断

### 1. 命名目标

顶层 skill 文件名要同时满足三件事：
- 不偷跑比第一层更多的路由结论
- 明确判断标准是 `usable issue`，不是 issue 是否字面存在
- 适合后续直接作为实现命名使用

### 2. 不推荐的命名

以下命名不够准确：
- `IBM-skill.md`
- `pre-brainstorms-skill.md`
- `has-usable-issue-skill.md`
- `no-usable-issue-skill.md`

原因：
- `IBM-skill.md` / `pre-brainstorms-skill.md` 过早暴露了第二层路由结论
- `has-usable-issue-skill.md` / `no-usable-issue-skill.md` 会误导成“是否存在 issue”的机械判断，而不是“是否存在可用 issue”

### 3. 当前更合适的命名候选

从当前研究结论出发，更适合的文件名是：
- `has-usable-issue-skill.md`
- `no-usable-issue-skill.md`

理由：
- 直接对应 AI 在顶层提示词中的判断结果
- 明确是 usable issue，而不是字面 issue existence
- 仍然只表达第一层判断，不替代后续状态分流

### 4. 未来提示词中的表述也应同步

因此顶层提示词更准确应写成：
- AI 根据输入分析意图，在 milestone 中判断是否有 **usable issue**
- 若 `no-usable-issue`：读取 `path/no-usable-issue-skill.md`
- 若 `has-usable-issue`：读取 `path/has-usable-issue-skill.md`

### 5. 暂时结论

若后续实现确实采用双主 skill 入口模型，当前最稳的正式命名建议是：
- `has-usable-issue-skill.md`
- `no-usable-issue-skill.md`

后续若觉得文件名过长，可再讨论缩写方案；但在研究阶段，优先保证语义准确，不优先追求短。
