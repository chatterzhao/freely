# Candidates - 20260427-0000--b1-intake-issue-sync

- Source brainstorm: `docs/B1-docs/raw-20260427-0000/brainstorms.md`

### C-20260427-0000-A

- title: `Issue-centric intake: platform isolation, local storage, deterministic sync`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `done_pre_brainstorm`
- status: `absorbed`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- problem: `freely 的 chat 插话和平台 issue 是两条独立的输入路径，存储结构不同（.freely/intake/ vs task-source-scan），sync 逻辑分散。AI 有时直接调平台 API，token 浪费且与平台耦合。`
- why_now:
  - IBM Framework 已统一 B1_IBM 的 Input 为 github/gitee issue
  - chat 插话→issue 评论的模型已收敛
  - issueme 提供了成熟的本地存储和 sync 参考设计
  - 这是一次性重构，后续新增平台或变更流程只需改脚本
- proposed_scope:
  - 新建 `docs/issues/` 本地 issue 存储（目录结构 + ISSUES.md 索引）
  - 实现 `bin/issue-sync` 脚本（push/pull，多平台）
  - 重构 `freely chat` → 底层写 issue comment 而非 `.freely/intake/`
  - 定义 B1/B2 生命周期 hook 触发 sync 的事件表
  - 废弃 `.freely/intake/`，迁移到 `docs/issues/`
  - gate 校验 issue 文档元数据规范
- non_goals:
  - 不实现 TUI/GUI issue 界面（CLI-first）
  - 不改变 `docs/B2-docs/` B2 产物目录结构
  - 不改变 `task-source-scan.py` 的扫描逻辑（下载到本地不变）
- session_refs:
  - {tool: ccds, session_id: "20260427-b1-intake-design", jsonl_path: "unavailable://manual", role: "author"}

---

## 决定

### D1. 本地 issue 目录结构

```
docs/issues/
├── ISSUES.md                          # 索引：所有 issue 的映射表
├── raw-{YYYYMMDD}-{NNNN}/             # raw issue（B1 输入）
│   └── issue.md                       # 正文 + ## Comments 章节（评论追加在此）
└── I-{YYYYMMDD}-{NNNN}-{split}/       # linked issue（B2 产出）
    └── issue.md                       # 摘要 + ## Comments 章节
```

**为什么评论在 issue.md 内而非独立文件？** 一个 issue = 一个文档。评论是 issue 的时间线，追加在 `## Comments` 章节下最自然。sync 时比较 `last_synced_comment_at` 和最新评论时间戳，只推送增量。

**评论在 issue.md 中的格式**（`## Comments` 章节下的 `###` 条目）：
```markdown
## Comments

### 2026-04-27T10:25:00Z - human (chat)
{source: chat, session_refs: [{tool: ccds, session_id: "xxx", role: "author"}]}

评论正文内容。

### 2026-04-27T11:00:00Z - github
{platform_ids: {github: {comment_id: "12345"}}}

从平台同步的评论。
```

`meta.env` 记录 `last_synced_comment_at`。sync 时取此时间戳后的新 `###` 章节推送到平台。



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
| candidate promoted | `pr-merge-guarded` 或 governance hook 检测到 status=promoted | `issue-sync create` 创建里程碑 issue |
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

1. 新建 `docs/issues/` 目录结构
2. 迁移脚本 `bin/issue-migrate-intake`：
   - 读取 `.freely/intake/` 下所有 intake item
   - 保留 meta.env 中的 author、channel、session_refs
   - 写入新的 `docs/issues/` 结构
3. 验证迁移完整性后，删除 `.freely/intake/`
4. `freely chat`、`freely intake chat` 改为写 `docs/issues/`

**`freely chat` 新行为**：
```
freely chat "xxx"
    → chat-routing skill 判断路由：
        ├── OPEN issue → comment
        ├── CLOSED issue → reopen + comment OR 新建 raw issue + link
        ├── 全新内容 → 新建 raw issue (proposed/needs_research)
    → 写入 docs/issues/comments/{comment-id}.md 或创建 raw-* 目录
    → bin/issue-sync comment <issue-id> <comment-id>（异步，不阻塞）
```

**chat skill 不做价值判断**：skill 只路由到正确的 issue 容器。最终是 promote、absorb 还是 drop，由 B1 预研决定。即使 chat 内容看似无价值，也创建 issue——B1 标记 `dropped` 并写清 `drop_reason`。

### D6. 评论的紧急标记

评论 frontmatter 增加 `urgent` 字段：
```yaml
urgent: true          # 需要 AI 立即处理
target_phase: in_dev  # 当前 issue 正在 dev-loop 中
```

`freely chat --urgent` 设置此标记。supervisor keepalive 检查时发现有 `urgent: true` 的新评论 → 触发 signal → 中断当前 worker。

如果 `belongs_to` 的 issue 当前不在 dev-loop 中，`--urgent` 无效（AI 不中断），评论正常等待 scan。


- absorbed_by_issue: `I-20260426-0000-A`
- promoted_issue_path: `docs/B2-docs/ibm/tool-alias-and-opencode-launcher-governance/issues/tool-alias-and-opencode-launcher-governance.md`
- decision_reason: `B1 pre-brainstorm for chat intake→issue unification. Implementation artifacts (scripts, storage, sync) absorbed into the canonical tool launcher governance issue.`

### Closeout

- completed_at: `2026-04-28`
- closeout_evidence: `I-20260426-0000-A (absorbing issue) merged via df21b4f8 and phase_state set to completed`
