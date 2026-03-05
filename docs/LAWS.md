# Freely 法律

> 我是项目法律，负责判定标准与验收口径。

---

## 0. 法律定位

法律只定义三类内容：
- 判定规则（什么算合规）
- 验收证据（什么算完成）
- 技能路由（由哪个 skill 执行）

法律不重复执行步骤。执行步骤以 `docs/system/workspace/skills/` 为唯一执行事实源。

### 0.1 三层职责边界（宪法 / 法律 / skills）

三层不冗余，职责如下：
- 宪法（What/Why）：定义不可逾越边界与原则，不写执行步骤。
- 法律（Check/Accept/Route）：定义判定门、证据口径、技能路由，不写执行步骤。
- skills（How）：定义可执行操作步骤，按法律门验收。

判定规则：
1. 宪法出现的硬约束，必须在法律中存在可检查门禁。
2. 法律出现的门禁，必须能路由到至少一个可执行 skill。
3. skills 变更不得绕开宪法与法律；仅可优化实现方式。

---

## 1. 当前阶段约束

在文档模型重构阶段，工作区 `docs/` 最小集合：
- `docs/PROJECT_INTENT.md`
- `docs/LAWS.md`
- `docs/CONSTITUTION.md`
- `docs/pre-brainstorms/`

判定规则：
1. 新讨论与新决策进入 `docs/pre-brainstorms/<YYYYMMDD-HHMM--topic>/`。
2. 历史执行态文档可以不在工作区常驻，但验收证据不得缺失；可通过 git 历史、评审记录或恢复记录提供可追溯证据。
3. 三件套（意图/法律/宪法）未一致前，不扩展旧目录模型。
4. 第 3 章门禁在本阶段采用“双轨验收”：满足“规范产物路径”或“等价可追溯证据”任一轨即视为通过。

---

## 2. 执行路由

默认执行链：
1. `skill:constitution-guard`（硬约束门禁）
2. `skill:laws-enforcer`（法律验收门禁）
3. 业务执行 skill（按场景）

业务执行 skill：
- 外循环编排：`skill:auto-loop-orchestrator`
- 文档内循环：`skill:doc-loop-execution`
- 开发内循环：`skill:dev-loop-execution`
- 分支与发布：`skill:branch-management`
- 复杂冲突：`skill:premerge-reconcile`
- 恢复与子代理：`skill:recovery-subagent-governance`
- 模块/接口治理：`skill:module-interface-governance`
- 配置备份：`skill:config-backup-guard`

---

## 3. 法律验收门

### 3.1 分支与发布门

通过条件：
1. `feature/*` 来源为 `pre-develop`。
2. `main/develop/pre-develop` 保持 add/commit 禁止。
3. merge 方向符合宪法分支表。
4. 从 `pre-develop` 提升到 `develop` 前，`TEST`（含集成测试验收）必需通过（允许“规范路径文件”或“等价可追溯证据”）。
5. 从 `pre-develop` 提升到 `develop` 前，必需评审记录存在（`docs/reviews/` 或等价评审记录）。
6. 从 `pre-develop` 提升到 `develop` 前，提升提交可从 `pre-develop` 到达（祖先可追溯）。
7. 从 `pre-develop` 提升到 `develop` 前，进度/恢复文档已更新提升结果（或等价记录）。
8. hook 拒绝消息必须指向宪法章节作为策略来源。
9. hotfix 合并到 `main/develop` 后，必须同步到 `pre-develop` 并留痕。
10. stage tag 符合 `YYYY.MM.DD-HHMM-stage` 与分支映射。
11. `alpha/beta` 不可 push。
12. `PRE_TEST` 只作为开发前验收标准定义，不得作为合并/提升通过证据。
13. 执行 merge/promotion/release/cleanup 前，必须执行 `./bin/wt-status-all` 且结果全为 `CLEAN`。
14. 执行 merge train 前，必须执行 `./bin/branch-merge-audit --only-unmerged`，输出需可见来源分支与目标分支合并状态。
15. `main/develop/pre-develop` 的推送增量必须包含 merge commit；不允许 fast-forward 方式绕过 merge 门禁。
16. 受治理分支合并必须通过 `./bin/merge-guarded <target> <source>` 执行，禁止直接 `git merge` 绕过策略检查。

执行技能：
- `skill:branch-management`
- `skill:constitution-guard`

### 3.2 Doc Loop 门

通过条件：
1. intake/brainstorm/map 产物完整（规范路径）或存在等价可追溯文档链路。
2. candidates 的 route/status 一致。
3. milestone 与 issue 映射同步（规范路径）或存在等价同步证据。
4. map 阶段已给出开发前 `PRE_TEST`（含集成验收标准）基线。

执行技能：
- `skill:doc-loop-execution`
- `skill:laws-enforcer`

### 3.3 Dev Loop 门

通过条件：
1. 代码与测试产物存在。
2. 进度/状态文档完成更新（规范路径）或存在等价可追溯记录。
3. 验收与实现一致，无文档漂移。
4. 开发中、review、test 阶段有持续补全测试用例并执行的证据。
5. 合并/提升使用 `TEST` 结果验收，不以 `PRE_TEST` 代替。

执行技能：
- `skill:dev-loop-execution`
- `skill:laws-enforcer`

### 3.4 Auto Loop 门

通过条件：
1. issue 发现来源可追踪。
2. 路由决策可解释（doc-loop/dev-loop）。
3. 回流后下一轮输入状态正确。

执行技能：
- `skill:auto-loop-orchestrator`
- `skill:laws-enforcer`

### 3.5 冲突与回退门

通过条件：
1. 冲突决策按语义，不按提交时间。
2. 合并后治理语义无回退（分支策略/worktree/命名/tag 口径一致）。
3. premerge 分支从 `pre-develop` 拉出并回并 `pre-develop`。

执行技能：
- `skill:premerge-reconcile`
- `skill:branch-management`

### 3.6 恢复与子代理门

通过条件：
1. 恢复记录含 branch/worktree/session 上下文。
2. 子代理任务有边界、状态与合并影响记录。
3. 不存在所有权不清的续接执行。

执行技能：
- `skill:recovery-subagent-governance`

### 3.7 模块接口门

通过条件：
1. 接口版本策略明确。
2. 破坏性变更有迁移路径与回滚路径。
3. 合约测试覆盖当前/候选实现。
4. 涉及第三方 API 时，以第三方 API 契约为外部事实源，本地代码/适配层已对齐。
5. 不存在“要求第三方 API 适配本地实现”的反向依赖设计。

执行技能：
- `skill:module-interface-governance`

### 3.8 配置备份门

通过条件：
1. 任何配置修改前已完成备份。
2. 备份命名符合宪法约束。
3. 执行记录可追溯备份路径。

执行技能：
- `skill:config-backup-guard`

### 3.9 产品身份与自治闭环门

通过条件：
1. 执行链保持“获取 Issue -> 文档 -> 开发 -> 验收 -> 获取 Issue”闭环。
2. 需求来源覆盖宪法定义输入面，不退化为单一固定待办列表。
3. 在无明确停止条件时维持自治循环与续接策略。

执行技能：
- `skill:auto-loop-orchestrator`
- `skill:laws-enforcer`

### 3.10 技术栈与基线结构门

通过条件：
1. 强制技术栈未被擅自替换（Tauri/Rust/React/Bun/xterm.js/Rust PTY）。
2. 项目基线结构满足宪法最低要求。
3. 研究阶段目录约束与当前阶段规则一致。

执行技能：
- `skill:constitution-guard`
- `skill:laws-enforcer`

### 3.11 终端架构与会话隔离门

通过条件：
1. 终端通过 PTY 执行真实 shell，而非伪执行。
2. 循环实例保持独立会话/PID/状态隔离。
3. 监控与恢复目标对齐到 AI CLI 会话生命周期。

执行技能：
- `skill:constitution-guard`
- `skill:recovery-subagent-governance`

### 3.12 AI 执行模式与输入约束门

通过条件：
1. AI 规格符合 `tool:model:mode`，模式含义不被破坏。
2. 仅使用宪法允许的主要输入面（路径/意图/宪法/AI规格）。
3. 其他上下文通过项目文件发现，不走隐式注入。

执行技能：
- `skill:constitution-guard`
- `skill:laws-enforcer`

### 3.13 工程纪律门

通过条件：
1. 命令面保持可脚本化、确定性、可检查。
2. 状态保持显式可落盘验证。
3. 项目根 `AGENTS.md` 保持存在并可用。
4. 代码与文档不一致时，已优先执行代码/测试修复路径。
5. 若存在规范文档改动，已在独立 `feature/*` + worktree 中完成，并绑定对应实现或门禁变更证据。

执行技能：
- `skill:laws-enforcer`
- `skill:dev-loop-execution`

### 3.14 子代理与并行领域门

通过条件：
1. 子代理委托有明确边界、完成标准、合并标准。
2. 并行开发遵守物理领域（worktree）与逻辑领域（所有权）约束。
3. 共享热点有串行窗口或显式排序策略。

执行技能：
- `skill:recovery-subagent-governance`
- `skill:laws-enforcer`

### 3.15 Freely 自举一致性门

通过条件：
1. Freely 自身开发不绕开宪法/法律/意图治理链。
2. 架构治理调整先进入 pre-brainstorms 再进入 doc/dev 落地。
3. 工具链同构（分支/worktree/hook/门禁）可复用到用户项目。
4. 外部权限问题提供预检与可执行修复路径。

执行技能：
- `skill:constitution-guard`
- `skill:branch-management`
- `skill:laws-enforcer`

---

## 4. 宪法全章节对齐矩阵

| 宪法章节 | 对齐法律门 | 验收证据（最小） | 主要技能路由 |
|---|---|---|---|
| 1. 产品身份 | 3.9 产品身份与自治闭环门 | issue 来源记录 + 闭环执行记录 | `skill:auto-loop-orchestrator`, `skill:laws-enforcer` |
| 2. 分支与工作树策略 | 3.1 分支与发布门, 3.5 冲突与回退门, 5 清理与退役 | 分支来源/merge 方向/worktree 清理记录 + 提升清单证据 | `skill:branch-management`, `skill:premerge-reconcile`, `skill:constitution-guard` |
| 3. 版本命名规则 | 3.1 分支与发布门 | tag 命名与分支 stage 对照记录 | `skill:branch-management` |
| 4. 强制技术栈 | 3.10 技术栈与基线结构门 | 技术栈检查记录 | `skill:constitution-guard`, `skill:laws-enforcer` |
| 5. 基线项目结构 | 3.10 技术栈与基线结构门 | 目录结构检查记录 | `skill:constitution-guard`, `skill:laws-enforcer` |
| 6. 终端架构规则 | 3.11 终端架构与会话隔离门 | PTY 执行与会话隔离记录 | `skill:constitution-guard`, `skill:recovery-subagent-governance` |
| 7. AI 执行模式 | 3.12 AI 执行模式与输入约束门 | `tool:model:mode` 规格校验记录 | `skill:constitution-guard`, `skill:laws-enforcer` |
| 8. 恢复策略 | 3.6 恢复与子代理门, 3.9 产品身份与自治闭环门 | 续接/桥接与恢复检查点记录 | `skill:recovery-subagent-governance`, `skill:auto-loop-orchestrator` |
| 9. 约束面 | 3.12 AI 执行模式与输入约束门 | 输入面白名单检查记录 | `skill:constitution-guard`, `skill:laws-enforcer` |
| 10. 工程纪律 | 3.13 工程纪律门 | 命令面/状态面/AGENTS 可检查记录 + 代码优先修复证据 | `skill:laws-enforcer`, `skill:dev-loop-execution` |
| 11. 方法论总述 | 3.2 Doc Loop 门, 3.3 Dev Loop 门, 3.4 Auto Loop 门 | loop 产物完整性与路由一致性记录 | `skill:doc-loop-execution`, `skill:dev-loop-execution`, `skill:auto-loop-orchestrator` |
| 12. 子代理规划与委托 | 3.6 恢复与子代理门, 3.14 子代理与并行领域门 | 委托边界/批次等待/失败回退记录 | `skill:recovery-subagent-governance`, `skill:laws-enforcer` |
| 13. 并行开发领域模型 | 3.14 子代理与并行领域门 | 物理/逻辑领域边界与冲突窗口记录 | `skill:recovery-subagent-governance`, `skill:laws-enforcer` |
| 14. 模块架构与接口版本 | 3.7 模块接口门 | 版本策略/迁移回滚/合约测试记录 + 第三方 API 契约对齐证据 | `skill:module-interface-governance` |
| 15. 变更前配置备份 | 3.8 配置备份门 | 备份文件路径与命名记录 | `skill:config-backup-guard` |
| 16. Freely 自举开发 | 3.15 Freely 自举一致性门 | pre-brainstorms -> doc/dev 落地链路记录 | `skill:constitution-guard`, `skill:branch-management`, `skill:laws-enforcer` |

对齐规则：
1. 任一宪法章节不得出现“无对应法律门”的空洞。
2. 任一法律门不得出现“无证据口径”的不可验收状态。
3. 任一法律门不得出现“无技能路由”的不可执行状态。

---

## 5. 清理与退役

判定规则：
1. 分支/worktree 仅在 `verified-retirable` 后删除。
2. 不能因“已合并”立即删除，必须先完成语义回退检查与测试。
3. 删除动作需保留记录（可追溯到合并与验证结果）。

执行技能：
- `skill:branch-management`

---

## 6. 违例处理

任一门禁失败：
1. 阻断后续 promotion/release。
2. 记录失败门、证据与修复路径。
3. 需要时转入 `skill:premerge-reconcile`。
