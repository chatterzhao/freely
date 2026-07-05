# B1_IBM 预研：chat 插话与 issue 统一

## 当前状态

B1_IBM 的 Input 有两个入口：
- **平台 issue**（github/gitee）：`task-source-scan.py` 扫到后路由到 B1
- **chat 插话**：`freely chat` → `.freely/intake/<id>/message.txt` → intake scan → 路由到 B1
- **intake chat**:`freely intake chat`

两者走不同的存储路径，chat 内容不在 issue 体系内。

## 目标

统一 Input source 为 github/gitee issue。chat 插话是 issue 的评论或新 issue 的创建方式。本地以 issue 为单位组织所有内容，平台 issue 是唯一真相源（本地是缓存 + 离线缓冲）。

## 设计问题

### 1. 本地 issue 存储结构

```
docs/issues/
├── ISSUES.md                # 索引：所有已知 issue 的映射表
├── {issue-local-id}/
│   └── issue.md             # 正文 + ## Comments 章节（评论追加在此）
```

`ISSUES.md` 索引记录：
- `local_id`：本地唯一 ID
- `platform_ids`：`github:<owner>/<repo>#<num>, gitee:<owner>/<repo>#<num>`
- `kind`：`raw`（原始 issue，B1 输入）/ `linked`（里程碑 issue，B2 产出）
- `comment_count`：本地评论数
- `canonical_issue_path`：B2 产物的 issue 路径（linked 类型）
- `sync_state`：每个平台的同步状态

### 2. chat 插话的 issue 路由

用户在终端 `freely chat "xxx"` 时，需要决定这条消息属于哪个 issue：

```
freely chat "xxx"
    │
    ├── 消息命中已有 issue？
    │   ├── 是 → 作为该 issue 的评论写入
    │   └── 否 → 新建 raw issue，消息为 issue body
    │
    ├── 如何判断"命中已有 issue"？
    │   ├── 用户在消息中显式引用 issue（#123、issue-abc）
    │   ├── AI 判断消息内容与已有 issue 相关
    │   └── 默认：创建新的 raw issue，标记 needs_research
    │
    └── 紧急？
        ├── 消息命中的 issue 正在 dev-loop 中 → 标记 urgent，触发通知
        └── 否则 → 不做特殊处理，等待 scan
```

### 3. 两种 issue 类型

沿用现有设计中的二分法：

| | raw issue | linked issue |
|---|---|---|
| 来源 | 用户直接创建（平台 or chat） | B2_IBM 产出，freely 创建 |
| 状态 | 未与 canonical docs 关联 | 已关联 `docs/epics/.../issues/` |
| scan 行为 | `restart_point=pre_brainstorm` | `restart_point=cleanup` |
| 用户评论 | 自由评论 | 评论触发 drift reconcile |
| 关闭时机 | B2 完成后由 freely 关闭 | 不需要关闭（或跟随 canonical completion） |

### 4. 用户直接评论已关闭的 raw issue

场景：raw issue 已被 freely 处理完毕（B1→B2→merge→cleanup），raw issue 已关闭。用户又在平台上评论了这个 issue。

行为：
- sync 脚本拉取评论到本地
- scan 发现 `linked_open_issue` + 新评论 → `restart_point=cleanup`
- AI 判断评论内容：是否需要 reopen？是否为新的 discovery？
- 如果是新 discovery → 创建新的 raw issue，引用原 issue 上下文

### 5. 紧急机制

某些 chat 内容需要更快让 AI 看到（比如纠正错误、提级）。

判断紧急的标准：消息命中的 issue 是否正在 dev-loop 中。

```
if issue 的 phase_state in {in_dev, in_verification}:
    → 写入评论后立即触发 runtime signal
    → supervisor 在下一次 keepalive 检查时发现 signal
    → 中断当前 worker，处理紧急评论
else:
    → 写入评论，等待下次 task-source-scan 自然扫到
```

### 6. 多平台同步

```
本地脚本 issue-sync：
    push：本地有变更的 issue/评论 → 推到配置的平台
    pull：平台上新的 issue/评论 → 拉到本地
    冲突：平台和本地都有新评论 → 两边都保留，按时间戳排序

平台优先级：
    - 如果 github 和 gitee 都配置了 → 主平台 push，副平台 mirror
    - 默认主平台按 remote 检测
```

### 7. UI 概念

简单 TUI 层：
- 显示当前活跃的 issue（正在 dev-loop 中的）
- 每个 issue 下有一个评论输入区
- 评论自动带 issue local_id
- 紧急标记：勾选"需要 AI 立即处理"

### 8. chat 命令变化

当前命令：
```
freely chat <message>              # 通用插话
freely chat --message-file <path>  # 文件插话
```

变更后：
```
freely chat <message>                           # 默认创建新 raw issue
freely chat --issue <id> <message>              # 指定已有 issue 的评论
freely chat --issue <id> --urgent <message>     # 紧急评论
freely chat --comment <id> <message>            # 等价于 --issue
```

### 9. 现有 intake 子系统（`freely intake chat/claim/resolve/status`）

当前 `freely intake` 是一套完整的轻量工作流：

```
[当前] freely intake chat → 写入 .freely/intake/<id>/message.txt（带 meta.env，待废弃）
freely intake claim   → 标记 claimed_by + reaction + classification
freely intake resolve → 标记 resolved（delegated/absorbed/dropped） + resolution_file
freely intake status  → 列出所有 intake item 及其状态
```

`freely chat` 内部调用 `freely intake chat`，然后触发 interruption dispatch（如果是新消息且 runtime 未活跃则引导启动）。

**与新模型的关系**：

intake 的 claim/resolve 生命周期本质上是"issue 评论的处理状态"，可以直接映射：

| 当前 intake 概念 | 新模型对应 |
|---|---|
| `intake chat` | 向 issue.md 追加 `###` 评论章节，或创建新 raw issue |
| `intake claim` | 评论标记为 claimed（`###` 元数据行加 `status: claimed`） |
| `intake resolve` | 评论标记 resolved（`###` 元数据行加 `status: resolved`） |
| `intake status` | 查看某个 issue 的未处理评论数量 |
| `INTAKE_ID` | 废弃，改用 `comment-{local_id}` |
| `message.txt` | 废弃，评论直接写入 issue.md 的 `## Comments` 章节 |

**命令兼容**：`freely intake chat --issue <id>` 替代 `--linked-artifact`，底层追加评论到 `docs/issues/<id>/issue.md` 的 `## Comments` 章节。整个 `.freely/intake/` 目录废弃。



### 10. 平台 issue ID 管理

**事实**：github 和 gitee 的 issue 编号都是平台自动分配的递增整数，不可自定义。本地 ID 和平台 ID 是两套体系，需要映射表。

**参考 issueme**：`issue.md` frontmatter 中的 `platform_ids` 字段，记录每个平台的 ID、URL、同步状态：

```yaml
platform_ids:
  github:
    issue_id: "123"
    url: "https://github.com/user/repo/issues/123"
    synced_at: "2025-01-15T10:30:00Z"
    status: synced
  gitee:
    issue_id: "456"
    url: "https://gitee.com/user/repo/issues/456"
    synced_at: "2025-01-15T10:35:00Z"
    status: synced
primary_platform: github
```

**freely 适配**：这个模式可以直接复用。`ISSUES.md` 索引中的 `platform_ids` 字段记录每个 issue 在各平台的 ID。新建 issue 时先创建本地 ID，同步到平台后回写平台 ID。

**多平台同步策略**：
- 主平台（primary）：push 优先，pull 优先
- 副平台：mirror 模式，从主平台同步
- 防止平台锁死：本地始终保留完整副本，随时可切换主平台

### 11. 本地 issue ID 设计

**现有 freely ID 体系**：
- `C-YYYYMMDD-NNNN-A`：candidate（B1 产物）
- `I-YYYYMMDD-NNNN-A`：正式 issue（B2 产物）
- `M-YYYYMMDD-XXXX`：milestone

**新的 issue local_id 需要区分来源**：
- `raw-YYYYMMDD-NNNN`：raw issue（B1 输入，用户创建或平台拉取）
- `I-YYYYMMDD-NNNN-A`：linked issue（B2 产出）——沿用现有格式

**raw issue 到 linked issue 的关联**：
- raw issue 的 issue.md frontmatter 记录其 B2 关联
- linked issue 的 frontmatter 反向引用：`source_raw_issue: raw-20260427-1030`
- sync 脚本通过 frontmatter 的 `platform_ids` 找到对应的平台 issue

### 12. 本地存储组织形式

**参考 issueme**：Story = Issue 目录，`M{milestone}-{story-name}/` 包含 issue.md + requirements.md + pre-tests.md + tasks.md。目录名直接带 milestone 前缀，方便查找。

**freely 的差异**：freely 已有 `docs/epics/{epic}/{story}/` 目录结构，不需要改名。但 `docs/issues/` 可以作为平台 issue 的本地缓存层，与 `docs/epics/` 的 B2 产物分离：

```
docs/issues/                    # 所有 issue 的本地存储（git 管理）
├── .scan-state                 # { last_scan_at: "..." }
├── ISSUES.md                   # 索引缓存（脚本维护）
├── raw-20260427-1030/          # raw issue（B1 输入）
│   └── issue.md                # frontmatter + 正文 + ## Comments
└── I-20260427-1030-A/          # linked issue（B2 产物）
    └── issue.md                # frontmatter + 摘要 + ## Comments

docs/epics/{epic}/{story}/      # B2 治理产物（canonical docs）
├── issues/
│   └── {issue-name}.md         # canonical issue 规格
├── pre-tests.md
├── tasks.md
└── code-reviews/
```

两层不重复——`docs/epics/` 是 B2 治理产物，`docs/issues/` 是平台同步存储。linked issue 的 frontmatter 中 `canonical_issue_path` 关联两边的文档。

### 13. issueme 可借鉴的设计

| issueme 设计 | freely 可复用 | 说明 |
|---|---|---|
| `platform_ids` frontmatter | ✅ 直接复用 | 多平台 ID 映射 |
| `primary_platform` | ✅ 直接复用 | 主平台标记 |
| hash 幂等 | ✅ 直接复用 | 变更检测，避免重复同步 |
| Story = Issue 目录 | 🔶 部分复用 | freely 已有 `docs/epics/{epic}/{story}/` |
| 讨论平台化存储 | ✅ 直接复用 | 评论存平台，本地只存元数据 |
| 快速失败策略 | ✅ 直接复用 | 多平台网络检测 |
| `sync.on_partial_failure` | ✅ 直接复用 | 部分平台失败时的行为 |
| `runId` | 🔶 改名为 `session_refs` | freely 已有 session_refs 约定 |

**不照搬的**：
- issueme 的 Epic/Story/Milestone 层次 vs freely 的 B1/B2 IBM 框架——治理哲学不同，目录结构不同
- issueme 的 AI 角色团队（PM/Arch/Dev 等）——freely 用 manager/worker/lead 三角色
- issueme 的讨论区 UI——freely 是 CLI-first，TUI 只是可选的 shell

### 14. 里程碑 issue 的平台创建与内容

**创建权限**：里程碑 issue（linked issue）只允许 freely 代码在 B2_IBM materialization 阶段创建。用户和第三方不应手动创建这类 issue——它们是 freely 的工作记录。

**创建时机**：candidate 被 promoted → milestone committed_issues → B2_IBM 的 I-B-M 流程中，freely 在平台上创建对应的里程碑 issue。

**issue 内容分层**：

平台 issue 和本地文档各司其职：

| 内容 | 在哪里 | 说明 |
|------|--------|------|
| 原始问题描述 | 平台 raw issue body | 用户创建时的原始内容 |
| B1 预研讨论 | 本地 `docs/pre-brainstorms/{id}/brainstorms.md` | AI 内部分析，不上平台 |
| B1 candidate | 本地 `docs/pre-brainstorms/{id}/candidates.md` | 本地治理产物 |
| 里程碑 issue 规格 | **平台 linked issue body** | 正式 issue 文档的摘要：scope、acceptance、状态 |
| 里程碑 issue 完整规格 | 本地 `docs/epics/{epic}/{story}/issues/{name}.md` | 详细版，平台 body 是摘要 |
| B2/IBM 实现头脑风暴 | 本地 `docs/epics/{epic}/{story}/brainstorms/b-{issue}.md` | AI 实现设计，不上平台 |
| PRD | 本地 `docs/epics/{epic}/{story}/prd.md` | 不上平台（可选） |
| pre-tests | 本地 `docs/epics/{epic}/{story}/pre-tests.md` | 不上平台 |
| tasks | 本地 `docs/epics/{epic}/{story}/tasks.md` | 不上平台 |
| 用户反馈 | 平台 issue comment | 用户在平台上对里程碑 issue 的评论 |
| AI 进展更新 | 平台 issue comment | freely 在关键节点写评论（如：B2 完成、进入 dev、合并） |

**里程碑 issue body 内容**：不是把 brainstorm 搬上去——是把 issue 规格的精简版放上去：

```markdown
## Summary
<1-2 sentence summary of what this issue is about>

## Scope
- <bullet list of in-scope items>

## Non-Goals  
- <bullet list of non-goals>

## Status
- phase_state: in_dev
- canonical: docs/epics/{epic}/{story}/issues/{name}.md
```

**原始 raw issue 的关闭**：当 raw issue 被 promote 为里程碑 issue 后，freely 在 raw issue 上写一条评论引用新的里程碑 issue，然后关闭 raw issue。评论内容：

```
This issue has been promoted to a milestone issue: {platform_link}
Canonical docs: docs/epics/{epic}/{story}/issues/{name}.md
```

这样用户在平台上看到 raw issue 已关闭，知道要去新的里程碑 issue 跟踪进展。

### 15. 平台 issue 与本地文档的双向链接

本地文档 ↔ 平台 issue 之间需要双向可追溯：

**本地 → 平台**（通过 issue.md frontmatter）：
```yaml
# docs/epics/.../issues/{name}.md frontmatter
platform_ids:
  github:
    issue_id: "42"
    url: "https://github.com/user/repo/issues/42"
```

**平台 → 本地**（通过 issue body 中的链接）：
```markdown
canonical: docs/epics/{epic}/{story}/issues/{name}.md
```

**sync 脚本查找本地文档**：给定一个平台 issue URL，sync 脚本通过以下方式找到对应的本地文档：
1. 查 ISSUES.md 索引（最快）
2. 搜 `docs/epics/` 下所有 issue.md 的 frontmatter（兜底）

### 16. 核心架构原则：平台与本地隔离，AI 只读本地

**根本约束**：freely 的 AI（manager/worker/lead）**永远不直接读平台内容**，也**永远不直接写平台内容**。平台和本地之间只有两条脚本桥接：

```
Platform (github/gitee)                    Local (docs/issues/, docs/)
     │                                              │
     │  ──① scan 下载（task-source-scan.py）──→      │
     │     raw issue, comment, 状态                    │
     │                                              │
     │                                        AI 工作区（doc-loop, dev-loop）
     │                                        只读本地文件，不感知平台
     │                                              │
     │  ←──② sync 上传（issue-sync 脚本）────         │
     │     创建 issue, 写 comment, 更新状态              │
     │     触发条件：hook / gate / 生命周期事件            │
```

**收益**：
- **省 token**：平台内容 scan 时下载一次，AI 读本地副本，不消耗 API 调用
- **平台解耦**：AI 代码不依赖任何平台 API。切换平台只需改 scan/sync 脚本
- **可重同步**：本地是完整真相。任何时候可以 wipe 平台数据，从本地重建
- **离线友好**：无网络时 AI 继续工作。sync 队列积压，网络恢复后批量推送
- **确定性同步**：sync 触发条件是可枚举的 hook/gate 事件，不是 AI 判断

**sync 触发条件**（可枚举的本地事件）：

| 事件 | 触发条件 | sync 动作 |
|------|---------|----------|
| chat 插话 | `freely chat` 执行后 | 本地写入 issue comment → sync 推送到平台 |
| candidate promoted | candidate status 变为 `promoted` | 创建里程碑 issue 到平台 |
| B2 完成 | `phase_state` 变为 `done_b2_ibm` | 更新平台 issue body（scope + status） |
| 进入 dev | `phase_state` 变为 `in_dev` | 写平台 comment："implementation started" |
| 进入 verification | `phase_state` 变为 `in_verification` | 写平台 comment："verification in progress" |
| 合并到 develop | merge commit 创建 | 写平台 comment："merged: {commit}" + 关闭 raw issue |
| cleanup 完成 | worktree 退役 | 写平台 comment："cleanup done" + 关闭里程碑 issue |
| 用户平台评论 | scan 检测到新评论 | 下载到本地 → 触发 auto-loop signal |

### 17. 本地为唯一真相源

平台 issue 是**本地真相的投影**，不是独立真相。任何时候平台数据丢失、错乱、或被手动修改，都从本地重建。

**重建流程**：
```
1. 读取 docs/issues/ISSUES.md 索引
2. 对每个 issue，比较本地 hash 和平台状态
3. 如果平台不存在 → 创建
4. 如果平台存在但内容不一致 → 用本地内容覆盖（force push）
5. 如果平台有本地没有的 comment → 下载（pull）
```

**hash 幂等**（参考 issueme）：每个 issue 计算 `hash = sha256(normalize(issue.md + comments))`。sync 时比较本地 hash 和上次 push 的 hash，相同则跳过。

**平台冲突处理**：如果平台 issue 在 freely 不知情的情况下被修改（用户手动编辑），sync 脚本：
- 下载平台版本，和本地版本 diff
- 如果只是格式差异 → 本地覆盖平台
- 如果有实质内容差异 → 保留两边，标记冲突，生成 conflict-{timestamp}.md 供人工处理

### 18. chat 路由 skill（修正：每条插话必须创建 issue）

**核心原则**：每条 `freely chat` 必须落地为一个 issue（或已有 issue 的评论）。不存在"丢弃"的插话——即使内容看似无价值，也创建 issue 容器，由 B1 决定其命运。

**路由 skill 的职责**（只做路由，不做价值判断）：

```
freely chat "xxx"
    │
    ▼
chat-routing skill（本地脚本 + AI 判断）
    │
    ├── 消息匹配到 OPEN issue？
    │   └── 是 → 作为该 issue 的 comment
    │
    ├── 消息匹配到 CLOSED issue？
    │   ├── 适合 reopen → reopen issue + comment
    │   └── 不适合 reopen → 新建 raw issue，link 到关闭的 issue，comment 说明关联
    │
    ├── 消息全新，且内容超前/探索性？
    │   └── 新建 raw issue，打标签 `needs_research`
    │
    ├── 消息内容看似无价值/闲聊？
    │   └── 新建 raw issue，打标签 `proposed`（B1 将判断为 dropped）
    │
    └── 无法判断？
        └── 新建 raw issue，打标签 `needs_research`
```

**关键约束**：
- skill 不做价值判断——不决定"这个值得做"或"这个应该丢弃"
- skill 只判断两件事：①这属于哪个已有 issue？②如果新建，打什么初始标签？
- 标签只是 hint，B1 预研时根据实际内容重新判断
- 标签和 status 不同：标签是 B1 输入的 hint，status 是 B1 输出的决定

**skill 实现方式**：
- 快速路径：脚本匹配（issue 编号引用、关键词命中 open issue title）
- AI 路径：无法快速匹配时，调 AI 做语义判断（这条消息和哪个 issue 相关？）
- AI 只做路由判断，不需要读完整 issue 内容（读 ISSUES.md 索引中的 title + status 即可）

**初始标签建议**：

| 标签 | 含义 | B1 处理后的可能结果 |
|------|------|-------------------|
| `proposed` | 待评估（默认） | promoted / absorbed / dropped |
| `needs_research` | 需要更多研究 | 留在 candidate_issues，标记 needs_research |
| `forward_looking` | 超前想法，当前不可行 | 留在 candidate_issues，记录 revisit_trigger |
| `reopen_candidate` | 关联已关闭 issue，可能需重开 | B1 判断是否 reopen 还是新建 |

### 19. dropped 的语义

即使插话最终被判定为"不值得做"，也必须走完 B1 流程才能标记 dropped。

**dropped 的完整路径**：
```
chat → 创建 raw issue (proposed) → scan → B1 预研 → candidate 标记 dropped
                                                         │
                                                    记录 drop_reason
                                                    记录 session_refs
                                                    sync 到平台（关闭 issue + comment）
```

**drop_reason 必须写清**，不能只是"不需要"。合法理由包括：
- `out_of_scope`：超出当前项目范围
- `already_addressed`：已被其他 issue 覆盖
- `not_worthwhile`：成本收益不成比例
- `superseded`：被后续更完整的 issue 替代
- `user_withdrawn`：用户自己撤回

平台上的关闭 comment 应写清 drop_reason，保持可追溯。

### 20. 重构后的 Input 统一

**之前**：两个入口——chat 插话和平台 issue，不同存储，不同路径。

**之后**：只有一个 Input source——issue。

用户的任何输入都是 issue 上的操作：
- 新话题 → 新建 raw issue（`freely chat "新想法"` → `docs/issues/raw-20260427-1030/issue.md`）
- 已有工作相关 → 对应 issue 的评论（`freely chat --issue raw-20260427-1000 "补充"` → 追加到该 issue.md 的 `## Comments`）

`freely chat` 不是 Input source——它是本地的 issue 创建/评论工具。Input source 永远是 issue。

### 21. Key 链规则

raw、C、I 共享同一个 date-time key：

```
raw-20260427-1030       key = "20260427-1030"
    ↓ B1_IBM
C-20260427-1030-A       key = "20260427-1030-A"    ← 以 raw key 开头
    ↓ milestone
I-20260427-1030-A       key = "20260427-1030-A"    ← 以 C key 开头
```

- key 格式：`YYYYMMDD-HHMM`，HHMM 是 issue 创建的实际时间
- `-A`/`-B` 后缀：candidate/issue 可以 split 成多个，共享 base key
- 门禁校验：issue_key 必须以 candidate_key 开头（已有）。raw→C 的校验需新增

### 22. 平台评论 ID 与本地评论的映射

平台（github/gitee）评论有唯一整数 ID。sync 流程：

1. 本地有新评论（`### comment-{local_id}`，元数据行中没有目标平台的 `comment_id`）
2. `bin/issue-sync comment` → 调平台 API，POST 评论
3. 平台返回 `{id: 12345}`
4. sync 将 `comment_id` 写回该 `###` 的元数据行

之后该评论在本地和平台之间有了双向映射。后续更新、删除等操作通过 platform comment_id 定位。

**本地 ID 的作用**：chat 执行后立即生成，不阻塞等网络。本地引用（如 urgent signal、session_refs）用 local_id。平台 ID 是异步补充的——即使 sync 失败，本地 ID 仍然有效。

### 23. 多平台元数据

每个 issue 和每条评论都需要记录各平台的同步状态，不依赖单一平台。

**issue 级别**：
```yaml
platform_ids:
  github: {issue_id: "42", synced_at: "..."}
  gitee: {issue_id: "17", synced_at: "..."}
primary_platform: github
last_synced_comment_at:
  github: "2026-04-27T10:25:00Z"
  gitee: "2026-04-27T10:20:00Z"
```

**评论级别**（`###` 标题下的元数据行）：
```
{source: chat, platform_ids: {github: {comment_id: "12345"}, gitee: {comment_id: "67890"}}}
```

- source 标记评论来源（chat / github / gitee / worker）
- platform_ids 标记各平台上的 comment_id
- 未同步的平台不出现该平台的 key

**sync 行为**：
- push：遍历 `## Comments` 下的所有 `###`，对每个平台，找没有该平台 `comment_id` 的评论，推送。推送后写回 `comment_id`，更新 `last_synced_comment_at`
- pull：从各平台拉取 `last_synced_comment_at` 之后的新评论，追加到 `## Comments`，写回 `last_synced_comment_at`

### 24. scan 如何集成 docs/issues/

当前 `task-source-scan.py` 扫描 6 个来源家族。重构后需要在 scan 中新增对 `docs/issues/` 的扫描：

**新增 scan 家族**：
- `scan_raw_issues()`：扫描 `docs/issues/raw-*/issue.md`
  - 未与 candidate 关联的 raw issue → `restart_point=pre_brainstorm`
  - 有新评论（`last_synced_comment_at` 之后有新的 `###`）但 issue 未活跃 → 标记有新评论待处理
- `scan_linked_issues()`：扫描 `docs/issues/I-*/issue.md`
  - 与新 raw issue 不同——linked issue 已经关联了 canonical docs
  - 有新评论 → `restart_point=cleanup`（drift reconcile）

**scan 增量逻辑**：
1. 读 `.scan-state` 获取 `last_scan_at`
2. `find docs/issues -name issue.md -newermt <last_scan_at>` 只处理修改过的文件
3. 处理完后更新 `last_scan_at`
4. ISSUES.md 缓存索引同步更新

**废弃的 scan 家族**：
- `scan_intake()`：`.freely/intake/` 不再存在，移除
- `scan_external_github/gitee()`：保留，但下载后的内容写入 `docs/issues/raw-*/` 而非临时处理

### 25. sync 的回写流程

sync 不仅推送，还要把平台返回的 ID 写回本地 frontmatter。

**创建 linked issue 的回写**：
1. candidate promoted → trigger `issue-sync create`
2. 脚本读取 `docs/issues/I-{key}/issue.md` 的 frontmatter，构建 platform issue body
3. 调平台 API 创建 issue → 平台返回 `{id: 42, url: "https://..."}`
4. 将 platform_id 写回 issue.md frontmatter 的 `platform_ids.{platform}.issue_id`
5. 更新 ISSUES.md 索引

**推送评论的回写**：
1. 扫描 `## Comments` 下所有 `###`，对每个平台，找没有该平台 `comment_id` 的章节
2. POST 到平台 API → 返回 `{id: 12345}`
3. 写回 `comment_id` 到该 `###` 的元数据行
4. 更新 `last_synced_comment_at.{platform}`

### 26. .freely/intake/ 迁移步骤

一次性重构，不保留兼容：

1. freeze：禁止新的 `freely chat` 写入 `.freely/intake/`（先切换到新路径）
2. migrate：`bin/issue-migrate-intake` 遍历 `.freely/intake/*/message.txt`，每条消息：
   - 判断是否匹配已有 raw issue → 追加为评论
   - 否则 → 创建新的 raw issue
3. validate：对比迁移前后的消息数量，确认无遗漏
4. remove：`rm -rf .freely/intake/`
5. 更新 `freely chat`、`freely intake *` 代码路径
