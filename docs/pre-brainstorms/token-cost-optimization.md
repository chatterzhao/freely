# Freely Token 花费优化设计

> **目标：节约 token 花费。** 同样的任务、同样的功能正确性，消耗更少的 token。提高缓存命中率、精简 prompt 冗余、复用 session 上下文——这些都是手段，不是目的。缓存命中节省的是 token 费用（cache_read 打 90% 折扣），prompt 精简节省的是 token 用量，session 复用（L1）避免重复传输已有上下文。日志和测试不计入 AI token 消耗。

### 核心原则：按需披露

**Prompt 只放"这轮必须知道的事情"，其余都靠路径引用 + tool call 按需读取。**

```
Prompt 里放（必须）：                    Prompt 里不放（按需读取）：
  exit contract directive                scan JSON 全文 → 放路径，AI 自己读
  continuity focus（锚定当前 lane）       surface snapshot 文本摘要 → scan JSON 里有
  新 intake items（本轮新出现的）         fleet snapshot → AI 运行 live-status 获取
  context warning（仅超阈值时）           milestone 摘要 → scan JSON 里有链接
                                         progress 摘要 → scan JSON 里有链接
                                         宪法/法律全文 → 路径引用，AI tool call 读
```

**scan JSON 是路由索引，不是内容摘要。** scan JSON 的每个 source 带 `artifact_path`——AI 读到这个路径后自己去打开关联文件。不需要把关联文件的内容预先嵌入 prompt。

**对照当前 prompt，以下内容应改为按需披露：**
- `append_task_source_patrol_seed_if_needed` 嵌入的 surface snapshot 文本 → 改为只放 scan JSON 路径
- `append_fleet_supervision_if_needed` 嵌入的 fleet snapshot → 改为 AI 自己运行 live-status
- `append_checkpoint_governance_if_needed` 嵌入的 checkpoint 文本 → 仅当超阈值时精简提醒
- `start-lead-agent.sh` 里的初始读取目标列表 → 保留（这是导航地图，不是数据）

## 1. ACP 协议概念清单

Freely 通过 ACP 协议编排 AI。先列出协议提供的所有基础能力。

### 1.1 连接模型

```
ACP 连接 = stdio 或 Unix socket，承载 JSON-RPC 2.0 双向消息

一个 claude-agent-acp 进程：
  └─ 一个连接
       ├─ session A (Manager)
       ├─ session B (Worker 1)
       ├─ session C (Worker 2)
       └─ session D (Worker 3)

每个 session 独立状态，独立对话历史
```

### 1.2 协议原语

| 原语 | 方向 | 语义 | 对 Freely 的意义 |
|------|------|------|-----------------|
| `initialize` | C→A | 握手，交换 capabilities | 每个连接一次 |
| `session/new` | C→A | **创建全新空白 session** | Manager 首次启动、Worker 不需要父上下文时 |
| `session/fork` | C→A | **创建新 session，从父 session 复制历史**（也是 new！） | Worker 从 Manager 继承上下文 |
| `session/prompt` | C→A | **在活跃 session 上发送 prompt**，阻塞等 stopReason | 每个 turn 的输入。**多 turn 靠它，不靠 resume** |
| `session/resume` | C→A | **重新挂载**已有 session（断连后恢复） | 进程重启后找回 session |
| `session/close` | C→A | 关闭一个 session，不杀进程 | Worker 完成后的清理 |
| `session/update` | A→C | 流式通知（文本、tool_call、状态） | AI 响应内容流 |
| `session/cancel` | C→A | 取消正在进行的 turn | 超时或插话时中断 |

### 1.3 两个创建原语：session/new vs session/fork

```
session/new：
  创建空白新 session
  对话历史为空
  用于：Manager 冷启动、Worker 不需要 Manager 上下文时

session/fork(parent)：
  创建新 session（也是 new！有自己的 session ID）
  从父 session 复制对话历史作为起点
  之后独立演化，不回写父 session
  用于：Worker 需要 Manager 上下文时
```

### 1.4 关键时序：多 turn 靠 session/prompt，不靠 session/resume

```
session/prompt 调用：
  → 阻塞等待（最长 900s）
  → 返回 stopReason（end_turn / max_tokens / ...）
  → session 仍然活跃！没有关闭！

多 turn 工作流：
  Turn 1: session/new 或 session/fork → session/prompt → end_turn
  Turn 2: session/prompt（同一 session）→ end_turn   ← 上下文全在，L1 命中
  Turn 3: session/prompt（同一 session）→ end_turn   ← L1 命中
  Turn N: session/prompt → end_turn → session/close

session/resume 只在断连后使用：
  进程重启 → session/resume(sid) → 重新挂载 session
  → 然后继续 session/prompt

  不是每轮都 resume！同一连接内的多轮直接 session/prompt。

---

## 2. Freely 功能场景 → ACP 模式映射

### 2.1 场景总览

| # | 场景 | 描述 |
|---|------|------|
| S1 | Manager 冷启动 | 项目首次启动 daemon |
| S2 | Manager 继续 | daemon 运行中，下一轮 cycle |
| S3 | Manager 旋转 | context_compacted 或 resume 次数达上限 |
| S4 | Worker 首次委派 | Manager 决定委派任务给 Worker |
| S5 | Worker 自己继续 | Worker 一轮没做完，需要下一轮 |
| S6 | Worker 被重新委派 | Manager 审视后修改任务方向 |
| S7 | Worker 完成 | Worker 任务完成，退出合同 worker_done |
| S8 | Worker 被阻塞 | Worker 遇到无法自行解决的障碍 |
| S9 | 多 Worker 并行 | 10 个 Worker 同时在跑 |
| S10 | 进程崩溃恢复 | bridge / claude-agent-acp 崩溃后重启 |

### 2.2 各场景的 ACP 模式

**S1：Manager 冷启动**

```
acp-bridge.py start → claude-agent-acp 进程启动
  → session/new (cwd=develop)
  → session/set_mode bypassPermissions
  → session/prompt (完整 prompt: T0 前缀 + patrol seed + exit contract directive)
  → 阻塞等待 → stopReason=end_turn
  → 检测 exit contract → resume_manager / delegate_workers / stop_ai
  → 不关 session！（bridge 保持连接）
  
缓存：L1 ❌ (首次)，L2: T0 前缀可命中（如果之前其他 session 缓存过）
```

**S2：Manager 继续（当前已正确 ✅）**

```
同一个 bridge，同一个 session：
  → session/prompt (增量 prompt: continuity focus + 新 intake + exit contract directive)
  → 阻塞等待 → stopReason=end_turn
  → 检测 exit contract
  
缓存：L1 ✅（session 上下文全在内存中）
问题：当前 prompt 发的是全量（~5000 tokens），不是增量
```

**S3：Manager 旋转**

```
检测到 context_compacted / resume_streak ≥ 24：
  → 写 session-handoff.txt（旋转原因 + 上轮日志摘录）
  → 旧 session: session/close（释放资源）
  → 新 session: session/new
  → session/prompt (完整 prompt + handoff 内容追加)

缓存：L1 ❌ (新 session)，L2: T0 前缀命中（同进程内之前的 session 缓存过）
```

**S4：Worker 首次委派（当前错误 ❌ → 应改为）**

```
当前：--agent claude-agent-acp → SubprocessTransport → session/new → 一次 prompt → 进程被杀

应改为：
  Manager bridge 内 → session/fork(Manager session)
  → Worker session 获得 Manager 的对话历史副本
  → session/prompt (Manager 写的 worker prompt)
  → 阻塞等待 → stopReason=end_turn
  → 检测 worker exit contract
  → 不关 session！（等 Manager 下轮审查）

缓存：L1 ❌ (fork 是新 session，但上下文从 Manager 继承)
```

**S5：Worker 自己继续（当前不支持 ❌ → 应改为）**

```
当前：SubprocessTransport.close() 杀了进程 → 必须重新 session/new → L1 ❌

应改为：
  同一个 Worker session（没关！）→ session/prompt (下一轮 prompt)
  → 阻塞等待 → stopReason=end_turn
  → 检测 exit contract
  
缓存：L1 ✅（session 上下文全在，Worker 自己的多轮对话都在）
```

**S6：Worker 被重新委派**

```
Manager 写入新的 worker prompt 文件
  → Worker session/prompt (新 prompt，可能包含修正后的指令)
  → 阻塞等待 → stopReason=end_turn
  → 检测 exit contract

是否要 session/close 旧 Worker session 再 fork 新的？看情况：
  - 任务方向大改 → session/close 旧 → session/fork(Manager) 新
  - 增量修正 → 同一个 session/prompt（保留历史上下文）← L1 ✅
```

**S7：Worker 完成 / S8：被阻塞**

```
检测到 exit_contract = worker_done 或 worker_blocked：
  → session/close (释放 ACP 进程内的 session 资源)
  → bridge 继续运行（为其他 Worker 服务）

当前：SubprocessTransport.close() → 杀 claude-agent-acp 子进程 → 太粗暴
```

**S9：多 Worker 并行**

```
所有 Worker session 在同一个 claude-agent-acp 进程内：

  Manager bridge → claude-agent-acp
    ├─ Manager session (长期活跃)
    ├─ Worker 1 session (fork from Mgr, 活跃)
    ├─ Worker 2 session (fork from Mgr, 活跃)
    ├─ Worker 3 session (fork from Mgr, 等待 Manager 审查)
    ├─ Worker 4 session (已 close，Worker 4 完成)
    └─ Worker 5-10 (尚未创建，排队等待委派)

关键：错峰创建 session，不并发 session/new 风暴
  - Manager 每轮只创建 1-2 个新 Worker session
  - 已完成 Worker 及时 session/close
  - 稳态下 3-5 个活跃 session，总量 < 11

当前：10 个独立 claude-agent-acp 子进程，10× 内存，各自为战
```

**S10：进程崩溃恢复**

```
claude-agent-acp 崩溃：
  → bridge 检测到 stdout 关闭 → _restart_server
  → 新 claude-agent-acp 进程启动
  → 所有 session 丢失（进程内存中的状态没了）
  
恢复：
  → Manager: 从 session-store 找回 session ID
    → session/resume → 如果 session 在 ACP 进程中丢失 → 降级 session/new
  → Worker: 同理尝试 resume，失败则 Manager 重新 fork
  
缓解：
  - session-store 持久化所有 session ID
  - 崩溃后错峰恢复（先 Manager，再逐个 Worker）
  - 不要同时恢复 10 个 session
```

### 2.3 组合模式矩阵

```
                    创建新 session        继续对话         恢复连接        清理
                    session/new  session/fork  session/prompt  session/resume  session/close
S1 Manager 冷启动      ✅ (空白)                           ✅ (首轮)       
S2 Manager 继续                                        ✅ (每轮)       
S3 Manager 旋转        ✅ (空白新)                         ✅ (首轮)                       ✅ (关旧)
S4 Worker 首次委派            ✅ (fork Mgr)              ✅ (首轮)       
S5 Worker 自己继续                                    ✅ (下轮)       
S6 Worker 重新委派                                    ✅ (修正后)       
S7 Worker 完成                                                                          ✅ (清理)
S8 Worker 阻塞                                                                           ✅ (清理)
S9 多 Worker 并行      错峰创建   错峰 fork    各自 prompt                  各自 close
S10 崩溃恢复          降级 fallback                         ✅ (重连)       
```

---

## 3. 当前实现 vs 正确实现

### 3.1 逐项对比

| 场景 | 当前实现 | 问题 | 正确实现 |
|------|---------|------|---------|
| **S2 Manager 继续** | bridge socket → session/resume → session/prompt | prompt 发全量不精简 | 增量 prompt（层面 C） |
| **S4 Worker 委派** | `--agent` SubprocessTransport → session/new → prompt → **进程被杀** | ① L1 永远冷启动 ② 独立进程浪费资源 ③ session 无法复用 | Manager bridge 内 session/fork → prompt → session 保持 |
| **S5 Worker 继续** | **不支持**。Worker 进程已死，必须重新 launch | 多 turn 工作不可能 | 同一 session 再发 session/prompt → L1 ✅ |
| **S7 Worker 完成** | SubprocessTransport.close() 杀整个进程 | 杀进程 ≠ 关 session | session/close（轻量清理） |
| **S9 多 Worker** | 10 个独立 `claude-agent-acp` 进程 | 10× 内存，资源浪费 | 一个进程内 10 个 session，1× 内存 |
| **S10 崩溃恢复** | 依赖 session-store try resume | Manager 恢复OK，Worker 进程全死了 | 同一进程内所有 session 受影响，需逐个恢复 |

### 3.2 需要重构的点

**重构 1：`run-acp-prompt.py` 改 one-shot 为 loop**

当前 one-shot 模式：
```python
session/prompt → 等响应 → 退出
```

改为 loop 模式（新增 `--loop` 参数）：
```python
# 首次
session/new 或 session/resume
session/prompt → 等响应 → stopReason

# loop 模式：不退出，等待指令
while True:
    read_next_prompt()  # 从 stdin / 文件 / socket 读下一轮 prompt
    if exit_signal:
        session/close
        break
    session/prompt(next_prompt) → 等响应 → stopReason
```

**重构 2：Worker launch 改用 bridge socket + session/fork**

从：
```bash
python3 run-acp-prompt.py --agent claude-agent-acp --launch-kind fork ...
```

到：
```bash
python3 run-acp-prompt.py --bridge-socket "$manager_bridge" --launch-kind fork --loop ...
```

Worker session 由 Manager bridge 内的 `claude-agent-acp` 进程托管，fork 自 Manager session。

**重构 3：多 Worker 共享一个 bridge**

当前每个 Worker 独立 subprocess → 自己的 `claude-agent-acp`。

正确做法：所有 Worker session 在 Manager 的 bridge 进程内。一个 `claude-agent-acp` 承载 1+10 个 session。

**不需要重构的：**
- `acp-bridge.py`：已经正确，handle_client 本身就是 while loop，支持多请求、多 session
- Manager 的 session/resume 逻辑：已经正确

### 3.3 重构后各层面的缓存效果

| 场景 | 重构前 | 重构后 |
|------|--------|--------|
| **S1** Manager 冷启动 | L1 ❌ L2 △ | 不变 |
| **S2** Manager 继续 | L1 ✅（prompt 冗余 5000 tokens） | L1 ✅（prompt 精简到 ~700 tokens） |
| **S4** Worker 首次 | L1 ❌ L2 ❌（独立进程，全冷） | L1 ❌ L2 ✅（共享进程，fork 继承上下文） |
| **S5** Worker 继续 | L1 ❌（必须重建 session/new） | **L1 ✅**（同一 session 再 prompt） |
| **S7** Worker 完成 | 杀进程 | session/close（轻量） |
| **S9** 多 Worker 并行 | N× 进程，N× 内存 | 1× 进程，1× 内存 |
| **跨角色** Manager→Worker | 无缓存共享 | L2 ✅（同进程、同 bridge） |

最大收益：**S5 Worker 继续从不可能变为 L1 命中。** 这是当前架构最大的缓存浪费——Worker 的每个 turn 都是冷启动。

---

## 4. 可观测性基础设施

**约束：任何 AI 会消费的路径上不得新增非业务内容。** 缓存度量必须写入 AI 不读的通道。

### 4.1 AI 消费路径审查

```
AI 会读到的（禁止写入缓存度量）：
  cycle log 的尾部 80 行           ← fresh_with_handoff 时注入 prompt
  session-handoff.txt              ← 包含 cycle log 摘录
  manager-continuity-*.md          ← AI 自己写的，但下轮 resume 焦点时引用
  scan JSON                        ← AI 的 patrol 入口
  worker prompt 文件                ← Worker 的任务输入

AI 不会读到的（可以写入缓存度量）：
  stderr                           ← run-acp-prompt.py 的 stderr，写到 daemon 日志
  runtime-events.log               ← 运维日志，AI 从不直接读
  session-store (freely.db)        ← SQLite，AI 通过 CLI 查询
  测试脚本输出                      ← 不在 Freely 运行时内
```

### 4.2 缓存度量写入位置

**`run-acp-prompt.py` → stderr（不进 cycle log）：**
```
[CACHE] session_id=xxx launch_kind=fork cache_read=2500 cache_create=700
```
stderr 重定向到 daemon-launch.log 和 supervisor 的 recovery log，不被 AI 消费。

**`freely` runtime → runtime-events.log（运维日志）：**
```
event=cache_metrics session_id=xxx role=worker launch_kind=fork 
  prompt_bytes=12345 cache_read=2500 cache_create=700
  acp_process_count=3 active_session_count=5
```
`runtime-events.log` 只被运维脚本和测试脚本读取，AI 从不直接消费。

**测试脚本 → 捕获 stderr + 查询 session-store（不进入 Freely 运行时）：**
```bash
# 捕获 stderr 中的 [CACHE] 行
stderr_output=$(run-acp-prompt.py ... 2>&1 >/dev/null)
cache_read=$(echo "$stderr_output" | grep '\[CACHE\]' | ...)

# 查询 session-store
python3 session-store.py get-active --db freely.db --project <path> --role worker
```

### 4.3 基线采集脚本

**不在 AI 上下文中运行。** 纯运维命令，读取 stderr 和 SQLite。

```bash
./bin/freely token-cost-baseline --project <path> --duration 30m --output baseline-before.json
```

# 输出 JSON：
{
  "period": "30m",
  "manager_cycles": 12,
  "cycles": [
    {"seq": 1, "launch_kind": "fresh", "rotation_reason": "acp_first_launch",
     "prompt_bytes": 4850, "context_ratio_after": 0.12},
    {"seq": 2, "launch_kind": "resume", "rotation_reason": "acp_session_persists",
     "prompt_bytes": 5020, "context_ratio_after": 0.18},
    ...
  ],
  "worker_launches": [
    {"prompt_file": "...", "launch_mode": "subprocess",
     "turn_count": 1, "exit_kind": "worker_done"}
  ],
  "rotations": [
    {"trigger": "context_compacted", "after_cycles": 15}
  ],
  "acp_processes_peak": 8
}
```

---

## 5. Freely 能力面 vs 被开发项目面：提示词分层

### 5.0 当前混淆的根源

Freely 用自己开发自己（吃狗粮），导致一个仓库里混了两类内容：

```
当前 Freely 仓库内的文档：

Freely 产品能力（所有项目通用）：         Freely 开发项目治理（仅本项目）：
  runtime/freely                         CONSTITUTION.md
  start-lead-agent.sh                    LAWS.md
  agents/ (lead/manager/worker)          AGENTS.md（混了两类内容）
  skills/                                PROJECT_INTENT.md
  acp-bridge.py                          milestones.md
  session-store.py                       docs/issues/
  tools.md                               docs/progress/
  IBM Framework                          docs/pre-brainstorms/
```

**设计必须分开。** 如果不分开，用户用 Freely 开发其他项目时，Freely 的宪法和法律会被当成用户项目的规则塞进 prompt，或者反过来——Freely 能力面没有正确进入系统提示词，导致换了项目就失效。

### 5.1 分层定义

```
┌─ 层面 0：Freely 产品能力（系统提示词）────────────┐
│                                                    │
│ 来源：Freely 安装目录（docs/system/workspace/）     │
│ 范围：所有项目通用                                  │
│ 稳定性：跨版本稳定（Freely 升级时更新）              │
│ 缓存：T0 稳定前缀，所有 session 共享                │
│                                                    │
│ 内容：                                              │
│   - 角色模型：Manager/Worker 职责、边界             │
│   - 读取约定：skill 语义、分页策略                  │
│   - ACP session 模型：new/resume/fork/close 语义    │
│   - 退出合同规范：5 种 EXIT_KIND 格式               │
│   - IBM Framework 路由：B1_IBM vs B2_IBM 判定       │
│   - Agent/Skill/Tool 索引结构                       │
│   - 执行规则：路由、工具选择、委派流程              │
│                                                    │
│   ≠ CONSTITUTION.md（那是项目自己的）               │
│   ≠ LAWS.md（那是项目自己的）                       │
│   ≠ PROJECT_INTENT.md（那是项目自己的）             │
├────────────────────────────────────────────────────┤
│                                                    │
│ 层面 1：项目入口文档（项目级，由 freely init 生成） │
│                                                    │
│ 来源：项目根目录                                    │
│ 范围：当前项目                                      │
│ 稳定性：项目初始化后基本不变                        │
│ 缓存：T1 慢变前缀                                  │
│                                                    │
│ 内容：                                              │
│   - AGENTS.md（项目治理入口）                       │
│   - CONSTITUTION.md（项目硬性约束）                 │
│   - LAWS.md（项目操作规则）                         │
│   - PROJECT_INTENT.md（产品方向）                   │
│   - milestones.md（里程碑计划）                     │
│                                                    │
│ 进入 Prompt 的方式：路径引用 + tool call 读取        │
│   ≠ 嵌入 prompt 文本（不同项目的文档不同）           │
├────────────────────────────────────────────────────┤
│                                                    │
│ 层面 2：运行时状态（动态，项目特定）                │
│                                                    │
│ 来源：.freely/run/ + git status + tool call         │
│ 范围：当前项目的当前时刻                            │
│ 稳定性：T2-T4，逐层变快                            │
│                                                    │
│ 内容：                                              │
│   - T2: milestone/progress/pre-brainstorm 摘要      │
│   - T3: worktree 状态、checkpoint、fleet snapshot   │
│   - T4: continuity focus、exit contract、intake     │
└────────────────────────────────────────────────────┘
```

### 5.2 治理文档的真相：宪法/法律已被"消化"为 workspace 能力

**CONSTITUTION.md 和 LAWS.md 是 Freely 的开发治理文档，不会打包进 Freely 产品。** 它们的内容已经消化为 `docs/system/workspace/` 下的具体能力产物：

```
CONSTITUTION.md / LAWS.md 中的规则         消化到的 workspace 能力
─────────────────────────────────────────────────────────────────
Git 治理（分支/worktree/merge）        → workspace/hooks/*.sh
Gate 检查（pre-push/pre-merge）        → workspace/hooks/*.sh
IBM Framework (B1_IBM/B2_IBM)          → workspace/ibm-framework.md ✅ 已就位
三循环方法论                           → workspace/three-loop-capability-lifecycle.md ✅ 已就位
Agent 角色（Manager/Worker）           → workspace/agents/manager-agent.md, worker-agent.md
Skill 定义                             → workspace/skills/*/SKILL.md
ACP session 模型                       → workspace/acp-session-architecture.md
退出合同规范                           → workspace/agents/ (agent 角色定义的一部分)
工具选择规则                           → workspace/tools.md
```

**这些 workspace/ 下的文件才是 Freely 的交付物。** 用户安装 Freely 后，这些是 Freely 工具能力的一部分。用户不升级 Freely，它们就不变——这就是 T0 系统提示词的权威来源。

**用户的宪法/法律是用户自己项目的治理文档。** 用户在项目宪法里写的是"使用 Freely Git Governance"、"遵循 Freely IBM Framework"——**引用** Freely 的能力，不是继承 Freely 的宪法。

### 5.3 对提示词组织的影响

```
T0 系统提示词（Freely 安装包的一部分，用户不升级不变）：
  来源：docs/system/workspace/
  
  workspace/agents/          → agent 角色、职责、边界（Manager/Worker 的灵魂）
  workspace/skills/README    → skill 索引
  workspace/tools.md         → 工具选择规则
  workspace/ibm-framework.md → B1_IBM vs B2_IBM 路由
  workspace/acp-session-architecture.md → session 模型
  workspace/hooks/           → git governance 规则（gate 检查逻辑）

T1 项目文档（用户项目根目录，每个项目不同）：
  来源：<user-project>/
  
  AGENTS.md              → 项目治理入口（freely init 生成）
  docs/CONSTITUTION.md   → 用户项目的宪法（"使用 Freely XXX"）
  docs/LAWS.md           → 用户项目的法律
  docs/PROJECT_INTENT.md → 用户项目的产品方向

  进入 prompt 的方式：路径引用，不嵌入内容。
  这些文档一般不变，放在 T0 系统提示词尾部作为路径引用列表。
```

### 5.4 IBM Framework 检查

`docs/system/workspace/ibm-framework.md` 已正确就位。AGENTS.md 第 72 行引用它作为权威来源。`start-lead-agent.sh` 的执行要求中引用了 B1_IBM/B2_IBM 路由。

**但有一个风险：** workspace/ibm-framework.md 需要和 CONSTITUTION.md ch11（三循环方法论）保持语义一致。当前两者独立维护——宪法改了，workspace 文档可能没同步。需要一个"宪法→workspace 消化检查"来保证 workspace 能力确实是宪法原则的最新投影。

---

### 5.5 `freely init` 应该生成什么

```bash
freely init --project /path/to/user-project
```

**生成文件：**

1. `AGENTS.md`（最小入口）：
```markdown
# Agent 上下文入口

## 权威来源
1. docs/CONSTITUTION.md（硬性约束）
2. docs/LAWS.md（操作规则）
3. docs/PROJECT_INTENT.md（产品方向）
4. AGENTS.md（本文件）

## 当前项目阶段
<用户填写>

## 会话启动
- 分支/Worktree 检查：先执行 cd <project>，再使用 freely wt-create 创建 feature worktree
- Hook 检查：确认 git config --get core.hooksPath 返回 .githooks
- 测试前判 lane：feature/* → feature-local，test-pre-merge-* → premerge-integration
```

2. `.freely/config.env`（项目配置）：
```
PROJECT_ROOT=/path/to/user-project
INTENT_FILE=/path/to/docs/PROJECT_INTENT.md
CONSTITUTION_FILE=/path/to/docs/CONSTITUTION.md
AI_TOOL=cc-ds-flash-auto
...
```

3. 模板文件（如果不存在）：
   - `docs/CONSTITUTION.md`（空模板，用户填写）
   - `docs/LAWS.md`（空模板，用户填写）
   - `docs/PROJECT_INTENT.md`（空模板，用户填写）

### 5.4 T0 系统提示词的来源

```
Freely 安装后的系统提示词来源：

安装目录（如 ~/.freely/ 或 /usr/local/share/freely/）：
  system-prompt/
    ├── 00-role-model.md          ← Manager/Worker 角色定义
    ├── 01-reading-conventions.md ← skill 语义、分页策略
    ├── 02-acp-session-model.md   ← session/new/resume/fork/close
    ├── 03-exit-contracts.md      ← 退出合同规范
    ├── 04-ibm-framework.md       ← B1_IBM vs B2_IBM 路由
    ├── 05-skill-index.md         ← 可用 skill 的索引
    └── 06-execution-rules.md     ← 路由、工具选择、委派流程

运行时：
  build_prompt() 组装 prompt 时：
    1. cat 安装目录/system-prompt/*.md → T0 前缀
    2. 追加项目 AGENTS.md 路径引用 → T1
    3. 追加运行时状态 → T2-T4
```

### 5.5 用 Freely 开发其他项目的完整 prompt 结构

```
用户项目 /home/user/my-app/ 的 Manager prompt：

┌─ T0: Freely 系统提示词（~2500 tokens）──────────────┐
│ 来自 Freely 安装目录，所有项目完全相同                 │
│                                                       │
│ §1 角色模型                                           │
│   你是 Freely Manager，运行在 develop 分支上           │
│   你的职责是 patrol → 判断 → 委派 → 收口              │
│   你不能在 develop 上直接修改版本管理产物              │
│                                                       │
│ §2 读取约定                                           │
│   skill:<name> 表示打开对应的 SKILL.md                │
│   大型文档用分段读取，不要整文件硬读                   │
│                                                       │
│ §3 ACP Session 模型                                   │
│   session/new → session/resume (L1 命中)              │
│   session/fork → Worker 从 Manager 继承上下文          │
│   session/close → 完成清理                             │
│                                                       │
│ §4 退出合同规范                                       │
│   Manager: stop_ai | resume_manager | delegate_workers │
│   Worker:  worker_done | worker_blocked | handoff_needed│
│                                                       │
│ §5 IBM Framework                                      │
│   B1_IBM: Input → Brainstorm → Milestone              │
│   B2_IBM: Input → Brainstorm → Map (epic/story/tasks) │
│                                                       │
│ §6 执行规则                                           │
│   路由规则、工具选择优先级、委派流程                   │
├──────────────────────────────────────────────────────┤
│                                                       │
│ T1: 项目文档引用（~200 tokens）                        │
│   - 项目治理入口：/home/user/my-app/AGENTS.md          │
│   - 宪法：/home/user/my-app/docs/CONSTITUTION.md       │
│   - 法律：/home/user/my-app/docs/LAWS.md               │
│   - 项目意图：/home/user/my-app/docs/PROJECT_INTENT.md │
│   运行上下文：PROJECT_ROOT=..., AI_TOOL=...            │
│                                                       │
│ T2-T4: 运行时状态（动态，与本项目无关）                 │
│   - worktree 状态、checkpoint                          │
│   - scan JSON 路径引用                                 │
│   - continuity focus、exit contract directive          │
└──────────────────────────────────────────────────────┘
```

### 5.6 对自己狗粮的特殊处理

Freely 开发 Freely 时，T0 系统提示词和项目文档（AGENTS.md 等）来自同一个仓库。这是合理的——**设计上分开，当前仓库内共存**。

```
Freely 开发 Freely 时的实际情况：

T0 系统提示词来源：
  docs/system/workspace/ 下的 agent/skill/runtime 定义
  → 这些是 Freely 产品能力，也是当前仓库的一部分

项目文档来源：
  docs/CONSTITUTION.md, docs/LAWS.md, AGENTS.md
  → 这些是 Freely 开发 Freely 的项目治理

冗余不可避免（同一个仓库），但设计接口是清晰的：
  - T0 = workspace/ 下的能力定义（跨项目复用）
  - T1 = 项目根目录文档（项目特定）
  - 用户用 Freely 开发其他项目时，T0 一样，T1 是用户自己的文档
```

---

## 6. Session ID 管理：SQLite + CLI 模式的优劣

### 6.1 当前实现

ACP 模式下，session ID 通过 `session-store.py` 管理，底层是 `.freely/freely.db` SQLite 数据库。

```
每次 session 操作 = 一个 Python 子进程：

  select_launch_kind()
    → python3 session-store.py get-active --db ... --project ... --role manager
    → 子进程启动 → 连接 SQLite → 查询 → 返回结果 → 子进程退出

  monitor-ai-acp.sh
    → python3 session-store.py upsert --db ... --session-id ... 
    → python3 session-store.py complete --db ... --session-id ... --status completed
```

### 6.2 SQLite 的优势

**WAL 模式（Write-Ahead Logging）保证了崩溃安全。** 写入先记日志再合并，进程崩溃不会损坏数据库。

**结构化查询能力：**
```
-- 找 Manager 的活跃 session（决定 resume vs fresh）
SELECT session_id FROM sessions 
WHERE project = ? AND role = 'manager' AND status = 'active' 
ORDER BY updated_at DESC LIMIT 1

-- 找某个 session 的 fork 子节点（Worker session 层级）
SELECT session_id FROM sessions WHERE parent_session_id = ?

-- 统计当前活跃 session 数（资源监控）
SELECT COUNT(*) FROM sessions WHERE project = ? AND status = 'active'

-- 找所有失败 session（诊断）
SELECT session_id, error_reason FROM sessions WHERE status = 'failed'
```

**单文件，无服务进程。** 不与 claude-agent-acp 耦合，crash 后独立存活。

**跨语言可访问。** Python（session-store.py）、bash（sqlite3 CLI）、Rust 都能直接读。

### 6.3 当前 CLI 模式的效率

```
每个查询启动一个 Python 子进程：
  - 进程启动开销：~50-100ms
  - SQLite 连接 + 查询：~1-5ms
  - 总开销：~50-105ms/查询

查询频率：
  - select_launch_kind：每 cycle 1-2 次（cycle 间隔 1-5 分钟）
  - upsert：每 cycle 1 次
  - complete：每 cycle 1 次
  - 总计：每 cycle 3-4 次子进程调用

开销占比：~200-400ms / (60-300s cycle) ≈ 0.1-0.7%
```

**结论：CLI 子进程模式对当前频率完全够用。** 开销可忽略。

但如果未来需要高频查询（如每次 Worker turn 都查 session 状态、实时监控活跃 session 数），子进程开销会累积。那时可以考虑：

### 6.4 优化方向：acp-bridge.py 内化管理

`acp-bridge.py` 已经是持久 Python 进程——它可以持有 SQLite 连接，避免每次查询都重新连接。

```
改进方案（可选，非紧急）：

acp-bridge.py 新增内部方法：
  def session_get_active(self, role):
      """直接从持久连接查询，零子进程开销"""
  
  def session_upsert(self, session_id, role, launch_kind, ...):
      """写入不离开进程"""

暴露方式（二选一）：
  A) bridge 内部查询 + 通过 socket 返回结果给 bash runtime
  B) bridge 直接写 session-state.env，bash runtime 只读 env 文件
```

**但这不是 P0。** 当前 CLI 模式的开销在 cycle 级别可忽略。这个优化的真正价值是：当多 Worker 并发时，bridge 内化管理可以原子地追踪 session 层级（fork 树），避免并发 CLI 调用的竞态。

### 6.5 是否要暴露为 API 给 AI 使用

```
当前 AI 对 session 的感知：
  - 知道自己有 session（prompt 里的 CLAUDE_SESSION_ID_CURRENT）
  - 知道 fork 的父 session（SESSION_PARENT_ID）
  - 不知道 fork 的子节点（自己的 Worker fork 了哪些 session）
  - 不知道历史 session（之前的 cycle 用了哪些 session）

AI 可能需要的能力：
  - 知道自己的 Worker 在哪些 session 里跑 → list-children
  - 知道上次崩溃前的 session → list (filter by status=failed)
  - 诊断 session 层级 → 可视化 fork 树

暴露方式：
  ./bin/freely session list --project <path>
  ./bin/freely session children --project <path> --session-id <id>
  ./bin/freely session tree --project <path>   ← 打印 fork 树
```

**建议：暴露为 `freely` CLI 子命令。** AI 通过 tool call 运行命令获取 session 信息。不需要额外 API 服务——CLI 已经够用。优先级 P2（功能完整性的 nice-to-have，不影响缓存核心指标）。

### 5.1 当前有哪些进度信息来源

| 来源 | 存储位置 | 写入者 | 崩溃后可靠？ | 内容 |
|------|---------|--------|------------|------|
| **milestones.md** | git 版本管理 | AI + 人类 | ✅ 可靠 | 所有 milestone 的 candidate/committed/completed 队列 |
| **progress/*.md** | git 版本管理 | AI | ✅ 可靠 | 每个 issue 的 phase_state、runtime_state、session_refs |
| **issues/*/issue.md** | git 版本管理 | AI + 人类 | ✅ 可靠 | issue 的完整内容和状态 |
| **task-source-scan JSON** | `.freely/run/` | Runtime 脚本 | ⚠️ 可能过时 | 扫描以上所有来源的结构化摘要 |
| **manager-continuity-*.md** | `.freely/run/` | AI Manager | ✅ 可靠 | Manager 的 patrol 结论、queue、frozen、delegation |
| **exit-contract.env** | `.freely/run/` | AI | ⚠️ 可能缺失 | 本轮退出合同（crash 前来不及写） |
| **session-state.env** | `.freely/run/` | Runtime | ✅ 可靠（原子写） | session ID、resume_streak、context_ratio 等 |
| **session-store (SQLite)** | `.freely/freely.db` | Runtime | ✅ 可靠（WAL 模式） | 所有 session 的 ID、状态、父子关系 |
| **AI 对话历史 (JSONL)** | 工具目录 | AI 工具 | ✅ 可靠 | 完整的对话历史 |
| **AI 会话内存** | claude-agent-acp 进程 | ACP | ❌ 进程死即丢失 | session 上下文 |

### 5.2 崩溃恢复的真相

**session 上下文是最可靠的恢复机制，不是磁盘文件。**

```
崩溃后恢复优先级：
  1. session/resume → AI 从 JSONL + ACP 内存恢复对话历史
     → AI "记得" 之前的所有 patrol 结论、委派决定、当前 lane
     → 这是最完整的恢复，零信息丢失
  
  2. session-state.env → 恢复 session ID、counters
     → 告诉 runtime 用哪个 session 去 resume
  
  3. exit-contract.env → 如果存在，runtime 知道上轮的退出合同
     → 如果不存在（crash 前来不及写），runtime 照常继续
  
  4. manager-continuity-*.md → 如果 session 丢失（ACP 进程也崩了）
     → 新 session 的 AI 可以读取 continuity 文件来恢复上下文
     → 这是 BACKUP，不是 primary
```

**关键洞察：continuity 文件和 scan JSON 都不是恢复的主路径。** 主路径是 session/resume——AI 的对话记忆。只有在 ACP 进程崩溃（session 内存丢失）时，磁盘文件才作为 fallback。

### 5.3 什么信息应该进 Prompt、什么靠 Tool Call

基于"session 上下文是 primary"的原则，按稳定性分层：

```
Prompt 必须有的（T4，每轮增量）：
  exit contract directive  — AI 必须知道要写退出合同
  continuity focus         — 锚定当前 lane，告诉 AI "这轮重点做什么"
  新 intake items          — 人类插话、delegated continuation（本轮新出现的）
  context warning          — 仅当 context_ratio 超阈值时才提醒

Prompt 可以有但放 T3（条件触发）：
  checkpoint governance    — 仅当 dirty ≥ 40 或 checkpoint required
  fleet supervision        — 仅当 fleet 状态变化（worktree 增删）

Tool Call 读取（不占 prompt）：
  task-source-scan JSON    — AI 需要 patrol 时自己读
  milestones.md            — AI 需要看具体 milestone 时自己读
  progress/*.md            — AI 需要看具体 issue 进度时自己读
  issues/*/issue.md        — AI 需要看 issue 详情时自己读
  live-status              — AI 运行命令获取当前态
  fleet-status             — AI 运行命令获取 fleet 快照

可废弃（session 上下文已覆盖）：
  surface snapshots 文本   — scan JSON 中有同样内容，不需要嵌入 prompt
  continuity 全文          — session 历史中已有，除非 session 丢失
  handoff 中的 fleet 快照  — 仅在 fresh_with_handoff 时需要（session 丢了才用）
```

### 5.4 Continuity 文件还需要吗？

**需要，但不是给同一个 session 用的。**

```
Continuity 文件的真正作用：
  1. 跨 session 交接 — fresh_with_handoff 时，新 session 的 AI 读取 continuity
     → 了解上一个 session 的 patrol 结论和 queue 状态
  
  2. 崩溃 fallback — ACP 进程崩了，session 内存丢失
     → 新 session/resume 失败，降级 session/new
     → AI 读取 continuity 恢复上下文
  
  3. Runtime 消费 — 提取 worker prompt 路径、queue 状态
     → manager_runtime_launch_workers_from_latest_handoff 解析 continuity
  
  4. 人类可读 — 项目状态的快照文档

不是给同一个 session 的下一轮用的。
同一个 session 内，AI 靠 session/resume 的记忆，不需要 continuity。
```

### 5.5 Scan 结果怎么用

```
推荐模式：scan JSON 做索引 → tool call 做深度读取

Prompt 中只放：
  machine_readable_scan_json: <path>      ← 路径引用（~50 bytes）

AI 工作流：
  1. 读 scan JSON → 了解全局（哪些 issue 需要关注、哪些 candidate 卡住了）
  2. 选最高优先级的 source → tool call 读具体文件
     - 需要看 issue 详情 → 读 issues/I-xxx/issue.md
     - 需要看进度 → 读 progress/xxx/p-xxx.md
     - 需要看候选 → 读 pre-brainstorms/xxx/candidates.md
  3. 定点核对后形成判断 → 写 continuity 和 exit contract

不推荐：把 surface snapshot 文本嵌入 prompt
  - 浪费 context window（每轮 ~500 tokens）
  - 大部分内容本轮不需要
  - scan JSON 中已有结构化版本
```

### 5.6 中断恢复后的信息重建

```
场景：ACP 进程崩溃 → session 内存丢失 → 所有磁盘文件完好

恢复步骤：
  Step 1: Runtime 从 session-store 找回 session ID
  Step 2: session/resume → 失败（session 在 ACP 进程中丢失）
  Step 3: 降级 session/new
  Step 4: Prompt 中包含：
    - T0 稳定前缀（角色规则、读取约定）
    - T1 项目上下文
    - 指向最新 continuity 文件的引用
    - 指向 scan JSON 的引用
  Step 5: AI 先读 scan JSON（了解全局）
  Step 6: AI 再读 latest continuity（了解上一个 session 的决定）
  Step 7: AI 从 continuity 中的 route_kind + next_action 继续

关键：不需要把 continuity 全文嵌入 prompt。
AI 只需知道去哪读，不是把内容全塞进 prompt。
```

---

## 6. 验证体系

缓存优化涉及多个独立工作面，每个面有自己的验证逻辑。

### 验证面总览

```
面 1：Session 生命周期      — Worker session 持久化、resume、close
面 2：Session 隔离          — fork 不污染、并行不串扰、close 不影响其他
面 3：Prompt 结构           — T0 稳定性、增量发送、L2 缓存前缀
面 4：上下文连续性           — AI 不迷失、exit contract 有效、handoff 恢复
面 5：资源与稳定性           — 进程数、内存、崩溃恢复、错峰调度
面 6：跨角色协作             — Manager→Worker 委派、重新委派、结果消费
```

### 5.1 面 1：Session 生命周期

**验证目标：** Worker session 从 one-shot 变为持久，支持跨 turn 的 session/prompt。

```
T1.1 — loop 模式基本功能
  前置：run-acp-prompt.py --loop --bridge-socket <sock>
  步骤：
    1. 发送 prompt_1 → 验证 stopReason=end_turn → session 保持
    2. 发送 prompt_2（同一 session）→ 验证响应正确
    3. 发送 prompt_3（同一 session）→ 验证响应正确
    4. 验证 turn 2 的 AI 引用了 turn 1 的内容（上下文保留证明）
    5. 发送 exit 信号 → 验证 session/close 被调用 → 进程退出 rc=0
  度量：
    - session/new 调用次数 = 1
    - session/prompt 调用次数 = 3
    - [CACHE] turn 2/3 的 cache_read > 0（L1 命中证明）

T1.2 — one-shot 向后兼容
  前置：run-acp-prompt.py --bridge-socket <sock>（不带 --loop）
  步骤：
    1. 发送 prompt → 验证 stopReason=end_turn
    2. 验证进程退出 rc=0
    3. 行为与重构前完全相同
  度量：与重构前 one-shot 行为一致

T1.3 — session/resume 恢复
  前置：session-store 中有 session ID
  步骤：
    1. 创建 session（session/new）→ 发送 prompt → 记录 sid
    2. 进程退出（模拟重启）
    3. 新进程 session/resume(sid) → 发送 prompt
    4. 验证 resume 后的上下文可用（AI 知道之前说了什么）
  度量：resume 成功率，resume 失败时降级到 session/new 的行为

T1.4 — session/close 清理
  前置：活跃 session
  步骤：
    1. session/close
    2. 验证 session-store 中该 session status=closed
    3. 验证同一 ACP 进程内其他 session 不受影响
    4. 验证 close 后再发 prompt 到该 session → error
  度量：session-store 状态正确
```

### 5.2 面 2：Session 隔离

**验证目标：** fork 不污染父 session，并行 session 互不串扰。

```
T2.1 — fork 隔离性（核心）
  前置：Manager session 有 5 轮对话历史
  步骤：
    1. session/fork(Manager sid) → Worker 1 sid
    2. Worker 1：发送 3 轮 prompt
    3. Manager：发送 1 轮 prompt
    4. 检查 Manager 对话历史 ← 不包含 Worker 1 的消息
    5. 检查 Worker 1 对话历史 ← 包含 fork 前的 Manager 历史 + 自己的 3 轮
    6. 检查 Worker 1 对话历史 ← 不包含 fork 后 Manager 新增的消息
  度量：跨 session 消息隔离率 = 100%

T2.2 — 并行 session 隔离
  前置：Manager session + 3 个 fork Worker session
  步骤：
    1. Worker 1/2/3 同时发送 prompt（并发）
    2. 验证各 Worker 只看到自己的消息 + 公共的 fork 前历史
    3. 验证 Worker 1 看不到 Worker 2 的消息
    4. 验证 Worker 2 看不到 Worker 3 的消息
  度量：并行隔离率 = 100%

T2.3 — close 隔离
  前置：Manager session + Worker 1 session + Worker 2 session
  步骤：
    1. Worker 1: session/close
    2. 验证 Manager session 仍在（可发 prompt）
    3. 验证 Worker 2 session 仍在（可发 prompt）
    4. 验证 Worker 1 session 不可再发 prompt
  度量：close 不影响其他 session

T2.4 — cancel 隔离
  前置：Worker 1 正在 session/prompt（阻塞中）
  步骤：
    1. 发送 session/cancel(Worker 1 sid)
    2. 验证 Worker 1 session/prompt 返回 cancelled
    3. 验证 Manager session 不受影响
    4. 验证 Worker 1 session 仍可继续发 prompt（不是 close）
  度量：cancel 不影响其他 session
```

### 5.3 面 3：Prompt 结构

**验证目标：** T0 前缀稳定，resume 增量发送，L2 缓存命中。

```
T3.1 — T0 前缀字节一致性（L2 缓存前提）
  前置：重构后的 prompt builder
  步骤：
    1. 构建 Manager fresh prompt → 取前 2500 tokens → hash_1
    2. 构建 Manager fresh_with_handoff prompt → 取前 2500 tokens → hash_2
    3. 构建 Worker 首次 prompt（fork 前）→ 取前 2500 tokens → hash_3
    4. 验证 hash_1 == hash_2 == hash_3
  度量：T0 前缀哈希一致

T3.2 — 动态内容位置
  前置：重构后的 prompt
  步骤：
    1. 扫描 prompt 文本
    2. 验证 T3/T4 动态内容（worktree 状态、exit contract）在 T0 之后
    3. 验证 prompt 前 2000 tokens 中不含 DIRTY/CLEAN、checkpoint 等 T3 值
  度量：T0 区域零动态内容

T3.3 — Resume 增量大小
  前置：Manager resume 模式
  步骤：
    1. 采集 10 轮 resume 的 prompt 大小
    2. 计算平均 prompt_bytes
    3. 验证 avg_prompt_bytes ≤ 1000 tokens
  度量：resume prompt 大小

T3.4 — L2 缓存命中验证（端到端）
  前置：重构后运行 30 分钟
  步骤：
    1. 采集所有 cycle 的 [CACHE] 行
    2. 对于 launch_kind=fresh/fresh_with_handoff/fork 的 cycle：
       验证 cache_read_input_tokens > 0（非零即命中）
    3. 计算 L2 命中率 = 有 cache_read 的 cycle / 总非 resume cycle
  度量：L2 命中率 ≥ 80%
```

### 5.4 面 4：上下文连续性

**验证目标：** AI 在增量 prompt 和旋转后不迷失，exit contract 有效。

```
T4.1 — 增量 prompt 不迷失
  前置：Manager resume 10 轮，每轮只发增量（无 T0 前缀）
  步骤：
    1. 每轮验证 AI 产出有效的 manager-exit-contract.env
    2. 每轮验证 AI 正确遵循角色规则（Manager 不写代码，只在 develop 上输出判断）
    3. 第 5 轮插入一个需要宪法知识的场景（如 break-glass 判断）
       验证 AI 仍然知道宪法规则（来自 session 历史，不是本轮 prompt）
  度量：exit contract 有效率 = 100%，角色越界次数 = 0

T4.2 — Fresh 恢复全量
  前置：触发 fresh_with_handoff
  步骤：
    1. 验证新 prompt 包含完整 T0 前缀
    2. 验证 handoff 内容正确追加
    3. 验证 AI 理解 handoff 中的 rotation_reason
    4. 验证 AI 能从 handoff 恢复上下文（知道上一轮在做什么）
  度量：恢复成功率，AI 产出有效 continuity

T4.3 — 长期运行不退化
  前置：运行 50+ cycle
  步骤：
    1. 采集所有 cycle 的 exit contract 有效性
    2. 记录 rotation 次数和原因
    3. 验证后期 cycle 的 AI 产出质量不退化
  度量：exit contract 有效率不随 cycle 数下降
```

### 5.5 面 5：资源与稳定性

**验证目标：** 进程数可控，崩溃不扩散，错峰调度有效。

```
T5.1 — 进程数控制
  前置：Manager + 5 Worker 并行 30 分钟
  步骤：
    1. 每 30 秒采集 claude-agent-acp 进程数
    2. 画时序图
  度量：
    - peak_acp_processes ≤ 3（Manager bridge + 最多 2 个额外）
    - 稳态 acp_processes = 1（所有 session 在同一个 bridge 内）

T5.2 — 内存控制
  前置：同上
  步骤：
    1. 采集 claude-agent-acp 进程的内存（RSS）
    2. 对比重构前（N+1 个进程）的内存总和
  度量：重构后总内存 ≤ 重构前总内存 × 0.5

T5.3 — session/new 并发峰值
  前置：Manager 需要委派 5 个 Worker
  步骤：
    1. 监控同一秒内 session/new 调用次数
    2. 验证峰值 ≤ 2
  度量：session/new 并发峰值 ≤ 2

T5.4 — 崩溃恢复
  前置：运行中 kill -9 claude-agent-acp
  步骤：
    1. 验证 bridge 检测到 stdout 关闭 → _restart_server
    2. 验证 Manager session 尝试 resume → 失败 → 降级 session/new
    3. 验证 Manager 能在 60s 内恢复工作
    4. 验证 Worker session 恢复：逐个尝试 resume
    5. 验证恢复后不会出现 7-13 个 session/new 同时冲击
  度量：
    - 恢复时间 ≤ 60s
    - 恢复时 session/new 并发 ≤ 2

T5.5 — 错峰调度
  前置：Manager 队列中有 10 个待委派 Worker
  步骤：
    1. 运行 10 个 Manager cycle
    2. 验证每轮最多创建 2 个新 Worker session
    3. 验证 Worker 完成后 session/close 被调用
    4. 验证稳态活跃 session 数 ≤ 5
  度量：每轮新 Worker ≤ 2，活跃 session ≤ 5
```

### 5.6 面 6：跨角色协作

**验证目标：** Manager→Worker 委派链完整，Worker 结果正确消费。

```
T6.1 — fork 委派链
  前置：Manager 运行 3 轮，产出 worker prompt
  步骤：
    1. Manager session/fork → Worker session
    2. Worker 接收 fork 的上下文 + Manager 写的 prompt
    3. Worker 执行 3 turn（loop 模式）→ 完成任务 → session/close
    4. Manager 下一轮 resume 时看到 Worker 的完成 intake
    5. Manager 正确消费 Worker 结果（写 continuity + exit contract）
  度量：委派→执行→收口全链路通过

T6.2 — 重新委派
  前置：Worker 运行中，Manager 决定改方向
  步骤：
    1. Manager 写入新 worker prompt
    2. Worker session/prompt(新 prompt) → 不是 fork，是同一 session
    3. Worker 理解新方向（上下文中有旧方向的历史）
    4. Worker 调整执行 → 完成 → session/close
  度量：同一 session 接收新 prompt 后行为正确

T6.3 — Worker 阻塞回传
  前置：Worker 遇到无法解决的障碍
  步骤：
    1. Worker 写 exit_contract=worker_blocked + BLOCKED_REASON
    2. Worker session/close
    3. Manager 下轮 resume 看到 blocked intake
    4. Manager 正确解读 BLOCKED_REASON 并调整委派
  度量：阻塞信息完整传递

T6.4 — 多 Worker 并行互不干扰
  前置：5 个 Worker 同时在不同 worktree 上工作
  步骤：
    1. 每个 Worker 读写不同 worktree
    2. 验证 Worker 1 的 git 操作不影响 Worker 2 的文件
    3. 验证 Manager 能区分各 Worker 的结果
  度量：并行正确性 = 100%
```

---

## 7. 实施路径 + A/B 验证

### Phase 1：`run-acp-prompt.py` 增加 loop 模式

改动：新增 `--loop` 参数；loop 模式首次 prompt 后不退出；收到 exit 信号 → `session/close` → 退出；不带 `--loop` 保持 one-shot 向后兼容。

**覆盖的验证面：** 面 1（T1.1, T1.2），面 3（T3.4），面 5（T5.1）

**验证：**
```
功能：
  T1.1 ✓ loop 多轮 prompt 正常工作
  T1.2 ✓ one-shot 向后兼容

改进：
  指标                    重构前                      重构后（loop, 3 turns）
  Worker session/new 次数  3 (每 turn 重建)            1
  Worker 进程数            3 (每 turn 重建 subprocess)  1 (持久)
  Worker [CACHE] turn 2+  0 (全冷)                    cache_read > 0 (L1 证明)
```

### Phase 2：Worker 改用 Manager bridge + session/fork

改动：`launch_worker_from_manager_prompt_if_needed` 不再用 `--agent`；改为 bridge socket → `session/fork`(Manager)；后续 turn 用 loop 模式。

**覆盖的验证面：** 面 2（全部），面 5（T5.1, T5.3），面 6（T6.1, T6.2）

**验证：**
```
功能：
  T2.1 ✓ fork 不污染父 session
  T2.2 ✓ 并行 session 互不串扰
  T2.3 ✓ close 不影响其他 session
  T2.4 ✓ cancel 不影响其他 session
  T6.1 ✓ fork 委派链端到端
  T6.2 ✓ 同一 session 重新委派

改进：
  指标                      重构前                      重构后
  claude-agent-acp 进程数    N+1 (线性增长)              1 (全部共享)
  Worker 上下文继承          全靠 prompt 文本            fork 继承 Manager 对话历史
  Worker L2 缓存             不可用（跨进程）            可用（同进程、同 API key）
  Worker 启动延迟            含 claude-agent-acp 冷启动  session/fork 毫秒级
```

### Phase 3：prompt 增量发送 + T0 稳定性分层

改动：`build_prompt()` 区分 resume vs fresh；Resume 只发增量；Fresh 发全量 + T0 在 prompt 最前面。

**覆盖的验证面：** 面 3（全部），面 4（全部）

**验证：**
```
功能：
  T3.1 ✓ T0 前缀哈希一致（Manager fresh == Worker 首次）
  T3.2 ✓ 动态内容在 T0 之后
  T4.1 ✓ 10 轮增量 prompt 不迷失
  T4.2 ✓ fresh_with_handoff 恢复全量
  T4.3 ✓ 50+ cycle 不退化

改进：
  指标                    重构前                      重构后
  Resume prompt 大小       ~5000 tokens                ~700 tokens
  Context window 消耗速率  5000 tokens/cycle            700 tokens/cycle
  连续 resume 次数         15-24                        ≥50
  L2 缓存 T0 命中率        0%                           ≥80%
```

### Phase 4：多 Worker 错峰调度

改动：每轮最多创建 2 个新 Worker session；完成即 close；稳态活跃 ≤ 5。

**覆盖的验证面：** 面 5（全部），面 6（T6.3, T6.4）

**验证：**
```
功能：
  T5.3 ✓ session/new 峰值 ≤ 2
  T5.4 ✓ 崩溃后恢复时间 ≤ 60s
  T5.5 ✓ 错峰创建 + 完成 close
  T6.3 ✓ Worker 阻塞回传
  T6.4 ✓ 5 Worker 并行互不干扰

改进：
  指标                    重构前                      重构后
  ACP 进程峰值             N+1                         ≤3
  内存                     ~500MB × (N+1)              ~500MB × 2
  session/new 并发峰值     7-13 (同秒风暴)             1-2 (错峰)
  bridge 崩溃/小时         3 次                        0 次
```

---

## 8. 成功阈值总表

### 8.0 总则

**每个 Phase 独立 worktree、独立 issue、独立 merge。** Phase N 不通过成功标准，不得开 Phase N+1 的 worktree。Phase N merge 后至少观察 1 天稳定再继续。

**测试不可跳过。** 每个 Phase 的测试必须在 worktree 上跑通、结果达标，才能提 PR merge。

**Phase 0 必须先做。** 没有基线数据，所有"缓存命中率提升 X%"无法验证。

---

### Phase 0：可观测性基础设施

**改动范围：** `run-acp-prompt.py` 加 `[CACHE]` 日志行；`freely` runtime 加 `cache_metrics` 事件；新增 `cache-baseline` 采集命令。

**不改任何业务逻辑。** 这是纯观测——给后续 Phase 提供"眼睛"。

| # | 成功标准 | 测量方式 | 阈值 |
|---|---------|---------|------|
| 0.1 | `[CACHE]` 日志正常输出 | 每个 cycle 的 cycle log 末尾有 `[CACHE]` 行 | 100% cycle 覆盖 |
| 0.2 | `cache-baseline` 可执行 | `./bin/freely cache-baseline --project <path> --duration 10m` 输出 JSON | 有效 JSON，无报错 |
| 0.3 | 现有功能不受影响 | daemon 正常启停，Manager/Worker 正常完成 cycle | 无回归 |
| 0.4 | 基线数据采集完成 | 运行 1 小时，产出 `baseline-before.json` | 包含 ≥10 个 cycle 的完整指标 |

**不通过条件：** `[CACHE]` 日志缺失任何 cycle；`cache-baseline` 命令报错；任何现有功能回归。

**达标后动作：** 记录 baseline 值（L1/L2 命中率、prompt_bytes、resume_streak、进程数），merge Phase 0，进入 Phase 1。

---

### Phase 1：run-acp-prompt.py loop 模式

**改动范围：** 仅 `run-acp-prompt.py`（435 行 Python）。新增 `--loop` 参数。不碰 bash runtime。不改现有 Worker launch 路径。

**涉及验证面：** 面 1（Session 生命周期）

| # | 成功标准 | 测量方式 | 阈值 |
|---|---------|---------|------|
| **功能** |
| 1.1 | one-shot 向后兼容 | `run-acp-prompt.py --bridge-socket ...`（不带 --loop）行为与重构前完全一致 | 行为一致 |
| 1.2 | loop 模式：3 turn 正常工作 | 同一 session 连续 `session/prompt` 3 次，每次 stopReason=end_turn | 3/3 成功 |
| 1.3 | loop 模式：exit 信号正确清理 | 收到 exit → `session/close` 被调用 → session-store status=closed | close 成功 |
| 1.4 | loop 模式超时不崩溃 | 设置短超时，验证 TimeoutError 被正确处理，进程不挂 | 进程退出 rc≠0，不挂起 |
| **缓存** |
| 1.5 | Worker L1 命中率提升 | 同一 Worker 任务的 3 个 turn，对比 Phase 0 baseline 的 Worker L1 命中率 | 从 0% → ≥60% |
| **回归** |
| 1.6 | Manager 功能不受影响 | Manager cycle 正常完成，exit contract 有效 | 无回归 |
| 1.7 | 现有 Worker（one-shot）不受影响 | one-shot Worker 正常启动、执行、退出 | 无回归 |

**不通过条件：** 1.1-1.4 任一失败；1.5 L1 命中率未提升；1.6-1.7 任一回归。

**达标后动作：** merge Phase 1，观察 Manager + 现有 Worker 稳定 1 天，进入 Phase 2。

---

### Phase 2：Worker 独立 subprocess + loop 多 turn

**实际实施：** 修复 Worker 从共享 bridge（`--bridge-socket`）改为独立 subprocess（`--agent`），配合 Phase 1 的 `--loop` 实现多 turn。**原设计的 session/fork 方案在此 Phase 未实施**——独立 subprocess 是崩溃修复（P0），session/fork 是后续缓存优化（P2）。

**改动范围：** `launch_worker_from_manager_prompt_if_needed`（bash ~10 行）；`run-acp-prompt.py` loop 模式。

**涉及验证面：** 面 1（Session 生命周期）、面 5（资源、故障隔离）

| # | 成功标准 | 测量方式 | 阈值 |
|---|---------|---------|------|
| **功能** |
| 2.1 | Worker 独立进程不崩溃 | 5 个 Worker 并行，不再出现之前的 7-13 session/new 风暴崩溃 | 无 bridge 崩溃 |
| 2.2 | Worker 多 turn（loop 模式） | Worker --loop 启动后，写入 next-prompt-file，发送第二个 prompt | 同一 session 完成 2+ turn |
| 2.3 | 故障隔离 | 1 个 Worker subprocess 崩溃，Manager 和其他 Worker 不受影响 | 隔离正确 |
| **回归** |
| 2.4 | Manager 功能不受影响 | Manager cycle 正常完成，exit contract 有效 | 无回归 |
| 2.5 | one-shot Worker 不受影响 | 不带 --loop 的 Worker 正常启动、执行、退出 | 无回归 |

**不通过条件：** 2.1 bridge 崩溃；2.2 loop 模式失败；2.4-2.5 回归。

**达标后动作：** merge Phase 2，进入 Phase 3。

---

### Phase 3：prompt 增量发送 + T0 稳定性分层

**改动范围：** `build_prompt()`（bash ~80 行）；`start-lead-agent.sh`（重排输出顺序 ~30 行）。

**涉及验证面：** 面 3（Prompt 结构）、面 4（上下文连续性）

| # | 成功标准 | 测量方式 | 阈值 |
|---|---------|---------|------|
| **功能** |
| 3.1 | T0 前缀字节一致 | Manager fresh / Manager fresh_with_handoff / Worker 首次 的 prompt 前 2500 tokens 哈希相同 | 哈希 100% 一致 |
| 3.2 | 动态内容在 T0 之后 | prompt 前 2000 tokens 中不含 DIRTY/CLEAN、checkpoint 等 T3 动态值 | 零 T3 内容 |
| 3.3 | 增量 prompt 不迷失 | Manager resume 10 轮，每轮只发增量（~700 tokens），AI 不越界、产出有效 exit contract | 10/10 有效 |
| 3.4 | Fresh 恢复全量 | fresh_with_handoff 时 prompt 包含完整 T0 + handoff 内容，AI 正确恢复上下文 | 恢复成功 |
| **缓存** |
| 3.5 | Resume prompt 大小 | 10 轮 resume 的 prompt_bytes 平均值 | ≤1000 tokens |
| 3.6 | 连续 resume 次数 | 从 Phase 2 的 baseline 值提升 | ≥50 次（或 ≥ Phase 2 baseline × 2） |
| 3.7 | L2 缓存命中率 | 所有 launch_kind=fresh/fork/fresh_with_handoff 的 cycle 中 cache_read > 0 的占比 | ≥80% |
| **长期** |
| 3.8 | 50+ cycle 不退化 | 连续运行 50 cycle，exit contract 有效率不随 cycle 数下降 | 后期有效率 ≥ 前期 |
| **回归** |
| 3.9 | Worker 功能不受影响 | Phase 2 的 Worker fork→多 turn→close 流程正常 | 无回归 |

**不通过条件：** 3.1-3.2 任一失败（T0 不稳定）；3.3 AI 迷失；3.5 prompt 未精简；3.6 resume 未延长。

**达标后动作：** merge Phase 3，观察 50+ cycle 稳定，进入 Phase 4。

---

### Phase 4：多 Worker 错峰调度

**改动范围：** `manager_runtime_launch_workers_from_latest_handoff`（bash ~30 行）。

**涉及验证面：** 面 5（资源与稳定性）

| # | 成功标准 | 测量方式 | 阈值 |
|---|---------|---------|------|
| **功能** |
| 4.1 | 错峰创建 | Manager 需委派 5 Worker，验证每轮最多创建 2 个新 session，剩余排队 | 每轮新 Worker ≤2 |
| 4.2 | 完成即 close | Worker 完成后 session/close 被调用，session-store status=closed | close 率 100% |
| 4.3 | 稳态活跃数受控 | 10 个 Worker 排队时，稳态活跃 session 数 | ≤5 |
| **稳定性** |
| 4.4 | 崩溃恢复 | kill -9 claude-agent-acp → bridge 检测 → 60s 内恢复 → 恢复时 session/new 并发 | 恢复 ≤60s，并发 ≤2 |
| 4.5 | 崩溃不扩散 | 1 个 Worker session 故障 → 其余 session 正常 | 故障隔离 |
| **回归** |
| 4.6 | Phase 1-3 功能不受影响 | 全链路端到端测试通过 | 无回归 |

**不通过条件：** 4.1-4.3 任一失败（调度不正确）；4.4 恢复超时或风暴；4.5 故障扩散。

**达标后动作：** merge Phase 4。全部 Phase 完成，token 花费优化结束。

---

## 9. 自举开发的提示词组装

### 9.1 编译器自举模型

用上一个稳定版本的 Freely 开发下一个版本。AI 执行遵守当前运行的版本，AI 修改的是下一个版本。

```
Freely v1.0 (打包好的应用)              Freely 仓库 (开发中)
┌──────────────────────────┐          ┌──────────────────────────┐
│ workspace/agents/        │  ──运行──→ │ 修改 CONSTITUTION.md     │
│ workspace/skills/        │  开发对象  │ 修改 workspace/agents/   │
│ workspace/hooks/         │           │ 新增 pre-brainstorms/    │
│ workspace/ibm-framework  │           │ 修改 milestones.md       │
│ bin/ + runtime/          │           └──────────────────────────┘
│                          │                      │
│ AI 的"操作系统"           │           验证通过、稳定
│ 当前运行版本不变           │                      ▼
└──────────────────────────┘           ┌──────────────────────────┐
                                       │ 打包 → Freely v1.1       │
                                       │ 然后用 v1.1 开发 v1.2    │
                                       └──────────────────────────┘
```

### 9.2 版本号规则

```
dev 版（内部开发用）：  <YYYYMMDD>-<序号>-dev
  例: 20260501-001-dev, 20260501-002-dev
  从 develop 打包，用于开发 Freely 自己

beta 版（对外测试）：   <YYYYMMDD>-beta
  例: 20260501-beta, 20260601-beta

stable 版（正式发布）： <YYYY>.<MM>.<DD>-stable
  例: 2026.05.01-stable
```

### 9.3 自举验收循环

```
develop (当前)
  │
  ├─ 1. 打包
  │    freely-package --version 20260501-001-dev
  │    → 输出到 ~/.freely/versions/20260501-001-dev/
  │
  ├─ 2. 用打包版本开发 Freely
  │    ~/.freely/versions/20260501-001-dev/bin/freely daemon start --project <freely-repo>
  │    → AI 在打包版本的 workspace/ 规则下运行
  │    → AI 修改 develop 上的 workspace/ 文件
  │
  ├─ 3. 验证：新版本能否成功打包并开发？
  │    → 合并 workspace 改动到 develop
  │    → 打包 20260502-001-dev
  │    → 用 20260502-001-dev 启动 daemon
  │    → 让它开发 Freely → 能正常完成一个 cycle → 验收通过
  │
  └─ 4. 循环
       20260502-001-dev 继续开发 → 打包 20260503-001-dev → ...
```

**验收标准：打包版本能成功开发 Freely 自己。** 这是一个完美的自举测试——如果新版本有 bug，它开发的产物会有问题，或者根本跑不起来。

### 9.4 打包脚本设计

`freely-package --version <ver> [--output <dir>]`

```
打包内容（Freely 产品能力，随版本发布）：
  docs/system/workspace/agents/       → agent 角色定义
  docs/system/workspace/skills/       → skill 定义
  docs/system/workspace/hooks/        → git gate 脚本
  docs/system/workspace/scripts/      → 运行时 (freely, acp-bridge, run-acp-prompt, ...)
  docs/system/workspace/ibm-framework.md
  docs/system/workspace/three-loop-capability-lifecycle.md
  docs/system/workspace/tools.md
  docs/system/workspace/acp-session-architecture.md
  bin/                                → 入口脚本
  .githooks/                          → git hook 包装层
  templates/                          → freely init 模板

不打包（仅 Freely 开发仓库内使用）：
  CONSTITUTION.md, LAWS.md            → Freely 的开发笔记本
  AGENTS.md                           → 项目治理入口
  PROJECT_INTENT.md                   → 产品方向
  milestones.md, pre-brainstorms/     → 开发计划和预研
  issues/, progress/                  → 开发状态
```

### 9.3 提示词组装逻辑

```
Freely 开发 Freely 时：

T0（来自打包版本的 workspace/，稳定）：
  agents/manager-agent.md        → Manager 身份和职责
  agents/worker-agent.md         → Worker 身份和职责
  skills/README.md               → 技能索引
  ibm-framework.md               → B1_IBM/B2_IBM 路由
  tools.md                       → 工具选择规则
  acp-session-architecture.md    → session 模型
  → 这些是 AI 的"操作系统"，来自当前运行的 Freely 版本
  → AI 本轮不能修改它们（即使 AI 同时在开发它们的下一个版本）

T1（来自开发仓库，AI 可以修改）：
  CONSTITUTION.md 路径引用       → "使用 Freely Git Governance"
  LAWS.md 路径引用               → "遵循 Freely IBM Framework"
  PROJECT_INTENT.md 路径引用     → Freely 的产品方向
  AGENTS.md 路径引用             → 项目治理入口
  → 路径引用，不嵌入内容。一般不变，放在 T0 尾部

T2-T4: 运行时状态（scan JSON, exit contract, ...）
```

### 9.4 用户项目的提示词组装

```
用户开发自己的 app 时：

T0：同 Freely 开发 Freely —— 来自 Freely 打包版本的 workspace/
T1：用户项目文档 —— CONSTITUTION.md / LAWS.md / AGENTS.md / PROJECT_INTENT.md
     用户写"使用 Freely Git Governance"、"技术栈: Next.js"
T2-T4：运行时状态
```

---

---

## 10. 与打包自举开发的排期关系

两个预研工位不是并行的，是**前后依赖**的：

```
工位 1：打包 + 自举验证（先做）
  └─ 产出：freely-package 脚本 + 版本号规则 + test-pre-merge 门禁

工位 2：token 花费优化（后做，依赖工位 1）
  └─ 每个 Phase 的验证方式：
      Phase N 改动完成
        → 打包出 test-pre-merge 版本
        → 用打包版本开发 Freely（自举验证）
        → 对比 Phase N-1 的 token 指标
        → 达标 → merge develop
```

**没有工位 1，工位 2 的每个 Phase 无法可靠验证。** 因为：
- 没有打包 → 运行的是"改了 workspace 的开发树"，不是稳定版本
- 没有自举 → 不知道改动是否导致 Freely 开发 Freely 时出 bug
- 没有基线 → token 指标对比没有锚点

建议排期：先开工位 1 的预研（打包脚本设计、test-pre-merge 门禁设计），预研通过后立即实施。工位 1 完成后，工位 2 的每个 Phase 有可靠的验证基础设施。

### 最终达标判定

全部四个 Phase 通过后：

| 指标 | Phase 0 基线 | 最终目标 | 判定 |
|------|------------|---------|------|
| Worker L1 缓存命中率 | 0% | ≥60% | 必须 |
| Resume prompt 大小 | ~5000 tokens | ≤1000 tokens | 必须 |
| 连续 resume 次数 | ~15-24 | ≥50 | 必须 |
| ACP 进程峰值 | N+1 | ≤3 | 必须 |
| session/new 并发峰值 | 7-13 | ≤2 | 必须 |
| Bridge 崩溃次数/小时 | ~3 | 0 | 必须 |
| Manager 功能正确性 | 正常 | 正常 | 必须 |
| Worker 功能正确性 | 正常 | 正常 | 必须 |

| # | 验证面 | 指标 | 当前基线 | 目标 | 测量方式 |
|---|--------|------|---------|------|---------|
| 1A | Session 生命周期 | Worker session/new 次数/task | 每 turn 1 次 | 1 次/task | [CACHE] 日志 |
| 1B | Session 生命周期 | Worker L1 缓存命中 | 0% | ≥60% (3-turn task) | cache_read > 0 的 turn 占比 |
| 2A | Session 隔离 | fork 污染率 | N/A | 0 | 对话历史检查 |
| 2B | Session 隔离 | 并行 session 串扰率 | N/A | 0 | 跨 session 消息隔离 |
| 3A | Prompt 结构 | T0 前缀一致性 | 0 (动态破坏) | 100% | 哈希对比 |
| 3B | Prompt 结构 | Resume prompt 大小 | ~5000 tokens | ≤1000 tokens | prompt_bytes 度量 |
| 3C | Prompt 结构 | L2 缓存命中率 | 0% | ≥80% | cache_read > 0 的非 resume cycle 占比 |
| 4A | 上下文连续性 | Exit contract 有效率 | — | 100% | manager/worker exit contract 验证 |
| 4B | 上下文连续性 | 连续 resume 次数 | ~15-24 | ≥50 | resume_streak 计数 |
| 5A | 资源稳定性 | ACP 进程峰值 | N+1 | ≤3 | ps aux 计数 |
| 5B | 资源稳定性 | session/new 并发峰值 | 7-13 | ≤2 | 日志时间戳聚合 |
| 5C | 资源稳定性 | Bridge 崩溃次数/小时 | ~3 | 0 | runtime events 计数 |
| 6A | 跨角色协作 | 委派→执行→收口全链路 | 仅 Manager 正常 | Worker 也正常 | 端到端测试 |
| 6B | 跨角色协作 | 多 Worker 并行正确性 | 不适用（独立进程） | 100% | 文件隔离验证 |
