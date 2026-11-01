---
analysis_id: DM-20261101T231000Z
phase_state: in_progress
topic: Freely 交付闭环的概念模型
created_at: 2026-11-01
---

# Freely 到底怎么交付：B1/B2、SDD/TDD、三角色、四个循环

## 0. 为什么要单独写

README 的图容易让人以为 Freely 是“Manager/Worker/Reviewer 多 agent 编排器”。这只说对了执行段，没说清：

- B1-IBM / B2-IBM 到底产出什么？
- SDD / TDD 与 B1/B2 是什么关系？
- 文档由谁写、谁读、谁验证？
- Manager/Worker/Reviewer 各自在哪、怎么循环？
- 哪些是 script/skill/command/MCP/harness？
- 当前仓库“吃自己的狗粮”与产品架构是什么关系？

这一篇把这些概念钉死；README 图和文字都以此为真源。

## 1. 一句话模型

> Freely 用 B1-IBM 把问题收敛成“值得做、边界清楚”的 candidate；用 B2-IBM 把 candidate 物化成 I-* + PRD + pre-tests + tasks（SDD/TDD 合同）；Manager 按 scan/文档派工，Worker 按合同实现并自测，Reviewer 按合同独立验收；最后经 PR/merge gates 收口。

## 2. B1/B2 与 SDD/TDD 的关系

### 2.1 B1-IBM：问题规格

- 输入：平台 issue/comment、chat、scan 发现的治理/runtime 信号。
- 动作：读 Intent/Constitution/LAWS、验收、依赖；发散→收敛→决策。
- 产物：`brainstorms.md`、`candidates.md`；candidate 进 milestone。
- 回答：**为什么做、值不值得做、边界是什么、排在哪。**
- 不是：实现设计，不是测试计划。

### 2.2 B2-IBM：实现规格 + 验收规格

- 输入：milestone 里的正式 I-*。
- 动作：读实现面、替代方案、验收标准；物化目录。
- 产物：`issues/I-*.md`、`prd.md`、`pre-tests.md`、`tasks.md`、`code-reviews/`。
- 回答：**怎么做、怎么验、分几步、替代方案是什么。**
- 不是：写代码；不是“再写一份 B1”。

### 2.3 SDD 与 TDD 是两份合同

| 合同 | 由谁生成 | 内容 | 谁消费 | 何时验证 |
| --- | --- | --- | --- | --- |
| SDD（规格驱动） | B1 + B2 | 问题、边界、PRD、验收标准、code-review | Manager/Worker/Reviewer | B2 完成时、review/merge 时 |
| TDD（测试驱动） | B2 | pre-tests、tasks、RED/GREEN 证据、test-gate | Worker/Reviewer/Gates | dev-loop、test-pre-merge、PR 前 |

关键区分：

- **B1 不是 SDD**：B1 产出“问题规格/candidate”，SDD 是贯穿 B1/B2 的规格纪律与文档集。
- **B2 不是 TDD**：B2 产出 pre-tests（TDD 的合同），TDD 是 Worker 执行时“先 RED 再实现”的纪律。
- **B1/B2 是过程；SDD/TDD 是产物+纪律。** 不要把四个词当成四个阶段。

## 3. 三个角色：位置与责任

| 角色 | 位置 | 读什么 | 写什么 | 不做什么 |
| --- | --- | --- | --- | --- |
| Manager | 控制面，常驻 | scan、milestone、issue phase、A2A、fleet | 派工、纠偏、收口、升级 | 不读代码、不下实现指令、不替 Reviewer 判 |
| Worker | 执行面，按 issue 派生 | I-*、PRD、pre-tests、tasks、相关代码 | 代码、测试、证据、commit | 不合并、不关 issue、不自己判 pass |
| Reviewer | 审查面，独立 | PRD、pre-tests、diff、测试证据 | verdict、required fixes | 不替 Worker 改代码、不替 Manager 派工 |

关系：

```
Manager --派工--> Worker --提交--> Reviewer --fail--> Worker
   ^                                   |
   |                                   +--pass--> PR/merge
   +------------ 收口/状态 <---------------------+
```

责任边界：

- Manager 拥有“现在做什么/下一步”。
- Worker 拥有“怎么实现”。
- Reviewer 拥有“是否达标”。
- 三者不能互相替代；Reviewer 的独立性是 Freely 的质量差异，不是 Super-agent 的对应角色。

## 4. 四个循环

| 循环 | 触发 | 主体 | 产物 | 结束条件 |
| --- | --- | --- | --- | --- |
| auto-loop | 常驻/scan | Manager | 派工、收口、raw issue | 无待办/需人 |
| doc-loop | 新 raw issue/candidate | Worker（B1/B2 skill） | brainstorm/candidate/PRD/pre-tests/tasks | B2 完成、可进入 dev |
| dev-loop | 已派工 issue | Worker | 代码、测试、commit | RED→GREEN、可提 PR |
| review/delivery loop | PR 创建 | Reviewer + gates | verdict、merge、closeout | 合并/关闭 |

四个循环不是串行瀑布：doc-loop 可以在 dev-loop 前，也可以在 review 发现规格缺口时回流；review fail 回到 dev-loop；merge 后 auto-loop 收口。

## 5. 谁实现：scripts / skills / commands / MCP / harness

| 层 | 具体 | 在闭环里的位置 |
| --- | --- | --- |
| scripts | `task-lifecycle-scan.py`、`wt-create`、`governance-check`、`pretests-gate`、`pr-*-guarded`、`test-lane`、`a2a_task.py`、`issue-sync` | 确定性调度、状态搬运、门禁 |
| skills | `freely-doc-B1_IBM-execution`、`B2`、`dev-loop`、`test-RED`、`test-execution`、`review`、`workflow-guarded` | 把流程/角色知识给 agent |
| commands | `bin/freely` 及其子命令 | 多步治理动作的封装 |
| MCP | 由底层 AI CLI 提供；Freely 当前传 `mcpServers: []` | 不是编排层；可用性取决于 harness |
| harness | ACP（Claude/Codex/OpenCode/Cline） | 真正跑模型会话的执行基座 |
| tools | agent 的 read/write/shell 等工具 | 由 harness 提供，受 worktree/权限约束 |

对应到闭环：

- B1：scan/wt-create + skill B1 + 平台副本。
- B2：skill B2 + 模板 + I-*/PRD/pre-tests/tasks。
- Manager：scan + live-status + a2a_task + bin/freely。
- Worker：skill dev/test + commands + harness + tools。
- Reviewer：pr-review-guarded + review skill。
- Gates：pretests/PR/merge/wt-close + test-lane。

## 6. 吃狗粮：当前仓库与产品架构的区别

当前仓库是 **Freely 用 Freely 开发自己**：

- 同一个 B1/B2/SDD/TDD 流程，既用于托管项目，也用于 Freely 自身迭代。
- `docs/B1-docs/`、`docs/B2-docs/`、`docs/milestones.md` 是**本仓库的自开发产物**，不是 runtime 组件。
- `docs/system/`、`bin/`、`src/` 是**产品能力目录**，会被 runtime/agent/skill/CLI 长期消费。
- 架构图描述的是**产品闭环**，不是当前仓库的 issue 列表/工位状态。

常见混淆：

1. 把 `docs/B1-docs` 当成 Freely 产品的一部分 → 错；它是每个项目自己的过程产物。
2. 把当前 issue 的 phase 画进产品架构 → 错；那是本仓库运行态。
3. 把 B1/B2 写成 runtime 组件 → 错；它们是 skill+文档+门禁组成的开发流程。
4. 把 Reviewer 当成 Super-agent 的角色 → 错；Super-agent 没有独立 Reviewer。

## 7. 与 Super-agent 的位置对照

| Freely | Super-agent | 说明 |
| --- | --- | --- |
| Manager | Router（部分） | 都路由/对外；Manager 还巡检/建工位/收口 |
| Worker | Worker | 都隔离执行；Freely Worker 还承担 SDD/TDD/PR |
| Reviewer | 无 | Freely 额外设计；不是对应关系 |
| scan/issue/chat | Trigger/Source | 事件来源相似；scan 是批量派生，不是事件对象 |
| B1/B2 + docs | 无 | Freely 的规格层；Super-agent 用 Ticket 承载 |
| Gates | 外部 review/CI + 人 | Freely 内建合并治理；Super-agent 靠外部 |
| watchdog | Watchdog（文章） | 意图相近；原型未实现 |

## 8. 这张图不表达什么

- 不表达当前仓库的 issue/phase/工位状态。
- 不表达所有脚本的调用细节；只表达主脊与责任边界。
- 不表达 MCP 已集成；MCP 由 harness 决定。
- 不表达 GUI 已产品化；GUI 仍是 Tauri probe。

## 9. 待确认

- B1/B2 的产物是否要 schema 化（candidate/PRD/pre-tests 字段）？
- Manager 是否应该读 PRD 摘要，还是只读 scan/issue 状态？
- Reviewer 的 verdict 是否要结构化（pass/fail + required fixes + evidence）？
- 四个循环的 handoff 是否要消息级 ownership？
- SDD/TDD 文档在 merge 后是否要归档/索引，供后续 issue 复用？
