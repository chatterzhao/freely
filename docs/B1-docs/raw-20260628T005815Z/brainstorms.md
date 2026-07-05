---
b1_id: B1-20260628T005815Z
phase_state: completed
source_raw: raw-20260628T005815Z15Z
source_url: https://github.com/chatterzhao/freely/issues/3601
produced_candidate: C-20260628T005815Z-A
created_at: 2026-06-28
---

# B1_IBM: chat 重构 — 拆分为 comment 和 discuss

## Input
- 来源：GitHub issue #3601 `raw-20260628T005815Z15Z`
- 平台评论含完整检查清单和补充设计（comment #4823655300、#4823715542）
- 前置讨论在中进行了深入设计（评论/讨论分离、群聊模型、讨论执行 skill、导出 skill）

## Discovery（价值与时效性审视）

- **提出时间**：2026-06-28T00:58:15Z
- **当前阶段**：Freely 自举开发整合阶段。chat 是核心入口，直接影响开发体验和 AI 协作效率
- **相关性**：高。当前 chat 三种场景（--issue 评论、--new-issue 创建、--conversation 讨论）共享同一套本地 DB 路径，已导致入口混淆和延迟同步问题
- **是否被覆盖**：chat-conversation-extension（I-20260518T020406Z-A，completed）已添加 conversation_id 分组能力，但只解决了"分组"问题，未解决"去哪里"的问题。freely-comment candidate（C-20260518T020345Z-A，needs_research）探索了 comment 命令，但依赖 I-* phase_state redirect（现已过时）
- **时效判断**：当前仍有价值，且随着多平台、多人协作场景增长，问题会加剧

## 边界文档分析

### CONSTITUTION.md
- §1（产品身份）："chat 输入"作为 AI 发现源 — 语义不变，comment/discuss 仍然是输入
- §2（分支策略）：worktree 规范不受影响，comment 不写本地文件因此不涉及 worktree
- **需改**：无。comment/discuss 不违反任何硬性约束

### LAWS.md
- §1.1（发现源）："chat/session evidence" — 仍然成立
- §2B.1（产品架构讨论分类）：这里的"讨论"指开发过程中的治理讨论，与 `freely discuss` 功能不同，无需混淆
- **需改**：无。comment/discuss 符合现有法律框架

### PROJECT_INTENT.md
- 产品架构图中 "chat" 节点（L48、L60）→ 拆分为 "comment" 和 "discuss"
- "chat 输入" 语义保留，但实现路径变了
- **需改**：
  - L48：`chat` → `comment / discuss`
  - L60：`chat / status family` → `comment / discuss / status family`

### AGENTS.md（改动最大）
- L25-26：开发流程列出 feedback→wt-create→B1→B2→dev... 未体现 comment/discuss
- L28：只列出 `freely feedback`，缺 `freely comment` 和 `freely discuss`
- L141-143："入口是'或'的关系" — 缺少 comment/discuss 作为日常入口
- L150："阶段0" 只有 feedback
- L214-217：`chat` 在 CLI 家族中的定位
- **需改**（详见 §边界文档变更清单）：
  - 新增 `freely comment` 入口说明
  - 新增 `freely discuss` 入口说明
  - 更新开发流程图

## 依赖分析

### 讨论 agent 与 agent-table.toml / agent-id.env

讨论 agent 与其他 agent 的同与异：

| 维度 | manager / worker | discuss |
|------|-----------------|---------|
| agent-table.toml | 有，`pool` 控制并发 | 有，`pool=1`（1个 agent 实例） |
| agent-id.env 记录 | `{worktree_path}={role}={agent_id}` | `{project_root}=discuss={session_id}` |
| 工位 | 各自独立 worktree | 项目根工位（develop），所有讨论共用 |
| 并发 | pool 限制，空闲才委派 | 允许同时多个开放讨论，不限 |
| 移除时机 | wt-close 清掉工位 | 归档成功 → 平台讨论关闭 → 移出 agent-id.env |
| 未关闭 | reconcile 清理僵尸 | 未归档的讨论保留记录，不清理 |

关键差异：
- 其他 agent 的 agent-id.env value 是 `{role}_{num}`（如 `worker_03`），讨论的 value 是 `{session_id}`
- 其他 agent 一个工位一个 entry，讨论多个 session 可共存在同一 project_root 下
- 其他 agent 靠 pool 限制并发数，讨论不限制（允许同时多个开放讨论）
- 讨论以平台讨论关闭为准移出 agent-id.env，不是本地 wt-close

### agent-id.env 重构需求

当前 agent-id.env 解析假设 `{path}={role}={agent_id}` 三分段。讨论引入后：
- `{project_root}=discuss={session_id}` — session_id 格式不同于 agent_id（不是 `discuss_01` 而是讨论的时间戳 ID）
- `manager_reconcile_agent_id_env` 需识别 discuss 条目：平台讨论已关闭 → 移出；未关闭 → 保留
- `count_active_running_workers_for_manager_project` 类函数不应把 discuss 条目计入 worker 数

### 已有相关 work
| 已有 | 状态 | 关系 |
|------|------|------|
| chat-conversation-extension (I-20260518T020406Z-A) | completed | 本重构基于其 conversation_id 分组能力，但替换物化路径 |
| freely-comment (C-20260518T020345Z-A) | needs_research | 本设计的 comment 模块将取代该 candidate。其 phase_state redirect 已过时（I-* 不对外维护） |
| chat-inbox-sqlite (I-20260429T204000Z-A) | completed | 保留 chats 表查询能力，删除 materialize 路径 |
| #3599 (B1/B2 模板修复) | 独立 issue | 不依赖 |
| #3600 (wt-create assignee) | 独立 issue | 不依赖，但 wt-create 重构后 assignee 感知与 comment 的 ACP 通知互补 |

### 不受影响
- A2A 协议、ACP session 管理、agent-id.env 绑定
- pr-create-guarded / pr-merge-guarded 流程（新增评论门禁检查，不改变合并路径）
- scan（comment 不写本地，discuss session 由导出 skill 处理）

## Brainstorm

### Option A: 在现有 chat 上修补
- 给 `freely chat` 加更多 flag（`--platform-direct`、`--discussion-mode`）
- 保持本地 DB 为核心，评论也先写 DB 再同步
- 优势：改动最小
- 劣势：flag 爆炸、入口仍混淆、本地 DB 仍是单机瓶颈、新老行为通过 flag 切换容易出错

### Option B: 拆为 comment + discuss，评论直写平台
- `freely comment`：adapter 直写所有平台，本地不留，成功后 ACP 通知
- `freely discuss`：AI 群聊模型，本地 DB + 平台 Discussions 双向同步，@ 引用
- 讨论归档：`freely discuss --archive <session-id>` 命令 → 查 sessions 表找 discuss agent session_id → ACP session/prompt 发送固定提示词 `"根据 skill:freely-discuss-archive-execution 将 session {id} 归档"` → 讨论 agent 加载归档 skill 执行
- 讨论 agent：agent-table.toml 注册 `discuss_id = "discuss_01"`，独立 agent，pool=1。agent 详细设计文档等 UI 阶段再做
- 优势：职责清晰、各自走最优路径、多平台兼容（Gitee 跳过 Discussions）、导出纯手工避免 AI 自动创建 noise
- 劣势：改动大（~10 文件）、新 skill 需从零建、旧 chat 入口废弃需要迁移

### Option C: 全部走平台，废弃本地 DB
- chat 消息直写平台 Discussions，本地 DB 只做缓存
- 优势：彻底消除本地同步问题
- 劣势：讨论 session 较长，平台同步慢影响体验；Gitee 无 Discussions 导致该平台完全不可用；讨论过程失去隐私

### 收敛

| 维度 | Option A | Option B | Option C |
|------|----------|----------|----------|
| 评论实时性 | 差（等工位同步） | 优（直写平台） | 优 |
| 讨论体验 | 一般 | 优（本地+平台双写） | 差（慢） |
| Gitee 兼容 | ✅ | ✅（comment可用，discuss跳过） | ❌ 全平台不可用 |
| 改动量 | 小 | 大 | 大 |
| 多设备协作 | ❌ 单机DB瓶颈 | ✅ 平台同步 | ✅ |
| 扩展性 | 差 | 优（独立命令、独立agent） | 中 |

**收敛结论**：Option B 在实时性、多设备协作、Gitee 兼容、扩展性上均优于 A 和 C。改动量大是短期代价，但拆分后各模块独立演进，长期收益远超成本。

## Decision: Option B

1. **评论 = 原话**：一句话直达平台，没必要走本地 DB。adapter 封装多平台，简单高效。
2. **讨论 = AI 协作**：本地存储保证速度与隐私，平台同步保证可见与多人参与。@ 引用模型天然适合群聊渲染。
3. **出口独立**：手工触发导出 skill，人判断讨论够了才调用。避免 AI 自动创建不必要的 issue/comment。
4. **Gitee 兼容**：comment 走全部平台（issue comments 四个平台都有）。discuss 走有 Discussions 的平台，Gitee 跳过。
5. **新 agent + 新 skill**：讨论 agent 用独立 skill，不污染 B1（worker 用）。讨论执行 skill 借鉴 B1 思考框架独立重建。
6. **close issue 不自动 reopen**：comment 对已关闭 issue 直接拒绝，reopen 是独立路径。

## 边界文档变更清单

重构后 `freely chat` 不复存在，拆为 `freely comment` + `freely discuss`。以下在 B2 实现阶段一并修改，确保宪法/法律/意图与实际一致。

### CONSTITUTION.md
- [ ] L9：`chat 输入` → `comment/discuss 输入`（发现源语义不变，术语更新）
- [ ] L248：command/semantic surface 列表中 `chat` → `comment / discuss`

### LAWS.md
- [ ] L107：发现源 `chat/session evidence` → `comment/discuss session evidence`
- [ ] §2B.1、§10A 中的"讨论"是开发治理概念，非 `freely discuss` 功能，**不改**

### PROJECT_INTENT.md
- [ ] L9：`chat 输入` → `comment/discuss 输入`
- [ ] L48：semantic surface 列表中 `chat` → `comment / discuss`
- [ ] L60：`chat / status family` → `comment / discuss / status family`
- [ ] L91-96：§Chat 输入与会话证据 → 重写为 §Comment/Discuss 输入与会话证据。comment 是直写平台不产生 session evidence；discuss session 产生 session_refs 并可由导出 skill 收敛
- [ ] L204：submit/intervention 语义面 `chat` → `comment / discuss`
- [ ] L215：`chat` 不是 shell 的 peer → `comment / discuss` 不是 shell 的 peer

### AGENTS.md
- [ ] L25-26：开发流程图补充 comment/discuss 入口标注
- [ ] L28：新增两行
  ```
  评论: freely comment --issue raw-{key} "原话"          (向已有 raw issue 追加评论)
  讨论: freely discuss [--continue <id>] [--archive <id>]  (AI 群聊讨论)
  ```
- [ ] L141-143："入口是'或'的关系" → 新增 comment 和 discuss 入口
- [ ] L150：阶段0 补充 comment 说明
- [ ] L165-168：步骤表格新增 comment/discuss 行
- [ ] L214-217：`chat` 节点说明更新为 `comment / discuss`

## Candidate
- candidate_id: C-20260628T005815Z-A
- status: promoted
- milestone: M-20260628T005815Z-A
