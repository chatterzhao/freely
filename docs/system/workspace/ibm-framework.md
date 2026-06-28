# IBM Framework

Freely doc-loop 的治理框架。每个工作项经历两个 IBM 阶段——B1_IBM 和 B2_IBM——由 Milestone 串联。

每个阶段的引擎是 AI 做 Brainstorm（B）：从 Input source（I）摄取输入，经发散→收敛→决策，产出 Milestone candidate 或 Map 文档集（M）。两个阶段共享 I→B→M 骨架，区别在于 I 的来源不同、M 的产物不同，因此命名为 B1_IBM 和 B2_IBM——B 打头强调 Brainstorm 是核心，IBM 是贯穿两个阶段的 I-B-M 结构。

本文件是 IBM Framework 的能力真源。Freely 开发自身项目时吃自己的狗粮，外部项目由 Freely 托管时同样以此框架推进。执行路由（auto/dev loop）见 `docs/system/workspace/three-loop-capability-lifecycle.md`，治理规则见 `docs/LAWS.md` §2。

> **注意**: 以下 ASCII 图不反映 chat-inbox 架构（chat 不再直接写 `docs/issues/`）。
> 计划后续用 SVG 重绘。

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

从 scan 发现的 Input source 到 candidate 进入 milestone 规划。

| 字母 | 含义 | 说明 |
|------|------|------|
| I | Input source | github issue、gitee issue、Freely chat 插话。其他信号（runtime anomaly、review 发现等）需通过 chat 或创建平台 issue 进入 |
| B | Brainstorm | 发散→收敛→决策。读边界（CONSTITUTION/LAWS/PROJECT_INTENT）、读验收、读依赖。产物：`brainstorms.md` |
| M | Milestone | 产出 candidate（`candidates.md`）：scope、non-goals、priority、status、milestone 归属 |

**信号进入 B1_IBM**：
- 平台 issue（github/gitee）：`task-source-scan.py` 下载到本地 `docs/issues/`。raw issue 的 `restart_point=pre_brainstorm`，lead agent 路由到 B1_IBM
- chat 插话：`freely chat` → `chat-routing skill` 判断属于哪个 issue → 写入 `.freely/freely.db`（git-ignored 暂存，不污染 protected branch）。`task-source-scan` 扫出未消费的 chat，AI 判断后创建工位（wt-create 自动 materialize 到 `docs/issues/`）或追加评论
- chat 写入时若有对应工位，则直接同步到 worktree 的 `docs/issues/`，跳过暂存
- 其他信号（runtime anomaly、review 发现）：通过 chat 插话进入，同上
- AI **永远不直接读平台内容**——只读本地 `docs/issues/` 中的副本。平台内容由 scan 脚本下载一次
- 详细路由见 `freely-context-source-skill` 和 `docs/system/workspace/three-loop-capability-lifecycle.md`

**B1_IBM 回答**：这个值得做吗？排在哪？边界是什么？

**目录**：`docs/pre-brainstorms/{b1-id}/`

```
{b1-id}/
├── brainstorms.md    # 预研讨论、上下文、决策理由
└── candidates.md     # candidate 规格：scope/non-goals/priority/status
```

**candidate status**：`proposed` → `needs_research` → `blocked` → `promoted` / `absorbed` / `dropped`

**对应 three-loop**：doc-loop 的 pre-brainstorm 子循环（`three-loop-capability-lifecycle.md` 行 43-60）

## B2_IBM：Input → Brainstorm → Map

从 scan、A2A task 与 continuity evidence 选出并提交到 milestone 的 issue 到 map 产物完整交付。

| 字母 | 含义 | 说明 |
|------|------|------|
| I | Input source | milestone `committed_issues` 中的正式 issue（I-{key}）。已排期、已分配 priority、已有正式 issue 文档 |
| B | Brainstorm | 实现前置设计。读实现面、读验收标准、评估替代方案。产物：`brainstorms/b-{issue-name}.md` |
| M | Map | 实现设计落地为完整目录结构和文档集 |

**B2_IBM 回答**：怎么做？怎么验收？替代方案是什么？

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

**完成后衔接**：B2_IBM 完成后，进入 Dev 实现 → test-pre-merge 验证 → pr-create-guarded（提 PR）→ pr-merge-guarded（门禁合并）→ wt-close（收口）

## B1_IBM 与 B2_IBM

| | B1_IBM | B2_IBM |
|---|---|---|
| I（输入） | github/gitee issue、chat 插话 | milestone committed_issues 中的正式 issue（I-{key}） |
| B（头脑风暴） | 边界收敛、价值判断 | 实现设计、替代方案评估、验收标准 |
| M（产物） | candidate → milestone 规划队列 | Map：issues + PRD + pre-tests + tasks + code-review |
| 核心问题 | 做不做？排哪？边界？ | 怎么做？怎么验？替代方案？ |
| 执行循环 | doc-loop pre-brainstorm 子循环 | doc-loop IBM 子循环 → dev-loop |
| 状态字段 | `candidate.status` | `issue.phase_state` |

## milestone 的角色

milestone 是 B1_IBM 和 B2_IBM 之间的排序与承接层。

- `candidate_issues`：B1_IBM 产出的 candidate 队列。未收口的 candidate 继续留在此处，写清 `next_action` 和 `revisit_trigger`
- `committed_issues`：B2_IBM 管道内部的 I 来源（任务选择来自 scan、A2A task 与 continuation evidence）。candidate 被 promoted 后，正式 issue 进入此队列
- milestone 的 `M-{key}` 是 candidate 身份，不等于执行编排身份。IBM materialization 产出 `I-{key}` 后，编排切到 I-*

## 与 Three-Loop 的关系

IBM Framework 定义 **doc-loop 内的治理生命周期**。Three-Loop 定义 **AI 的执行路由**（auto/doc/dev loop）。两者正交：

```
B1_IBM  ←→  doc-loop pre-brainstorm 子循环
B2_IBM  ←→  doc-loop IBM 子循环（设计）+ dev-loop（实现）
auto-loop ←→ 信号捕获、B1/B2 之间的 routing、completion/verification/cleanup/retirement
```

详细 routing 见 `docs/system/workspace/three-loop-capability-lifecycle.md`。治理规则见 `docs/LAWS.md` §2。

## Issue 存储与平台隔离

IBM Framework 的 I（Input source）统一为 github/gitee issue。平台 issue 通过 scan 下载到本地，AI 只读写本地副本。

### 本地存储

```
docs/issues/
├── raw-{YYYYMMDD}-{HHMM}/             # raw issue（旧格式）
├── raw-{YYYYMMDDTHHMM[SS]Z}/              # raw issue（新格式, ISO 8601 紧凑型）
└── I-{YYYYMMDDTHHMM[SS]Z}-{A,B,C}/       # linked issue（新旧格式均支持）
    └── issue.md
```

### ID 命名规范

四种 issue 共享同一 `{key}`，逐级继承，从 C-* 开始带 `{suffix}`：

| 类型 | 命名 | 生成阶段 | 说明 |
|------|------|---------|------|
| `raw-{key}` | `key` = UTC 创建时间戳，如 `20260505T101010Z` | feedback / 平台扫描 | 对外联络的平台 issue |
| `C-{key}-{suffix}` | 继承 raw key，加后缀 A/B/C… | B1 预研 | 候选 issue。一个 raw 可拆为多个 C-* |
| `M-{key}-{suffix}` | 与 C-* 同名 | B1 里程碑编排 | 进入里程碑的候选。未被丢弃的 C-* |
| `I-{key}-{suffix}` | 与 M-* 同名 | B2 物化 | 当前里程碑正在开发的正式 issue。由 B2 skill 物化到 `docs/issues/` |

**关键规则**：
- `{key}` 从 raw issue 取（`raw-` 前缀之后的部分）
- `{suffix}` 从 C-* issue 取（第一个 `-` 之后的部分），如 `C-20260505T101010Z-A` → suffix = `A`
- 整个命名链：`raw-{key}` → `C-{key}-{suffix}` → `M-{key}-{suffix}` → `I-{key}-{suffix}`
- 代码中不能自编后缀，必须从 C-* 或 I-* 文件系统 glob 获取

`YYYYMMDDTHHMMSSZ` 为 ISO 8601 紧凑型 UTC 时间，精确到秒。旧格式 `YYYYMMDD-HHMM` 仍兼容。

**raw-* 和 I-* 的关系**：

```
chat 插话 / 平台扫描
        │
        ▼
   raw-*        kind: raw, phase_state: proposed
   B1_IBM       预研收敛 → candidate
        │
   ┌────┼────────────┐
   │    │            │
  drop absorb      promote → I-*   kind: linked, phase_state: in_b2_ibm
                      │           B2_IBM 实现设计 → Map 产物
                      │
                 merge to develop
                      │
                 phase_state: completed
```

- raw-* 只存在于 B1_IBM 阶段。一旦 promote 为 I-*，raw 的 `phase_state` 变为 `absorbed`，`absorbed_into` 指向 I-*
- I-* 是 B2_IBM 阶段的唯一 issue 标识。后续所有 chat、comment、状态变更都发生在 I-* 上
- **ID 格式**：`raw-YYYYMMDDTHHMM[SS]Z`（新，ISO 8601）/ `raw-YYYYMMDD-HHMM`（旧，仍兼容）。C-* 和 I-* 在此基础上加 `-A`/`-B`/`-C` 后缀。一个 raw 可孵化多个 I-*。门禁用 `startswith(raw_key)` 验证父子关系，用 `candidate_key == issue_key`（去前缀）验证 C→I
- `chat --issue raw-xxx` 会自动检测 `phase_state=absorbed`，路由到 `absorbed_into` 指向的 I-*
- I-* 采用自包含摘要 + 链接模式：平台 body 包含足够上下文，深水区讨论链接到 B1_IBM 产物

### 平台隔离

- AI **永远不直接读写平台**（不调 github/gitee API）
- **scan**（`task-source-scan.py`）是平台→本地的唯一桥梁：下载 issue、评论到 `docs/issues/`
- **sync**（`bin/issue-sync`）是本地→平台的唯一桥梁：创建 issue、更新状态、推送评论
- sync 触发是确定性的生命周期事件（candidate promoted、phase_state 变更、merge），不是 AI 判断
- 本地是唯一真相源。平台数据丢失时从本地重建

### chat 插话 → issue

每条 `freely chat` 必须落地为 issue 或已有 issue 的评论：

- 所有 chat 先写入 `.freely/freely.db`（SQLite，git-ignored），不直接写 `docs/issues/`
- chat 写入时若有对应工位，直接同步到 worktree 的 `docs/issues/`，标记 consumed=1
- 无工位时留在 DB（consumed=0），由 task-source-scan 扫出供 AI 判断
- 如果是新话题（`--new-issue`）：AI 创建工位 → wt-create 自动 materialize 到 worktree 的 `docs/issues/`
- 如果是已有 issue 的评论（`--issue <id>`）：AI 在 worktree 中追加评论
- 噪声（如"你好"）：标记 consumed=-1 丢弃
- 如果 `--issue raw-xxx` 但该 raw 已被 promote（`phase_state=absorbed`）：自动路由到 `absorbed_into` 指向的 I-*
- skill 只做路由，不做价值判断。最终 promote/absorb/drop 由 B1_IBM 决定

### issue 生命周期中的 sync 触发点

| 事件 | sync 动作 | 触发机制 |
|------|----------|---------|
| chat 插话（写入 chat-inbox） | `issue-sync comment` | AI 消费后 |
| raw issue 创建（wt-create materialize） | `issue-sync create` | wt-create 内部调用 |
| candidate promoted → I-* | `issue-sync promote` | B1_IBM 收口时脚本调用 |
| phase_state 变更 | `issue-sync update` | daemon worker 完成状态更新后 |
| merge 到 develop | `issue-sync close`（关闭已完成的 I-*） | `pr-merge-guarded` post-merge hook |
| cleanup 完成 | `issue-sync close` | daemon worker 收口 |

### 平台 issue 格式

每个 platform issue 由三要素组成：标题前缀 + 标签 + metadata body。

| 要素 | raw-* | I-* |
|------|-------|-----|
| 标题 | `[RAW-20260428-0542] <title>` | `[I-20260426-1423] <title>` |
| 标签 | `kind/raw`, `phase/proposed` | `kind/linked`, `phase/<phase_state>` |
| body | 元数据表 + issue 正文 | 元数据表 + Pre-Brainstorm Summary + Scope + References |

body 结构（I-*）：
```markdown
## <issue_title>
| local_id | kind | phase | promoted_from |
|----------|------|-------|---------------|
| I-xxx | linked | completed | raw-xxx |

### Pre-Brainstorm Summary
<2-3 句从 candidate.md 抽取的结论，足够让平台读者理解决策>

### Scope
<从 candidate.md 或 issue doc 提取的 scope/non-goals>

### References
- B1 预研: docs/pre-brainstorms/<b1-id>/
- Candidate: docs/pre-brainstorms/<b1-id>/candidates.md#c-xxx
- 正式 Issue: docs/epics/<epic>/<story>/issues/<name>.md
```

## 术语约定

| 旧称 | 新称 | 说明 |
|------|------|------|
| 预研头脑风暴 | B1_IBM | I → B → M 第一阶段，Input 是平台 issue 或 chat 插话 |
| IBM 头脑风暴 | B2_IBM | I → B → M 第二阶段，Input 是 milestone 中的正式 issue |
| 候选 | candidate | B1_IBM 产物，milestone 输入 |
| 里程碑 | milestone | B1_IBM 和 B2_IBM 之间的排序层 |
| 正式 issue | issue | B2_IBM 的 I，milestone committed_issues 中的 I-{key} |

在 prompt、文档、代码中引用：使用 "按 IBM Framework B1_IBM/B2_IBM" 或 `@ibm-framework`。

**issue.md 格式**（frontmatter 元数据 + 正文 + Comments 章节）：

```markdown
---
local_id: I-20260426-1423
issue_title: "Add opencode direct launcher and AI_TOOL alias resolution"
kind: linked
phase_state: completed
promoted_from: raw-20260426-0001            # I-* 专有：来源 raw issue
absorbed_into: ""                           # raw-* 专有：被哪个 I-* 吸收
platform_ids:
  github: {issue_id: "42", url: "https://...", synced_at: "..."}
  gitee: {issue_id: "IJFOAK", url: "https://...", synced_at: "..."}
primary_platform: github
canonical_issue_path: "docs/epics/.../issues/....md"
last_synced_comment_at:
  github: "2026-04-27T10:25:00Z"
  gitee: "2026-04-27T10:25:00Z"
hash: ""
created_at: "2026-04-27T10:00:00Z"
updated_at: "2026-04-27T10:25:00Z"
session_refs:
  - {tool: ccds, session_id: "xxx", role: "author"}
---

## Pre-Brainstorm Summary
<简要结论，从 candidate.md 提取，I-* 专有>

## Scope
<scope/non-goals>

## References
- B1: docs/pre-brainstorms/{b1-id}/
- Issue: docs/epics/{epic}/{story}/issues/{name}.md

## Comments

### comment-20260427T102500Z
- source: chat
- author: human

评论内容。
```

**frontmatter 字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `local_id` | string | 本地唯一 ID，`raw-{ts}` 或 `I-{ts}` |
| `issue_title` | string | 人类可读标题，用于平台 issue 标题 |
| `kind` | raw\|linked | raw = B1_IBM 输入，linked = B2_IBM 正式 issue |
| `phase_state` | string | 治理生命周期。<br>raw-*: proposed\|absorbed\|dropped<br>I-*: in_b2_ibm\|done_b2_ibm\|in_dev\|blocked_dev\|in_verification\|completed |
| `platform_state` | string | 平台同步状态：open\|closed。由 issue-sync create/close 自动管理 |
| `promoted_from` | string | I-* 专有：来源 raw-* 的 local_id |
| `absorbed_into` | string | raw-* 专有：被 promote 到哪个 I-* |
| `platform_ids` | dict | 每个平台的 issue_id、url、synced_at |
| `primary_platform` | string | github\|gitee，优先推送/拉取的主平台 |
| `canonical_issue_path` | string | I-* 专有：B2_IBM 正式 issue 文档路径 |
| `last_synced_comment_at` | dict | 按平台记录最后评论同步时间 |
| `created_at` / `updated_at` | ISO8601 | 时间戳 |

- 所有元数据在 YAML frontmatter 中（参考 issueme `data-model.md`）
- `platform_ids`：issue 级别记录每个平台的 issue_id 和同步时间。评论级别记录每个平台的 comment_id
- `last_synced_comment_at`：**按平台分别记录**。sync 时比较各平台的时间戳，只推送增量
- `primary_platform`：主平台标记。push 优先 push 主平台，pull 优先从主平台拉取
- 每条评论的标题为 `### comment-{local_id}`。local_id 在创建时立即生成（`comment-YYYYMMDDTHHMMSSZ`），不依赖平台返回
- `platform_ids` 记录平台上的 comment_id。sync 后异步写回，未同步时字段为空
- 本地引用永远用 local_id，不依赖平台 ID 的存在
- `hash`：内容幂等校验，避免重复推送
- 每条评论是一个 `###` 章节，按时间倒序或正序排列
