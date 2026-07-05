# Brainstorms — freely comment 命令

## Discovery

- **提出时间**: 2026-05-18T02:03:45Z (GitHub #538)
- **提出方式**: 平台反馈
- **当前阶段**: Freely 自举开发整合阶段
- **相关性**: 高 — 当前 chat→issue 流程缺少显式外部命令接口。`_write_chat_to_issue` 已有 comment 写入能力，但只能通过 chat dispatch 内部调用。对外 CLI 接口只提供了 `freely feedback`（创建 raw issue），没有 `freely comment`（追加评论）。
- **时效判断**: 当前仍有价值。chat comment 已通过内部路径工作（`freely chat --issue <id>`），但缺少外部脚本/工具调用的稳定入口。

## Research

### 现有命令结构

`freely` 子命令通过 `main()` 的 `case "$cmd"` 分发（line ~21600）：
- `freely feedback` — 创建 raw issue（`cmd_feedback` at line 20083）
- `freely issue-sync` — 平台 issue 同步
- `freely chat` — 通过 ACP bridge 的 chat 交互

### 现有 comment 基础设施

`_write_chat_to_issue()` (line 5604) 已完整支持 comment 写入：
- `FREELY_CHAT_TARGET_ISSUE` 环境变量控制目标 issue
- 当设置了 `TARGET_ISSUE`，chat_type="comment"
- 写入 `freely.db` chats 表
- 通过 `chat-inbox.py materialize-comment` 同步到 worktree
- 会触发 `intake_pending_signal` 通知 daemon

### 依赖关系

- **#536**: wt-create 更新 phase_state（comment 重定向依赖 `phase_state=absorbed` 判断）
  - 当 phase_state 正确反映 absorbed/dropped 时，comment 可以决定是否重定向到 I-*
  - 如果 #536 未合并，freely comment 应跳过 phase_state 重定向，直接写入目标 issue

### 现有 _route_chat_to_issue

`_route_chat_to_issue()` (line 5694) 实现了 script-based fast path 路由。freely comment 不需要这个路由——用户显式指定 --issue 参数。

### 参考文档

- `docs/B1-docs/issue-state-lifecycle.md` §5, §7.2 — phase_state 生命周期与 issue 状态转换

## 设计决策

### 决策 1：封装层级

将 `freely comment` 设计为 wrapper 命令，复用 `_write_chat_to_issue` 的核心逻辑：

```
freely comment --issue <raw-xxx|I-xxx> --message <text>
                ↓
  设置 FREELY_CHAT_TARGET_ISSUE=<issue>
  调用 _write_chat_to_issue() 内部逻辑（不经过 chat dispatch）
                ↓
  写入 freely.db → materialize → consume
```

**理由**：复用已有基础设施，零重复代码。等价于 `freely chat` 的 `--issue` 模式的独立封装。

### 决策 2：phase_state 重定向

- 依赖 #536 合并后生效
- raw issue 的 `phase_state=absorbed/dropped` + `absorbed_into` 存在 → 重定向到 I-*
- 纯脚本判断，零 AI 语义依赖

### 决策 3：错误防御

| 条件 | 行为 |
|------|------|
| `platform_state=closed` | 拒绝，提示 issue 已关闭 |
| raw absorbed/dropped + 无 absorbed_into | 拒绝，提示无 I-* 可重定向 |
| I-* 目标不存在 | 拒绝，提示 issue 不存在 |
| 成功 | 写入 materialize 消费 |

## 收敛

- **范围明确**: 仅封装 comment 写入。不涉及 chat dispatch、不涉及 issue 创建。
- **独立可交付**: 即使 #536 未合并，freely comment 可以作为简化版发布（跳过重定向）。
- **实现路径**: 新增 `cmd_comment` 函数 → 在 `main()` 的 case 中添加 `comment` 路由 → 添加到 usage。

## 结论

推荐 promote 为单个 candidate，直接进入 B2_IBM materialize I-* issue。实现范围小、边界清晰、复用现有基础设施。
