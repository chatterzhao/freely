# B1:IBM — Issue 状态治理：scan 对齐分析

**关联 raw issue**: raw-20260517T231837Z
**日期**: 2026-05-18
**状态**: pre-brainstorm (v2 — 状态/scan 匹配分析)

---

## 一、scan 如何决定"显示什么"

`task-lifecycle-scan.py` 是 manager 的眼睛。理解它怎么过滤很重要。

### 1.1 优先级规则（从高到低）

```
优先级 1: platform_state=closed（所有平台都关了） → 跳过，不显示
优先级 2: phase_state ∈ {absorbed, dropped}       → 跳过，不显示（TERMINAL_RAW）
优先级 3: phase_state = completed                  → 跳过，不显示（I-* 完成）
优先级 4: 其他                                    → 显示在 scan 中
```

关键代码 `task-lifecycle-scan.py:336-398` `check_completion()`：

```python
# 最高权威：平台关闭 → item 完成
if all platforms CLOSED → skip

# 其次：本地终端状态
if raw.phase_state in TERMINAL_RAW → skip  # {absorbed, dropped}
if child.phase_state == "completed" → skip

# 其余 → 显示
```

### 1.2 scan 输出标签（stage）

| stage | 含义 | trigger条件 |
|-------|------|------------|
| `chat_unconsumed` | 未消费的 chat | chats.consumed=0 |
| `chat_comment_pending` | 未同步的评论 | chat_type=comment, consumed=0 |
| `local_only` | 本地有 raw 但平台无 issue | phase_state ∉ TERMINAL_RAW, 无 platform_id |
| `platform_only` | 平台有 issue 但本地无 raw | GitHub OPEN issue 不在本地 |
| `state_mismatch` | 本地 completed 但平台仍 OPEN | phase=completed, platform=open |
| `local_needs_closeout` | 平台关了但本地未标记完成 | platform=closed, phase ∉ TERMINAL |
| `raw_not_created` | scan 链中 raw 文件缺失 | docs/issues/raw-{key}/ 不存在 |
| `b1_dir_missing` | 无 B1 预研目录 | 无预研但 raw 未 absorbed |
| `not_promoted_to_I` | raw 未被 promote 为 I-* | 无 children |
| `phase_not_completed` | I-* 未完成 | phase_state ∉ DONE_STATES |
| `github_not_closed` | GitHub 端未关闭 | platform GitHub issue 仍 OPEN |
| *(显示)* | raw 处于 active 状态 | phase_state=proposed / in_dev |

### 1.3 核心洞察

**如果一个 raw issue 的 `phase_state` 永远不更新，它会永远出现在 scan 中。**

当前只有 `issue-sync promote-finalize` 会设置 `phase_state=absorbed`。如果 raw issue 不经过 promote 流程（直接 fix 无 I-*），`phase_state` 永远不会变成 `absorbed`，scan 会永远显示它。

---

## 二、当前状态：每个 phase_state 值何时被设置

### 2.1 raw-* phase_state

| 值 | 设置时机 | 设置方 | 类型 |
|----|---------|--------|:---:|
| `proposed` | materialize 时初始写入 | `chat-inbox.py` / `platform-adapter.py` | ✅ 脚本 |
| `absorbed` | promote-finalize 时 | `issue-sync promote-finalize` | ✅ 脚本（仅 promote 路径） |
| `absorbed` | 手动 closeout batch 脚本 | 一次性脚本 | ⚠️ 手动 |
| `dropped` | 无脚本触发 | 无 | 🔴 断档 |

**问题**: promote 之外没有脚本路径到 `absorbed`。非 promote 的 raw issue 永远停在 `proposed`。

### 2.2 I-* phase_state

| 值 | 设置时机 | 设置方 | 类型 |
|----|---------|--------|:---:|
| `in_b2_ibm` | promote 后初始 | 无脚本 | 🔴 AI 手动写 |
| `done_b2_ibm` | B2 脑暴完成 | 无脚本 | 🔴 AI 手动写 |
| `in_dev` | 开发中 | 无脚本 | 🔴 AI 手动写 |
| `blocked_dev` | 开发受阻 | 无脚本 | 🔴 AI 手动写 |
| `in_verification` | 验证中 | 无脚本 | 🔴 AI 手动写 |
| `completed` | 完成 | 无脚本 | 🔴 AI 手动写 |

**问题**: 整个 I-* 状态机零脚本触发。

### 2.3 chats.consumed

| 值 | 设置时机 | 设置方 | 类型 |
|----|---------|--------|:---:|
| 0 | chat 入库 | `chat-inbox.py add` | ✅ 脚本 |
| 1 | consume | `chat-inbox.py consume` | ✅ 脚本 |
| -1 | discard | `chat-inbox.py discard` | ✅ 脚本 |

✅ 完整。无断档。

### 2.4 platform_state

| 值 | 设置时机 | 设置方 | 类型 |
|----|---------|--------|:---:|
| open | issue-sync create | `issue-sync` | ✅ 脚本 |
| closed | issue-sync close | `issue-sync` / `wt-close` | ✅ 脚本 |

✅ 完整。无断档。

---

## 三、链路追踪：raw issue 从创建到消失的全生命周期

```
                     chat-inbox / platform
                           │
                           ▼
                     phase_state: proposed
                     platform_state: open
                           │
                     ┌─────┼─────────────┐
                     │                   │
               [B1 评估通过]        [B1 评估不通过]
               promote → I-*        phase_state: dropped
                     │                   │
                     ▼                   ▼
              phase_state: in_b2_ibm    scan 不再显示
                     │                 (TERMINAL_RAW)
                     ▼
              B2 脑暴完成
              phase_state: done_b2_ibm
                     │
                     ▼
              wt-create 工位
              phase_state: in_dev
                     │
                     ▼
              merge to develop
              phase_state: in_verification
                     │
                     ▼
              wt-close + issue-sync close
              phase_state: completed
              platform_state: closed
                     │
                     ▼
              scan 不再显示
```

**现在的问题**：

1. 如果 raw issue 不经过 promote（无 I-*）→ 没有 B1→I-* 链路 → phase_state 永远 `proposed` → scan 永远显示
2. I-* 的 phase_state 全由 AI 手动管理 → 可能遗忘、错标
3. wt-create 创建工位但不更新任何 phase_state → wt-create 与状态机脱节
4. merge-guarded 合并后不更新 phase_state → merge 与状态机脱节

---

## 四、改造方案：确定性脚本触发点

### 4.1 原则

- **wt-create** 创建工位时，应更新对应 issue 的 phase_state
- **merge-guarded** 合并时，应更新对应 issue 的 phase_state
- **wt-close / issue-sync close** 关闭时，应更新 phase_state 为终端值
- **只有 blocked / dropped 的判断可能需要 AI 语义**，其他都是确定性的

### 4.2 raw-* phase_state 改造

| 转换 | 触发点 | 脚本位置 | 说明 |
|------|--------|---------|------|
| (空) → proposed | materialize / pull | `chat-inbox.py` / `platform-adapter.py` | ✅ 已有 |
| proposed → in_dev | wt-create 创建工位后 | `wt-create` 新增 | 表示"已有工位在开发" |
| in_dev → absorbed | merge-guarded 合并后 | `merge-guarded` → `issue-sync close` | 表示"代码已合入，吸收完成" |
| proposed → dropped | AI 判定或 feedback reject | AI 语义 / 新增 CLI | 允许脚本+AI 两种触发 |

**新增状态 `in_dev`**：在 `TERMINAL_RAW` 之外，scan 会显示但 stage 为 "dev_worktree"。

或者**不新增状态，直接用 `absorbed`**：
- wt-create → `absorbed`，表示"已被工位吸收"
- merge-guarded → 关平台 issue，收口完成
- scan 不再显示（TERMINAL_RAW 跳过）

**推荐后者**：更简单，不改变 scan 逻辑，不新增状态值。

### 4.3 I-* phase_state 改造

| 转换 | 触发点 | 脚本位置 | 说明 |
|------|--------|---------|------|
| (空) → in_b2_ibm | issue-sync promote | `issue-sync promote` 新增 | promote 时自动设置 |
| in_b2_ibm → in_dev | wt-create 创建工位 | `wt-create` 新增 | 判断 source 是 I-* |
| in_dev → in_verification | merge-guarded 合并 | `merge-guarded` 新增 | 合并到 develop 后 |
| in_verification → completed | wt-close | `wt-close` 新增 | 关闭工位+同步平台 |
| * → blocked_dev | AI 语义 | AI 手动 | 需要判断阻塞原因 |
| * → done_b2_ibm | AI 语义 | AI 手动 | B2 脑暴完成 |

### 4.4 实现细节

#### wt-create 改造

在 `_pull_raw_issue` 或 `_fill_platform_ids` 成功后：

```bash
# 如果是 raw issue，标记为 absorbed（已被工位吸收）
if [[ "$using_new" -eq 1 ]]; then
  local issue_file="$ROOT_DIR/docs/issues/raw-${raw_key}/issue.md"
  if [[ -f "$issue_file" ]]; then
    python3 -c "
import yaml
with open('$issue_file') as f: c = f.read()
p = c.split('---', 2)
fm = yaml.safe_load(p[1])
fm['phase_state'] = 'absorbed'
new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
with open('$issue_file', 'w') as f: f.write('---\n' + new_fm + '\n---' + p[2])
"
  fi
fi
```

#### merge-guarded 改造

合并后遍历 diff 中的 issue 文件（已有 `_sync_issues_changed_in_merge`），对 raw issue 设置为 `absorbed`，对 I-* issue 设置为 `in_verification` 或 `completed`。

### 4.5 scan 的一致性

改造后，scan 看到的状态与实际情况匹配：

| 实际情况 | phase_state | scan 表现 |
|---------|------------|----------|
| raw 刚创建，无工位 | proposed | 显示为 raw_not_created / chat_unconsumed |
| wt-create 已创建工位 | absorbed | **不显示**（TERMINAL_RAW） |
| 代码已合并 | absorbed + platform=closed | 不显示 |
| raw 被丢弃 | dropped | 不显示 |
| I-* 刚 promote | in_b2_ibm | 显示为 B2_active |
| I-* 在开发 | in_dev | 显示为 dev_worktree |
| I-* 合并验证 | in_verification | 显示为 verifying |
| I-* 完成 | completed | 不显示 |

**关键**：wt-create 后 raw issue 不再出现在 scan 中（已被吸收），但 I-* issue 会出现在 scan 中（如果还没完成）。manager 看到的是 I-* 级别的进度，不是 raw 级别的。

---

## 五、评论写入：重定向 + 封装命令

### 5.1 当前流程

```
freely chat --issue raw-xxx "message"
        │
        ▼
_write_chat_to_issue()
        │
        ├── chat_type=comment, issue_id=raw-xxx
        ├── INSERT into freely.db (consumed=0)
        ├── 如果 worktree 存在 → materialize-comment → consume (consumed=1)
        └── 如果 worktree 不存在 → 留在 DB，等 scan 扫出
```

**问题**：
1. 无 phase_state 检查——已 absorbed 的 raw issue 仍可写评论
2. 无 absorbed_into 重定向——raw 已 promote 为 I-*，评论应写到 I-*
3. 无 platform_state 检查——已关闭的 issue 仍可写评论
4. 没有独立的 command 入口——散落在 `freely chat` 里

### 5.2 scan 如何消费评论

scan 的 `scan_chat_inbox()` 读取 `chats WHERE consumed=0`：
- `chat_type=comment` + `consumed=0` → stage=`chat_comment_pending` → 显示在 scan
- `chat_type=comment` + `consumed=1` → **不显示**（已消费）
- `chat_type=new-issue` + `consumed=0` → stage=`chat_waiting_worktree` → 显示

评论的"消费"路径：DB 写入 → worktree 同步 → consume → 从 scan 消失。
如果 worktree 不存在，评论永远 unconsumed，scan 永远显示。

### 5.3 封装 `freely comment` 命令

与 `wt-create`、`wt-close`、`feedback` 同级，统一对外接口：

```
Usage: freely comment --issue <raw-xxx|I-xxx> --message <text>
       freely comment --issue <raw-xxx|I-xxx> --message-file <path>

行为:
  1. 读取目标 issue 的 phase_state
  2. phase_state ∈ {absorbed, dropped} + absorbed_into → 自动重定向到 I-*
  3. phase_state ∈ {absorbed, dropped} + 无 absorbed_into → 拒绝 + 提示
  4. platform_state = closed → 拒绝
  5. 检查通过 → 写入 DB + 寻找 worktree 同步
```

脚本确定性判断，不依赖 AI 语义做路由。

### 5.4 重定向逻辑

```bash
_resolve_comment_target() {
  local issue_id="$1"
  local issue_file="$PROJECT_ROOT/docs/issues/$issue_id/issue.md"
  
  # 只对 raw-* 做重定向检查
  [[ "$issue_id" == raw-* ]] || { echo "$issue_id"; return 0; }
  [[ -f "$issue_file" ]] || { echo "$issue_id"; return 0; }
  
  local phase absorbed_into
  phase=$(_fm_get "$issue_file" "phase_state")
  absorbed_into=$(_fm_get "$issue_file" "absorbed_into")
  
  if [[ "$phase" == "absorbed" || "$phase" == "dropped" ]]; then
    if [[ -n "$absorbed_into" && "$absorbed_into" != "None" ]]; then
      echo "[comment] raw $issue_id 已 $phase，重定向到 $absorbed_into" >&2
      echo "$absorbed_into"
      return 0
    else
      echo "[comment] 拒绝: raw $issue_id 已 $phase，无子 issue" >&2
      return 1
    fi
  fi
  
  if [[ "$(_fm_get "$issue_file" "platform_state")" == "closed" ]]; then
    echo "[comment] 拒绝: $issue_id 平台已关闭" >&2
    return 1
  fi
  
  echo "$issue_id"
}
```

### 5.5 scan 对齐

| 场景 | 评论去向 | consumed | scan 表现 |
|------|---------|:---:|------|
| 写 raw-xxx（proposed，有工位） | raw-xxx/issue.md | 1 | 不显示 |
| 写 raw-xxx（proposed，无工位） | DB 中等待 | 0 | `chat_comment_pending` |
| 写 raw-xxx（absorbed，有 I-*） | **重定向到 I-xxx** | 1 | 不显示 |
| 写 raw-xxx（absorbed，无 I-*） | 拒绝 | - | - |
| 写 I-xxx（任意状态） | I-xxx/issue.md | 1 | 不显示 |

---

## 六、用户交互模型与聊天历史设计

### 6.1 Freely 用户的两种交互方式

```
┌─────────────────────────────────────────────────────────┐
│                    用户如何与 Freely 交互                  │
├──────────────────────┬──────────────────────────────────┤
│ A. 平台 (GitHub/Gitee) │ B. Freely Chat (未来 UI)         │
├──────────────────────┼──────────────────────────────────┤
│ • 直接创建 raw issue   │ • 自由输入框 → 多轮对话            │
│ • 对 OPEN issue 写回复 │ • Issue 列表 → 每个有"评论"按钮    │
│                      │ • 聊天历史列表 → 物化/丢弃           │
├──────────────────────┴──────────────────────────────────┤
│              最终收口：scan → manager 处理                 │
└─────────────────────────────────────────────────────────┘
```

**A 路径**（平台）：用户在 GitHub/Gitee 上操作，scan 的 `scan_platform_issues` 和 `scan_classification` 自动拉取。回复（reply）算评论，通过 `platform-adapter.py` 拉取到 `docs/issues/{id}/issue.md` 的 `## Comments` 区域。

**B 路径**（Chat）：用户在 Freely UI 中聊天，消息存入 `freely.db`。分为两种子模式：
- **自由聊天**：无前置 issue，多轮对话形成"聊天历史"。用户可点击"物化"按钮，AI 分析整个对话，决定生成哪些 raw issue 和评论。
- **Issue 评论区**：用户在 issue 详情页点"评论"按钮，直接对该 issue 写评论。

### 6.2 聊天历史模型：只需扩展 `chats` 表，不需新表

**当前 `chats` 表**：一行 = 一条消息，没有对话分组。

**改动**：只加一个字段 `conversation_id`，不需要新建 `conversations` 表。

```sql
-- 扩展 chats 表
ALTER TABLE chats ADD COLUMN conversation_id INTEGER DEFAULT 0;

-- conversation_id = 0  → 独立消息（new-issue / comment），不属对话
-- conversation_id = N  → 属于同一个对话，N = 该对话首条消息的 id
```

**为什么 `conversations` 表冗余**：

| 需求 | 有 conversations 表 | 只用 conversation_id |
|------|-------------------|---------------------|
| 对话 ID | conversations.id | chats.conversation_id |
| 对话标题 | conversations.title | 从首条消息截取 |
| 对话 consumed | conversations.consumed | 所有消息 consumed=1 |
| 对话创建时间 | conversations.created_at | 首条消息 created_at |
| 查询未消费对话 | JOIN conversations | `SELECT DISTINCT conversation_id FROM chats WHERE consumed=0 AND conversation_id>0` |

`conversation_id` 本身就能标记分組，`consumed` 字段复用在每条消息上，物化/丢弃时批量更新。不需要同步两张表。

### 6.3 两表关系（化简后）

```
chats 表（唯一数据表）
│
├── conversation_id = 0  →  独立消息
│   ├── chat_type = new-issue  →  1 条 → 1 个 raw issue
│   └── chat_type = comment    →  1 条 → 追加到指定 issue
│
└── conversation_id = N  →  对话消息
    └── chat_type = chat-message  →  物化时才决定去向
        （多条消息共享同一个 conversation_id）
```

**对话生命周期（只用 chats 表）**：

```
用户开始聊天 → INSERT 首条消息 (id=N, conversation_id=N, consumed=0)
       │
       ├── 后续消息 → INSERT (id=M, conversation_id=N, consumed=0)
       │
       ▼
用户点"物化"按钮 → AI 分析全部消息 → 创建 issues/comments
       │
       ▼
UPDATE chats SET consumed=1 WHERE conversation_id=N  -- 批量消费
       │
       ▼
scan: consumed=1 → 不显示
```

**"丢弃"按钮**：

```
UPDATE chats SET consumed=-1 WHERE conversation_id=N
```

### 6.4 chats 表记录生命周期：只改 consumed，永不删除

**当前设计**：chats 表只标记 `consumed` 状态（0→1→-1），没有 DELETE。记录永久保留在 SQLite 中。

这个设计是对的——聊天记录是审计追踪，不应删除。但需要明确"何时清理"的语义：

| consumed 值 | 含义 | scan 可见 | 何时触发 |
|:---:|------|:---:|------|
| 0 | 未消费 | ✅ 显示 | chat 入库时 |
| 1 | 已消费 | ❌ 不显示 | materialize 成功写入 docs/issues/ 后 |
| -1 | 已丢弃 | ❌ 不显示 | 用户点"丢弃" / AI 判定噪声后 |

**消费链（先本地，后平台）**：

```
                    ┌── chat-inbox source ──┐     ┌── platform source ──┐
                    │                        │     │                      │
  chat 入库          │  GitHub issue          │     │  GitHub issue         │
  chats (consumed=0) │  (已有 OPEN)           │     │  (已有 OPEN)          │
     │               │     │                  │     │     │                 │
     ▼               │     ▼                  │     │     ▼                 │
  wt-create          │  wt-create             │     │  wt-create            │
     │               │     │                  │     │     │                 │
     ├─ materialize  │     ├─ raw-issue-pull  │     │     ├─ raw-issue-pull │
     │  → issue.md   │     │  → issue.md      │     │     │  → issue.md     │
     │               │     │                  │     │     │                 │
     ├─ consume      │     │                  │     │     │                 │
     │  consumed=1   │     │                  │     │     │                 │
     │               │     │                  │     │     │                 │
     └─ issue-sync   │     └─ issue-sync      │     │     └─ issue-sync     │
        create       │        create          │     │        create         │
        → GitHub     │        → GitHub        │     │        → GitHub       │
```

**关键顺序**：`docs/issues/` 本地文件 → 消费标记 → `issue-sync` 推送到平台。本地是唯一真相源，平台是镜像。

**清理策略**：chats 记录永久保留，不删除。`consumed=1` 和 `consumed=-1` 的记录是审计追踪。如果 DB 过大，未来可加 `VACUUM` 或归档策略，但当前阶段不需要。

### 6.5 聊天类型重新分类

| chat_type | 含义 | 前置条件 | 物化行为 |
|-----------|------|---------|---------|
| `new-issue` | 单条消息直接变 raw issue | 无 | 1 条消息 → 1 个 raw issue |
| `comment` | 对已有 issue 的评论 | 指定 `--issue` | 追加到 issue.md |
| `chat-message` | 自由对话中的一条消息 | 属于 conversation | 随 conversation 一起物化 |

`chat-message` 是新增类型。它不属于某个 issue，只属于一个 conversation。物化时才决定去向。

### 6.5 scan 对齐

| 场景 | 数据状态 | scan 表现 |
|------|---------|----------|
| conversation unconsumed | conversations.consumed=0 | 新 stage: `chat_conversation_pending` |
| conversation 已物化 | conversations.consumed=1 | 不显示 |
| conversation 已丢弃 | conversations.consumed=-1 | 不显示 |
| 单条 chat (new-issue, 无工位) | chats.consumed=0, chat_type=new-issue | `chat_waiting_worktree` |
| 单条 chat (comment, 无工位) | chats.consumed=0, chat_type=comment | `chat_comment_pending` |
| 平台回复 (GitHub comment) | 本地 issue.md 有未同步评论 | `unsynced_comments` |

### 6.6 封装命令一览

| 命令 | 用途 | 类似 |
|------|------|------|
| `freely chat` | 开始/继续自由对话 | 已有，需扩展 |
| **`freely comment`** | 对已有 issue 写评论 | **新增** |
| `freely feedback` | 直接创建 raw issue | 已有 |
| `wt-create` | 创建开发工位 | 已有 |
| `wt-close` | 关闭工位 | 已有 |

`freely chat` 和 `freely comment` 的区别：
- `chat`：自由对话，消息属于 conversation，需要物化步骤
- `comment`：对已有 issue 的定向评论，无需物化，直接写入

---

## 七、变更清单

### 7.1 状态机脚本触发点

| 文件 | 改动 | 优先级 |
|------|------|:---:|
| `wt-create` | 创建成功后设置 raw phase_state=absorbed | P0 |
| `wt-create` | 如果是 I-* 工位，设置 phase_state=in_dev | P1 |
| `issue-sync` `cmd_promote` | 设置 I-* phase_state=in_b2_ibm | P1 |
| `merge-guarded` `_sync_issues_changed_in_merge` | 对 raw 设 absorbed，对 I-* 设 in_verification | P1 |
| `wt-close` | 设置 I-* phase_state=completed | P2 |

### 7.2 评论命令封装

| 文件 | 改动 | 优先级 |
|------|------|:---:|
| **`freely` 新增 `cmd_comment`** | 封装写评论命令 + 内置 phase_state 重定向/防御 | **P0** |
| `freely` `_write_chat_to_issue` | 调用 `cmd_comment` 的重定向逻辑 | P1 |

### 7.3 聊天历史模型（不新增表，只扩展字段）

| 文件 | 改动 | 优先级 |
|------|------|:---:|
| `chat-inbox.py` | `chats` 表加 `conversation_id INTEGER DEFAULT 0` | P1 |
| `chat-inbox.py` | `chat_type` 新增 `chat-message`，`consume_conversation(conversation_id)` | P1 |
| `task-lifecycle-scan.py` | 新增 `chat_conversation_pending` stage | P1 |
| `freely` `cmd_chat` | 支持 conversation 模式（无 --issue 时自动创建/续接对话） | P2 |

### 7.4 防御

| 文件 | 改动 | 优先级 |
|------|------|:---:|
| `task-lifecycle-scan.py` | 确保 phase_state 优先于 status 回退（已有） | P2 |
