# 预研：外部 Issue 集成与 Freely 自身迭代闭环

## Context

- 日期：2026-04-03
- 触发：
  - Freely 已具备"打工"能力（为托管项目开发）
  - Freely 需求来源多元：GitHub issue、Gitee issue、打工发现、运行时反馈
  - 问题：如何统一管理外部 issue 与内部需求，形成完整闭环

## 核心概念

### Issue 状态分类

```
外部来源（未消化）                    Freely 内部（已消化）
─────────────────                    ──────────────────
GitHub issue ──┐
               │
Gitee issue ───┼──► 预研头脑风暴 ──► 候选 issue ──► Milestone
               │         │
其他来源 ──────┘         │
                         │
                         ▼
              是否同步到 GitHub？
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
  同步（带标签）            不同步
  如：status: triaged       纯内部
  不再被预研消费
```

### 标签体系

| 状态 | 来源 | 标签 | 是否被预研消费 |
|------|------|------|---------------|
| 未消化 | GitHub/Gitee issue | 无/`status: new` | ✅ 是 |
| 已消化 | 预研产出 | `status: triaged` | ❌ 否 |
| 进行中 | 已分配 worktree | `status: in-progress` | ❌ 否 |
| 已完成 | 已合并 | `status: completed` | ❌ 否 |
| 内部需求 | 打工发现/运行时 | 可选同步 | 取决于是否同步 |

## Problem

### 核心挑战

1. **外部 Issue 消化流程**
   - GitHub/Gitee issue 如何进入预研
   - 消化后如何标记避免重复消费
   - 消化结果如何反馈到原 issue

2. **内部需求回流**
   - 打工中发现的 Freely 缺口如何沉淀
   - 是否同步到 GitHub（透明化 vs 内部）
   - 如何避免循环消费（内部 issue 再被预研）

3. **Freely 自身迭代**
   - Freely 升级时如何不打断用户项目
   - 资源竞争如何调度
   - 发布节奏如何协调

## Candidate Models

### Model A：外部 Issue 消化流程

```
┌─────────────────────────────────────────────────────────────┐
│                     外部 Issue 生命周期                      │
│                                                              │
│  GitHub Issue        Gitee Issue        其他来源             │
│      │                   │                  │               │
│      └───────────┬───────┘                  │               │
│                  ▼                          │               │
│         ┌───────────────┐                   │               │
│         │ Freely 启动    │                   │               │
│         │ 扫描 open issue│                   │               │
│         └───────┬───────┘                   │               │
│                 │                           │               │
│                 ▼                           │               │
│         ┌───────────────┐                   │               │
│         │ 过滤已消化标签 │                   │               │
│         │ status: triaged│                  │               │
│         └───────┬───────┘                   │               │
│                 │                           │               │
│         ┌───────┴───────┐                   │               │
│         ▼               ▼                   │               │
│    未消化 issue    已消化 issue              │               │
│         │               │                   │               │
│         ▼               └── 跳过            │               │
│    进入预研流程                                │               │
│         │                                      │           │
│         ▼                                      │           │
│    pre-brainstorm                              │           │
│         │                                      │           │
│         ▼                                      │           │
│    候选 issue                                  │           │
│         │                                      │           │
│         ├──────────────────────────────────────┘           │
│         │                                                  │
│         ▼                                                  │
│    同步回 GitHub/Gitee：                                    │
│    - 添加标签 status: triaged                               │
│    - 评论：已进入预研，链接到 pre-brainstorm                │
│                                                            │
└─────────────────────────────────────────────────────────────┘
```

---

### Model B：内部需求回流流程

```
┌─────────────────────────────────────────────────────────────┐
│                     内部需求生命周期                         │
│                                                              │
│  打工中发现缺口      运行时异常        治理漂移               │
│      │                 │                 │                  │
│      └───────────┬─────┴─────────────────┘                  │
│                  │                                          │
│                  ▼                                          │
│         ┌───────────────┐                                   │
│         │ 判断是否 Freely │                                  │
│         │ 自身问题       │                                   │
│         └───────┬───────┘                                   │
│                 │                                           │
│         ┌───────┴───────┐                                   │
│         ▼               ▼                                   │
│    用户项目问题    Freely 自身问题                            │
│         │               │                                   │
│         ▼               ▼                                   │
│    写入用户项目    写入 Freely 的                             │
│    pre-brainstorm  pre-brainstorm                           │
│                         │                                   │
│                         ▼                                   │
│                  ┌───────────────┐                          │
│                  │ 是否同步到     │                          │
│                  │ GitHub？      │                          │
│                  └───────┬───────┘                          │
│                          │                                  │
│              ┌───────────┴───────────┐                      │
│              ▼                       ▼                      │
│         同步创建 issue          纯内部                       │
│         带标签：                不创建 issue                 │
│         status: triaged        直接进入 milestone           │
│         source: internal                                    │
│                                                            │
└─────────────────────────────────────────────────────────────┘
```

---

### Model C：标签体系设计

```yaml
# 状态标签
status:
  new:          # 新建，未消化
  triaged:      # 已消化，进入预研
  in-progress:  # 已分配 worktree，开发中
  completed:    # 已完成，已合并

# 来源标签
source:
  github:       # 来自 GitHub issue
  gitee:        # 来自 Gitee issue
  internal:     # Freely 内部发现
  chat:         # 来自 chat 输入

# 优先级标签
priority:
  blocking:     # 阻塞性，必须立即处理
  high:         # 高优先级
  normal:       # 正常
  low:          # 低优先级
```

---

### Model D：GitHub 状态同步策略

```
Freely 内部状态              GitHub Issue 状态
─────────────────           ─────────────────
候选 issue (triaged)   ──►  标签 status: triaged
                              评论：链接到 pre-brainstorm

Issue 进入 milestone    ──►  标签 status: in-progress
                              评论：已分配 worktree

Issue 完成              ──►  标签 status: completed
                              关闭 issue
                              评论：合并链接
```

---

## Confirmed Workflow

### Issue 阶段与编号

```
阶段              编号格式              位置                        是否同步到 GitHub
──────────────   ──────────────────   ────────────────────────   ────────────────
候选 issue       C-YYYYMMDD-HHMM-序号  pre-brainstorms/*/candidates.md   ❌ 内部
里程碑 issue     I-YYYYMMDD-HHMM-序号  docs/epics/*/issues/*.md          ✅ 是
```

**里程碑 issue 对应 GitHub issue 的理由：**
- 里程碑 issue 有完整的 `phase_state`（in_ibm/done_ibm/in_dev/blocked_dev/in_verification/completed）
- 候选 issue 还在预研阶段，可能被拒绝或需要更多研究
- 只有被里程碑正式接纳的 issue 才值得公开追踪

### GitHub Issue 消费区分

```
GitHub Issue 类型判断：
─────────────────────

扫描 GitHub open issues
       │
       ├─ 有 status: triaged 标签？
       │      │
       │      ├─ 是 + 有 source: github 标签 → 里程碑 issue（跳过，只同步状态）
       │      │
       │      └─ 是 + 无 source 标签 → 来源 issue 已消化（跳过，只同步评论）
       │
       └─ 无 status: triaged 标签 → 来源 issue 未消化（消费，进入预研）
```

**区分规则：**

| 类型 | status: triaged | source 标签 | 处理 |
|------|:---------------:|:-----------:|------|
| 来源 issue（未消化） | ❌ 无 | ❌ 无 | 消费，进入预研 |
| 来源 issue（已消化） | ✅ 有 | ❌ 无 | 跳过，只同步评论 |
| 里程碑 issue | ✅ 有 | ✅ 有 | 跳过，同步状态标签 |

### 映射关系

```
内部里程碑 issue         GitHub 里程碑 issue      GitHub 来源 issue
─────────────────       ───────────────────     ─────────────────
I-20260403-1000-A  ←─→  #456 (Freely 创建)  ←─→  #123 (用户创建)

存储位置：.freely/github-issue-mapping.json

{
  "I-20260403-1000-A": {
    "github_milestone_issue": 456,
    "github_source_issue": 123,
    "source_platform": "github"
  },
  "I-20260403-1000-B": {
    "github_milestone_issue": 457,
    "github_source_issue": null,
    "source_platform": "internal"
  }
}
```

### 外部 Issue 消化流程（来源是 GitHub issue）

```
GitHub Issue #123 (来源 issue，无 status: triaged 标签)
       │
       │  Freely 启动扫描
       │  过滤已消化（有 status: triaged 则跳过）
       ▼
  预研/消化
       │
       │  进入 pre-brainstorms/
       ▼
  候选 issue C-xxx (内部，不公开)
       │
       │  里程碑接纳 (status: promoted)
       ▼
  创建里程碑 issue I-xxx 到 GitHub (#456)
  - 标签: status: triaged
  - 标签: source: github
  - 内容: 标题 + 来源链接 (#123) + 预研链接 + 验收标准
       │
       ▼
  来源 issue #123 添加：
  - 评论: "已接纳为 #456，后续进展在此 issue 追踪"
  - 标签: status: triaged（标记为已消化，不再被预研消费）
  - 不关闭，保持打开状态
       │
       ▼
  存储映射关系：
  .freely/github-issue-mapping.json
  {
    "I-xxx": {
      "github_milestone_issue": 456,
      "github_source_issue": 123,
      "source_platform": "github"
    }
  }
```

### 里程碑 Issue 内容格式

```markdown
# I-20260403-1000-A: 外部 Issue 消化与闭环流程

## 来源
- 来源 issue: #123
- 预研链接: [20260403-1000--external-issue-integration-and-self-evolution](链接)

## 问题描述
Freely 需求来源多元...

## 验收标准
- [ ] 定义外部 issue 消化流程
- [ ] 定义里程碑接纳流程
- ...

## 状态追踪
- phase_state: in_ibm
- worktree: feature/external-issue-integration-20260403-xxxx
```

### 状态同步动作

```
phase_state 变更时：

in_ibm:
  - 来源 issue #123: 评论 "📋 需求分析中"
  - 里程碑 issue #456: 添加标签 status: in-progress

in_dev:
  - 来源 issue #123: 评论 "🔨 开发中，worktree: feature/xxx"
  - 里程碑 issue #456: 评论 "开发中"

in_verification:
  - 来源 issue #123: 评论 "✅ 验证中"
  - 里程碑 issue #456: 评论 "验证中"

completed:
  - 来源 issue #123: 评论 "✅ 已完成，合并: commit xxx" + 关闭
  - 里程碑 issue #456: 评论 "已完成" + 关闭
```

### Issue 绑定关系

```
来源 issue #123 (GitHub) ←──────────→ 里程碑 issue I-xxx (GitHub)
      │                                        │
      │  双向链接                               │
      │  状态同步                               │
      ▼                                        ▼
  用户可见进展                      Freely 内部追踪 (phase_state)
                                  + docs/epics/*/issues/*.md
```

### 状态同步机制

```
Freely 内部 phase_state      来源 issue #123        里程碑 issue I-xxx (GitHub)
─────────────────────        ──────────────        ───────────────────────────
in_ibm                       添加评论:              添加标签:
                             "需求分析中"           status: in-progress

in_dev                       添加评论:              评论:
                             "开发中"               "开发中，worktree: xxx"

in_verification              添加评论:              评论:
                             "验证中"               "验证中"

completed                    关闭 issue             关闭 issue
                             评论: "已完成"         评论: "已完成，合并: commit xxx"
```

### 内部需求流程（来源是内部）

```
内部需求（打工发现/运行时异常/治理漂移）
       │
       ▼
  预研/消化
       │
       │  进入 pre-brainstorms/
       ▼
  候选 issue C-xxx (内部，不公开)
       │
       │  里程碑接纳 (status: promoted)
       ▼
  创建里程碑 issue I-xxx 到 GitHub (#457)
  - 标签: status: triaged
  - 标签: source: internal
  - 内容: 标题 + 预研链接 + 验收标准（无来源链接）
       │
       ▼
  存储映射关系：
  {
    "I-xxx": {
      "github_milestone_issue": 457,
      "github_source_issue": null,
      "source_platform": "internal"
    }
  }
```

**单边追踪：** 无来源 issue，只同步里程碑 issue 状态

### 核心规则

1. **候选 issue (C-xxx) 仅内部追踪** - 预研阶段，可能被拒绝
2. **里程碑 issue (I-xxx) 同步到 GitHub** - 正式接纳后公开追踪
3. **来源 issue 绑定但不关闭** - 用户可持续追踪进展
4. **状态变更时同步更新来源 issue 和里程碑 issue** - 双边可见
5. **完成时同时关闭来源 issue 和里程碑 issue** - 一起收尾
6. **已消化 issue (status: triaged) 不再被预研消费** - 避免重复处理

## Open Questions

1. **多平台 Issue 集成**
   - GitHub 和 Gitee 的 API 差异如何抽象
   - 是否支持其他平台（GitLab、自建等）

2. **同步频率与时机**
   - 启动时全量扫描 vs 增量扫描
   - 运行时定期轮询还是 webhook 触发

3. **内部需求是否同步到 GitHub**
   - 透明化（用户可见）vs 内部（效率优先）
   - 标签 `source: internal` 是否足够区分

4. **Issue 状态冲突处理**
   - 外部 issue 在预研期间被关闭/更新
   - 外部 issue 与内部候选 issue 内容冲突

5. **Freely 升级与用户项目的协调**
   - Freely 升级时如何不打断用户项目
   - 版本锁定还是跟随更新

## Next Steps

1. 设计 GitHub/Gitee issue 扫描 skill
2. 定义标签体系与同步策略
3. 实现内部需求回流机制
4. 测试完整闭环流程

## Research Conclusion

**预研达标，产出 4 个候选 issue：**

| ID | 标题 | 优先级 | 状态 |
|----|------|--------|------|
| C-20260403-1000-A | 外部 Issue 消化与候选 Issue 闭环流程 | P1 | candidate |
| C-20260403-1000-B | GitHub Issue 扫描与状态同步 Skill | P2 | candidate |
| C-20260403-1000-C | 内部需求回流机制 | P2 | candidate |
| C-20260403-1000-D | Freely 自身迭代与用户项目开发调度策略 | P2 | candidate |

**核心设计已确认：**
- GitHub issue 对应里程碑 issue (I-xxx)，不是候选 issue (C-xxx)
- 来源 issue 绑定但不关闭，双边追踪直到完成
- 状态同步基于 phase_state：in_ibm → in_dev → in_verification → completed

**消费区分逻辑：**
- 有 `status: triaged` → 跳过（已消化）
- 无 `status: triaged` → 消费（进入预研）
- 区分：来源 issue 无 source 标签，里程碑 issue 有 source 标签

**映射关系存储：**
- `.freely/github-issue-mapping.json`
- 记录：内部里程碑 ID ↔ GitHub 里程碑 issue ↔ GitHub 来源 issue

**待后续迭代解决：**
- 多平台 API 抽象（先实现 GitHub，预留扩展点）
- 同步频率（先实现启动时扫描，后续可加增量/webhook）
- 调度策略细节（C-20260403-1000-D）
