# IBM Framework

Freely doc-loop 的治理框架。每个工作项在 doc-loop 中经历两个 I-B-M 阶段，由 Milestone 串联。本文件是 IBM Framework 的能力真源——Freely 开发自身项目时吃自己的狗粮，外部项目由 Freely 托管时同样以此框架推进。

执行路由（auto/dev loop）见 `docs/system/workspace/three-loop-capability-lifecycle.md`。治理规则（status 校验、gate 白名单、字段约束）见 `docs/LAWS.md` §2。

## 总览

```
 B1: Input → Brainstorm → Milestone          B2: Input → Brainstorm → Map
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

> runtime anomaly、review/test 新发现、治理漂移等信号由 auto-loop 捕获后，通过 chat 插话或创建平台 issue 进入 B1，不直接作为 B1 的 Input。

## B1：Input → Brainstorm → Milestone

从 Input source 到 candidate 进入 milestone。

| 字母 | 含义 | 说明 |
|------|------|------|
| I | Input source | github issue、gitee issue、Freely chat 插话。其他信号（runtime anomaly、review 发现等）需通过 chat 或创建平台 issue 进入 |
| B | Brainstorm | 发散→收敛→决策。读边界（CONSTITUTION/LAWS/PROJECT_INTENT）、读验收、读依赖。产物：`brainstorms.md` |
| M | Milestone | 产出 candidate（`candidates.md`）：scope、non-goals、priority、status、milestone 归属 |

**信号进入 B1**：
- github/gitee issue：`task-source-scan.py` 扫描到 raw issue 后，`restart_point=pre_brainstorm`，lead agent 路由到 B1
- chat 插话：`freely chat` → `.freely/intake/` → `interruption-manager-handler` 分类为 `discovery` → 路由到 B1
- 其他信号（runtime anomaly、review 发现）：先通过 chat 插话或创建平台 issue，再进入上述路径
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

## B2：Input → Brainstorm → Map

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

**issue phase_state**：`in_ibm` → `done_ibm` → `in_dev` → `blocked_dev` → `in_verification` → `completed`

**对应 three-loop**：doc-loop 的 IBM 子循环（`three-loop-capability-lifecycle.md` 行 61-78），完成后进入 dev-loop（行 79-105）

## B1 与 B2

| | B1 | B2 |
|---|---|---|
| I（输入） | github/gitee issue、chat 插话 | milestone committed_issues 中的正式 issue（I-{key}） |
| B（头脑风暴） | 边界收敛、价值判断 | 实现设计、替代方案评估、验收标准 |
| M（产物） | candidate → milestone queue | Map：issues + PRD + pre-tests + tasks + code-review |
| 核心问题 | 做不做？排哪？边界？ | 怎么做？怎么验？替代方案？ |
| 执行循环 | doc-loop pre-brainstorm 子循环 | doc-loop IBM 子循环 → dev-loop |
| 状态字段 | `candidate.status` | `issue.phase_state` |

## milestone 的角色

milestone 是 B1 和 B2 之间的排序与承接层。

- `candidate_issues`：B1 产出的 candidate 队列。未收口的 candidate 继续留在此处，写清 `next_action` 和 `revisit_trigger`
- `committed_issues`：B2 的 I 的来源。candidate 被 promoted 后，正式 issue 进入此队列
- milestone 的 `M-{key}` 是 candidate 身份，不等于执行编排身份。IBM materialization 产出 `I-{key}` 后，编排切到 I-*

## 与 Three-Loop 的关系

IBM Framework 定义 **doc-loop 内的治理生命周期**。Three-Loop 定义 **AI 的执行路由**（auto/doc/dev loop）。两者正交：

```
B1  ←→  doc-loop pre-brainstorm 子循环
B2  ←→  doc-loop IBM 子循环（设计）+ dev-loop（实现）
auto-loop ←→ 信号捕获、B1/B2 之间的 routing、completion/verification/cleanup/retirement
```

详细 routing 见 `docs/system/workspace/three-loop-capability-lifecycle.md`。治理规则见 `docs/LAWS.md` §2。

## 术语约定

| 旧称 | 新称 | 说明 |
|------|------|------|
| 预研头脑风暴 | B1 | I → B → M 第一阶段，Input 是平台 issue 或 chat 插话 |
| IBM 头脑风暴 | B2 | I → B → M 第二阶段，Input 是 milestone 中的正式 issue |
| 候选 | candidate | B1 产物，milestone 输入 |
| 里程碑 | milestone | B1 和 B2 之间的排序层 |
| 正式 issue | issue | B2 的 I，milestone committed_issues 中的 I-{key} |

在 prompt、文档、代码中引用：使用 "按 IBM Framework B1/B2" 或 `@ibm-framework`。
