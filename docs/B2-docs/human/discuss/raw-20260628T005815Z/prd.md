# PRD: chat 重构 — comment + discuss + archive skill

## Goal

将旧的 `freely chat` 拆分为三个独立模块：评论（comment）、讨论（discuss）、讨论导出（archive skill）。每种场景走最合适的存储路径，消除本地 DB 单机瓶颈和入口混淆。

## Dev-Loop Handoff

### 模块一：freely comment

- `cmd_comment` 函数，注册到 `freely` 子命令
- 参数：`--issue raw-{key}` `<原文>` | `--file <path>`
- adapter 并行写 GitHub + Gitee + GitCode
- 成功后：agent-id.env → session_id → ACP session/prompt 通知
- close 的 issue：直接拒绝
- I-* issue：不碰

### 模块二：freely discuss

- `cmd_discuss` 函数，子命令：`新建` / `--continue <id>` / `--archive <id>`
- 讨论 agent：`.ai-auth` slot 切换模型，讨论执行 skill 思考
- agent-table.toml：`discuss_slot` + `pool=1`
- 本地存储：SQLite `discussions` 表（元数据）+ JSONL `.freely/discussions/{id}.jsonl`（消息时间线）
- 平台同步：GitHub Discussions + GitCode Discussions（Gitee 跳过）
- @ 引用：@raw-{key} / @raw-{key}#comment-{id} / @discussion-{id} / @discussion-{id}#{sub-id}
- session 生命周期：active → archived/closed

### 模块三：freely discuss --archive <session-id>

命令内部：
1. 查 sessions 表找 discuss agent 的 session_id
2. ACP session/prompt，固定提示词：`"根据 skill:freely-discuss-archive-execution 将 session {session-id} 归档"`
3. 讨论 agent 收到 → 加载归档 skill → 执行：
   - 读取本地 DB session 全部消息
   - 分析 → 归并 @raw-{key} → `freely comment` 写评论 / `freely feedback` 创建 raw issue
   - 插入最后一条讨论消息，记录所有产出 ID
   - 标记 consumed/discard
   - 关闭平台 Discussions + 本地 platform_state: closed

纯手工触发，不自动调用。

### 跨切关注点

- 评论 resolution 子评论格式（adopted/discarded）
- pr-create-guarded / wt-close Phase 0 全平台检查
- 跨平台评论同步：SHA256 去重 + adapter 补建 + AI 语义合并
- 旧 chat 入口废弃/重定向
