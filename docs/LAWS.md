# Freely 法律

> 我是项目法律，具体规则，落实执行细节。

---

## 0. 研究优先阶段（当前生效）

在 Freely 文档模型重构完成前，`docs/` 目录采用最小集合约束：

- `docs/PROJECT_INTENT.md`
- `docs/LAWS.md`
- `docs/CONSTITUTION.md`
- `docs/research/`

执行规则：

1. 新讨论与新决策写入 `docs/pre-brainstorms/<id>/`（核心文件：`brainstorms.md`、`candidates.md`）。
2. 历史执行态文档已归档并移出工作区（见 `docs/research/ARCHIVE.md`），不作为当前主流程入口。
3. 在“意图-法律-宪法”三件套达成一致前，不恢复旧目录模型扩展。
4. 重构完成后，再从 `deferred/` 选择性迁移到新模型。

---

## 11. D:doc-loop(IBM) 文档循环方法论

### 11.1 目录结构

```text
docs/
├── milestones.md                              # 里程碑索引
├── blockers.md                                # 阻塞记录
├── temp/                                      # 临时讨论区
│   └── @<topic>.md                            # Issue 归属讨论
├── chat-todos/                                # Chat Todo 目录
│   └── <YYYYMMDD>-<topic>.md                  # 人类介入 Todo
├── reviews/                                   # 评审记录
│   └── <YYYYMMDD-HHMMSS>--<reviewer>--<branch>--<topic>.md
├── epics/                                     # EPIC 实例
│   └── <epic-name>/                           # Epic 目录
│       ├── README.md                          # Epic 概述
│       └── <story-name>/                      # Story 目录
│           ├── issues/                        # I: Issue 输入
│           │   └── <issue-name>.md
│           ├── brainstorm/                    # B: 头脑风暴
│           │   └── b-<issue-name>.md
│           ├── map/                           # M: 规划设计
│           │   └── design.md
│           └── act/                           # A: 执行产出
│               └── artifacts/
└── progress/                                  # 进度记录
    └── <epic-name>/
        └── p-<issue-name>.md
```

### 11.2 I (Intake) - 接入

#### 11.2.1 工作方法

在 `docs/temp/@<topic>.md` 讨论：
- Issue 归属
- 确定或新建 epic-name
- 确定或新建 story-name
- 确定里程碑 M.x.x

#### 11.2.2 工作结果

| 产出 | 位置 | 说明 |
|------|------|------|
| Issue 文件 | `epics/<epic-name>/<story-name>/issues/<issue-name>.md` | Issue 详情 |
| 里程碑索引 | `milestones.md` | 添加 Issue 路径，顺序即开发顺序 |

#### 11.2.3 Issue 文件格式

```markdown
# Issue: <issue-name>

## 基本信息
- Epic: <epic-name>
- Story: <story-name>
- 里程碑: M.1.0
- 来源: github-issue / 项目意图 / chat-todo / ...

## 描述
<!-- Issue 描述 -->

## 状态
- [ ] 待处理
```

### 11.3 B (Brainstorm) - 头脑风暴

#### 11.3.1 工作方法

- 意图分析：要解决什么问题
- 备选方案：可能的解决方案
- 决策：最终决策及理由
- 延期决策：是否延期、拆分

#### 11.3.2 工作结果

| 产出 | 位置 | 说明 |
|------|------|------|
| 头脑风暴记录 | `brainstorm/b-<issue-name>.md` | 分析过程和决策 |
| 延期标注 | `issues/<issue-name>.md` 状态 | 如有延期 |
| 里程碑更新 | `milestones.md` | 如有延期，更新里程碑 |

#### 11.3.3 文件格式

```markdown
# 头脑风暴: <issue-name>

## 意图分析
<!-- 要解决什么问题 -->

## 备选方案
<!-- 可能的解决方案 -->

## 决策
<!-- 最终决策及理由 -->

## 延期决策（如有）
- 里程碑: M.1.0 → M.2.0
- 原因: <!-- 延期原因 -->
- 处理: 拆分新 story-name
```

### 11.4 M (Map) - 映射

#### 11.4.1 工作方法

- 技术方案：如何实现
- 验收标准：如何验证完成

#### 11.4.2 工作结果

| 产出 | 位置 | 说明 |
|------|------|------|
| 设计文档 | `map/design.md` | 技术方案和验收标准 |

#### 11.4.3 文件格式

```markdown
# 设计: <story-name>

## 概述
<!-- 设计概述 -->

## 技术方案
<!-- 技术实现方案 -->

## 验收标准
- [ ] 标准1
- [ ] 标准2
```

### 11.5 里程碑规则

#### 11.5.1 里程碑格式

`M.<major>.<minor>`，示例：`M.1.0`、`M.2.0`、`M.2.1`

#### 11.5.2 milestones.md 格式

```markdown
# milestones.md

## M.1.0 (计划: 2026.03.01)
- [x] docs/epics/auth/story-login/issues/basic-auth.md
- 发布版本: 2026.03.01-1430-stable

## M.2.0 (计划: 2026.03.15)
- [ ] docs/epics/auth/story-mfa/issues/totp.md
- [ ] docs/epics/auth/story-login-phase2/issues/saml.md (从 M.1.0 延期)
```

#### 11.5.3 延期处理

延期 = 拆分新 Story，处理步骤：
1. 创建新 Story
2. 移动延期 Issue
3. 更新 milestones.md

### 11.6 评审记录

#### 11.6.1 文件命名

`<YYYYMMDD-HHMMSS>--<reviewer>--<branch>--<topic>.md`

#### 11.6.2 文件格式

```markdown
# 评审: <topic>

## 基本信息
- 时间: 2026.03.01-143000
- 评审者: codex-gpt5
- 分支: feature/auth-login
- Issue: docs/epics/auth/story-login/issues/basic-auth.md

## 结果
- [x] 通过
- [ ] 需修改
```

---

## 12. D:dev-loop(DDD) 开发循环方法论

### 12.1 循环结构

```
D:dev-loop(DDD)
│
├── D (doc) ── 阅读文档指导
├── D (dev) ── 开发（impl → review → test）
├── D (doc) ── 更新文档
│
└── 循环直到完成
```

### 12.2 D (doc) - 阅读文档指导

#### 12.2.1 工作方法

从以下文档获取指导：
- `issues/<issue-name>.md` - Issue 详情
- `brainstorm/b-<issue-name>.md` - 头脑风暴决策
- `map/design.md` - 技术方案和验收标准

#### 12.2.2 工作结果

无文档产出，输出理解指导。

### 12.3 D (dev) - 开发

#### 12.3.1 工作方法

开发包含三个阶段：

```
dev
│
├── impl ──── 编码实现
├── review ── 评审（Agent 对抗）
└── test ──── 测试验收
```

#### 12.3.2 工作结果

| 产出 | 位置 | 说明 |
|------|------|------|
| 代码实现 | `src/` | 实现代码 |
| 测试代码 | `tests/` | 测试用例 |
| 评审记录 | `docs/reviews/*.md` | 评审结果 |
| 执行产出 | `act/artifacts/` | 设计图、数据模型等 |

### 12.4 D (doc) - 更新文档

#### 12.4.1 工作方法

开发完成后更新相关文档。

#### 12.4.2 工作结果

| 产出 | 位置 | 说明 |
|------|------|------|
| 进度记录 | `progress/<epic-name>/p-<issue-name>.md` | 执行状态 |
| 里程碑状态 | `milestones.md` | Issue 完成标记 |
| Issue 状态 | `issues/<issue-name>.md` | 状态更新 |
| 阻塞记录 | `blockers.md` | 如有阻塞 |

### 12.5 进度跟踪

#### 12.5.1 文件格式

位置：`docs/progress/<epic-name>/p-<issue-name>.md`

```markdown
# 进度: <issue-name>

## 基本信息
- Epic: <epic-name>
- Story: <story-name>
- 里程碑: M.1.0
- 分支: feature/<branch-name>

## 循环状态
- [ ] D (doc): 阅读指导
- [ ] D (dev): 开发
  - [ ] impl
  - [ ] review
  - [ ] test
- [ ] D (doc): 更新文档

## 执行记录
- 2026.03.01-1430: 开始
- 2026.03.01-1500: 完成实现

## 下一步
<!-- 下一步动作 -->
```

### 12.6 阻塞处理

#### 12.6.1 blockers.md 格式

```markdown
# 阻塞记录

## 待处理
- [ ] 阻塞描述 → 产出：补充/修复/重构 Issue

## 已处理
- [x] 阻塞描述 → Issue: docs/epics/.../xxx.md
```

### 12.7 恢复策略

1. **续接分支**：支持无人值守续接时直接续接
2. **桥接分支**：不支持时执行：
   - 更新进度文档
   - 重启无人值守循环

---

## 13. A:auto-loop(ADD) 自主循环方法论

### 13.1 循环结构（统一循环图 + 产出物）

```text
A:auto-loop(ADD) [外循环]
│
├── A1 发现问题（持续）
│   ├── 新问题源：intent/review/test/chat/github-issue -> pre-brainstorms
│   ├── 候选源：pre-brainstorms/candidates
│   └── 执行源：milestones/progress(未完成)
│   产出：
│   - docs/pre-brainstorms/<id>/brainstorms.md
│   - docs/pre-brainstorms/<id>/candidates.md
│
├── A2 分流决策
│   ├── raw problem / candidate -> D:doc-loop(IBM)
│   └── ready issue / in-progress -> D:dev-loop(DDD)
│   产出：
│   - 更新 docs/pre-brainstorms/<id>/candidates.md 的 route/status
│
├── D:doc-loop(IBM) [I -> B -> M]
│   产出（重构目标目录）：
│   - docs/epics/{epic}/{story}/issues/{issue}.md
│   - docs/epics/{epic}/{story}/prd.md
│   - docs/epics/{epic}/{story}/pre-tests.md
│   - docs/epics/{epic}/{story}/tasks.md
│   - docs/milestones.md  (与 issue 原子同步写入：新增/调整归属)
│
├── D:dev-loop(DDD) [Doc-Read -> Dev-Do -> Doc-Update]
│   产出：
│   - src/** , tests/**
│   - docs/progress/{epic}/p-{issue}.md
│   - docs/milestones.md  (状态更新)
│   - docs/epics/{epic}/{story}/issues/{issue}.md  (状态更新)
│
└── A3 回流
    └── 返回 A1，继续发现与完成
```

### 13.2 Issue 发现机制

| 类型 | 来源 | 说明 |
|------|------|------|
| 发现候选 | pre-brainstorms/candidates | 候选 issue 等待收敛与晋升 |
| 思考产出或修改 | 项目意图 | 新需求 |
| 思考产出或修改 | review | 改进点 |
| 思考产出或修改 | test | Bug/修复 |
| 思考产出或修改 | 进度文档 | 未完成 Issue |
| 思考产出或修改 | chat-todo | 人类介入 |
| 获取 | github-issue | 外部输入 |
| 获取 | 里程碑 | 待处理 Issue |

### 13.3 Issue 路由规则

| Issue 来源 | 路由起点 | 说明 |
|-----------|---------|------|
| pre-brainstorms 候选 | D:doc-loop(B/M) | 候选 issue 需收敛并落位到 epic/story/milestone |
| 进度文档（未完成） | D:dev-loop | 文档已有，继续开发 |
| 里程碑（待处理） | D:doc-loop(M) 或 D:dev-loop | 视文档完整度 |
| 项目意图（新需求） | D:doc-loop(I) | 从接入开始 |
| review/test（Bug/改进） | D:doc-loop(B) 或 D:dev-loop | 视复杂度 |
| github-issue（外部输入） | D:doc-loop(I) | 从接入开始 |
| chat-todo（人类介入） | 视情况 | 人类产出或修改 Issue |

### 13.4 Chat Todo（人类介入）

#### 13.4.1 文件格式

位置：`docs/chat-todos/<YYYYMMDD>-<topic>.md`

```markdown
# Chat Todo: <topic>

## 讨论文档
<!-- AI 通过 Chat 思考产出的讨论内容 -->

## Todo 列表
- [ ] 待处理项1 → Issue: docs/epics/.../xxx.md
- [x] 已处理项2 → Issue: docs/epics/.../xxx.md

## 使用状态
- 创建时间: 2026.03.01-1430
- 最后更新: 2026.03.01-1500
- 状态: 进行中 / 已完成
```

#### 13.4.2 工作流程

```
人类 ←──→ Chat Session ←──→ AI
              │
              ├── AI 通过 Chat 思考产出讨论文档
              ├── 基于讨论结果生成 chat-todo
              ├── 基于 chat-todo 产生或修改 Issue
              └── 更新 chat-todo 使用状态
```

### 13.5 循环控制

| 操作 | 说明 |
|------|------|
| 启动 | 开始自主循环 |
| 停止 | 明确停止信号 |
| 恢复 | 从进度文档恢复未完成 Issue |

### 13.6 外循环闭环

```
获取 Issue → D:doc-loop(IBM) → D:dev-loop(DDD) → 完成 → 获取 Issue
     ↑                                                        │
     └──────────────────── 闭环 ───────────────────────────────┘
```
