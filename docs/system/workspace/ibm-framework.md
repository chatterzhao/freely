# IBM Framework

Freely doc-loop 的治理框架。每个工作项经历两个 IBM 阶段——B1_IBM 和 B2_IBM——由 Milestone 串联。

每个阶段的引擎是 AI 做 Brainstorm（B）：从 Input source（I）摄取输入，经发散→收敛→决策，产出 Milestone candidate 或 Map 文档集（M）。两个阶段共享 I→B→M 骨架，区别在于 I 的来源不同、M 的产物不同，因此命名为 B1_IBM 和 B2_IBM——B 打头强调 Brainstorm 是核心，IBM 是贯穿两个阶段的 I-B-M 结构。

本文件是 IBM Framework 的能力真源。Freely 开发自身项目时吃自己的狗粮，外部项目由 Freely 托管时同样以此框架推进。执行路由（auto/dev loop）见 `docs/system/workspace/three-loop-capability-lifecycle.md`，治理规则见 `docs/LAWS.md` §2。

## 总览

```
 B1_IBM：I → B → M                              B2_IBM：I → B → M
     ┌──────────┐   ┌──────────┐   ┌────┐        ┌───────┐   ┌──────────┐   ┌──────────────┐
     │ github   │   │          │   │    │        │formal │   │          │   │ epic/story/  │
     │ gitee    │ → │ 发散收敛  │ → │can-│  ───→  │issue  │ → │ 实现设计  │ → │  {name}      │
     │ issue    │   │ 边界决策  │   │did-│        │from   │   │ 替代评估  │   │  issues/     │
     │ chat     │   │          │   │ate │        │mile-  │   │ 验收标准  │   │  brainstorms/│
     │ 插话     │   └──────────┘   │    │        │stone  │   │          │   │  prd.md      │
     └──────────┘                  └────┘        └───────┘   └──────────┘   │  pre-tests.md│
                                     │                                    │  tasks.md    │
                                   milestone                                │  code-reviews│
                                   queue                                   └──────────────┘
```

> runtime anomaly、review/test 新发现、治理漂移等信号由 auto-loop 捕获后，通过 chat 插话或创建平台 issue 进入 B1_IBM，不直接作为 B1_IBM 的 Input。

## B1_IBM：Input → Brainstorm → Milestone

从 Input source 到 candidate 进入 milestone。

| 字母 | 含义 | 说明 |
|------|------|------|
| I | Input source | github issue、gitee issue、Freely chat 插话。其他信号（runtime anomaly、review 发现等）需通过 chat 或创建平台 issue 进入 |
| B | Brainstorm | 发散→收敛→决策。读边界（CONSTITUTION/LAWS/PROJECT_INTENT）、读验收、读依赖。产物：`brainstorms.md` |
| M | Milestone | 产出 candidate（`candidates.md`）：scope、non-goals、priority、status、milestone 归属 |

**信号进入 B1_IBM**：
- 平台 issue（github/gitee）：`task-source-scan.py` 下载到本地 `.freely/issues/`。raw issue 的 `restart_point=pre_brainstorm`，lead agent 路由到 B1_IBM
- chat 插话：`freely chat` → `chat-routing skill` 判断属于哪个 issue → 创建 raw issue 或已有 issue 的 comment → 写入 `.freely/issues/`。新 raw issue 进入 scan → B1_IBM
- 其他信号（runtime anomaly、review 发现）：通过 chat 插话进入，同上
- AI **永远不直接读平台内容**——只读本地 `.freely/issues/` 中的副本。平台内容由 scan 脚本下载一次
- 详细路由见 `context-source-skill` 和 `docs/system/workspace/three-loop-capability-lifecycle.md`

**B1 回答**：这个值得做吗？排在哪？边界是什么？

**目录**：`docs/pre-brainstorms/{b1-id}/`

```
{b1-id}/
├── brainstorms.md    # 预研讨论、上下文、决策理由
└── candidates.md     # candidate 规格：scope/non-goals/priority/status
```

**candidate status**：`proposed` → `needs_research` → `blocked` → `promoted` / `absorbed` / `dropped`

**对应 three-loop**：doc-loop 的 pre-brainstorm 子循环（`three-loop-capability-lifecycle.md` 行 43-60）

## B2_IBM：Input → Brainstorm → Map

从 milestone committed_issues 中的正式 issue 到 map 产物完整交付。

| 字母 | 含义 | 说明 |
|------|------|------|
| I | Input source | milestone `committed_issues` 中的正式 issue（I-{key}）。已排期、已分配 priority、已有正式 issue 文档 |
| B | Brainstorm | 实现前置设计。读实现面、读验收标准、评估替代方案。产物：`brainstorms/b-{issue-name}.md` |
| M | Map | 实现设计落地为完整目录结构和文档集 |

**B2 回答**：怎么做？怎么验收？替代方案是什么？

**目录**：`docs/epics/{epic-name}/{story-name}/`

```
{story-name}/
├── brainstorms/
│   └── b-{issue-name}.md   # 实现头脑风暴
├── issues/
│   └── {issue-name}.md     # 正式 issue 文档
├── prd.md                  # 可选：产品需求文档
├── pre-tests.md            # 验收测试计划
├── tasks.md                # 任务分解
└── code-reviews/           # 代码审查与验证证据
    └── {review-file}.md
```

**issue phase_state**：`in_b2_ibm` → `done_b2_ibm` → `in_dev` → `blocked_dev` → `in_verification` → `completed`

**对应 three-loop**：doc-loop 的 IBM 子循环（`three-loop-capability-lifecycle.md` 行 61-78），完成后进入 dev-loop（行 79-105）

## B1_IBM 与 B2_IBM

| | B1_IBM | B2_IBM |
|---|---|---|
| I（输入） | github/gitee issue、chat 插话 | milestone committed_issues 中的正式 issue（I-{key}） |
| B（头脑风暴） | 边界收敛、价值判断 | 实现设计、替代方案评估、验收标准 |
| M（产物） | candidate → milestone queue | Map：issues + PRD + pre-tests + tasks + code-review |
| 核心问题 | 做不做？排哪？边界？ | 怎么做？怎么验？替代方案？ |
| 执行循环 | doc-loop pre-brainstorm 子循环 | doc-loop IBM 子循环 → dev-loop |
| 状态字段 | `candidate.status` | `issue.phase_state` |

## milestone 的角色

milestone 是 B1_IBM 和 B2_IBM 之间的排序与承接层。

- `candidate_issues`：B1_IBM 产出的 candidate 队列。未收口的 candidate 继续留在此处，写清 `next_action` 和 `revisit_trigger`
- `committed_issues`：B2_IBM 的 I 的来源。candidate 被 promoted 后，正式 issue 进入此队列
- milestone 的 `M-{key}` 是 candidate 身份，不等于执行编排身份。IBM materialization 产出 `I-{key}` 后，编排切到 I-*

## 与 Three-Loop 的关系

IBM Framework 定义 **doc-loop 内的治理生命周期**。Three-Loop 定义 **AI 的执行路由**（auto/doc/dev loop）。两者正交：

```
B1  ←→  doc-loop pre-brainstorm 子循环
B2  ←→  doc-loop IBM 子循环（设计）+ dev-loop（实现）
auto-loop ←→ 信号捕获、B1/B2 之间的 routing、completion/verification/cleanup/retirement
```

详细 routing 见 `docs/system/workspace/three-loop-capability-lifecycle.md`。治理规则见 `docs/LAWS.md` §2。

## Issue 存储与平台隔离

IBM Framework 的 I（Input source）统一为 github/gitee issue。平台 issue 通过 scan 下载到本地，AI 只读写本地副本。

### 本地存储

```
.freely/issues/
├── ISSUES.md                          # 所有 issue 的映射索引
├── comments/
│   └── {comment-id}.md                # 评论（frontmatter 记录归属 issue）
├── raw-{YYYYMMDD}-{NNNN}/             # raw issue：B1_IBM 的 Input
│   ├── meta.env                       # 平台 ID、状态、canonical 关联
│   └── issue.md                       # issue 正文
└── I-{YYYYMMDD}-{NNNN}-{split}/       # linked issue：B2_IBM 的产物
    ├── meta.env                       # 平台 ID、canonical 路径
    └── issue.md                       # 正式 issue 摘要
```

### 平台隔离

- AI **永远不直接读写平台**（不调 github/gitee API）
- **scan**（`task-source-scan.py`）是平台→本地的唯一桥梁：下载 issue、评论到 `.freely/issues/`
- **sync**（`bin/issue-sync`）是本地→平台的唯一桥梁：创建 issue、更新状态、推送评论
- sync 触发是确定性的生命周期事件（candidate promoted、phase_state 变更、merge），不是 AI 判断
- 本地是唯一真相源。平台数据丢失时从本地重建

### chat 插话 → issue

每条 `freely chat` 必须落地为 issue 或已有 issue 的评论：

- `chat-routing skill` 判断消息归属（OPEN issue→comment，CLOSED→reopen 或新建并 link，新内容→新建 raw issue）
- skill 只做路由，不做价值判断。最终 promote/absorb/drop 由 B1_IBM 决定
- 即使内容看似无价值，也创建 raw issue——B1 标记 `dropped` 并写清 `drop_reason`

### issue 生命周期中的 sync 触发点

| 事件 | sync 动作 |
|------|----------|
| chat 插话 | `issue-sync comment`（异步） |
| candidate promoted | `issue-sync create`（创建里程碑 issue） |
| phase_state→in_dev | `issue-sync comment`（异步） |
| merge 到 develop | `issue-sync comment` + `issue-sync close`（关闭 raw issue） |
| cleanup 完成 | `issue-sync close`（关闭里程碑 issue） |

## 术语约定

| 旧称 | 新称 | 说明 |
|------|------|------|
| 预研头脑风暴 | B1_IBM | I → B → M 第一阶段，Input 是平台 issue 或 chat 插话 |
| IBM 头脑风暴 | B2_IBM | I → B → M 第二阶段，Input 是 milestone 中的正式 issue |
| 候选 | candidate | B1_IBM 产物，milestone 输入 |
| 里程碑 | milestone | B1_IBM 和 B2_IBM 之间的排序层 |
| 正式 issue | issue | B2_IBM 的 I，milestone committed_issues 中的 I-{key} |

在 prompt、文档、代码中引用：使用 "按 IBM Framework B1_IBM/B2_IBM" 或 `@ibm-framework`。
