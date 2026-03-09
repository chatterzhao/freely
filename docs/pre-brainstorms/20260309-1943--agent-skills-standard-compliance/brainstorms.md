# 研究：Freely Workspace Skills 与 Agent Skills 标准的合规差距

## Context

- 日期：2026-03-09 19:43 UTC
- 触发：审查 Anthropic 官方 skills 资料与当前 Freely `docs/system/workspace/skills/**` 的结构差距，判断哪些地方不达标、哪些地方只是建议项，以及 Freely 当前是否具备“修改 skill 本身”的明确能力。
- 外部事实源：
  - Anthropic repo README：skills 是按需动态加载的文件夹，最低门槛是带 YAML frontmatter 的 `SKILL.md`
  - Agent Skills specification：标准结构要求 skill 目录至少包含 `SKILL.md`；`name` / `description` 为必填；`metadata` 与 `allowed-tools` 为可选；推荐 `scripts/`、`references/`、`assets/`；强调 progressive disclosure、相对路径引用、以及将长内容拆分到引用文件
  - Anthropic/Codex `skill-creator`：强调 skill 应保持精简，正文尽量低上下文成本，必要时把变体/细节/资源拆到单独目录，并在更新 skill 时校验辅助元数据是否同步
- 受限事实源：
  - 微信文章 `https://mp.weixin.qq.com/s/T8q_ijEtAj8GNmLteOG2qg` 在当前环境返回“环境异常，完成验证后即可继续访问”，正文未取得，因此不能作为已验证内容引用
- 内部事实源：
  - `docs/system/workspace/skills/**`
  - `docs/system/workspace/skills/README.md`
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/PROJECT_INTENT.md`

## 当前已满足的部分

1. 所有 workspace skills 都有单独的 `SKILL.md`。
2. 所有 `SKILL.md` 都包含 `name` 与 `description` frontmatter。
3. 当前 skill 正文都明显低于 500 行，没有出现超长单文件失控。
4. 少数 skill 已经使用 `references/` 分离补充材料，例如 `constitution-guard`、`laws-enforcer`、`branch-management`、`premerge-reconcile`。

结论：如果只按最低标准看，Freely 当前 skill 体系不是“完全不合规”，而是“满足基础格式，但离推荐结构和可移植性还有明显距离”。

## 主要差距

### 1. 技能目录不够自包含

- Anthropic/Agent Skills 的默认心智模型是“skill 文件夹本身就是一个可搬运能力包”。
- Freely 当前把大量运行时真源放在 `docs/system/workspace/scripts/`、`docs/system/workspace/hooks/`、`bin/`，而不是 colocate 在 skill 目录下。
- 结果：
  - skill 与其可执行资源之间耦合存在，但目录结构上不可见
  - 可移植性弱
  - 另一个 agent 读 skill 时，需要跳出 skill 根目录才能找真源

### 2. 一部分 skill 的正文承担了过多治理语义

- `context-source-skill`、`doc-pre-brainstorm-execution`、`doc-ibm-execution`、`branch-management` 这类 skill 虽然行数不超标，但正文里同时承载职责、状态机、路由、产物要求、边界例外。
- 这些内容里有一部分本质上属于“引用资料”而不是“激活即读的主说明”。
- 这会提高激活成本，也会弱化 Anthropic 强调的 progressive disclosure。

### 3. 相对路径与一层引用原则执行不稳定

- Agent Skills specification 建议从 `SKILL.md` 使用相对路径引用资源，并避免深层级引用链。
- Freely 当前 skill 经常直接引用项目级路径，例如 `docs/system/workspace/scripts/...`、`docs/LAWS.md`、`docs/PROJECT_INTENT.md`。
- 这在 Freely 仓库内部可以工作，但不符合“skill 自身为能力包”的结构习惯。

### 4. 推荐项缺失：examples / edge cases / optional metadata

- 官方规范对正文格式限制很弱，但推荐包含：
  - step-by-step instructions
  - examples of inputs and outputs
  - common edge cases
- Freely 多数 skill 只有流程步骤，示例输入/输出和边界案例普遍不足。
- `metadata`、`allowed-tools` 在标准里是可选，不属于当前必须补的硬缺口，但如果未来希望更强的工具边界与 UI 发现能力，它们是可增加项。

### 5. 技能目录索引存在漂移

- `docs/system/workspace/skills/README.md` 仍列出 `skill:doc-loop-execution`
- 当前活跃 skill 目录实际上是：
  - `doc-pre-brainstorm-execution`
  - `doc-ibm-execution`
- 这说明 skill 清单与实际目录已经出现治理漂移，会影响 agent 发现与维护。

### 6. “修改 skill 本身”的流程没有在仓库内被显式封装成 workspace skill

- 当前会话中存在外部系统 skill：`skill-creator`，它确实能指导“创建/更新 skill”。
- 但 Freely 仓库内没有一个 workspace skill 明确说明：
  - 何时允许修改 `docs/system/workspace/skills/**`
  - 修改前必须先进入哪个 `pre-brainstorm`
  - 修改时如何同时对齐 `README`、引用资源、脚本/hook 真源、验证证据
- 结果：
  - “会改 skill”这件事存在于系统环境里，但不是 Freely 自己版本化治理的一部分
  - 对 Freely 自举来说，这仍然是治理缺口

## 是否已有“变 skill 的 skill”

判断分两层：

1. 外部环境层：有
- 当前可用的系统 skill `skill-creator` 就是专门用于创建或更新 skill 的。

2. Freely 仓库治理层：没有完全落地
- `PROJECT_INTENT.md` 已经把治理漂移路由到 `doc-ibm-execution`
- `CONSTITUTION.md` 已要求规范文档改动必须先审慎决策并在专用 feature/worktree 中进行
- 但仓库内没有一个明确的 workspace skill，把“skill 改动治理”从发现、预研、改动、验证到回写串成专门步骤

结论：
- “修改 skill 的能力”存在，但主要依赖外部系统 skill，而不是 Freely 自身版本化治理。
- 如果要严格吃自己的狗粮，Freely 应该把这条链路显式化。

## 遵守建议（先后顺序）

1. 先修治理清单漂移
- 修正 `docs/system/workspace/skills/README.md` 中已失效的 skill 入口名。

2. 再定义 skill 变更治理入口
- 新增一个明确面向 Freely 自身的 workspace skill，或在现有 `doc-ibm-execution` / `constitution-guard` 中补一段“修改 workspace skill 时的固定步骤”。
- 它不需要替代外部 `skill-creator`，而应明确“Freely 内部如何使用 `skill-creator` 并留下治理证据”。

3. 再做结构级瘦身
- 保持 `SKILL.md` 主体只放触发、职责、最短步骤、关键边界。
- 把长状态词典、场景矩阵、复杂例外、脚本细节迁到 `references/` 或 skill 内 `scripts/`。

4. 最后补推荐项，而不是一开始追求花哨字段
- `metadata`、`allowed-tools`、UI metadata 不是当前第一优先级。
- 当前更关键的是：
  - 自包含
  - 相对路径
  - 低上下文成本
  - skill 清单与真源一致

## 与 Freely 当前 skill 的逐项映射

### A. 应保持短而硬的门禁 skill

这些 skill 目前方向基本正确，不应把它们膨胀成大流程手册：

- `constitution-guard`
  - 现状：主体很短，核心步骤清晰，已经把细节下沉到 `references/constitutional-gates.md`
  - 判断：符合 progressive disclosure 方向
  - 建议：继续保持短；如果规则扩展，优先扩 reference，不扩主文

- `laws-enforcer`
  - 现状：主体很短，但 reference 还偏少
  - 判断：结构方向对，信息密度略低
  - 建议：保持主文短，把章节到验收项的映射继续放到 `references/`

### B. 应拆分为“主 skill + references”的核心编排 skill

这些 skill 当前不是错误，而是把太多“应该按需加载”的内容放进了激活即读正文：

- `context-source-skill`
  - 现状：`SKILL.md` 同时承载输入字典、输出字典、多来源场景路由、恢复判断、worktree 准备
  - 风险：每次激活都要加载完整路由矩阵
  - 建议拆分：
    - 主文只保留：触发条件、最小输入、最小输出、一级决策树
    - `references/source-classification.md`
    - `references/continuation-recovery-routing.md`
    - `references/worktree-preparation.md`

- `doc-pre-brainstorm-execution`
  - 现状：正文已经接近“模板 + 过程 + 状态回流”三合一
  - 风险：细节不少，但很多是可复用模板内容
  - 建议拆分：
    - 主文保留：何时进入、产物是什么、如何决定下一跳
    - `references/brainstorms-template.md`
    - `references/candidates-template.md`
    - `references/promotion-checklist.md`

- `doc-ibm-execution`
  - 现状：正文里同时写了 issue materialization、目录约束、字段回填、就绪判定
  - 风险：每次 IBM 激活都读到全部细则
  - 建议拆分：
    - 主文保留：进入条件、四类场景、done 条件
    - `references/ibm-artifact-map.md`
    - `references/issue-materialization-checklist.md`
    - `references/ready-for-dev-gate.md`

- `branch-management`
  - 现状：正文中既有原则，也有大量命令式细节与阶段流程
  - 风险：主 skill 变成半个 runbook
  - 建议拆分：
    - 主文保留：五条路由入口和关键禁止项
    - `references/feature-worktree-flow.md`
    - `references/pre-test-merge-flow.md`
    - `references/release-hotfix-flow.md`
    - 清理状态演进可移到单独 reference

### C. 当前过薄、未来可能需要补 examples/edge cases 的 skill

- `dev-loop-execution`
  - 现状：结构清楚，但几乎没有示例
  - 建议：补最小输入输出示例，不一定需要大量 reference

- `recovery-subagent-governance`
  - 现状：规则明确，但缺少恢复成功/失败、resume/restart 的示例路径
  - 建议：补 `references/recovery-examples.md`

- `module-interface-governance`
  - 现状：过于摘要，像 policy 摘要而不像可执行 skill
  - 建议：至少补 2 个具体场景示例，例如“第三方 API 版本变更”“本地模块协议破坏性升级”

- `config-backup-guard`
  - 现状：过短且缺操作例子
  - 建议：补一个 reference 说明适用文件类型、备份例外、恢复检查

## “变 skill 的 skill”在 Freely 里应该怎么落

不建议直接新发明一个与外部 `skill-creator` 重叠的大而全 skill。

更合适的落法是：

1. 在 Freely 内新增一个很窄的 workspace skill
- 例如：`skill:workspace-skill-governance`
- 它不负责教人“什么是 skill”
- 它只负责 Freely 仓库里修改 `docs/system/workspace/skills/**` 时的治理步骤

2. 这个 skill 应该显式规定
- 先进入 `pre-brainstorm`
- 外部通用 skill creation/update 指南，优先引用系统 `skill-creator`
- 改动时必须同步检查：
  - `docs/system/workspace/skills/README.md`
  - 相关 `references/`
  - 相关 `docs/system/workspace/scripts/**` / hooks / `bin/*`
  - 与 `CONSTITUTION.md` / `LAWS.md` 的一致性

3. 在路由上，这个 skill 不应替代 `doc-ibm-execution`
- discovery 到治理问题发现：仍然先 `doc-pre-brainstorm-execution`
- milestone-owned 治理 issue 收敛：仍然由 `doc-ibm-execution`
- `workspace-skill-governance` 只作为 IBM/dev 中的专门执行说明

结论：
- “skill 的 skill”在 Freely 中应是窄治理 skill，而不是第二套通用 skill-creator
- 外部 `skill-creator` 继续作为通用知识源
- Freely 自己只补“如何在本仓库合法地改 skill”这层

## Immediate remediation vs follow-up governance

### Completed remediation in this branch

- 已修正 `docs/system/workspace/skills/README.md` 中失效的 `doc-loop-execution` 入口
- 已新增 `workspace-skill-governance`
- 已把 `context-source-skill`、`doc-pre-brainstorm-execution`、`doc-ibm-execution`、`branch-management` 的长说明拆到各自 `references/`
- 已为 `dev-loop-execution`、`recovery-subagent-governance`、`module-interface-governance`、`config-backup-guard` 补足 examples / applicability references

### Remaining non-goals

- 本次没有重排 `docs/system/workspace/scripts/**`、hooks、`bin/*` 的物理位置
- 本次没有新增 `metadata` / `allowed-tools`

结论：

- 本轮已完成 skill 结构与治理入口整改
- 剩余项是可选增强，不再作为“必须后续补”的硬缺口

## 收敛判断

该问题不是单个 skill 的局部文案优化，而是“Freely 自己如何治理 skill”的结构问题。

下一步应进入一个治理类 issue，至少覆盖：
- skill 索引与实际目录对齐
- skill 变更治理入口显式化
- 核心 skill 的 progressive disclosure 重构
