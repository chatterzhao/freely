# 研究：Freely 文档层级与 Skill 边界规划

## Context

- 日期：2026-03-09 20:03 UTC
- 触发：基于 skill 合规审计继续上收问题，明确 `PROJECT_INTENT`、`CONSTITUTION`、`LAWS`、`AGENTS.md`、`README.md` 与 `docs/system/workspace/skills/**` 之间的职责边界，以及哪些内容应迁移到 skill，哪些不应迁移。
- 核心判断：Freely 是一个自治软件工程循环应用，而 skill 是其能力暴露面、执行面和治理编译层。因此文档边界规划本质上是产品能力架构规划，不是单纯文档整理。
- 自举约束：这里讨论的规则不仅用于用户项目，也必须用于 Freely 自己。Freely 正在使用 Freely 的能力开发 Freely，自我验证、吃自己的狗粮、先吃螃蟹，因此这些边界必须能在本仓库内真实运行，而不是只对外生效。

## 本次新增前置原则

### 0. 区分“本次采用”与“未来能力”

本条目中的规则需要分成两层理解：

- `current-governance-for-this-planning`
  - 指这次规划与后续实施阶段，当前就应采用的工作纪律
  - 例如：新议题开新 worktree、先 pre-brainstorm、重构后检查内容是否丢失、评审先判断修补还是撤销重做

- `target-freely-capability`
  - 指这些纪律未来不应只靠人工遵守，而应进入 Freely 的正式能力体系，并先在 Freely 自己身上完成自举验证
  - 例如：评审分流能力、重构完整性检查能力、循环提交粒度与 worktree 边界治理能力

结论：
- 不是本次讨论里的每一条都已经是 Freely 的现成功能
- 但只要某条长期有价值、且应由 Freely 自治承载，就应进入 `target-freely-capability`

### 1. 自举优先，不允许例外

- Freely 的文档层级、skill 设计、worktree 纪律、评审/恢复/重做规则，必须先在 Freely 仓库自身跑通。
- 不能出现“对用户项目要求很严格，但 Freely 自己临时例外”的治理豁免。
- 因此任何关于 skill、重构、评审、git 撤销重做的能力，都应被视为 Freely 的产品能力，而不是一次性开发习惯。

### 2. 重构必须防止无意内容丢失

- 无论是文档重构还是代码重构，默认风险不是“格式变了”，而是“语义或事实在重排时被无意丢失”。
- 因此重构过程必须把“检查内容是否完整保留”当成一等能力，而不是事后想起再人工比对。
- 这意味着 Freely 未来需要显式支持：
  - 重构前基线采样
  - 重构后差异核对
  - 若发现并非简单修补可恢复，则使用 git 回退并重新执行

### 3. 评审发现不对齐时，应先判断“修”还是“撤销重做”

- 这是 Freely 必须具备的一项能力，而不只是人为经验。
- 场景：
  - 代码与设计文档不对齐
  - skill 与治理文档不对齐
  - 重构后内容缺失、结构漂移、边界错位
- 处理分流：
  - 若问题是局部、边界清晰、可通过小改动恢复一致：直接修改
  - 若问题已污染结构、引入多处漂移、难以证明没有遗漏：优先用 git 撤销到上一个健康点后重做
- 这条规则适用于文档与代码两侧，不应只用于代码实现。

补充判断：
- `git 撤销` 本身不是 Freely 的能力目标
- 真正应被 Freely 承载的是：
  - 偏差识别
  - 评审后“直接修补 vs git 撤销重做”的分流判断
  - 撤销后回到正确循环边界继续执行

结论：
- “偏差处理与撤销重做”应进入 `target-freely-capability`
- 它属于治理与恢复能力，而不是主业务执行能力

### 4. 每个循环都应有明确的提交与 worktree 续用标准

- 如果没有“何时提交”“继续沿用旧 worktree 还是新建”的前置标准，agent 容易在连续修改中积累混杂上下文，最终进入高 token、低可控的修补地狱。
- 因此 Freely 需要把下列问题显式化：
  - 当前循环的完成标准是什么
  - 达到什么粒度必须先提交
  - 当前 worktree 是否仍然匹配本轮目标
  - 何时继续在原 worktree 工作
  - 何时必须新建 worktree

结论：
- “评审分流 + git 撤销重做 + 提交粒度控制 + worktree 续用标准”应被视为同一组前置治理能力。

## Freely 的六层信息架构

### 1. 产品层：`docs/PROJECT_INTENT.md`

回答的问题：
- Freely 是什么应用
- 为什么存在
- 核心闭环与非目标是什么

应保留的内容：
- 产品目标
- 三层循环的高层能力模型
- 输入面与非目标
- “治理漂移”“运行时异常”等来源类型的产品语义

不应承载的内容：
- 逐步执行流程
- 具体字段词典
- 详细路由矩阵
- 模板化产物清单的低层细节

判断：
- `PROJECT_INTENT.md` 目前已经混入了较多技能级的路由细节，后续应适度瘦身，但不必把三层循环模型本身移走，因为那是产品定义的一部分。

### 2. 宪法层：`docs/CONSTITUTION.md`

回答的问题：
- 哪些边界绝不能破

应保留的内容：
- 硬性约束
- 不可逾越原则
- 强制技术栈
- 分支/worktree 硬规则
- 恢复硬要求

不应承载的内容：
- 操作步骤
- 长命令序列
- 模板字段
- 细粒度案例处置流程

判断：
- `CONSTITUTION.md` 总体边界是对的；若未来发现“怎么做”的段落越来越长，应下沉到 skill references。

### 3. 法律层：`docs/LAWS.md`

回答的问题：
- 如何判定合规
- 最小证据是什么
- 状态语义是什么
- 技能如何路由

应保留的内容：
- `route_kind` / `phase_state` / `runtime_state` 等规范词典
- 最小验收证据
- route 规则
- 章节到 skill 的映射

不应承载的内容：
- 逐步 runbook
- 命令操作说明
- 模板正文
- 长边界案例展开

判断：
- `LAWS.md` 应是唯一规则语义源，而不是执行手册。

### 4. Skill 层：`docs/system/workspace/skills/**`

回答的问题：
- agent 真正如何执行 Freely 的能力

应保留的内容：
- 触发条件
- 主要职责
- 最小输入/输出
- 关键步骤
- 下一跳与回流
- 核心例外

应继续拆到 `references/` / `scripts/` 的内容：
- 状态矩阵
- 长模板
- 详细案例
- 长命令流程
- 可复用检查清单

判断：
- skill 是 Freely 的能力接口层，而不是对上层文档的复制粘贴层。

### 5. 入口层：`AGENTS.md`

回答的问题：
- 进入仓库后先看什么
- 当前活跃范围是什么
- 会话起步要做什么

应保留的内容：
- 权威来源顺序
- 当前阶段与活跃文档范围
- 会话启动检查
- 入口命令
- skills 发现规则

不应承载的内容：
- 宪法/法律正文
- 技能执行细节
- 产品长说明

判断：
- `AGENTS.md` 目前总体健康，应该继续保持“入口索引”定位。

### 6. 人类入口层：`README.md`

回答的问题：
- 这是什么项目
- 怎么启动
- 主要目录看哪里

应保留的内容：
- 项目一句话定义
- 快速开始
- 常用命令
- 面向人类的目录导航

不应承载的内容：
- 完整治理规则
- 复杂 skill 内部流程
- 与上层文档重复的细则

判断：
- `README.md` 当前已经有一些 worktree/门禁规则，后续应进一步压缩为“指向规范”的入口，而不是解释全部规则。

## 内容迁移矩阵

### 应迁移到 skill 或 skill references 的内容

1. 具体执行步骤
- 例如：创建 dedicated worktree、写 candidate、issue materialization、恢复路径

2. 场景化流程

## Migration ledger

| Layer | Keep | Move out | Notes |
|------|------|----------|-------|
| `PROJECT_INTENT.md` | 产品目标、三层循环模型、输入面、非目标 | 详细 route matrix、低层 artifact map、命令说明 | 保留产品语义，不做 skill 手册 |
| `CONSTITUTION.md` | 硬边界、硬约束、强制技术栈 | 操作步骤、长案例流程 | `What/Why` 不能继续向 `How` 漂移 |
| `LAWS.md` | 词典、验收口径、最小证据、skill 路由 | runbook、模板正文、长例子 | 保持唯一规则语义源 |
| `docs/system/workspace/skills/**` | 触发条件、最短步骤、输入输出、下一跳 | 过长矩阵、模板全文、长案例 | 主 skill 做薄，细节下沉 `references/` |
| `AGENTS.md` | 权威来源、会话启动、入口命令、技能发现 | 宪法/法律正文、技能细则 | 保持入口索引定位 |
| `README.md` | 项目介绍、快速开始、目录导航 | 完整治理规则、内部执行细节 | 对人类友好，不重复治理正文 |

## Candidate sequencing

建议按以下顺序推进：

1. 先做文档层级边界校准
- 目的是先防止继续把 `How` 写回 `PROJECT_INTENT/LAWS/README`

2. 再做 workspace skill 架构重组
- 目的是让新的边界有实际执行承载面

3. 最后做评审分流、撤销重做、提交粒度与 worktree 续用治理
- 这些能力依赖前两层已经有稳定边界，否则会和 skill 重构本身互相缠绕

结论：

- `C-20260309T200300Z-A` 应优先
- `C-20260309T200300Z-B` 依赖 A 的边界输出
- `C-20260309T200300Z-C` 虽然重要，但更适合作为 A/B 之后的治理收口
- 例如：不同来源如何路由、不同发布路径如何执行、边界外问题如何 reroute

3. 模板化产物说明
- 例如：`brainstorms.md` / `candidates.md` / issue / progress 的写法说明

4. 命令顺序与脚本衔接
- 例如：`wt-create` / `wt-add` / `wt-status-all` 的使用路径

5. 常见边界案例
- 例如：父分支依赖、恢复成功/失败、pre-test-merge 冲突批次

### 不应迁移到 skill 的内容

1. 产品身份与非目标
2. 分支/worktree 的宪法硬边界
3. `phase_state`、`route_kind` 的规范语义
4. 最小验收证据定义
5. 技术栈强制约束

## 对现有文件的规划建议

### `PROJECT_INTENT.md`

保留：
- 核心目标
- 三层循环高层模型
- 输入来源与非目标

后续可迁出：
- 过细的 route 表格细则
- 与 `LAWS` 重复的状态语义提醒
- 与 skill 重复的产物展开

### `CONSTITUTION.md`

保留：
- 所有硬边界

后续可迁出：
- 一旦出现过长操作样例，应进入对应 skill reference

### `LAWS.md`

保留：
- 规则词典
- 最小证据
- 路由与判定

后续可迁出：
- 模板类说明
- 详细场景流程

### `AGENTS.md`

保留：
- 入口索引
- 会话启动规则
- 当前阶段说明

不建议增加：
- 大量 skill 执行内容
- 规范细则复制

### `README.md`

保留：
- 项目介绍
- 快速开始
- 指向规范文档的链接

后续可压缩：
- 详细 worktree 与 hook 规则说明，改为引用规范和 skill

## Skill 架构规划

Freely 后续 skill 应按角色而不是仅按阶段理解：

1. `guard skills`
- `constitution-guard`
- `laws-enforcer`

2. `capability skills`
- `context-source-skill`
- `doc-pre-brainstorm-execution`
- `doc-ibm-execution`
- `dev-loop-execution`
- `recovery-subagent-governance`
- `branch-management`

3. `governance/operator skills`
- 未来建议新增：`workspace-skill-governance`

### 该类治理/operator 能力还应继续补齐

- `refactor-integrity-governance`
  - 用于重构前后内容完整性检查
  - 重点不是格式，而是语义、规则、事实是否被意外丢失

- `review-alignment-recovery`
  - 用于评审发现“不对齐”时的处理分流
  - 明确何时直接修补，何时 `git revert/reset-to-known-good-and-redo`
  - 明确撤销后如何返回正确循环边界继续执行

- `loop-boundary-governance`
  - 用于判断一个循环何时应该提交、何时继续在当前 worktree、何时必须创建新 worktree
  - 目标是降低跨循环污染与上下文混杂

说明：
- 这三个能力未必都要立刻拆成独立 skill，也可以先作为 `workspace-skill-governance` 的子能力收敛。
- 但语义上必须显式存在，否则 Freely 的自举治理会长期依赖人工直觉。
- 它们都属于 `target-freely-capability`，同时从现在开始以 `current-governance-for-this-planning` 的方式先行试用。

## 是否需要新的 worktree / 新规划

需要，而且应该分场景。

### 可以在现有实现分支内顺手处理的小项

- `README` 或 `skills/README` 的明显索引漂移
- 单个 skill 的轻微 wording 修正
- 增加缺失但不改变边界的小 reference

### 必须开新的治理 worktree 的项

- 重定义文档层级职责
- 调整 `PROJECT_INTENT` / `CONSTITUTION` / `LAWS` / `AGENTS.md` / `README.md` 的边界
- 新增治理类 workspace skill
- 大规模 skill 拆分与 references 重组
- 定义“评审后修补 vs git 撤销重做”的统一规则
- 定义循环提交粒度与 worktree 续用/新建规则

原因：
- 这些变更会改变 Freely 的能力暴露面和治理编译链
- 不应混在普通实现分支里顺手做
- 必须先经过新的 pre-brainstorm 收敛

## 评审分流与 git 撤销重做的初步判断标准

### A. 可以直接修补的情形

- 偏差是局部的
- 目标边界仍清楚
- 能明确指出缺失/错误只落在 1 个关注点
- 修补后可以低成本验证“没有引入新的遗漏”

示例：
- skill 入口名漂移
- 单个 reference 路径错误
- 局部 wording 导致与 `LAWS` 语义不一致
- 小范围代码实现与 issue 描述轻微脱节

### B. 应优先 git 撤销并重做的情形

- 修改已跨越多个关注点
- 已无法低成本证明没有内容遗漏
- 为了修补需要继续叠加 patch 才能勉强回正
- 当前 worktree 已混入多个循环的目标
- 评审显示偏差不是局部错误，而是执行基线本身错了

示例：
- 文档重构后多个章节边界混乱，无法确认哪些内容被吞掉
- skill 拆分后 references、README、scripts、laws 引用同时漂移
- 代码实现已明显偏离 issue/设计，继续补丁只会扩大脏面

结论：
- 这条能力的目的不是“更保守”，而是更省 token、更少语义漂移、更少补丁地狱。

## 循环提交与 worktree 续用的初步标准

### 何时应提交

- 当前循环已完成一个单一关注点
- 该关注点已有最小可验证结果
- 继续修改将进入下一个关注点或下一个能力边界

### 何时继续沿用当前 worktree

- 当前 worktree 的目标与本轮仍然一致
- 未引入第二个独立议题
- 评审结论表明只需在同一边界内继续收敛

### 何时必须新建 worktree

- 下一个循环开始处理另一个治理/产品/实现议题
- 当前 worktree 已需要跨 issue 或跨能力边界扩张
- 需要显式保留当前结果作为可回退基线
- 当前分支已经接近完成，继续叠加只会增加污染

结论：
- “是否新建 worktree”不是习惯问题，而是循环边界控制问题。

## 收敛判断

后续应把该研究拆成至少两个后续议题：

1. 文档层级瘦身与边界对齐
2. workspace skill 架构重组与治理入口新增
3. 评审分流、git 撤销重做与循环边界治理
