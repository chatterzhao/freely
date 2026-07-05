# Brainstorms — chats 表扩展 conversation_id + chat-message 类型 + scan 对齐

## Discovery

- **提出时间**: 2026-05-18T02:04:06Z (GitHub #539)
- **提出方式**: 平台反馈
- **依赖**: #538 freely comment 命令（已合并到 develop）
- **当前阶段**: Freely 自举开发整合阶段，聊天模型和评论命令共同构成 chat 体系
- **相关性**: 高 — 当前 chat→issue 流程只有 new-issue（创建 raw issue）和 comment（追加评论）两种类型，缺少自由对话模式。用户可以通过 `freely chat` 发送消息，但每条消息要么立刻变成 raw issue，要么追加到已有 issue。没有"先对话、再决定去向"的模式。
- **时效判断**: 当前仍有价值。#538 comment 命令已合入 develop，chat 体系的第三个类型（chat-message）是自然的扩展方向。

## Research

### 现有 chats 表结构

```sql
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,
    chat_type TEXT NOT NULL,       -- "new-issue" | "comment"
    issue_id TEXT NOT NULL,
    author TEXT NOT NULL DEFAULT 'human',
    channel TEXT NOT NULL DEFAULT 'chat',
    message TEXT NOT NULL,
    consumed INTEGER NOT NULL DEFAULT 0,
    session_refs TEXT DEFAULT '[]',
    intake_id TEXT DEFAULT '',
    materialized_as TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT ''
);
```

当前只有 `chat_type=new-issue` 和 `chat_type=comment` 两种类型。

### chat-inbox.py 当前能力

- `add_chat()` — INSERT 新消息，chat_type 为任意字符串（无校验）
- `query_pending()` — 查全部 `consumed=0` 的消息
- `query_by_issue()` — 按 issue_id 查消息
- `consume()` / `discard()` / `reset()` — 更新 consumed 状态
- `materialize()` — 将 chat 消息写为新的 raw issue (`docs/B1-docs/raw-{issue_id}/issue.md`)
- `materialize_comment()` — 将 chat 消息追加到现有 issue
- **缺少**: `consume_conversation()` — 按 conversation_id 批量消费

### task-lifecycle-scan.py scan_chat_inbox 当前行为

`scan_chat_inbox()` (line 684) 扫描 `freely.db` 中 `consumed=0` 的 chat 消息：

- `chat_type=new-issue` → stage=chat_waiting_worktree / chat_ready
- `chat_type=comment` → stage=chat_comment_pending
- 检查 worktree 是否存在、target issue 是否存在
- 返回每个单项消息的 scan item

**缺少**: 对 `chat-message` 类型的处理，以及按 conversation_id 分组展示的能力。

### _write_chat_to_issue 当前流程

`_write_chat_to_issue()` (freely line 5604) 是 chat 消息写入的核心函数：

1. 根据 `FREELY_CHAT_TARGET_ISSUE` 环境变量决定 chat_type（new-issue / comment）
2. INSERT 到 freely.db chats 表
3. 对于 new-issue：INSERT 后用 chat_id 作为 issue_id（`raw-{chat_id}`）
4. 尝试直接同步到 worktree（materialize / materialize-comment）
5. 若无 worktree：留下 pending 信号供 daemon 处理

**缺少**: 对 chat-message 类型的支持，以及 conversation_id 的赋值逻辑。

### cmd_chat 和 cmd_intake_chat 流程

`cmd_chat` (line 20037) → `submit_human_frontdoor_message` (line 20061) → `cmd_intake_chat` (line 20214)：

- `freely chat <message>` — 默认创建 new-issue（当无 --issue 也无 --new-issue 时）
- `freely chat --issue <id> <message>` — 追加为 comment
- `freely chat --new-issue <message>` — 显式创建 new-issue
- 调用 `_write_chat_to_issue()` 写入

**缺少**: `--conversation` 模式或自动对话检测。

### 依赖分析

- **#538 freely comment 命令**: 已合并到 develop。提供 `freely comment` 的外部 CLI 接口，是 chat 体系的第二块拼图。chat-message 是第三块，依赖 comment 已有的 materialize-comment 基础设施和 chat-type 路由模式。
- **conversation_id 赋值逻辑**: 首条消息 INSERT 后，需要 UPDATE 自己的 conversation_id 为首条消息的 id。后续消息在 INSERT 前就知道 conversation_id 的值。这里有一个窗口：如果首条消息 INSERT 成功但 UPDATE 失败，conversation_id=0，后续消息的 conversation_id 就指向一个不存在的 id。
- **存量兼容**: 现有记录 conversation_id 默认为 0，scan_chat_inbox 需要在 WHERE 条件中排除 conversation_id>0 的消息（避免重复计数），或者增加新的 scan stage。

### 参考文档

- `docs/B1-docs/raw-issue-state-lifecycle.md` §6, §7.3 — issue 状态生命周期和 chat-inbox scan 阶段
- `docs/B1-docs/raw-20260429T204000Z/brainstorms.md` — chat-inbox SQLite 原始设计
- `docs/B1-docs/raw-20260518T020345Z45Z/brainstorms.md` — freely comment 命令设计
- `docs/system/workspace/scripts/runtime/chat-inbox.py` — chat-inbox 模块源码
- `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py` — scan_chat_inbox 实现

## 设计决策

### 决策 1：conversation_id 赋值策略

**选择**: 首条消息 id 作为 conversation_id（如 issue 所述：`conversation_id=N，N=首条消息 id`）。

流程：
1. 用户开始对话 → 首条消息 INSERT 得 id=X，初始 `conversation_id=0`
2. 即时 UPDATE `SET conversation_id=X WHERE id=X`
3. 后续消息 INSERT 时直接 `conversation_id=X`

**理由**: 零额外 ID 生成逻辑。UTC timestamp 天然唯一且有序。
**风险**: UPDATE 失败 → 首条消息的 conversation_id 为 0。在将 WAL 模式 + 单连接序列化下概率极低。仍可通过 `_write_chat_to_issue` 的事务包装消除窗口。

**备选方案（已否决）**: 运行时生成 UUID 作为 conversation_id — 无需 UPDATE 首条消息，但需要额外 ID 生成逻辑，且 conversation_id 不具备时序含义。

### 决策 2：chat-message 的 chat_type 取值

**选择**: 新增 `chat_type='chat-message'`。

- `chat_type = 'chat-message'` — 自由对话消息，物化时才决定去向
- `chat_type = 'new-issue'` — 单条 raw issue（已有）
- `chat_type = 'comment'` — 追加评论（已有）

**理由**: 与现有 schema 兼容，chat-inbox.py 的 `add_chat()` 对 chat_type 无校验。scan 可以通过 chat_type 过滤分类。

### 决策 3：consume_conversation() 接口

新增函数，签名与行为：

```python
def consume_conversation(
    db_path: str,
    conversation_id: int,
    action: str,        # "materialize" | "materialize-all-as-comment"
    target: str,        # target dir (for materialize) or issue file (for comment)
) -> int:               # returns count of consumed messages
```

**materialize**: 将所有对话消息合并为一条 raw issue。消息体用分隔符连接。
**materialize-all-as-comment**: 将所有对话消息依次追加到同一 issue 文件的尾部。

**理由**: 与单个 chat 的 consume 模式一致。action 参数让 AI 在消费时决定去向，而非写入时决定。

### 决策 4：scan 新增 chat_conversation_pending stage

在 `task-lifecycle-scan.py` `scan_chat_inbox()` 之后新增一个子阶段：

```python
SELECT conversation_id, COUNT(*) as msg_count, MIN(created_at) as first_msg
FROM chats
WHERE conversation_id > 0 AND consumed = 0
GROUP BY conversation_id
ORDER BY MIN(id) ASC
```

输出格式：
```json
{
    "source_family": "chat_conversation_pending",
    "key": "conv-{conversation_id}",
    "stage": "chat_conversation_pending",
    "conversation_id": <int>,
    "message_count": <int>,
    "first_message_at": "<timestamp>",
    "incomplete": ["conversation_unconsumed"],
    "next_action": "AI 判断 → consume_conversation() 批量消费 → materialize / comment / discard"
}
```

**理由**: 独立的 source_family 避免与单项 chat 混淆。按 conversation_id 分组展示，而非逐条展示。

### 决策 5：存量兼容

`ALTER TABLE chats ADD COLUMN conversation_id INTEGER DEFAULT 0;` 是纯 SQLite DDL，零风险：

- 现有 `new-issue` / `comment` 记录的 conversation_id=0
- `query_pending()` 不受影响（WHERE consumed=0 不变）
- 现有查询增加 AND conversation_id=0 过滤可排除对话消息
- scan_chat_inbox 中在 WHERE 增加 `AND (conversation_id = 0 OR conversation_id IS NULL)` 保持现有分类逻辑

### 决策 6：chat-message 的触发方式

**选择**: 通过 `freely chat --conversation` 命令行开关显式控制。

```
freely chat --conversation <message>   # 在已有对话中发送（如果无活跃对话，自动创建新对话）
freely chat --conversation --new <message>   # 显式创建新对话
```

- 无 `--conversation` 也无 `--issue`：默认 `new-issue`（行为不变，向后兼容）
- `--conversation` 且当前有活跃对话：追加到该对话
- `--conversation --new` 或当前无活跃对话：创建新对话

**备选方案（暂不实现）**: TUI 内隐式对话检测。连续 chat 消息自动聚合为对话。这需要 daemon 侧的状态管理，复杂度较高。

### 决策 7：raw-key shorthand 与 conversation 的对应关系

对话本身没有单独的 ID——`conversation_id` 就是首条消息 id。但对于 consume/conversation 级操作，需要能在 scan 输出和 CLI 参数中引用。

**选择**: `conv-{conversation_id}` 作为 shorhand key：
- `consume_conversation(conversation_id=N)` 内部实现
- 每条 chat-message 仍然有自己的 `id`，可用作 `raw-{id}` 单独引用
- 但在 scan 输出中，按 `conv-{conversation_id}` 分组展示

## 收敛

- **范围明确**: 不新增表，只在 chats 表扩展列 + 新增 chat-type + scan stage
- **向后兼容**: conversation_id=0 默认值，现有查询不受影响
- **依赖就绪**: #538 已合并，comment 基础设施可用
- **增量交付**: 可以先做 schema + consume_conversation + scan，再做 --conversation CLI 触发

## 结论

推荐 promote 为单个 candidate，进入 B2_IBM materialize I-* issue。实现可以分两步：
1. schema 扩展 + consume_conversation + scan stage
2. --conversation CLI 触发方式
