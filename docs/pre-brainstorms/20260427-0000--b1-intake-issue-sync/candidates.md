# Candidates - 20260427-0000--b1-intake-issue-sync

- Source brainstorm: `docs/pre-brainstorms/20260427-0000--b1-intake-issue-sync/brainstorms.md`

### C-20260427-0000-A

- title: `Issue-centric intake: platform isolation, local storage, deterministic sync`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `done_pre_brainstorm`
- status: `proposed`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- problem: `freely 的 chat 插话和平台 issue 是两条独立的输入路径，存储结构不同（.freely/intake/ vs task-source-scan），sync 逻辑分散。AI 有时直接调平台 API，token 浪费且与平台耦合。`
- why_now:
  - IBM Framework 已统一 B1_IBM 的 Input 为 github/gitee issue
  - chat 插话→issue 评论的模型已收敛
  - issueme 提供了成熟的本地存储和 sync 参考设计
  - 这是一次性重构，后续新增平台或变更流程只需改脚本
- proposed_scope:
  - 新建 `.freely/issues/` 本地 issue 存储（目录结构 + ISSUES.md 索引）
  - 实现 `bin/issue-sync` 脚本（push/pull，多平台）
  - 重构 `freely chat` → 底层写 issue comment 而非 `.freely/intake/`
  - 定义 B1/B2 生命周期 hook 触发 sync 的事件表
  - 废弃 `.freely/intake/`，迁移到 `.freely/issues/`
  - gate 校验 issue 文档元数据规范
- non_goals:
  - 不实现 TUI/GUI issue 界面（CLI-first）
  - 不实现 AI 自动归类 inbox（本次只建存储，分类逻辑后续）
  - 不改变 `docs/epics/` B2 产物目录结构
  - 不改变 `task-source-scan.py` 的扫描逻辑（下载到本地不变）
- session_refs:
  - {tool: ccds, session_id: "20260427-b1-intake-design", jsonl_path: "unavailable://manual", role: "author"}

---

## 决定

### D1. 本地 issue 目录结构

```
.freely/issues/
├── ISSUES.md                          # 索引：所有 issue 的映射表
│                                       # 每行一个 issue 的摘要 frontmatter
├── comments/
│   └── {comment-id}.md                # 所有评论存这里
│                                       # frontmatter 记录所属 issue、作者、来源平台
├── raw-{YYYYMMDD}-{NNNN}/             # raw issue（B1 输入）
│   ├── meta.env                       # 本地 ID、平台 ID、状态、关联
│   └── issue.md                       # issue 正文（从平台下载或 chat 创建）
├── I-{YYYYMMDD}-{NNNN}-{split}/       # linked issue（B2 产出）
│   ├── meta.env                       # 本地 ID、平台 ID、canonical 路径
│   └── issue.md                       # 正式 issue 摘要（sync 时推送到平台 body）
└── inbox/                             # 未归类的 chat 消息
    ├── {timestamp}-{id}.md            # 待 AI 分类的消息
    └── ...
```

**为什么 comments 独立于 issue 目录？** 一条评论可能需要在多个 issue 上显示（交叉引用），且 sync 时按评论粒度操作比按 issue 粒度更高效。条评论的 frontmatter 记录 `belongs_to`。

**comment 文件格式**：
```markdown
---
id: comment-20260427-0001
belongs_to: raw-20260427-0001
author: human
source: chat                    # chat | github | gitee | worker
platform_ids:
  github:
    comment_id: "12345"
    synced_at: "2026-04-27T10:30:00Z"
created_at: "2026-04-27T10:25:00Z"
session_refs:
  - {tool: ccds, session_id: "xxx", role: "author"}
---

评论正文内容。
```

**ISSUES.md 格式**（每行一个 YAML frontmatter 块）：
```markdown
---
local_id: raw-20260427-0001
kind: raw
platform_ids:
  github: {issue_id: "42", synced_at: "..."}
  gitee: {issue_id: "17", synced_at: "..."}
primary_platform: github
canonical_issue_path: ""
sync_state: synced
hash: "sha256:abc123..."
created_at: "2026-04-27T10:00:00Z"
---

---
local_id: I-20260426-0000-A
kind: linked
platform_ids:
  github: {issue_id: "43", synced_at: "..."}
primary_platform: github
canonical_issue_path: "docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/issues/tool-alias-and-opencode-launcher-governance.md"
sync_state: synced
hash: "sha256:def456..."
created_at: "2026-04-26T18:00:00Z"
---
```

### D2. 平台事件与 CLI

四种平台操作，本地提供 CLI，由 hook/gate 触发：

| 平台操作 | CLI 命令 | 触发时机 |
|---------|---------|---------|
| 创建 issue | `bin/issue-sync create <local-id>` | B1 candidate promoted，B2 开始时 |
| 更新 issue 状态 | `bin/issue-sync update <local-id>` | phase_state 变更时（in_dev, in_verification, completed） |
| 关闭 issue | `bin/issue-sync close <local-id>` | raw issue 被 promote 后、里程碑 issue cleanup 后 |
| 添加评论 | `bin/issue-sync comment <local-id> <comment-id>` | chat 插话后、生命周期关键节点 |

**CLI 实现**：
```bash
bin/issue-sync create <local-id>       # 在配置的平台上创建 issue
bin/issue-sync update <local-id>       # 更新平台 issue body（scope + status）
bin/issue-sync close <local-id>        # 关闭平台 issue
bin/issue-sync comment <local-id> <comment-id>  # 推送评论到平台
bin/issue-sync pull                     # 从平台拉取新 issue/comment
bin/issue-sync rebuild <local-id>       # 从本地重建平台 issue（force push）
bin/issue-sync status <local-id>        # 查看同步状态
```

**平台适配**：`bin/issue-sync` 内部根据 ISSUES.md 中的 `primary_platform` 选择对应的 API 适配器。适配器实现统一接口（create/update/close/comment/pull），平台差异封装在适配器内。

### D3. B1/B2 生命周期 hook 触发 sync 事件表

| 生命周期事件 | 触发 gate/hook | sync 动作 |
|-------------|---------------|----------|
| chat 插话 | `freely chat` 执行后 → 写本地 comment → sync | `issue-sync comment` |
| candidate promoted | `merge-guarded` 或 governance hook 检测到 status=promoted | `issue-sync create` 创建里程碑 issue |
| B2 IBM 完成 | phase_state 变为 `done_b2_ibm` | `issue-sync update` 更新 issue body（scope + acceptance） |
| 进入 dev-loop | phase_state 变为 `in_dev` | `issue-sync comment` "implementation started" |
| 进入 verification | phase_state 变为 `in_verification` | `issue-sync comment` "verification in progress" |
| merge 到 develop | post-merge hook | `issue-sync comment` "merged: {commit}" |
| raw issue promote | raw issue 被 promote，里程碑 issue 创建后 | `issue-sync comment` + `issue-sync close`（关闭 raw issue） |
| cleanup 完成 | worktree 退役后 | `issue-sync comment` "cleanup done" + `issue-sync close`（关闭里程碑 issue） |

**关键原则**：sync 是异步的，不阻塞 AI 工作。网络不可用时 sync 失败不阻断 hook/gate。失败的 sync 进入重试队列，下次 `issue-sync pull` 或 daemon patrol 时重试。

### D4. gate 校验 issue 文档元数据规范

`governance-merge-gate` 和 `pretests-gate` 增加对 issue 元数据的校验：

| 校验项 | 规则 |
|--------|------|
| `platform_ids` 非空 | linked issue 至少有一个平台的同步记录 |
| `primary_platform` 存在 | linked issue 必须指定主平台 |
| `canonical_issue_path` 有效 | linked issue 的 canonical 路径指向存在的文件 |
| `hash` 一致 | issue.md 内容变更后 hash 已更新 |
| `sync_state` = synced | 合并到 develop 前必须已同步 |

这些校验确保：每次 merge 到 develop 时，对应的平台 issue 是同步状态。

### D5. 现有 `.freely/intake/` 的迁移

**迁移策略**（不保留兼容，一次性重构）：

1. 新建 `.freely/issues/` 目录结构
2. 迁移脚本 `bin/issue-migrate-intake`：
   - 读取 `.freely/intake/` 下所有 intake item
   - 按 message 内容创建对应的 raw issue 或 inbox 条目
   - 保留 meta.env 中的 author、channel、session_refs
   - 写入新的 `.freely/issues/` 结构
3. 验证迁移完整性后，删除 `.freely/intake/`
4. `freely chat`、`freely intake chat` 改为写 `.freely/issues/`

**`freely chat` 新行为**：
```
freely chat "xxx"
    → 判断消息属于哪个 issue（显式引用 or 默认 inbox）
    → 写入 .freely/issues/comments/{comment-id}.md
    → bin/issue-sync comment <issue-id> <comment-id>（异步，不阻塞）
```

### D6. 评论的紧急标记

评论 frontmatter 增加 `urgent` 字段：
```yaml
urgent: true          # 需要 AI 立即处理
target_phase: in_dev  # 当前 issue 正在 dev-loop 中
```

`freely chat --urgent` 设置此标记。supervisor keepalive 检查时发现有 `urgent: true` 的新评论 → 触发 signal → 中断当前 worker。

如果 `belongs_to` 的 issue 当前不在 dev-loop 中，`--urgent` 无效（AI 不中断），评论正常等待 scan。

### D7. 关于 inbox

inbox 不是永久状态。它是一个**临时缓冲区**，存放无法立即归类到已有 issue 的 chat 消息。

**inbox 处理流程**：
1. `freely chat "xxx"` → 无法匹配已有 issue → 写入 `inbox/{ts}-{id}.md`
2. supervisor patrol 或 AI 空闲时 → 扫描 inbox → 判断每条消息归属
3. 归属判断：创建新 raw issue OR 作为已有 issue 的评论
4. 处理完成后从 inbox 删除（或标记 `classified: true`）
5. inbox 超过 N 条 → supervisor 触发优先处理

**inbox 不需要 `issue-sync`**：inbox 内容不上平台。只有当消息被归类到具体 issue 后，才通过正常 sync 流程推送。

## 未决

1. **issue local_id 格式**：`raw-YYYYMMDD-NNNN` vs `raw-YYYYMMDD-HHMM` vs UUID？建议用日期前缀，可读且可排序，递增数字由脚本自动分配。
2. **comment 粒度**：一条 chat 消息 = 一个 comment 文件。但如果 chat 内容很长（multi-paragraph），是否拆分为多个 comment？建议不拆——完整性优先，一个 chat = 一个 comment。
3. **sync 失败重试策略**：退避算法？最大重试次数？死信队列？
4. **多平台 comment ID 映射**：github 的 comment ID 是全局递增整数，gitee 也是。映射存储在 comment frontmatter 的 `platform_ids` 中。
5. **raw issue 何时被 promote 的检测**：需要 scan 脚本或 hook 能检测到 "raw issue 已经被 B1 处理完毕，candidate 已 promoted" 这个状态。当前 scan 用 `linked_open_issue` 检测已关联但未关闭的 raw issue。不变。
