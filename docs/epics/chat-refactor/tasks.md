# Tasks: chat 重构 — comment + discuss + archive skill

- issue_id: I-20260628T005815Z-A

## B2 文档（已完成）
- [x] brainstorms/b-I-20260628T005815Z-A.md — 实现方案评估与验收对齐
- [x] prd.md — Goal → Dev-Loop Handoff
- [x] pre-tests.md — 6 条 acceptance（4端到端+2单元）
- [x] tasks.md — 7 阶段 50+ 子项
- [x] code-reviews/implementation-decision-note.md — 5 字段完整

## 阶段一：comment 命令

- [ ] 1.1 新增 `cmd_comment` 函数到 `freely`
  - `--issue raw-{key}` + `<原文>` 或 `--file <path>`
  - adapter 并行写所有平台（GitHub + Gitee + GitCode）
  - 成功：agent-id.env → session_id → ACP session/prompt 通知
  - close issue → 直接拒绝
  - I-* issue → 不碰
- [ ] 1.2 注册 `comment` 子命令到 `freely` main()
- [ ] 1.3 废弃 `freely chat --issue` 入口，输出重定向提示

## 阶段二：discuss 命令

- [ ] 2.1 新增 `cmd_discuss` 函数到 `freely`
  - `freely discuss` 新建 session
  - `freely discuss --continue <id>` 继续
  - `freely discuss --archive <id>` — 查 sessions 表 → ACP session/prompt 发送固定提示词给 discuss agent
- [ ] 2.2 存储：混合方案
  - SQLite `discussions` 表（元数据）：session_id TEXT PK, owner TEXT, status TEXT('active'|'archived'|'closed'), platform_ids TEXT(JSON), created_at TEXT, updated_at TEXT
  - JSONL `.freely/discussions/{session_id}.jsonl`（消息内容）：每行 `{"author":"...","body":"...","refs":[...],"created_at":"...","consumed":-1|0|1}`
  - `freely_db_manager.py` 新增 discussions 表 handler
- [ ] 2.3 agent-table.toml 配置
  ```toml
  [[agents]]
  discuss_id = "discuss_01"
  discuss_slot = "claude-apikey-ds-pro-auto"
  reviewer_id = ""
  reviewer_slot = ""
  pool = 1
  ```
  字段名 `reviewer_id`/`reviewer_slot` 对齐 manager/worker，值留空（暂不设讨论 reviewer）
- [ ] 2.4 平台 Discussions 同步
  - `platform-adapter.py` 新增：create_discussion, reply_discussion, close_discussion
  - 开始讨论 → 创建平台 Discussion（GitHub + GitCode，Gitee 跳过）
  - 每条回复 → 写为平台 Discussion reply
- [ ] 2.5 实时同步：webhook/轮询
  - webhook 优先，无则轮询
  - 平台新回复 → sync 到本地 session
- [ ] 2.6 @ 引用解析：@raw-{key} / @raw-{key}#comment-{id} / @discussion-{id} / @discussion-{id}#{sub-id}
- [ ] 2.7 废弃 `freely chat --conversation` 入口
- [ ] 2.8 agent-id.env 讨论条目管理
  - 格式：`{project_root}=discuss={session_id}`
  - 新建讨论 → 插入条目
  - 归档成功 + 平台讨论关闭 → 移出条目
  - `manager_reconcile_agent_id_env` 适配：识别 discuss 条目（平台关闭→移除，未关闭→保留）
  - 计数函数不把 discuss 条目计入 worker 数

## 阶段三：讨论执行 skill

- [ ] 3.1 新建 `docs/system/workspace/skills/freely-discuss-execution/SKILL.md`
  - 借鉴 B1 发散→收敛→决策框架，独立重建
  - 使用者：讨论 agent
  - 返回结构化 brainstorm 格式内容
- [ ] 3.2 讨论 agent 配置：读 `.ai-auth` slot → 选模型效果

## 阶段四：讨论归档 skill

- [ ] 4.1 新建 `docs/system/workspace/skills/freely-discuss-archive-execution/SKILL.md`
  - 输入：本地 freely.db session id（不查网络）
  - 分析讨论，归并 @raw-{key} 引用
  - 适合已有 issue → `freely comment` 写评论
  - 不适合 → `freely feedback` 创建 raw issue（可多个）
  - 插入最后一条讨论消息，记录所有产出 ID（comment IDs + raw issue IDs）
  - 标记 session 消息 consumed/discard
  - 综合摘要写回 session
- [ ] 4.2 归档成功后：adapter 关闭平台 Discussions（GitHub + GitCode） + 本地 discussion 元数据 platform_state: closed

## 阶段五：评论门禁

- [ ] 5.1 评论 resolution 子评论格式（adopted/discarded + reason + resolved_by）
- [ ] 5.2 pr-create-guarded：全平台扫描，未 resolution 评论 → 拦截
- [ ] 5.3 wt-close Phase 0：同上
- [ ] 5.4 跨平台评论同步：SHA256 去重 + adapter 补建 + AI 语义合并差异

## 阶段六：旧 chat 拆除

- [ ] 6.1 `_write_chat_to_issue`：删除与新设计冲突路径
- [ ] 6.2 `chat-inbox.py`：删除 materialize 路径，保留查询
- [ ] 6.3 `freely_db_manager.py`：删除 `action=materialize`
- [ ] 6.4 `freely chat --new-issue`：废弃，指向 feedback
- [ ] 6.5 deploy-skills：部署新 skill 到 ~/.claude/skills/
- [ ] 6.6 scan 清理 chat 相关扫描
  - 删除 `get_chat_inbox()`（评论不写DB，讨论走JSONL）
  - 删除 `_merge_chat_inbox()`
  - 删除 Cat 1c "chat_signal"
  - 删除 Cat 2d "chat_unconsumed"
  - 删除 `chat_inbox` 变量和相关 timer

## 阶段七：边界文档变更

- [ ] 7.1 CONSTITUTION.md L9：`chat 输入` → `comment/discuss 输入`
- [ ] 7.2 CONSTITUTION.md L248：command 列表 `chat` → `comment / discuss`
- [ ] 7.3 LAWS.md L107：`chat/session evidence` → `comment/discuss session evidence`
- [ ] 7.4 PROJECT_INTENT.md L9：`chat 输入` → `comment/discuss 输入`
- [ ] 7.5 PROJECT_INTENT.md L48：semantic surface `chat` → `comment / discuss`
- [ ] 7.6 PROJECT_INTENT.md L60：`chat / status family` → `comment / discuss / status family`
- [ ] 7.7 PROJECT_INTENT.md L91-96：§Chat 输入与会话证据 → 重写为 §Comment/Discuss 输入
- [ ] 7.8 PROJECT_INTENT.md L204：submit semantics `chat` → `comment / discuss`
- [ ] 7.9 PROJECT_INTENT.md L215：`chat` → `comment / discuss`
- [ ] 7.10 AGENTS.md L25-26：开发流程图补充 comment/discuss
- [ ] 7.11 AGENTS.md L28：新增 freely comment / freely discuss 入口
- [ ] 7.12 AGENTS.md L141-143：入口新增 comment + discuss
- [ ] 7.13 AGENTS.md L150：阶段0 补充 comment
- [ ] 7.14 AGENTS.md L165-168：步骤表格新增 comment/discuss
- [ ] 7.15 AGENTS.md L214-217：chat → comment / discuss
