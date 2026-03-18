# 候选项收敛（阶段 1）

日期：2026-03-05

## 收敛规则
每个候选项在进入 issue 队列前需通过反向约束检查：

1. 意图适配（`docs/PROJECT_INTENT.md`）
2. 宪法/法律适配（`docs/CONSTITUTION.md`、`docs/LAWS.md`）
3. 流程适配统一循环图（A1 -> A2 -> IBM+G/DDD -> A3）
4. 当前架构/范围内的实现可行性
5. 价值 > 成本（若改变循环/流程逻辑）

只有通过全部 5 项检查的候选项才能成为 issue-ready。

## Issue-Ready（立即入队）

### 批次 P0-核心
1. `C-20260304-601` Owner Loop 契约
- 路由：A1/A2 -> doc-loop(IBM+G)
- 输出目标：循环契约 + 状态转换
- 依赖：无

2. `C-20260304-602` 门禁契约
- 路由：A1/A2 -> doc-loop(IBM+G)
- 输出目标：可执行的门禁定义
- 依赖：C-20260304-601

3. `C-20260304-603` 恢复契约
- 路由：A1/A2 -> doc-loop(IBM+G)
- 输出目标：续接/桥接协议
- 依赖：C-20260304-601

4. `C-20260304-604` Issue 发现 + 路由器内核
- 路由：A1 -> A2 -> auto-loop(ADD)
- 输出目标：来源扫描 + 路由决策逻辑
- 依赖：C-20260304-601

5. `C-20260304-607` 文档契约编译器
- 路由：doc-loop(IBM+G) -> dev-loop(DDD)
- 输出目标：验收标准 -> 可执行检查
- 依赖：C-20260304-602

6. `C-20260303-101` CLI 编排 MVP
- 路由：auto-loop(ADD) / dev-loop(DDD)
- 输出目标：命令编排 + 重试/超时/日志
- 依赖：C-20260304-601

7. `C-20260303-102` 集成测试优先门禁
- 路由：dev-loop(DDD)
- 输出目标：提升前的集成门禁
- 依赖：C-20260304-602, C-20260304-607

8. `C-20260304-201` 后端 API 契约 v1
- 路由：doc-loop(IBM+G)
- 输出目标：前端解耦的稳定 API
- 依赖：C-20260304-601, C-20260304-602

### 批次 P1-后续
9. `C-20260304-203` 后端优先执行门禁
10. `C-20260303-003` 验收契约 + 自包含检查器
11. `C-20260303-103` 会话生命周期（续接/压缩/新会话）
12. `C-20260304-202` 多项目 UI 隔离实现
13. `C-20260304-606` 提升与清理执行器

## 需要研究（保留在候选池）
1. `C-20260303-002` 独立审计门禁
- 原因：当前阶段需要最小可实现边界。

2. `C-20260304-501` Freely-on-OpenClaw 配置
- 原因：外部运行时假设需重新检查当前架构。

3. `C-20260304-605` 子代理批量编排器
- 原因：并发边界和推广范围未收敛。

## 已放弃（超出当前架构范围）
1. `C-20260304-301` EvoMap 集成作为 P2 插件
2. `C-20260304-401` 验收到能力资产映射

## 下一步行动
- 先将批次 P0-核心转换为可执行 issue 规范。
- 保持所有流程/契约变更在价值验证检查之后。

## 变更（2026-03-05 自举 + 治理）

### 新增到 P0-核心
- `C-20260305-701` Worktree 根目录执行器 + 权限预检
- `C-20260305-702` 钩子策略模板编译器
- `C-20260305-704` Freely 自举治理契约

### 新增到 P1-后续
- `C-20260305-703` 钩子/Worktree 约束治理 UI

## 变更（2026-03-05 目录统一）

### 新增到 P0-核心
- `C-20260305-801` 目录迁移契约（Doc-Loop Contract）
- `C-20260305-802` 文档门禁对齐到新目录
- `C-20260305-901` Doc-loop 治理维护职责显式化（IBM+G）

### 新增到 P1-后续
- `C-20260305-803` Deferred 资产选择性迁移执行器

## 变更（2026-03-05 治理编译链对齐）

### 新增到 P0-核心
- `C-20260305-902` Governance Alignment Compiler for Skills / Hooks / Bin

## 变更（2026-03-05 字段收敛与口径统一）

- 候选字段统一：`promoted_issue_path`、`milestone`、`session_refs` 不再留空，统一使用显式 pending/空列表值。
- 路由口径统一：`doc-loop(IBM)` 统一升级为 `doc-loop(IBM+G)`，匹配当前治理职责定义。

## 变更（2026-03-05 pre-test-merge 职责迁移）

### 新增到 P0-核心
- `C-20260305-903` `pre-develop` -> `pre-test-merge` 职责迁移
- `C-20260305-904` `wt-enter` / `post-checkout` worktree 引导修复

## 变更（2026-03-06 hooks 安装模式）

### 新增到 P0-核心
- `C-20260306-001` Freely 托管 hooks 默认落在 `.freely/.githooks`
- `C-20260306-002` Hooks 托管模式前端开关与用户接管退出路径

## 变更（2026-03-06 标准 worktree 提示统一）

### 新增到 P0-核心
- `C-20260306-1001` 标准 `git worktree` 提示统一

## 变更（2026-03-06 issue 绑定头脑风暴路由）

### 新增到 P0-核心
- `C-20260306-1101` `auto-loop-lead-agent.md`
- `C-20260306-1102` `context-source-skill.md`
- `C-20260306-1103` `no-skill.md`
- `C-20260306-1104` `has-skill.md`
- `C-20260306-1105` `auto-loop-orchestrator` / guidance 对齐到两层 auto-loop 模型

## 变更（2026-03-08 状态联动与会话证据治理）

### 新增到 P0-核心
- `C-20260308-0101` 状态联动、流程标识词典与 session evidence 传播治理

## 变更（2026-03-08 premerge / pre-test-merge 收敛批次）

### 批次背景
- 目的：收敛 `feature/governance-alignment-hardening-20260305`、`feature/issue-brainstorm-routing-guard-20260306`、`feature/state-sync-and-session-evidence-governance-20260308`
- 临时验证路径：
  - `pre-test-merge`
  - `feature/premerge-20260308-0235--governance-convergence`
- 原因：旧 feature 与当前 `develop` 在治理文档、hooks 与路由模型上出现高冲突，直接顺序 merge 风险高

### 合并与验证证据
- `feature/state-sync-and-session-evidence-governance-20260308` 先固化为提交 `efca6c4`
- `feature/premerge-20260308-0235--governance-convergence` 收敛提交链：
  - `85a10eb` merge `feature/governance-alignment-hardening-20260305`
  - `a08ba20` merge `feature/issue-brainstorm-routing-guard-20260306`
  - `b4eeb8b` merge `feature/state-sync-and-session-evidence-governance-20260308`
  - `d74a543` 修复历史 candidate 字段格式，消除当时的治理检查阻塞（现命名为 `governance-check`）
- `pre-test-merge` 验证批次提交：`454d0e3`
- 提升到 `develop` 的提交：`64cd6d4`
- 验证命令与结果：
  - `./bin/wt-status-all` -> `CLEAN`
  - `./bin/bmad-check` -> `passed`（现命名为 `./bin/governance-check`）
  - `./bin/test-pre-push-hook` -> `pass=6 fail=0`

### cleanup 结果
- 已删除本地分支与 worktree：
  - `feature/premerge-20260308-0235--governance-convergence`
  - `pre-test-merge`
  - `feature/state-sync-and-session-evidence-governance-20260308`
  - `feature/governance-alignment-hardening-20260305`
  - `feature/issue-brainstorm-routing-guard-20260306`
  - `feature/loop-routing-derived-worktree-governance-20260307`
  - `feature/ai-tool-worktree-directory-access-20260307`
  - `feature/freely-githooks-install-strategy-20260306`
  - `feature/worktree-date-prefix-20260307`
  - `feature/worktree-naming-doc-sync-20260307`
- 当前 worktree 卫生状态：
  - 仅保留主工作树 `develop`
  - `./bin/wt-status-all` 汇总：`total=1, dirty=0`

## 变更（2026-03-08 阶段前缀式进度标识）

### 收敛结论
- `C-20260308-1631` 用阶段前缀式主进度标识替代 `in_progress` / `active`
  - 问题：现有主状态词无法从值本身看出阶段，仍需要额外字段拼读
  - 结论：采用 `phase_state=<prefix>_<stage>`，如 `in_ibm`、`done_ibm`、`in_dev`
  - 吸收关系：`20260308-1500--milestone-state-identifier-refinement` 仅作为前置探索保留，不再单独 materialize
  - 已完成实现落点：`docs/LAWS.md`、`docs/PROJECT_INTENT.md`、`docs/milestones.md`、`docs/system/workspace/skills/context-source-skill/SKILL.md`、`docs/system/workspace/skills/doc-ibm-execution/SKILL.md`、`docs/system/workspace/skills/dev-loop-execution/SKILL.md`
  - 验证证据：`./bin/bmad-check` 于 2026-03-08 通过（现命名为 `./bin/governance-check`）；全文检查未发现 `status=in_progress`、`milestone_state=in_progress`、`ready_for_dev` 回流到正式治理口径
  - 当前状态：completed，作为 `I-20260308-1631` 进入 milestone completed_issues

## 变更（2026-03-08 业务阻塞与系统崩溃恢复分层）

### 收敛结论
- `C-20260308-1931` 业务阻塞状态与系统崩溃恢复定位治理
  - 问题：`blocked_*` 容易与 PID 消失、CLI 崩溃等系统事件混用，导致恢复时伪造 AI 交接
  - 结论：把业务阻塞和系统崩溃明确分层；系统崩溃先做恢复定位，不直接改 `phase_state`
  - 已完成实现落点：`docs/LAWS.md`、`docs/system/workspace/skills/context-source-skill/SKILL.md`、`docs/system/workspace/skills/recovery-subagent-governance/SKILL.md`、`docs/milestones.md`
  - 验证证据：`./bin/bmad-check` 于 2026-03-08 通过（现命名为 `./bin/governance-check`）；全文检查确认 `blocked_*` 仅作为业务阻塞口径出现在正式治理资产中，系统崩溃统一先走 recovery 判定
  - 当前状态：completed，作为 `I-20260308-1931` 进入 milestone completed_issues

## 变更（2026-03-08 里程碑状态标识符语义收敛）

### 收敛结论
- `C-20260308-1501` 里程碑状态标识符重命名与职责边界收紧
  - 问题：`milestone_state=in_progress` 与 `loop_stage` 存在语义重叠
  - 初步方案：将 `in_progress` 改为 `active`，`completed` 改为 `delivered`
  - 后续处理：该方案已被 `20260308-1630--stage-prefixed-progress-identifier` 吸收并替代，不再单独进入 milestone 或 issue materialization
  - 当前状态：dropped，保留为前置探索记录

## 变更（2026-03-16 首跳同工具第二跳 dev-loop 验证）

### 等价执行证据
- issue: `I-20260307-1201`
- phase_state: `in_verification`
- branch: `feature/dogfood-codex-auto-20260316`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260316-feature-dogfood-codex-auto`

## 变更（2026-03-18 checkpoint commit 与多 worktree 监督治理）

### 收敛结论
- `C-20260317-0735-B` 与 `C-20260317-0735-C` 已合并物化为 `I-20260318-0930`
  - 问题：当前 Freely runtime 能续跑会话，但不会在 dirty tree 持续扩大时主动要求 checkpoint，也没有项目级多 worktree 摘要来做主管视角判断。
  - 结论：runtime/status 必须暴露 `project dirty entries` 与 `worktree dirty summary`，并把 dirty-budget 进入 prompt / handoff / rotation 判定。
  - 当前落点：`docs/LAWS.md`、`docs/system/workspace/scripts/runtime/freely`、`docs/milestones.md`、`docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
  - 当前状态：in_dev
- 原因：当前研究阶段尚未启用正式 `docs/progress/**` / `docs/recovery/**`，按宪法与法律允许把 dev-loop 验证批次临时写入本文件。

### 验证范围
- 首跳 prompt 明确禁止只输出 `next_prompt` 结束。
- 同工具场景必须在当前会话继续进入第二跳。
- monitor/runtime 参数面继续覆盖 `reasoning_effort` 与真实 pid 留痕。

### 已执行 TEST
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
- `bash tests/test_doc_gate.sh`

### review 证据
- `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/code-reviews/20260316-first-hop-second-hop-verification.md`

### promote 前置检查
- `./bin/wt-status-all`
- 结果摘要：
  - `DIRTY | feature/dogfood-codex-auto-20260316 | /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260316-feature-dogfood-codex-auto`
  - `Summary: total=6, dirty=1`

### 当前结论
- `I-20260307-1201` 已从 `done_ibm` 推进到 `in_verification`。
- 现有脚本与治理文档改动已满足本轮最小验证要求，review 证据也已落盘。
- 由于当前 feature worktree 仍为 `DIRTY`，本轮不能进入 promote / cleanup，因此不宣告 `completed`。

### continuity refresh
- context_ratio_warn: `0.5577 >= 0.50`
- route_decision: 当前 issue `I-20260307-1201` 的下一有效动作已收敛为 clean worktree + promote / cleanup，当前轮次不重复在同一 verification 上空转。
- next_focus: `I-20260308-0101`
- next_route: `doc-ibm-execution`

## 变更（2026-03-16 状态同步治理 verification）

### 等价执行证据
- issue: `I-20260308-0101`
- phase_state: `in_verification`
- branch: `feature/dogfood-codex-auto-20260316`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260316-feature-dogfood-codex-auto`
- 原因：当前研究阶段尚未启用正式 `docs/progress/**` / `docs/recovery/**`，按宪法与法律允许把本轮 verification 批次临时写入本文件。

## 变更（2026-03-17 Rust/Tauri bridge contract 对齐 frontend 当前消费面）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- route: `milestone -> dev-loop-execution`
- selected_tool: `codex`
- why_selected: 当前最高优先池仍是 `docs/milestones.md`，且 `I-20260317-1005` 已是 committed + `in_dev`，工作内容是仓库内 Rust/Tauri bridge 实现与状态回写，明显更适合当前会话直接执行而不是交回 runtime
- next_prompt_summary: 继续在同会话内收紧 backend bridge 与 frontend probe 的真实 contract，而不是只追加文档或抽象 reducer 拆分

### 本轮收敛
- `probe_request_snapshot` 已从旧的 Rust 内部 shape 收紧为 frontend 当前真实消费的 `ProbeSnapshot` 形状：
  - `projectSummary`
  - `activeSessions`
  - `activeRuns`
  - `activeAgents`
  - `terminalTargets`
  - `governanceSummary`
  - `recoverySummary`
  - `lastEventId`
- `probe_send_command` 已从旧的 `(project_id, command, payload)` 三段式 Tauri 入参，改为直接接收 frontend 当前发送的单个 `ClientCommand` 形状，并在 Rust 侧解析 `projectId/type`
- `probe_server_event` 已从泛化包装对象收紧为 frontend `ServerEvent` 形状
- `ControlRun` 现在一次发出：
  - `RunStatusChanged`
  - `AgentStatusChanged`
  - `TerminalChunkAppended`
- `CreateOrResumeSession` 发出 `SessionUpserted`
- `SendChatIntervention` 发出 `InputArbitrationRecorded`

### 涉及产物
- `src-tauri/src/model.rs`
- `src-tauri/src/state.rs`
- `src-tauri/src/lib.rs`
- `src-tauri/src/bridge_logic.rs`
- `src-tauri/src/event_payload.rs`
- `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- `docs/milestones.md`

### 验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前 blocker
- blocker 本质未变：当前机器缺少 Rust toolchain，仍无法执行 `cargo check/test`
- 但 blocker 已不再被 frontend/backend contract 漂移掩盖；一旦进入具备 `cargo` 的环境，可直接围绕当前 snapshot / command / event 三条面对齐结果做最小编译验证与联调

## 变更（2026-03-17 Rust typed payload 继续对齐 ClientCommand 字段语义）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- route: `milestone -> dev-loop-execution`
- selected_tool: `codex`
- why_selected: 当前仍是 committed + `in_dev` 的 backend bridge continuation，工作内容是仓库内 Rust/Tauri bridge 语义收口与状态回写，适合在当前会话直接继续

### 本轮收敛
- `src-tauri/src/command_payload.rs` 现在不再只解析抽象的 `action/title/content`
- 已对齐 frontend 当前真实发送的最小字段子集：
  - `ControlRun.runId/action/reason`
  - `CreateOrResumeSession.sessionId/resumeHint/commandSource`
  - `SendChatIntervention.sessionId/messageId/content/runId/targetAgentId`
- 这些字段现在已经真实进入 backend 行为层，而不只是被解析：
  - 指定 `runId` 会驱动 active run 与 terminal target
  - 指定 `sessionId` 会驱动 active session
  - `resumeHint` 会进入 session ack 与 governance summary

### 涉及产物
- `src-tauri/src/command_payload.rs`
- `src-tauri/src/bridge_logic.rs`
- `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- `docs/milestones.md`
- `docs/pre-brainstorms/CONVERGENCE.md`

### 验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前 blocker
- blocker 未变，仍是缺少 Rust toolchain
- 但现在 backend bridge 不仅外形对齐 frontend contract，连 command payload 的字段语义也已开始对齐，后续进入有 `cargo` 的环境后可以更直接做最小联调

## 变更（2026-03-17 commandSource / reason / messageId 进入 bridge 行为层）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- route: `milestone -> dev-loop-execution`
- selected_tool: `codex`
- why_selected: 当前仍是 committed + `in_dev` 的 backend bridge continuation，工作内容是仓库内 Rust/Tauri bridge 语义收口与状态回写，适合继续在当前会话执行

### 本轮收敛
- `CreateOrResumeSession.commandSource` 已进入 `SessionUpserted.source`
- `ControlRun.reason` 已进入 pause recovery 文案与 terminal chunk 文案
- `SendChatIntervention.messageId` 已进入 `InputArbitrationRecorded.details`
- 这让 backend bridge 对 frontend 当前真实发送值的利用又前进了一层，不再只是解析字段但不消费

### 涉及产物
- `src-tauri/src/event_payload.rs`
- `src-tauri/src/bridge_logic.rs`
- `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- `docs/milestones.md`
- `docs/pre-brainstorms/CONVERGENCE.md`

### 验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前 blocker
- blocker 仍未变化，依旧是缺少 Rust toolchain
- 但 bridge 现在已经不只是 contract 外形对齐，而是开始对齐 frontend 已发送字段的最小行为语义

## 变更（2026-03-17 targetAgentId / runId 进入 chat intervention 行为层）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- route: `milestone -> dev-loop-execution`
- selected_tool: `codex`
- why_selected: 当前仍是 committed + `in_dev` 的 backend bridge continuation，工作内容是仓库内 Rust/Tauri bridge 语义收口与状态回写，适合继续在当前会话执行

### 本轮收敛
- `SendChatIntervention.targetAgentId` 已开始驱动 active agent 标识
- `SendChatIntervention.runId` 已开始驱动 active run 与 terminal target
- chat governance summary 与 `InputArbitrationRecorded.details` 现在会一起带出 `sessionId/messageId/targetAgentId/runId`
- 这让 chat intervention 在 backend 里不再只是“收到一段文本”，而是开始保留“发给谁、落在哪个 run”这层最小联调语义

### 涉及产物
- `src-tauri/src/bridge_logic.rs`
- `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- `docs/milestones.md`
- `docs/pre-brainstorms/CONVERGENCE.md`

### 验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前 blocker
- blocker 仍未变化，依旧是缺少 Rust toolchain
- 但 backend bridge 现在连 chat intervention 的目标 agent / run 语义也开始保留了，后续在有 `cargo` 的环境中更容易做 probe 联调

## 变更（2026-03-17 Rust bridge compile hygiene cleanup）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- route: `milestone -> dev-loop-execution`
- selected_tool: `codex`
- why_selected: 当前仍是 committed + `in_dev` 的 backend bridge continuation，这轮动作是继续清掉后续 `cargo check` 会先暴露的低成本 Rust 噪音

### 本轮收敛
- `src-tauri/src/bridge_logic.rs` 测试中残留的未使用 `ProbeEventKind` 引用已删除
- 这是纯 compile hygiene，但能减少后续进入真实 Rust 编译验证时的无关噪音

### 涉及产物
- `src-tauri/src/bridge_logic.rs`
- `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- `docs/pre-brainstorms/CONVERGENCE.md`

### 验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前 blocker
- blocker 仍未变化，依旧是缺少 Rust toolchain
- 但当前桥接代码里已知的一处低成本 compile 噪音已先清掉

## 变更（2026-03-17 backend projectName 规则对齐 frontend title-case）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- route: `milestone -> dev-loop-execution`
- selected_tool: `codex`
- why_selected: 当前仍是 committed + `in_dev` 的 backend bridge continuation，这轮动作是继续消除未来 mock/runtime 联调时的小型 contract 漂移

### 本轮收敛
- `src-tauri/src/state.rs` 新增 `to_project_name`
- backend 默认 `projectName` 已对齐 frontend 当前 mock/runtime 的 title-case 逻辑
- 例如 `my-project` 现在在 Rust snapshot 中会产出 `My Project`，不再是旧的 `Project my-project`

### 涉及产物
- `src-tauri/src/state.rs`
- `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- `docs/milestones.md`
- `docs/pre-brainstorms/CONVERGENCE.md`

### 验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前 blocker
- blocker 仍未变化，依旧是缺少 Rust toolchain
- 但 backend 默认 snapshot 的展示语义现在也与 frontend 当前运行时逻辑对齐了

## 变更（2026-03-17 backend 默认 session/run/terminal 命名对齐 frontend mock）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- route: `milestone -> dev-loop-execution`
- selected_tool: `codex`
- why_selected: 当前仍是 committed + `in_dev` 的 backend bridge continuation，这轮动作是继续清理 mock transport 与真实 Tauri bridge 初始状态之间的默认值漂移

### 本轮收敛
- `src-tauri/src/state.rs` 的默认命名已对齐 frontend mock 约定：
  - `sessionId -> <projectId>-session-1`
  - `runId -> <projectId>-run-1`
  - `terminalTarget -> <projectId>-run-1:pty-0`
- 这样未来比较 mock transport 与真实 bridge 的初始 snapshot 时，不再多出一层无意义的 ID 命名差异

### 涉及产物
- `src-tauri/src/state.rs`
- `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- `docs/milestones.md`
- `docs/pre-brainstorms/CONVERGENCE.md`

### 验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前 blocker
- blocker 仍未变化，依旧是缺少 Rust toolchain
- 但 mock 与真实 bridge 的默认初始状态命名现在也更一致了

## 变更（2026-03-17 backend 默认 lastEventId 对齐 frontend mock）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- route: `milestone -> dev-loop-execution`
- selected_tool: `codex`
- why_selected: 当前仍是 committed + `in_dev` 的 backend bridge continuation，这轮动作是继续消除 mock transport 与真实 Tauri bridge 初始 snapshot 的默认值漂移

### 本轮收敛
- `src-tauri/src/state.rs` 的默认 `lastEventId` 已从 `event-0` 调整为 `event-1`
- 这样 frontend mock 与真实 bridge 的初始 snapshot 在最小事件计数面也更一致

### 涉及产物
- `src-tauri/src/state.rs`
- `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- `docs/milestones.md`
- `docs/pre-brainstorms/CONVERGENCE.md`

### 验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前 blocker
- blocker 仍未变化，依旧是缺少 Rust toolchain
- 但 mock 与真实 bridge 的初始事件计数默认值现在也更一致了

## 变更（2026-03-17 Rust/Tauri bridge reducer 抽离）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- branch: `feature/dogfood-codex-auto-20260316`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260316-feature-dogfood-codex-auto`

### 本轮变更
- 新增 `src-tauri/src/bridge_logic.rs`
- `probe_send_command` 的最小 day-1 bridge reducer 已从 `src-tauri/src/lib.rs` 抽离到纯后端逻辑模块
- `lib.rs` 现在只保留 Tauri command 注册、state 接线和 `probe_server_event` 发射
- `bridge_logic.rs` 增补了最小测试骨架，覆盖：
  - `ControlRun -> RunStatusChanged`
  - `CreateOrResumeSession -> SessionUpserted`

### 本轮验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前结论
- 当前路由仍是 `milestones -> I-20260317-1005 -> dev-loop-execution`
- 本轮新增价值是把 Rust bridge 的语义处理与 Tauri 壳解耦，后续在具备 Rust toolchain 的环境中可直接围绕 reducer 补 `cargo test/check`
- blocker 未变化，仍是本地缺少 Rust toolchain，而不是 bridge reducer 缺位

## 变更（2026-03-17 Rust bridge control action 对齐）

### 等价执行证据
- issue: `I-20260317-1005`
- phase_state: `in_dev`
- branch: `feature/dogfood-codex-auto-20260316`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260316-feature-dogfood-codex-auto`

### 本轮变更
- `src-tauri/src/bridge_logic.rs` 的 `ControlRun` reducer 已开始读取最小 payload `action`
- day-1 action 子集现在显式对齐：
  - `start/resume/retry -> running`
  - `pause -> paused`
  - `terminate -> terminated`
- `pause` 会同步写入 agent blocker 与 `recovery_summary`
- 补了对应的 reducer 测试骨架

### 本轮验证
- `bun run typecheck` -> passed
- `bun run rust:preflight` -> failed
  - `[missing] cargo`
  - `[missing] rustc`
  - `[missing] rustup`

### 当前结论
- 当前路由仍是 `milestones -> I-20260317-1005 -> dev-loop-execution`
- 本轮新增价值是让 backend day-1 reducer 与 frontend 当前 control surface 再对齐一层
- blocker 仍未变化，依旧是本地缺少 Rust toolchain

### 已执行验证检查
- `rg -n "source_class|route_kind|phase_state|runtime_state|session_refs|done_ibm -> in_dev|in_verification|completion verification" docs/LAWS.md docs/PROJECT_INTENT.md docs/milestones.md docs/system/workspace/skills/context-source-skill/SKILL.md docs/system/workspace/skills/doc-ibm-execution/SKILL.md docs/system/workspace/skills/dev-loop-execution/SKILL.md`

### review 证据
- `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/code-reviews/20260316-state-sync-verification.md`

### continuity refresh
- context_ratio_warn: `0.5997 >= 0.50`
- route_decision: `I-20260308-0101` 已从 `done_ibm` 推进到 `in_verification`，当前轮次不重复停留在 doc-loop handoff。
- next_route: `completion_verification`

### completion verification 前置检查
- `./bin/wt-status-all`
- 结果摘要：
  - `DIRTY | feature/dogfood-codex-auto-20260316 | /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260316-feature-dogfood-codex-auto`
  - `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.6266 >= 0.50`
- route_decision: `I-20260308-0101` 的下一有效动作已收敛为 clean worktree + completion verification / cleanup，本轮不重复生成新的 verification 产物。
- next_route: `completion_verification`

### continuity refresh
- context_ratio_warn: `0.6526 >= 0.50`
- route_decision: 当前 issue 仍是 `I-20260308-0101`，且 blocker 未变化；在 worktree 清洁前不继续生成新的 verification / completion 产物。
- next_route: `completion_verification`

### continuity refresh
- context_ratio_warn: `0.6862 >= 0.50`
- route_decision: 当前 issue 仍是 `I-20260308-0101`，completion blocker 依旧是 dirty worktree；本轮继续只维护 continuity，不重开 doc-loop / dev-loop 产物。
- next_route: `completion_verification`

### continuity refresh
- context_ratio_warn: `0.6933 >= 0.50`
- route_decision: 当前 issue 与 blocker 均未变化；继续等待 clean worktree，再进入 completion verification / cleanup。
- next_route: `completion_verification`

### continuity refresh
- context_ratio_warn: `0.6999 >= 0.50`
- route_decision: 当前 issue 仍为 `I-20260308-0101`，阻塞条件仍为 dirty worktree；本轮继续只维护 continuity。
- next_route: `completion_verification`

### continuity refresh
- handoff_context: `fresh_with_handoff` after `context_usage_threshold`; 当前轮次已吸收上一轮交接并重新执行首跳闭环。
- demand_pool_priority:
  - `milestones`: 最高优先；`I-20260308-0101` 仍在 `committed_issues` 且 `phase_state=in_verification`
  - `progress/recovery`: 正式目录仍未启用，本研究阶段等价 continuity 继续写入本文件
  - `review/test`: 最小证据已存在，不构成新的更高优先入口
  - `human chat / session evidence`: 仅提供 continuity/handoff，不产生新的稳定 issue 边界
  - `github issue`: 当前仓库内无比 milestone continuation 更高优先的本地输入
  - `PROJECT_INTENT`: 仍是长期发现源，但当前不覆盖已承接且未完成的 committed issue
- route_classification:
  - source_class: `continuation`
  - route_kind: `completion_verification`
  - route_reason: 当前输入带有明确 handoff、活跃 milestone issue 与现存 verification 证据；不属于新的 `pre-brainstorm` 或新的 issue-bound brainstorm
- tool_selection:
  - selected_tool: `codex`
  - why_selected: 当前工作是对已明确 issue 执行仓库内 continuity/verification 回写；`codex` 更匹配现有 worktree 中的直接读写，且与当前 `AI_TOOL` 一致，可立即进入第二跳
  - target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification` continuation only)
  - next_prompt: `继续承接 I-20260308-0101 的 completion_verification。先把本轮 lead-agent/context-source-skill 的池扫描、优先级与工具选择写入当前 continuity artifact；保持 source_class=continuation、route_kind=completion_verification。若 ./bin/wt-status-all 仍为 DIRTY，则不要重开 doc-loop/dev-loop 实现，只记录 blocker 未变并等待 clean worktree；若转为 CLEAN，再补 completion verification / cleanup 证据并推进 milestone/issue 到 completed。`

### continuity refresh
- first_hop_recheck: 本轮重新执行 `constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill`，结论与上一轮一致。
- pool_revalidation:
  - `milestones`: 仍优先于其他池；当前唯一已命中并可继续执行的是 `I-20260308-0101`
  - `progress/recovery`: 规范目录仍不存在，因此不触发 recovery route
  - `review/test`: `pre-tests` 与 code-review 均已存在，当前只剩 completion blocker
  - `human chat / session evidence`: 只提供“重跑首跳”的输入，不改变 issue 边界
  - `github issue`: 规则存在，但当前仓库无更高优先的外部输入落点
  - `PROJECT_INTENT`: 继续作为发现源保留，但不会覆盖未完成的 committed verification
- route_revalidation:
  - current_problem_kind: `issue continuation`
  - why_not_pre_brainstorm: 已有稳定 issue 边界与正式 issue 文档
  - why_not_issue_bound_brainstorm: IBM 产物、review 与 verification 检查已齐，不缺 `b-issue/prd/pre-tests/tasks`
  - why_this_next_hop: `phase_state=in_verification`，按 milestone routing 只做 completion verification 回写，不重开实现
- execution_guard:
  - workspace_action: `continue_current_worktree`
  - execution_base: `develop`
  - integration_target: `develop`
  - depends_on: `none`
  - blocker: `./bin/wt-status-all` 仍为 `DIRTY`; `Summary: total=6, dirty=1`

### continuity refresh
- first_hop_rerun: 用户再次要求进入首跳闭环；本轮按最小复核重新确认池优先级、issue 分类与同工具第二跳义务。
- selected_pool: `milestones`
- why_selected_pool: committed issue `I-20260308-0101` 仍处于 `in_verification`，其 completion blocker 明确且尚未解除；这比 discovery 类来源更接近可执行收口。
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作仍是仓库内 verification continuity 回写，不是新的 research/doc materialization；`codex` 与当前 `AI_TOOL` 一致，可直接在同会话执行第二跳。
- target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification`)
- next_prompt: `继续承接 I-20260308-0101 的 completion_verification continuation。保持 milestones 为当前最高优先池、保持 current_problem_kind=issue continuation。若 wt-status-all 仍是 DIRTY，则仅维护 continuity artifact，不重开实现或 IBM；若变为 CLEAN，再补 completion verification / cleanup 并推进 completed。`
- blocker_recheck: `./bin/wt-status-all` 结果未变，仍为 `Summary: total=6, dirty=1`

### continuity refresh
- first_hop_minimal_recheck: 本轮再次执行首跳最小复核，优先验证 milestone/issue 事实与 blocker 是否变化。
- facts_reconfirmed:
  - `docs/milestones.md` 仍将 `I-20260308-0101` 置于 `committed_issues` 且 `phase_state=in_verification`
  - issue 文档仍要求保持 `in_verification`，直到 clean worktree 后补 completion verification / cleanup
  - `./bin/wt-status-all` 仍返回 `Summary: total=6, dirty=1`
- unchanged_decision:
  - selected_pool: `milestones`
  - current_problem_kind: `issue continuation`
  - selected_tool: `codex`
  - target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification`)
  - why_continue_same_route: 当前没有新的 `pre-brainstorm` 输入，也没有缺失 IBM 产物；唯一有效动作仍是等待 worktree 清洁后继续 completion 收口

### continuity refresh
- first_hop_review_recheck: 本轮把 review/test 池作为辅助校验再次复核。
- review_test_status:
  - code-review 仍为 `no blocking findings`
  - verification checks 已存在，未暴露需要回退到 IBM 或 pre-brainstorm 的新问题
  - residual_risk 仍是未形成 promote / cleanup 证据
- routing_confirmation:
  - selected_pool: `milestones`
  - current_problem_kind: `issue continuation`
  - selected_tool: `codex`
  - target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification`)
  - why_not_handoff: `selected_tool` 与当前 `AI_TOOL` 相同，且当前仍能在本会话内完成 continuity 回写
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- first_hop_lead_agent_reentry: 用户要求重新进入 Freely 首跳闭环；本轮按 `constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill` 完成最小复核并继续第二跳。
- demand_pool_priority:
  - `milestones`: 当前最高优先；`I-20260308-0101` 仍在 `committed_issues` 且 `phase_state=in_verification`
  - `progress/recovery`: 正式目录仍未启用，continuity 继续等价写回本文件
  - `review/test`: 提供辅助验证，但未暴露比 milestone continuation 更高优先的新问题
  - `human chat / session evidence`: 提供本轮首跳重跑输入，但未形成新的稳定 issue 边界
  - `github issue`: 当前仓库无比现有 committed verification 更高优先的外部输入
  - `PROJECT_INTENT`: 保留为长期发现源，但不覆盖未完成的 committed issue
- route_classification:
  - source_class: `continuation`
  - route_kind: `completion_verification`
  - current_problem_kind: `issue continuation`
  - why_not_pre_brainstorm: 已有稳定 issue 边界与正式 issue 文档
  - why_not_issue_bound_brainstorm: `b-issue/prd/pre-tests/tasks` 与 review 已齐，当前不缺 IBM 产物
- tool_selection:
  - selected_tool: `codex`
  - why_selected: 当前动作是仓库内 verification continuity 与证据回写；`codex` 比 `iflow` 更适合直接修改现有 issue/review/continuity 产物，且与当前 `AI_TOOL` 相同，可直接继续第二跳
  - target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification`)
  - next_prompt: `继续承接 I-20260308-0101 的 completion_verification continuity。保持 milestones 为当前最高优先池，保持 current_problem_kind=issue continuation。把本轮 lead-agent/context-source-skill 的池扫描、优先级、selected_tool=codex、target_skill=dev-loop-execution 写回 continuity artifact；若 ./bin/wt-status-all 仍为 DIRTY，则不要重开 IBM 或实现，只记录 blocker 未变并等待 clean worktree；若转为 CLEAN，再补 completion verification / cleanup 证据并推进 completed。`
- verification_recheck:
  - `rg` 词典/状态检查已通过
  - `./bin/wt-status-all`: `Summary: total=6, dirty=1`
  - `./bin/governance-check`: 当前环境下因 `mapfile` / `find -printf` 兼容性失败，不能计作通过证据

### continuity refresh
- first_hop_rule_recheck: 本轮补做“规则引用是否仍支撑当前路由”的快速复核。
- pool_and_route_confirmation:
  - `PROJECT_INTENT` 仍要求扫描 `milestones/progress/code-reviews/test/chat/github-issue`
  - `milestones.md` 仍把 `phase_state=in_verification` 留在 committed 队列直到 completion evidence 回写
  - `lead-agent` 仍要求同工具场景在当前会话继续第二跳，而不是只输出 `next_prompt`
- unchanged_result:
  - selected_pool: `milestones`
  - current_problem_kind: `issue continuation`
  - selected_tool: `codex`
  - target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification`)
  - why_same_result: 规则层和仓库事实层都没有变化，且 blocker 仍是 dirty worktree
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- first_hop_compact_recheck: 本轮继续执行首跳闭环，但只保留最小结论。
- compact_result:
  - selected_pool: `milestones`
  - current_problem_kind: `issue continuation`
  - selected_tool: `codex`
  - target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification`)
  - blocker: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`
  - why_no_route_change: 既没有新的 discovery 输入，也没有 cleanup 条件满足，因此继续维护 continuity 而不是切换路由

### continuity refresh
- first_hop_no_change: 本轮首跳复核未发现任何新入口或状态变化。
- unchanged_result:
  - selected_pool: `milestones`
  - current_problem_kind: `issue continuation`
  - selected_tool: `codex`
  - target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification`)
  - blocker: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- first_hop_still_unchanged: 结论未变；继续等待 clean worktree 后再推进 completion verification / cleanup。

### continuity refresh
- first_hop_still_same: `milestones -> issue continuation -> codex -> completion_verification` 结论保持不变。

### continuity refresh
- first_hop_no_delta: dirty worktree blocker 未解除，路由结论无增量。

### continuity refresh
- first_hop_no_progress: blocker 仍在，继续保持当前路由与等待条件。

### continuity refresh
- first_hop_waiting: 继续等待 clean worktree。

### continuity refresh
- first_hop_standby: 状态未变，继续待命。

### continuity refresh
- context_ratio_warn: `0.5018 >= 0.50`
- phase_artifact: 当前为 verification continuation；研究阶段等价 continuity 继续写入本文件。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5112 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5208 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5303 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5398 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5493 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5588 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5683 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5779 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5874 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- context_ratio_warn: `0.5969 >= 0.50`
- phase_artifact: 当前仍为 verification continuation；先更新 continuity，再继续当前 issue。
- route_status: `milestones -> issue continuation -> codex -> completion_verification`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### continuity refresh
- session_rotation: `fresh session with handoff`
- handoff_absorbed:
  - previous_tool_session_id: `019cfa61-b626-7452-820d-c8f1c13c4b0f`
  - previous_tool_jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/03/16/rollout-2026-03-16T23-00-33-019cfa61-b626-7452-820d-c8f1c13c4b0f.jsonl`
  - previous_cycle_log: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260316-feature-dogfood-codex-auto/.freely/logs/cycle-20260316-232319.log`
- first_hop_rerun:
  - governance_guard: `constitution-guard -> laws-enforcer`
  - lead_agent: `workspace/agents/lead-agent.md`
  - delegated_skill: `workspace/skills/context-source-skill/SKILL.md`
- demand_pool_priority:
  - `milestones`: 最高优先；`I-20260308-0101` 仍在 `committed_issues` 且 `phase_state=in_verification`
  - `progress / recovery`: 正式目录尚未启用；研究阶段等价 continuity 继续写入本文件
  - `review / test`: 已有最小 review 与 verification 证据，不构成更高优先入口
  - `human chat / session evidence`: 当前只提供 resume handoff 与 fresh-session 连续性，不形成新的稳定 issue 边界
  - `github issue`: 当前仓库内无比现有 committed verification 更高优先的外部输入
  - `docs/PROJECT_INTENT.md`: 仍是长期 discovery 源，但不覆盖未完成的 committed issue continuation
- route_decision:
  - source_class: `continuation`
  - current_problem_kind: `issue continuation`
  - route_kind: `completion_verification`
  - why_not_pre_brainstorm: 已有稳定 issue 边界与正式 issue 文档
  - why_not_issue_bound_brainstorm: `b-issue/prd/pre-tests/tasks` 已齐，且当前 `phase_state=in_verification`
- tool_selection:
  - selected_tool: `codex`
  - why_selected: 当前动作是仓库内 continuity / verification 回写，且 `selected_tool` 与当前 `AI_TOOL` 相同，必须在本会话直接继续第二跳
  - target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification`)
  - next_prompt: `继续承接 I-20260308-0101 的 completion_verification continuation。保持 milestones 为当前最高优先池、保持 source_class=continuation 与 current_problem_kind=issue continuation。若 ./bin/wt-status-all 仍为 DIRTY，则仅维护 continuity artifact，不重开实现或 IBM；若变为 CLEAN，再补 completion verification / cleanup 并推进 issue/milestone 到 completed。`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`

### 当前结论
- 状态词典、联动矩阵与 session evidence 传播口径已在正式治理产物中对齐。
- 本轮已补齐最小 review / verification 证据，但由于当前 feature worktree 仍为 `DIRTY`，尚未形成 completion verification / cleanup 证据，因此不宣告 `completed`。

## 变更（2026-03-17 Frontend Probe v0 dev-loop skeleton）

### 等价执行证据
- issue: `I-20260317-1002`
- phase_state: `in_dev`
- branch: `feature/dogfood-codex-auto-20260316`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260316-feature-dogfood-codex-auto`
- 原因：当前研究阶段尚未启用正式 `docs/progress/**`，按宪法与法律允许把 dev-loop 等价进度写入本文件。

### 已更新产物
- `src/frontend_probe_v0/contracts.ts`
- `src/frontend_probe_v0/panels.ts`
- `src/frontend_probe_v0/index.ts`
- `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
- `docs/milestones.md`

### 当前结论
- 已落下 Probe v0 的最小实现骨架：contract types、panel view-model 和统一导出入口。
- 当前仍未进入完整 Tauri/React shell 实现；后续继续沿 `I-20260317-1002` 扩展。

### 增量（React shell）
- 已新增：
  - `src/frontend_probe_v0/mockSnapshot.ts`
  - `src/frontend_probe_v0/AppShell.tsx`
- 当前实现已从纯类型骨架推进到可消费 snapshot 的最小 React shell，但仍未接入真实 Tauri / Bun / build pipeline。

### 增量（adapter seam）
- 已新增：
  - `src/frontend_probe_v0/adapter.ts`
  - `src/frontend_probe_v0/useProbeRuntime.ts`
- 当前实现已具备从 adapter 请求 snapshot 的最小 seam；后续可把 `MockProbeAdapter` 替换成真实 Tauri bridge，而不需要重写 `AppShell`。

### 增量（Tauri bridge stub）
- 已新增：
  - `src/frontend_probe_v0/tauriAdapter.ts`
- 当前实现已具备 `TauriProbeAdapter` 骨架，可把 `probe_request_snapshot` / `probe_send_command` 映射到真实桌面 bridge；仍未接入实际 Tauri runtime。

### 增量（control actions）
- 已新增：
  - `src/frontend_probe_v0/commands.ts`
  - `src/frontend_probe_v0/useProbeControls.ts`
- `AppShell` 已能通过 adapter 触发最小 run control action，不再只是静态展示 panel summary。

### 增量（event seam）
- 已新增：
  - `src/frontend_probe_v0/events.ts`
  - `src/frontend_probe_v0/useProbeEvents.ts`
- 当前实现已具备最小事件订阅 seam；后续真实 bridge 接入后，shell 可从一次性 snapshot 过渡到 snapshot + event stream。

### 增量（Tauri event bridge）
- 已更新：
  - `src/frontend_probe_v0/tauriAdapter.ts`
- 当前 `TauriProbeAdapter` 已从单纯 invoke stub 推进到 `invoke + listen` 双通道骨架，可把 `probe_server_event` 映射到 shell 的 event seam。

### 增量（adapter factory）
- 已新增：
  - `src/frontend_probe_v0/createAdapter.ts`
- 当前实现已具备从 runtime 能力自动选择 `MockProbeAdapter` 或 `TauriProbeAdapter` 的最小接线入口，避免组件层手写分支。

### 增量（bootstrap entry）
- 已新增：
  - `src/frontend_probe_v0/bootstrap.tsx`
- 当前实现已具备最小装配入口，可把 runtime -> adapter -> shell 组装成统一 bootstrap 路径，而不是散落在调用方里。

### 增量（default entry）
- 已新增：
  - `src/frontend_probe_v0/entry.ts`
- 当前实现已具备默认宿主入口，可从 `window.__TAURI__` 读取 runtime 能力并创建 Probe app。

### 增量（mount helper）
- 已新增：
  - `src/frontend_probe_v0/mount.tsx`
- 当前实现已具备最小挂载辅助层；宿主可统一调用 `createDefaultProbeApp` 和 render，而不必自行拆解入口与组件。

### 增量（React host helper）
- 已新增：
  - `src/frontend_probe_v0/host.tsx`
- 当前实现已具备面向 `createRoot` 风格宿主的最小挂载辅助，宿主不必再手写 `entry -> bootstrap -> AppShell` 拆解逻辑。

## 变更（2026-03-17 Frontend Probe v0 reroute）

### reroute reason
- issue: `I-20260317-1002`
- previous_phase_state: `in_dev`
- new_phase_state: `blocked_dev`
- next_recommended_route: `doc-pre-brainstorm-execution`
- why: `frontend build/runtime baseline` 是当前 Probe v0 实现中暴露出来的边界外新问题；继续在同一 dev issue 内补样板已开始失真。

### new discovery artifact
- `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/brainstorms.md`
- `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/candidates.md`

## 变更（2026-03-17 Frontend Probe v0 unblock）

### unblock reason
- issue: `I-20260317-1002`
- previous_phase_state: `blocked_dev`
- new_phase_state: `in_dev`
- dependency_resolved_by: `I-20260317-1004`
- why: `frontend runtime baseline` 已完成最小 IBM 收敛，当前可以回到 Probe v0 的实现态，继续真实宿主接线

### continuity refresh
- first_hop_repeat_recheck: 用户再次要求进入首跳闭环；本轮重新执行最小门禁与需求池扫描。
- selected_pool: `milestones`
- why_selected_pool: `docs/milestones.md` 仍存在 committed issue，且 `I-20260308-0101` 继续处于 `phase_state=in_verification`；研究阶段正式 `progress/recovery` 目录尚未启用，因此 milestone continuation 仍高于其他 discovery 池。
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作仍是仓库内 continuity 回写与 blocker 复核，`codex` 比 `iflow` 更适合直接修改仓库产物，且与当前 `AI_TOOL` 相同，必须在当前会话继续第二跳。
- target_skill_or_loop: `skill:dev-loop-execution` (`completion_verification`)
- next_prompt: `继续承接 I-20260308-0101 的 completion_verification continuity。保持 milestones 为当前最高优先池，保持 current_problem_kind=issue continuation。若 ./bin/wt-status-all 仍为 DIRTY，则只维护 continuity artifact，不重开 IBM 或实现；若转为 CLEAN，再补 completion verification / cleanup 证据并推进 completed。`
- blocker_recheck: `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`
- blocker_detail:
  - `docs/system/workspace/**` 与 `tests/**` 仍存在 runtime / monitor / tests 未提交改动
  - `docs/epics/workspace-routing-foundation/**` 仍有 issue / review / verification 文档改动
  - `docs/pre-brainstorms/**` 仍有 session-rotation / first-hop 相关新增目录与 continuity 留痕

### continuity refresh
- dirty_ownership_mapping:
  - `docs/system/workspace/scripts/**`、`docs/system/workspace/tools.md`、`tests/test_doc_gate.sh` 主要对应 workspace-routing / session-lifecycle 相关治理与 runtime 变更，不属于可直接跳过的临时噪音
  - `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/**` 对应 `I-20260307-1201`
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/**` 对应 `I-20260308-0101`
  - `docs/pre-brainstorms/20260316-1800--session-lifecycle-rotation-and-handoff/`、`docs/pre-brainstorms/20260316-1838--context-window-aware-session-rotation/`、`docs/epics/workspace-routing-foundation/session-lifecycle-rotation-and-handoff-governance/` 对应已完成但尚未提交收束的 session-lifecycle 批次
  - `docs/pre-brainstorms/20260316-2202--first-hop-must-execute-second-hop/` 对应当前首跳闭环相关发现留痕
- routing_implication:
  - 当前最高优先池仍是 `milestones`，因为 `I-20260307-1201` / `I-20260308-0101` 仍在 committed verification
  - 但 dirty blocker 已明显跨 issue 批次；下一次真正解阻时，应先按 ownership 收束或分流未提交改动，而不是继续追加空转 verification 文本

### continuity refresh
- unblock_order_hint:
  1. 先处理 `docs/system/workspace/**`、`tests/**` 与 session-lifecycle 相关产物，确认它们是独立收束还是需要分流到单独批次
  2. 再回到 `I-20260307-1201` / `I-20260308-0101` 的 verification 文档批次，补齐仍缺的 completion / cleanup 证据
  3. 最后在 `./bin/wt-status-all` 变为 `CLEAN` 后推进 milestone 从 `in_verification` 到 `completed`
- why_this_order:
  - 当前 verification issue 本身的 review / checks 已存在，真正阻塞它们的是跨批次未提交改动，而不是缺少新的 verification 文本

## 变更（2026-03-17 Frontend Probe v0 host wiring fix）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `docs/milestones.md` 中 `M-20260308-frontend-probe-dogfooding-loop` 仍存在 `phase_state=in_dev` 的 committed issue，且 `I-20260317-1002` 已由 `I-20260317-1004` 解阻，当前最接近可执行实现
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内 Probe v0 实现推进与 continuity 回写；`codex` 最适合直接修改实现与 issue 文档，且与当前 `AI_TOOL` 相同，必须在当前会话继续第二跳
- target_skill_or_loop: `skill:dev-loop-execution`
- why_not_pre_brainstorm: 当前没有新的边界外问题；`frontend runtime baseline` 已被独立 issue 承接并收敛到 `done_ibm`
- why_not_issue_bound_brainstorm: `I-20260317-1002` / `I-20260317-1004` 的 IBM 已齐，当前瓶颈在实现接线，不在文档边界
- next_prompt: `继续承接 I-20260317-1002。保持 milestones 为当前最高优先池，保持 current_problem_kind=issue continuation。优先把已定义的 runtime baseline 真正接进宿主路径，避免继续补只增面积不增可运行性的样板。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/useProbeRuntime.ts`
  - `src/frontend_probe_v0/AppShell.tsx`
  - `src/frontend_probe_v0/bootstrap.tsx`
  - `src/frontend_probe_v0/entry.ts`
  - `src/frontend_probe_v0/mount.tsx`
  - `src/frontend_probe_v0/host.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `useProbeRuntime` 不再在每次 render 时重建 adapter，减少 snapshot 请求重复触发和宿主注入抖动
  - `bootstrap` 现在会为当前 runtime / projectId 绑定稳定的 `AppShell`
  - `mount` / `host` 现在把 React element 交给宿主，而不是把组件类型误当作 render payload
- residual_gap:
  - 真实 Tauri runtime 与 frontend build/test baseline 仍未接入，因此这轮仍属于 host wiring 修补，不宣称已可运行

## 变更（2026-03-17 Frontend Probe v0 mock runtime loop）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是 frontend milestone 中唯一处于 `in_dev` 的 committed issue，且其 blocker 已从“缺 baseline 定义”收敛到“继续推进真实接线”
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内实现推进，不是新的边界收敛；`codex` 更适合直接推进 `src/frontend_probe_v0/**`，且与当前 `AI_TOOL` 相同，必须在本会话继续第二跳
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先把 control/event/snapshot 的最小回路打通，让 Probe shell 至少能在 mock runtime 下表现出状态变化；在此基础上再接真实 Tauri runtime。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/adapter.ts`
  - `src/frontend_probe_v0/tauriAdapter.ts`
  - `src/frontend_probe_v0/useProbeRuntime.ts`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `MockProbeAdapter` 现已维护内部 snapshot 状态，并在 `ControlRun` 后发出 `RunStatusChanged`、`AgentStatusChanged`、`TerminalChunkAppended`
  - `useProbeRuntime` 会在 event-capable adapter 事件到达后自动重新请求 snapshot，使 shell 不再停留在首帧静态快照
  - `TauriProbeAdapter.subscribe` 已改为同步返回 cleanup 函数，避免 React effect cleanup 与异步订阅返回值语义不匹配
- residual_gap:
  - 仍未接入真实 frontend build/test baseline，这轮只证明最小 runtime seam 更接近可运行，不等于已完成宿主集成

## 变更（2026-03-17 Frontend Probe v0 panel rendering pass）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: 当前仍是 `I-20260317-1002` 这条 `in_dev` committed issue 最接近可执行；其他池没有比它更高优先的新边界
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 这轮工作是直接推进 Probe UI 实现，不是新的文档收敛；`codex` 更适合在仓库内连续修改 `src/frontend_probe_v0/**`
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先让最小 UI panel 真正消费 snapshot / events，把 control/session/agent/terminal 的最小反馈都显示出来，再考虑真实宿主接线。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/AppShell.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - control bar 现在展示当前 runId / status，并在没有 active run 时禁用 control buttons
  - chat intervention panel 现在展示 active sessions 与 recent decision/governance events
  - agent roster 现在展示 phase / lastAction / blocker
  - embedded terminal 现在展示 attachable target 与 recent terminal stream
- residual_gap:
  - 真实 message input 与真正的 Tauri runtime 仍未接入；当前只是把已存在的 mock snapshot / event seam 体现在 UI 上

## 变更（2026-03-17 Frontend Probe v0 chat intervention path）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；本轮没有更高优先的新 discovery 池信号
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续推进 Probe v0 的最小交互实现，`codex` 适合直接在仓库内补命令路径、hook 与 UI 交互
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先把 chat intervention panel 从只读状态推进到最小可提交的人类介入路径，并让 mock runtime 能回写仲裁结果。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/commands.ts`
  - `src/frontend_probe_v0/adapter.ts`
  - `src/frontend_probe_v0/useProbeChatIntervention.ts`
  - `src/frontend_probe_v0/AppShell.tsx`
  - `src/frontend_probe_v0/index.ts`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - 新增 `createChatInterventionCommand` 与 `useProbeChatIntervention`
  - `AppShell` 新增 intervention draft textarea 和 send button
  - `MockProbeAdapter` 现可处理 `SendChatIntervention` 并回写 `InputArbitrationRecorded`
  - chat panel 的 recent decisions 现在可展示介入内容本身，而不只是抽象 outcome
- residual_gap:
  - 这仍是 mock runtime 下的最小交互闭环；真实 Tauri bridge、真实 message delivery 与 frontend build/test baseline 仍未接入

## 变更（2026-03-17 Frontend Probe v0 session lifecycle path）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍然是当前唯一活跃的 frontend dev issue，且上一轮已把 chat intervention 打通，当前自然继续补最小会话控制面
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续推进 Probe v0 的最小交互流实现，`codex` 最适合直接修改 `src/frontend_probe_v0/**`
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先把 session create/resume 的最小交互流接进 chat panel，并让 mock runtime 能回写 SessionUpserted。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/commands.ts`
  - `src/frontend_probe_v0/useProbeSessionLifecycle.ts`
  - `src/frontend_probe_v0/adapter.ts`
  - `src/frontend_probe_v0/AppShell.tsx`
  - `src/frontend_probe_v0/index.ts`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - 新增 `createOrResumeSessionCommand` 与 `useProbeSessionLifecycle`
  - UI 新增 `create / resume session` 控件
  - `MockProbeAdapter` 现可处理 `CreateOrResumeSession` 并回写 `SessionUpserted`
  - chat panel 现在既能看到 session 列表，也能主动触发最小 session lifecycle 动作
- residual_gap:
  - 这仍是 mock runtime 下的最小 session lifecycle；真实 Tauri runtime、真实 session persistence 与 frontend build/test baseline 仍未接入

## 变更（2026-03-17 Frontend Probe v0 project switch path）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最可推进的 frontend dev issue；在 session/chat 最小交互打通后，下一步自然是补 PRD 中要求的 project switch
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作仍是 Probe v0 实现推进，`codex` 更适合直接改 UI state 与交互路径
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先把 project switch 从文档要求推进到最小可交互实现，让 snapshot / session / control / chat 都受当前 project 上下文驱动。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/AppShell.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - UI 新增 `Project Switch` selector
  - `selectedProjectId` 现在驱动 `useProbeRuntime`、`useProbeControls`、`useProbeChatIntervention`、`useProbeSessionLifecycle`
  - Probe shell 不再固定绑定单一 `freely` project id
- residual_gap:
  - project switch 目前仍是本地 mock 候选列表，不是来自真实项目清单或真实 Tauri runtime 的动态枚举

## 变更（2026-03-17 Frontend Probe v0 per-project mock state）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前前端实现主线；上一轮虽已加 `project switch`，但还缺真正的项目态隔离，因此本轮继续同一 dev issue
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续推进仓库内 mock runtime 与 UI 的一致性，`codex` 最适合直接修改 `src/frontend_probe_v0/**`
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先把 project switch 从单纯 UI 选择器推进成真正切换不同 project snapshot 的 mock runtime 路径。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/adapter.ts`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `MockProbeAdapter` 现按 `projectId` 用 map 维护独立 snapshot
  - `requestSnapshot` / `CreateOrResumeSession` / `SendChatIntervention` / `ControlRun` 都会命中对应 project 桶
  - project switch 现在会切到不同 project 的 sessionId / runId / terminalTarget / projectName，而不只是切换标题文字
- residual_gap:
  - 这仍是本地 mock runtime 的多项目模拟；真实项目枚举、真实 session persistence 与 Tauri runtime 注入仍未接入

## 变更（2026-03-17 Frontend Probe v0 project summary and bounded event buffer）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在多项目 mock state 已存在后，下一步自然是把 project-level summary 真正暴露到 UI
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续推进 Probe 观测面与状态呈现，`codex` 适合直接修改 shell 和 hook
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先把 projectName / governance / recovery 这些已有 snapshot 信息显示到 UI，并避免 event buffer 无界增长。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/AppShell.tsx`
  - `src/frontend_probe_v0/useProbeEvents.ts`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - header 现在展示 `projectSummary.projectName`
  - header 现在展示 `governanceSummary` 与 `recoverySummary`
  - `useProbeEvents` 现将 event buffer 限制在最近 20 条，避免事件无限增长
- residual_gap:
  - governance / recovery 仍来自 mock snapshot，而不是来自真实 runtime 回写；真实 frontend build/test baseline 仍未接入

## 变更（2026-03-17 Frontend Probe v0 dynamic governance and recovery summaries）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前唯一活跃的 frontend dev issue；在 project summary 已显示后，下一步自然是让 governance / recovery 摘要跟随动作变化，而不是保持静态
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续推进 mock runtime 与 UI 摘要的一致性，`codex` 最适合直接修改 adapter 与 continuity artifact
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先让 governanceSummary / recoverySummary 随 session、chat、pause 等动作动态变化，使 Probe 对治理与恢复状态的显示不再停留在静态假数据。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/adapter.ts`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `CreateOrResumeSession` 现在会刷新 governance summary
  - `SendChatIntervention` 现在会刷新 governance summary
  - `ControlRun.pause` 现在会刷新 recovery summary
  - header 中展示的 governance / recovery 摘要已开始反映 mock runtime 的近期动作
- residual_gap:
  - 这些摘要仍由 mock runtime 生成，不是来自真实 Tauri runtime 或真实 backend 的持久化记录

## 变更（2026-03-17 Frontend Probe v0 recent activity timeline）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前前端实现主线；在 governance / recovery summary 已动态化后，下一步最自然的是给事件本身一个统一时间线入口
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续推进 shell 的可观测性，`codex` 适合直接修改 UI 并回写 continuity
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先补一个最小 recent activity timeline，让 Probe 能总览最近事件，而不是只从各 panel 的局部状态反推。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/AppShell.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - header 新增 `Recent Activity` 时间线
  - 时间线展示最近 5 条 event 的 `type` 与 `occurredAt`
  - Probe 现在对 project-level summary、governance、recovery 与近期事件都有统一总览入口
- residual_gap:
  - 时间线仍来自本地 mock runtime 的 event buffer，不是来自真实 runtime 持久化历史

## 变更（2026-03-17 Frontend Probe v0 semantic activity timeline）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前实现主线；在 recent activity 已出现后，下一步最自然的是把事件从抽象类型提升成可读的业务摘要
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续提升 Probe shell 的可读性与可追溯性，`codex` 最适合直接修改 UI 细节并回写 continuity
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先把 recent activity timeline 从 type-only 列表提升成带最小业务语义的事件摘要。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/AppShell.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `Recent Activity` 现在会按事件类型生成最小业务摘要
  - session / run / agent / chat / terminal / recovery 事件不再只显示抽象 `type`
  - 时间线的可读性比上一轮明显更接近真实产品面的事件流
- residual_gap:
  - 语义摘要仍来自前端本地映射，尚未与真实 backend 事件 schema 做严格对齐

## 变更（2026-03-17 Frontend Probe v0 event source visibility）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前实现主线；在事件语义摘要已具备后，下一步最小增量是把来源维度一起显示出来
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续提升 Probe 时间线的可追溯性，`codex` 适合直接改 UI 并回写 continuity
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先把 recent activity timeline 的 event.source 显示出来，让时间线同时回答“发生了什么”和“是谁触发的”。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/AppShell.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `Recent Activity` 现在展示 `event.source`
  - session / run / agent / chat / terminal / recovery 事件都能区分其触发来源
  - 时间线比上一轮更接近真正的审计/追踪视角
- residual_gap:
  - source 仍来自 mock/runtime contract 字段，尚未接入真实 backend 事件来源枚举与持久化日志

## 变更（2026-03-17 Frontend Probe v0 last event anchor）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前实现主线；在 recent activity 与 source 都已可见后，本轮补一个最小事件锚点最合适
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续提升 Probe 事件可追踪性，`codex` 适合直接修改 shell 并回写 continuity
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先把 snapshot.lastEventId 暴露到 UI，给当前项目状态一个最小的事件锚点。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/AppShell.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - header 现在展示 `lastEventId`
  - 当前 project snapshot 不再只有人类可读摘要，也有一个最小事件锚点
- residual_gap:
  - `lastEventId` 仍来自 mock snapshot，不是来自真实 runtime / backend 的稳定事件序列

## 变更（2026-03-17 Frontend Probe v0 diminishing-returns checkpoint）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue，但现阶段 mock shell 已覆盖最小产品面骨架
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作不再是补新的 mock UI，而是把“继续空转”这个风险显式写回 continuity，让下一轮改做真实 runtime / build 接线
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002，但不要再优先追加 mock-only UI polish。下一步把重点切到真实 Tauri runtime / frontend build baseline 接线，或显式记录为什么当前环境还不能接。`

### continuity conclusion
- current_effect:
  - 当前 Probe v0 已具备 project switch、session create/resume、chat intervention、control bar、agent roster、embedded terminal、governance/recovery summary、recent activity timeline
  - 继续只在 mock 层补小 UI 细节，收益已明显低于真实 runtime / build 接线
- updated_artifacts:
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- residual_gap:
  - 真实 Tauri runtime、真实 frontend build/test baseline、真实 backend event schema 仍未接入；这是当前真正的高价值下一跳，而不是继续 mock polish

## 变更（2026-03-17 Frontend Probe v0 minimal frontend build baseline）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；上一轮已明确 mock-only polish 的边际价值下降，因此本轮直接转向真实 build baseline
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接补前端构建骨架，`codex` 比 `iflow` 更适合直接创建基线文件并回写 continuity
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。不要再优先追加 mock UI 细节，改为补最小 Bun + React + Vite build baseline，并把 Probe v0 挂到真实前端入口上。`

### implementation delta
- updated_artifacts:
  - `package.json`
  - `tsconfig.json`
  - `vite.config.ts`
  - `index.html`
  - `src/frontend_probe_v0/main.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - 仓库根现在已有最小前端构建骨架
  - `index.html` 与 `src/frontend_probe_v0/main.tsx` 已把 Probe v0 挂到真实 DOM root
  - `package.json` 已声明最小 React/Vite/TypeScript 依赖和 `dev/build/typecheck` scripts
- residual_gap:
  - 本轮未安装依赖，也未执行 `vite` / `tsc`
  - 这仍只是前端 build baseline，不等于已接入真实 Tauri runtime

## 变更（2026-03-17 Frontend Probe v0 dependency install blocker）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；build baseline 已落盘后，下一步自然是安装依赖并跑最小验证
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接验证新基线，`codex` 可以直接执行 `bun install` / `bun run typecheck` 并回写真实结果
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先解决 frontend baseline 的依赖安装问题，让 typecheck 和后续 build 至少能真正执行一次，而不是继续停留在声明层。`

### verification result
- executed_checks:
  - `bun --version` -> `1.2.23`
  - `bun install` -> 两次尝试都停在 resolving，未产出 `node_modules` / lockfile
  - `bun run typecheck` -> `tsc: command not found`
- updated_artifacts:
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- residual_gap:
  - 当前最真实的 frontend baseline blocker 已从“没有基线文件”变成“依赖未安装，typecheck 无法执行”
  - 真实 Tauri runtime 仍未接入

## 变更（2026-03-17 Frontend Probe v0 bun mirror diagnosis）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在 install/typecheck 失败后，下一步最有价值的是把 blocker 从“安装卡住”具体化
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是直接诊断本地 frontend baseline 的安装路径，`codex` 适合执行网络与 install 命令并回写结果
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先确认 bun install 卡在哪个 registry / mirror 路径，而不是继续重复抽象的“安装未完成”描述。`

### verification result
- executed_checks:
  - `curl -I --max-time 10 https://registry.npmjs.org/react` -> `200`
  - `bun install --verbose` -> 明确显示请求目标为 `registry.npmmirror.com`
  - `bun install --verbose` 最终仍未落盘 `node_modules` / lockfile，并被中断
- updated_artifacts:
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- residual_gap:
  - blocker 已具体化为 bun registry/mirror 解析路径问题，而不是 npm registry 完全不可达
  - 真实 Tauri runtime 仍未接入

## 变更（2026-03-17 Frontend Probe v0 build baseline verified）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在 bun mirror 问题已具体化后，最有价值的下一步就是确认显式 registry override 能否真正打通 install 与编译验证
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接执行 install / typecheck / build 并回写结果，`codex` 比 `iflow` 更适合完成这一轮真实验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。不要回到 mock polish；优先基于已通过的 build baseline，把真实 Tauri runtime / backend event bridge 接进当前 Probe 宿主入口。`

### verification result
- executed_checks:
  - `BUN_CONFIG_REGISTRY=https://registry.npmjs.org bun install --verbose` -> 成功安装 68 packages，并落盘 `node_modules` / `bun.lock`
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过，产出 `dist/index.html` 与 `dist/assets/index-*.js`
- implementation_delta:
  - 修复 `src/frontend_probe_v0/adapter.ts` 中的语法错误与重复 `governanceSummary` 字段，恢复 mock runtime 分支的可编译状态
- updated_artifacts:
  - `src/frontend_probe_v0/adapter.ts`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- residual_gap:
  - frontend build baseline 已从“声明存在”推进到“真实可安装、可 typecheck、可 build”
  - 当前剩余高价值缺口已收敛为真实 Tauri runtime、真实 backend event schema 与宿主侧命令/事件桥接尚未接入

## 变更（2026-03-17 Frontend Probe v0 Tauri runtime shape resolution）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；build baseline 已通过后，下一步自然是缩小真实宿主接线的不确定性
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接推进宿主接线层，`codex` 更适合修改 adapter/bootstrap/entry 这类实现文件并立即验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。不要再回到 mock-only polish；直接把 Rust/Tauri 侧命令与事件桥接接到当前已支持 v1/v2 宿主形状的 Probe 入口上。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/tauriRuntime.ts`
  - `src/frontend_probe_v0/bootstrap.tsx`
  - `src/frontend_probe_v0/createAdapter.ts`
  - `src/frontend_probe_v0/entry.ts`
  - `src/frontend_probe_v0/index.ts`
- current_effect:
  - Probe 入口不再只假设单一 `window.__TAURI__.invoke/listen` 形状
  - 现在可同时解析直接 `invoke/listen` 与 Tauri v2 常见的 `core.invoke` / `event.listen`
  - 宿主能力解析已从 entry 层集中收口为单独 runtime resolver，后续 Rust/Tauri 接线无需再把形状判断散落到 UI 层
- executed_checks:
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过
- residual_gap:
  - 前端已具备更稳健的宿主能力解析，但 Rust 侧命令名与事件源仍未真正提供
  - 当前真正剩余的高价值工作是把 `probe_request_snapshot` / `probe_send_command` / `probe_server_event` 接到真实 Tauri backend

## 变更（2026-03-17 Frontend Probe v0 configurable bridge bindings）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在宿主 runtime 形状已支持后，下一步最有价值的是去掉前端入口对三条 bridge 名称的硬编码
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接推进 frontend-to-host bridge seam，`codex` 更适合修改 adapter/entry/bootstrap 并立即验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。优先让真实 Rust/Tauri backend 提供或映射三条 bridge 绑定；前端侧默认值和宿主覆盖入口已准备好。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/bridgeBindings.ts`
  - `src/frontend_probe_v0/tauriAdapter.ts`
  - `src/frontend_probe_v0/createAdapter.ts`
  - `src/frontend_probe_v0/bootstrap.tsx`
  - `src/frontend_probe_v0/entry.ts`
  - `src/frontend_probe_v0/index.ts`
- current_effect:
  - Tauri bridge 命令名与事件名已收口成单独配置对象，不再散落在 adapter 和 entry 里硬编码
  - 默认仍使用 `probe_request_snapshot` / `probe_send_command` / `probe_server_event`
  - 宿主现在可通过 `window.__FREELY_PROBE_BRIDGE__` 覆盖这三条绑定，而不必回头修改前端源码
- executed_checks:
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过
- residual_gap:
  - 前端 bridge seam 已从“形状解析”推进到“名称绑定可配置”，但真实 Rust/Tauri backend 仍不存在
  - 下一轮真正高价值的工作仍是提供 backend bridge 实现，而不是继续细修 frontend seam

## 变更（2026-03-17 Frontend Probe v0 runtime diagnostics surfaced）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在 bridge 绑定已可配置后，下一步最有价值的是把这些接线元信息直接暴露到 shell，降低真实宿主接线时的诊断成本
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接推进 Probe UI 与 bootstrap 集成，不是新的边界收敛；`codex` 更适合连续修改并即时验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。当前前端已经会显示 runtime mode 和生效 bridge 绑定；下一步直接把真实 Rust/Tauri backend 接进来，并用这块诊断面确认宿主状态。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/AppShell.tsx`
  - `src/frontend_probe_v0/bootstrap.tsx`
- current_effect:
  - bootstrap 结果现在会显式携带 `runtimeMode` 与 `bridgeBindings`
  - shell header 现在会直接显示当前是 `mock` 还是 `tauri`
  - shell header 也会直接显示当前使用的三条 bridge 绑定
- executed_checks:
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过
- residual_gap:
  - 前端诊断面已能显示宿主模式和 bridge 绑定，但真实 Rust/Tauri backend 仍未提供
  - 下一轮真正的高价值动作仍是 backend bridge 接入，而不是继续补前端诊断字段

## 变更（2026-03-17 Frontend Probe v0 tauri-mock transport）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在真实 Rust backend 缺席的情况下，最有价值的下一步是让前端至少能演练一遍 `invoke/listen` 形状的 transport，而不是永远只走 adapter 直连路径
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接补 transport shim 与入口切换逻辑，`codex` 更适合连续修改实现文件并即时验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。当前浏览器里已经可以用 tauri-mock 走一遍 Tauri transport；下一步直接把真实 Rust/Tauri backend 替换进这层 transport。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/mockTauriRuntime.ts`
  - `src/frontend_probe_v0/entry.ts`
  - `src/frontend_probe_v0/main.tsx`
  - `src/frontend_probe_v0/index.ts`
- current_effect:
  - 新增浏览器内 `tauri-mock` transport，可把 `MockProbeAdapter` 包装成 `invoke/listen` 形状
  - `main.tsx` 现在支持通过 query 参数 `?transport=tauri-mock` 或全局 `__FREELY_PROBE_TRANSPORT__` 切到这条 transport
  - 默认行为仍然不变，没有强行把默认启动路径改成伪 Tauri
- executed_checks:
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过
- residual_gap:
  - 前端现在已能在浏览器里模拟 Tauri transport，但真实 Rust/Tauri backend 仍未存在
  - 下一轮真正高价值的动作仍是提供真实 bridge，而不是继续加更多 mock transport 变体

## 变更（2026-03-17 Frontend Probe v0 browser transport verification）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在 `tauri-mock` transport 已落盘后，最有价值的下一步就是做页面级验证，确认这不是只停在静态编译层
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接起本地 Vite、验证浏览器行为并回写结果，`codex` 最适合完成这一轮页面级证据收集
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。当前页面级验证已经证明 tauri-mock transport 会把 runtime mode 切成 tauri 并回写事件；下一步直接用真实 Rust/Tauri backend 替换这层 transport。`

### verification result
- executed_checks:
  - `bun run dev -- --host 127.0.0.1 --port 4173`
  - 浏览器打开 `http://127.0.0.1:4173/` -> header 显示 `Runtime mode: mock`
  - 浏览器打开 `http://127.0.0.1:4173/?transport=tauri-mock` -> header 显示 `Runtime mode: tauri`
  - 在 `tauri-mock` 页面点击 `start` -> `Buffered event count: 3`，并出现 `RunStatusChanged` / `AgentStatusChanged` / `TerminalChunkAppended`
- updated_artifacts:
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- residual_gap:
  - 页面级 transport 验证已通过，但这仍是浏览器内 mock transport，不是 Rust/Tauri backend
  - 下一轮真正高价值的动作仍是接入真实 backend bridge

## 变更（2026-03-17 Frontend Probe v0 runtime error surface）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在 transport 页面级验证通过后，下一步最有价值的是确认真实宿主缺桥接时不会让页面无声卡死
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接补失败面并做页面级验证，`codex` 更适合连续修改 hooks/UI 并立即验证结果
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。当前 Probe 在 tauri 形状宿主抛错时已能显式显示 runtime error；下一步直接接真实 Rust/Tauri backend，而不是继续补前端失败面。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/useProbeRuntime.ts`
  - `src/frontend_probe_v0/useProbeControls.ts`
  - `src/frontend_probe_v0/useProbeChatIntervention.ts`
  - `src/frontend_probe_v0/useProbeSessionLifecycle.ts`
  - `src/frontend_probe_v0/AppShell.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - snapshot 请求失败现在会回写 `runtime error`，而不是只停在 loading
  - run control、session lifecycle、chat intervention 的命令错误现在也有显式错误位
  - shell header 已能直接把 runtime 失败面呈现给用户
- executed_checks:
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过
  - 页面注入一个 `invoke` 抛错的 tauri-shaped runtime -> header 显示 `Runtime error: bridge offline`
- residual_gap:
  - 前端失败面已补齐到足够接真实宿主，但真实 Rust/Tauri backend 仍未存在
  - 下一轮真正高价值的动作仍是提供真实 bridge，而不是继续扩写错误展示文案

## 变更（2026-03-17 Frontend Probe v0 tauri-broken transport）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在 runtime error surface 已补齐后，最有价值的下一步是把这条失败面变成可直接访问的显式 transport，而不是继续依赖 devtools 注入
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接补 transport 分支并做页面级验证，`codex` 更适合连续修改入口文件并立即验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。当前 `tauri-mock` 与 `tauri-broken` 两条浏览器 transport 都已可直接访问；下一步不再继续补 mock transport，而是接真实 Rust/Tauri bridge。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/mockTauriRuntime.ts`
  - `src/frontend_probe_v0/entry.ts`
  - `src/frontend_probe_v0/main.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - 新增 `tauri-broken` transport，不再需要额外注入脚本也能走 tauri-shaped error path
  - 浏览器访问 `?transport=tauri-broken` 即可直接看到 `Runtime error: bridge offline`
- executed_checks:
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过
  - 浏览器打开 `http://127.0.0.1:4173/?transport=tauri-broken` -> header 显示 `Runtime mode: tauri` 与 `Runtime error: bridge offline`
- residual_gap:
  - 浏览器 transport 验证面已经足够，不需要再继续补 mock transport 变体
  - 下一轮真正高价值的动作仍是提供真实 Rust/Tauri backend bridge

## 变更（2026-03-17 Frontend Probe v0 transport selector）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在 `mock` / `tauri-mock` / `tauri-broken` 三条 transport 都存在后，最有价值的下一步是把这些验证入口直接放进 UI，而不是继续要求手改 URL
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接推进 Probe UI 与 URL 状态联动，`codex` 更适合连续修改 shell/bootstrap/main 并立即做页面级验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。当前 shell 已内建 transport selector；下一步不再继续做 transport UX，而是接真实 Rust/Tauri bridge。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/AppShell.tsx`
  - `src/frontend_probe_v0/bootstrap.tsx`
  - `src/frontend_probe_v0/main.tsx`
  - `src/frontend_probe_v0/host.tsx`
  - `src/frontend_probe_v0/mount.tsx`
- current_effect:
  - shell header 现已内建 `Transport` 下拉
  - transport 选择会驱动 URL `transport` 参数，而不是只改本地显示
  - 用户现在可以在 UI 内直接切换 `mock` / `tauri-mock` / `tauri-broken`
- executed_checks:
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过
  - 页面默认加载 `mock` 后，通过 UI 下拉切到 `tauri-broken` -> URL 变成 `?transport=tauri-broken`，header 显示 `Runtime mode: tauri` 与 `Runtime error: bridge offline`
- residual_gap:
  - transport 验证入口已经足够，不需要再继续细修 transport selector
  - 下一轮真正高价值的动作仍是接真实 Rust/Tauri backend bridge

## 变更（2026-03-17 Frontend Probe v0 bridge manifest）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在 transport 验证入口已经足够后，最有价值的下一步是把 backend 所需实现的最小 bridge 要求收口成代码级 manifest
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接推进 contract/bootstrapping 代码，不是新的文档收敛；`codex` 更适合补 manifest 并即时验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。当前 frontend 已显式暴露 `freely.probe.v1` bridge manifest；下一步直接让真实 Rust/Tauri backend 对齐这份 manifest。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/bridgeManifest.ts`
  - `src/frontend_probe_v0/bootstrap.tsx`
  - `src/frontend_probe_v0/AppShell.tsx`
  - `src/frontend_probe_v0/index.ts`
- current_effect:
  - 当前默认 bridge 绑定已被收口成代码级 manifest，而不是只散在 adapter/entry 里
  - bootstrap 现在会把 `bridgeContractVersion` 带进 shell
  - shell header 现在会直接显示当前 bridge contract 版本
- executed_checks:
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过
- residual_gap:
  - 前端现在已把 bridge contract 版本、绑定与 transport 诊断都显式化
  - 下一轮真正高价值的动作仍是让真实 Rust/Tauri backend 按这份 manifest 提供 bridge

## 变更（2026-03-17 Frontend Probe v0 manifest exposure）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在代码级 bridge manifest 已存在后，最有价值的下一步是把它直接暴露给浏览器宿主与调试脚本
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接推进 frontend runtime 暴露面，并做浏览器级验证；`codex` 更适合完成这轮实现与验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。当前浏览器里已经能直接读取 `window.__FREELY_PROBE_MANIFEST__`；下一步不再继续扩写前端暴露面，而是让真实 Rust/Tauri backend 消费这份 manifest。`

### implementation delta
- updated_artifacts:
  - `src/frontend_probe_v0/entry.ts`
  - `src/frontend_probe_v0/main.tsx`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - 当前 bridge manifest 已通过 `window.__FREELY_PROBE_MANIFEST__` 暴露给浏览器 runtime
  - 宿主脚本和调试环境不需要再 import frontend 模块就能读取 `freely.probe.v1`
- executed_checks:
  - `bun run typecheck` -> 通过
  - `bun run build` -> 通过
  - 浏览器执行 `window.__FREELY_PROBE_MANIFEST__` -> 返回 `freely.probe.v1` 及当前默认命令/事件绑定
- residual_gap:
  - frontend 已把 bridge contract 暴露到足够让宿主读取的程度
  - 下一轮真正高价值的动作仍是让真实 Rust/Tauri backend 消费并实现这份 manifest

## 变更（2026-03-17 Frontend Probe v0 static manifest endpoint）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue；在浏览器全局 manifest 已可读取后，最有价值的下一步是把同一份 contract 做成静态可抓取产物
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接补宿主可抓取产物并做本地验证，`codex` 更适合连续修改并立即验证
- target_skill_or_loop: `skill:dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1002。当前 bridge manifest 已可通过全局变量和静态 endpoint 读取；下一步不再继续扩写暴露面，而是让真实 Rust/Tauri backend 消费这份 manifest。`

### implementation delta
- updated_artifacts:
  - `public/freely-probe-bridge-manifest.json`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - bridge manifest 不再只存在于源码与浏览器全局
  - 宿主和外层 runtime 现在可以直接抓取 `/freely-probe-bridge-manifest.json`
- executed_checks:
  - `bun run build` -> 通过
  - `curl http://127.0.0.1:4173/freely-probe-bridge-manifest.json` -> 返回 `freely.probe.v1` 及当前默认命令/事件绑定
- residual_gap:
  - frontend 侧的 bridge contract 暴露面已经足够，不需要再继续增加新的暴露渠道
  - 下一轮真正高价值的动作仍是让真实 Rust/Tauri backend 消费并实现这份 manifest

## 变更（2026-03-17 Frontend Probe v0 reroute to backend bridge pre-brainstorm）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1002` 仍是当前最高优先的 frontend dev issue，但这轮已确认前端侧的高价值 seam 基本收敛，继续在当前 issue 内追加包装层边际价值很低
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是同会话内根据 dev-loop 情景 C 触发 reroute，并直接产出新的 pre-brainstorm 证据，`codex` 可以在当前仓库里连续完成这轮切换
- target_skill_or_loop: `doc-pre-brainstorm-execution`
- next_prompt: `围绕 Rust/Tauri Probe Bridge v1 继续收敛，不要再把 backend bridge 缺口伪装成 I-20260317-1002 的 frontend 细节。`

### reroute evidence
- discovered_problem:
  - 当前仓库不存在 `Cargo.toml`、`src-tauri/` 或任何 `*.rs` bridge 实现
  - frontend 已经具备 manifest、transport diagnostics、error surface 和静态 manifest endpoint
  - 当前真正缺的是新的 backend issue 边界，而不是更多 frontend seam
- updated_artifacts:
  - `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/brainstorms.md`
  - `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/candidates.md`
  - `docs/pre-brainstorms/INDEX.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- status:
  - `status=reroute_required`
  - `next_recommended_route=doc-pre-brainstorm-execution`

## 变更（2026-03-17 Rust/Tauri Probe Bridge v1 candidate milestone sync）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: frontend milestone 仍是当前最有价值的活跃池，而新的 backend bridge 问题已经由 `I-20260317-1002` 明确回流成 milestone 内 candidate
- current_problem_kind: `pre-brainstorm`
- selected_tool: `codex`
- why_selected_tool: 当前动作是继续执行 `doc-pre-brainstorm-execution`，补齐 candidate 记录并与 milestone 做原子同步，`codex` 适合直接在仓库内完成这批文档修改
- target_skill_or_loop: `doc-pre-brainstorm-execution`
- next_prompt: `继续围绕 Rust/Tauri Probe Bridge v1 做 pre-brainstorm 收敛，优先明确 Rust/Tauri 工程落点、三条 bridge 的最小签名，以及 day-1 snapshot/event 返回面。`

### implementation delta
- updated_artifacts:
  - `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/candidates.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - backend bridge candidate 已从简略占位记录收紧为标准 pre-brainstorm candidate
  - `C-20260317-0332` 已同步进入 frontend milestone 的 `candidate_issues`
- residual_gap:
  - backend bridge 仍未稳定到可直接 materialize；下一轮应继续 pre-brainstorm，而不是回到 frontend mock seam 细节

## 变更（2026-03-17 Rust/Tauri Probe Bridge v1 day-1 landing sketch）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: frontend milestone 当前不仅包含 active dev issue，也已包含 backend bridge candidate；这轮最有价值的动作是继续收紧这个 candidate，而不是返回 frontend UI 细节
- current_problem_kind: `pre-brainstorm`
- selected_tool: `codex`
- why_selected_tool: 当前动作仍是 `doc-pre-brainstorm-execution` 的文档收敛，`codex` 适合在当前仓库里直接补工程落点与 day-1 contract 草案
- target_skill_or_loop: `doc-pre-brainstorm-execution`
- next_prompt: `继续围绕 Rust/Tauri Probe Bridge v1 收敛，优先确认根目录 src-tauri + Cargo.toml 是否作为 day-1 落点，以及 probe_send_command / probe_server_event 的最小粒度。`

### implementation delta
- updated_artifacts:
  - `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/brainstorms.md`
  - `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/candidates.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - backend bridge pre-brainstorm 已不再停留在“缺 Rust/Tauri”抽象结论
  - 当前已形成 day-1 倾向：优先走根目录 `src-tauri/ + Cargo.toml` 的标准 Tauri app 落点
  - 三条 bridge 的最小职责也已被拆成可继续判断的草案
- residual_gap:
  - 仍需确认 `probe_send_command` 是保持单入口还是拆分多命令
  - 仍需确认 day-1 最小 snapshot/event 子集足不足以直接 materialize 为正式 issue

## 变更（2026-03-17 Rust/Tauri Probe Bridge v1 materialized to issue）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: frontend milestone 仍是当前最有价值的活跃池，而 backend bridge candidate 已经收敛到足够稳定，适合直接提升为正式 issue
- current_problem_kind: `issue-bound brainstorm`
- selected_tool: `codex`
- why_selected_tool: 当前动作是把 pre-brainstorm candidate 提升为 milestone-owned issue，并在同会话内继续进入 `doc-ibm-execution` 的最小产物落盘，`codex` 适合直接完成这批文档物化
- target_skill_or_loop: `doc-ibm-execution`
- next_prompt: `继续承接 I-20260317-1005，补齐 Rust/Tauri Probe Bridge v1 的 IBM 产物，并把 day-1 contract 收紧到足够进入实现。`

### implementation delta
- updated_artifacts:
  - `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/candidates.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/brainstorms/b-rust-tauri-probe-bridge-v1.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/prd.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/pre-tests.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/tasks.md`
  - `docs/milestones.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `C-20260317-0332` 已提升为 `I-20260317-1005`
  - backend bridge 问题已不再停留在 pre-brainstorm，而是进入正式 issue-bound IBM
  - `I-20260317-1002` 的 blocker 现在有了明确 issue owner
- residual_gap:
  - `I-20260317-1005` 仍处于 `in_ibm`，还没有进入 Rust/Tauri 实现阶段

## 变更（2026-03-17 Rust/Tauri Probe Bridge v1 done_ibm）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: frontend milestone 当前最有价值的活跃条目已从 pre-brainstorm 进入 backend bridge issue，本轮继续收紧它的 IBM 边界最直接
- current_problem_kind: `issue-bound brainstorm`
- selected_tool: `codex`
- why_selected_tool: 当前动作是同会话内完成 bridge issue 的 IBM 收口并回写 milestone/依赖 issue，`codex` 适合直接做这批文档变更
- target_skill_or_loop: `doc-ibm-execution`
- next_prompt: `继续承接 I-20260317-1005 的 dev-loop，实现最小 Rust/Tauri bridge，并用 Frontend Probe v0 做第一次真实宿主联调。`

### implementation delta
- updated_artifacts:
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/prd.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/pre-tests.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/tasks.md`
  - `docs/milestones.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `I-20260317-1005` 已从 `in_ibm` 推到 `done_ibm`
  - backend bridge 的 day-1 落点、单命令入口和最小 snapshot/event 子集已冻结
  - `I-20260317-1002` 的下一推荐路由已从 `doc-ibm-execution` 切到依赖 `I-20260317-1005` 的 backend dev-loop
- residual_gap:
  - bridge 仍未真正实现；下一轮价值最高的动作是 Rust/Tauri 实现与联调，而不是继续扩写 IBM

## 变更（2026-03-17 Rust/Tauri Probe Bridge v1 dev-loop skeleton landed）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 已进入 backend bridge 的实现态，当前最有价值的动作是直接落最小 Rust/Tauri 骨架并验证环境，而不是返回 doc-loop
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接实现 backend bridge 骨架并做本地验证，`codex` 适合连续修改与即时检查
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，优先在具备 cargo 的环境里执行 cargo check，并把前端 Frontend Probe v0 与真实 Rust/Tauri bridge 做第一次联调。`

### implementation delta
- updated_artifacts:
  - `Cargo.toml`
  - `src-tauri/Cargo.toml`
  - `src-tauri/build.rs`
  - `src-tauri/tauri.conf.json`
  - `src-tauri/src/main.rs`
  - `src-tauri/src/lib.rs`
  - `bin/check-rust-toolchain`
  - `bin/cargo-check-probe-bridge`
  - `package.json`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- executed_checks:
  - `bun run typecheck` -> 通过
  - `cargo --version` -> 当前环境无 `cargo`
  - `cargo check -p freely-probe-bridge` -> 因缺少 `cargo` 未执行
  - `bash bin/check-rust-toolchain` -> `[missing] cargo/rustc/rustup`
  - `bash bin/cargo-check-probe-bridge` -> 预检即失败，统一停在 `[missing] cargo/rustc/rustup`
  - `bun run rust:preflight` -> 同样停在 `[missing] cargo/rustc/rustup`
  - `bun run cargo:check:probe` -> 同样停在 `[missing] cargo/rustc/rustup`
- current_effect:
  - backend bridge 的 day-1 Rust/Tauri 骨架已实际落盘，不再只是 issue 文档
  - Rust toolchain blocker 现已收敛成仓库内可重复执行的脚本与 `package.json` 统一入口，而不是一次性 shell 观察
  - `I-20260317-1005` 已从 `done_ibm` 推进到 `in_dev`
- residual_gap:
  - 当前环境缺少 `cargo`，Rust 侧编译验证与真实联调尚未完成

## 变更（2026-03-17 Rust bridge manifest constants anchored in backend）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，本轮最有价值的动作是把 Rust 侧命令名和 contract version 的事实源也收口
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里验证 Rust bridge；当前后续实现应统一复用 src-tauri/src/bridge_manifest.rs 里的 contract 常量。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/bridge_manifest.rs`
  - `src-tauri/src/lib.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - Rust 侧不再把 contract version 和 bridge 名称硬编码散落在实现中
  - backend bridge 现在也有了自己的最小命令名事实源
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，所以这次收口仍未能转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust command subset anchored in backend）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是继续把 Rust 侧单入口 command 语义收口
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里验证 Rust bridge；当前后续实现应统一复用 src-tauri/src/command_kind.rs 里的 command 子集。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/command_kind.rs`
  - `src-tauri/src/lib.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - Rust 侧不再用散落字符串直接匹配 `ControlRun/CreateOrResumeSession/SendChatIntervention`
  - backend bridge 的单入口 command 子集现在也有了自己的 typed 事实源
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，这次收口仍未转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust event subset anchored in backend）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是继续把 Rust 侧最小事件子集收口
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里验证 Rust bridge；当前后续实现应统一复用 src-tauri/src/event_kind.rs 里的最小事件子集。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/event_kind.rs`
  - `src-tauri/src/lib.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - Rust 侧不再用散落字符串直接匹配最小 event subset
  - backend bridge 的 `RunStatusChanged/SessionUpserted/InputArbitrationRecorded/TerminalChunkAppended` 现在也有了自己的 typed 事实源
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，这次收口仍未转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust bridge models extracted from lib.rs）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是继续把 Rust 侧 snapshot/schema 模型从主入口里拆出
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里验证 Rust bridge；当前后续实现应统一复用 src-tauri/src/model.rs 里的后端模型。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/model.rs`
  - `src-tauri/src/lib.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - Rust 侧 snapshot/run/session/agent/terminal/ack/event 模型不再继续堆在 `lib.rs`
  - backend bridge 现在也有了自己的最小数据模型事实源
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，这次结构收口仍未转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust bridge state extracted from lib.rs）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是继续把 Rust 侧 app state 与默认 snapshot 生成从主入口里拆出
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里验证 Rust bridge；当前后续实现应统一复用 src-tauri/src/state.rs 里的 app state 与默认 snapshot 生成。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/state.rs`
  - `src-tauri/src/lib.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - Rust 侧 app state 与默认 snapshot 生成不再继续堆在 `lib.rs`
  - backend bridge 现在也有了自己的最小 state 事实源
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，这次结构收口仍未转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust bridge contract tests scaffolded）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是给 Rust 侧最容易漂移的 contract 点补最小测试骨架
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里先跑 Rust bridge 的最小 contract tests，再做编译验证与联调。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/command_kind.rs`
  - `src-tauri/src/event_kind.rs`
  - `src-tauri/src/state.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - Rust 侧 command/event/state 的最小 contract 已不再只有实现，没有测试骨架
  - 一旦具备 toolchain，后续可以先验证这些最小语义，再继续编译/联调
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，所以这些测试骨架尚未实际执行

## 变更（2026-03-17 Rust bridge command payload typed 化）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是把 day-1 command payload 从裸 JSON 读取收口成最小 typed 事实源
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里验证 Rust bridge；当前后续实现应统一复用 src-tauri/src/command_payload.rs 里的 day-1 payload 解析。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/command_payload.rs`
  - `src-tauri/src/bridge_logic.rs`
  - `src-tauri/src/lib.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `ControlRun`、`CreateOrResumeSession`、`SendChatIntervention` 的最小 payload 解析不再散落在 reducer 中直接裸读 JSON
  - backend bridge 的 day-1 command contract 现在多了一层 typed 事实源
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，所以这些 typed payload 解析尚未转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust bridge event payload builder 收口）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是把 day-1 server event payload 从 reducer 内联 JSON 拼装收口成统一 builder
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里验证 Rust bridge；当前后续实现应统一复用 src-tauri/src/event_payload.rs 里的 day-1 event payload builder。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/event_payload.rs`
  - `src-tauri/src/bridge_logic.rs`
  - `src-tauri/src/lib.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - backend bridge 的出站 event payload 不再继续散落在 reducer 内联拼装 JSON shape
  - day-1 event contract 现在也有了自己的最小 builder 事实源
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，所以这层收口尚未转化为 Rust 侧编译验证

## 变更（2026-03-17 typed payload 开始驱动 snapshot 语义）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是让 typed payload 不只停在解析层，而是真正驱动 day-1 snapshot 行为
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里验证 Rust bridge；当前后续实现应围绕 typed payload 继续收紧后端 day-1 语义，而不是回退到裸 JSON 行为。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/bridge_logic.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `CreateOrResumeSession` 的 typed payload 已开始影响 session title 与 `governance_summary`
  - `SendChatIntervention` 的 typed payload 已开始影响 agent `last_action` 与 `governance_summary`
  - typed payload 现在已经从“解析层”推进到“行为层”
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，所以这些行为层收口仍未转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust bridge ack 语义化）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是把 ack 从固定文案推进成最小语义化确认
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge 代码并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里验证 Rust bridge；当前后续实现应保持 ack、event、snapshot 三条返回面的一致最小语义。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/bridge_logic.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - backend bridge 的 ack 不再固定返回同一条文案
  - `ControlRun`、`CreateOrResumeSession`、`SendChatIntervention` 现在都开始返回最小语义化确认
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，所以这些 ack 语义收口仍未转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust bridge summary 滚动规则对齐 frontend mock）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是消除 Rust bridge 与 frontend mock 在 governance/recovery summary 滚动规则上的行为漂移
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge reducer、补测试并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里先验证 Rust bridge；当前后续实现应保持 summary、snapshot 与 event 的滚动行为和 frontend mock 一致。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/bridge_logic.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - backend `governance_summary` 与 `recovery_summary` 不再在 session/chat/pause 时整段覆盖
  - 新 summary 现在统一采用“最新前插 + 最多 4 条”规则，和 frontend mock adapter 的 header 摘要滚动逻辑一致
  - Rust reducer 已补最小测试覆盖这条 prepend/cap 规则
- verification:
  - `bun run typecheck` ✅
  - `bun run rust:preflight` ❌ `cargo/rustc/rustup` 缺失
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，所以这轮 reducer/test 收口仍未转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust bridge 动态事件时间戳与 event 测试期望收口）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是消除 Rust bridge 与 frontend/mock 在事件时间戳和默认 event 测试期望上的残余漂移
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge event builder、补依赖并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里先验证 Rust bridge；当前后续实现应继续收掉 event builder 与 frontend runtime 之间剩余的语义漂移。`

### implementation delta
- updated_artifacts:
  - `src-tauri/Cargo.toml`
  - `src-tauri/src/event_payload.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - backend `occurredAt` 不再固定为 `1970-01-01T00:00:00Z`，而是开始生成运行时 RFC3339 时间戳
  - `event_payload.rs` 的最小 Rust 测试期望已改为匹配当前默认 `sessionId/runId` 命名与动态时间戳行为
  - 后续一旦进入真实 `cargo test`，不再先被这组过时 event 断言绊住
- verification:
  - `bun run typecheck` ✅
  - `bun run rust:preflight` ❌ `cargo/rustc/rustup` 缺失
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，所以这轮 event builder / test 收口仍未转化为 Rust 侧编译验证

## 变更（2026-03-17 Rust bridge 空态 event fallback 命名对齐）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation，这轮最有价值的动作是收掉 event builder 在空态 fallback 命名上的剩余漂移
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内直接修改 Rust bridge event builder、补最小测试并回写 continuity，`codex` 适合继续这条 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005，在具备 cargo 的环境里先验证 Rust bridge；当前后续实现应继续收掉 snapshot / event builder 的剩余命名与空态漂移。`

### implementation delta
- updated_artifacts:
  - `src-tauri/src/event_payload.rs`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - backend event builder 在缺少活跃 session/run/terminal target 时，不再回退到旧的 `session-<project>` / `run-<project>` 命名
  - fallback 现在统一对齐到 `<projectId>-session-1` / `<projectId>-run-1` / `<projectId>-run-1:pty-0`
  - Rust 侧已补最小测试覆盖这条空态 fallback 约定
- verification:
  - `bun run typecheck` ✅
  - `bun run rust:preflight` ❌ `cargo/rustc/rustup` 缺失
- residual_gap:
  - 当前环境仍缺少 `cargo/rustc/rustup`，所以这轮 event fallback 收口仍未转化为 Rust 侧编译验证

## 变更（2026-03-17 lead-agent 重入后继续 Rust bridge dev-loop）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `docs/progress/**` 与 `docs/recovery/**` 当前不存在，`review/test` 池只有 workspace-routing 的既有验证条目，`human chat/session evidence` 与 `github issue` 也没有形成比现有 committed issue 更高优先的新输入；因此最高优先级仍是 `docs/milestones.md` 中 `I-20260317-1005`
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前问题不是继续做研究或 IBM，而是在现有 worktree 中承接 `in_dev` issue、核对 blocker 并回写 continuity；`codex` 最适合这类仓库内实现/验证/修文档动作
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005 Rust/Tauri Probe Bridge v1，优先在具备 Rust toolchain 的环境执行 bun run rust:preflight 与 bun run cargo:check:probe；若仍缺 cargo/rustc/rustup，则保持当前 route_kind=dev_loop、phase_state=in_dev，并把 blocker 明确留在 continuity artifact，而不是误路由成 pre-brainstorm 或 IBM。`

### continuation evidence
- scanned_pools:
  - `milestones`: `I-20260317-1005` 仍为 committed + `in_dev`
  - `progress/recovery`: 当前仓库无规范目录，暂无比 milestone 更强的 continuation 落点
  - `review/test`: 当前仅见 workspace-routing 旧 verification 文档，没有 frontend probe / rust bridge 新 review 信号
  - `human chat / session evidence`: 现有 `session_refs` 仍指向 `current-thread`，但没有新的人类输入把当前问题改写成 discovery
  - `github issue`: 仓库内只有 policy/brainstorm 对该池的规则描述，没有新的外部 issue 落点
  - `PROJECT_INTENT`: 仍提供原始发现面，但当前不应覆盖已稳定的 milestone-owned issue continuation
- current_blocker:
  - 本轮阻塞点仍是环境缺少 `cargo/rustc/rustup`
  - 这属于当前 dev-loop 的外部执行环境缺口，不构成重新路由到 `doc-pre-brainstorm-execution` 或 `doc-ibm-execution` 的理由
- handoff_need:
  - 当前会话已完成首跳与第二跳判定，也已把 continuity 补回仓库
  - 若外层 runtime 需要继续推进真实 Rust 编译联调，应在具备 Rust toolchain 的环境重新进入同一 `dev-loop`

## 变更（2026-03-17 Rust toolchain preflight 从被动报错改为可操作指引）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: 当前最高优先仍是 `I-20260317-1005` 的 dev-loop continuation，而最直接的剩余阻塞点已经稳定收敛为 Rust toolchain 缺失
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是在仓库内把 blocker 从“知道缺东西”推进到“给出可执行的下一步”，属于实现/验证支撑面改动，`codex` 适合直接修改脚本与文档
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005；若本机缺少 cargo/rustc/rustup，则先根据 bun run rust:preflight 输出完成 rustup 安装与 shell reload，再回跑 cargo check。`

### implementation delta
- updated_artifacts:
  - `bin/check-rust-toolchain`
  - `src-tauri/README.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - `bun run rust:preflight` 不再只输出 `[missing]`，而会明确列出缺失命令、建议 `rustup` 安装步骤、提示 `source "$HOME/.cargo/env"`，并给出下一步重跑命令
  - 当前 dev-loop blocker 仍然存在，但已经从模糊环境缺口收敛成可执行的 operator guidance

## 变更（2026-03-17 Rust toolchain guidance 加回归测试）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: 当前最高优先仍是 `I-20260317-1005` 的 dev-loop continuation，且最直接可推进的仓库内动作是把新加的 preflight guidance 固定成可回归测试，而不是再次只做手工验证
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是新增 shell 测试与 continuity 回写，属于仓库内实现/验证工作，`codex` 适合直接完成
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005；在缺少 Rust toolchain 的环境里，至少保持 preflight guidance 和回归测试不退化，待环境具备 cargo/rustc/rustup 后再回到真实 cargo check / Tauri 联调。`

### implementation delta
- updated_artifacts:
  - `docs/system/workspace/scripts/tests/test-rust-toolchain-preflight`
  - `bin/test-rust-toolchain-preflight`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - 仓库现在会固定验证 `bin/check-rust-toolchain` 在缺少 Rust 命令时必须输出缺失命令汇总、`rustup` 安装建议、shell reload 提示与重跑命令
  - 当前环境 blocker 仍在，但 preflight operator guidance 已不再只依赖人工观察

## 变更（2026-03-17 Rust preflight test 接入统一 package script）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: 当前最高优先仍是 `I-20260317-1005` 的 dev-loop continuation，而当前最有价值的仓库内动作是把新测试接入统一脚本入口，降低后续调用门槛
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内脚本与文档收口，不需要换工具
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005；统一通过 bun run rust:preflight / bun run rust:preflight:test / bun run cargo:check:probe 管理 Rust toolchain blocker，待环境具备 cargo/rustc/rustup 后恢复真实 bridge 编译联调。`

### implementation delta
- updated_artifacts:
  - `package.json`
  - `src-tauri/README.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/milestones.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_effect:
  - Rust toolchain preflight guidance 现在不仅有脚本和测试，还有统一的 `bun run rust:preflight:test` 入口
  - 当前 blocker 仍是环境缺少 Rust toolchain，但仓库内调用面已经统一

## 变更（2026-03-17 首跳闭环继续 Rust bridge dev-loop）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: 当前没有正式 `docs/progress/**` / `docs/recovery/**`；`review/test` 池没有比 frontend probe backend bridge continuation 更高优先的新信号；`human chat/session evidence`、`github issue` 与 `PROJECT_INTENT` 也没有把当前问题改写回 discovery，因此最高优先仍是 `docs/milestones.md` 中 committed + `in_dev` 的 `I-20260317-1005`
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作需要在同一 worktree 内继续做实现验证、检查 blocker 并回写仓库产物，`codex` 比偏研究/托管型工具更适合当前 dev-loop
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005。保持当前 route_kind=dev_loop，不要回退到 pre-brainstorm 或 IBM；先复核 bun run typecheck / build / rust:preflight / rust:preflight:test / cargo:check:probe 的真实结果，并把 blocker 与下一跳写回 continuity artifact。`

### execution evidence
- governance_precheck:
  - 当前分支：`feature/dogfood-codex-auto-20260316`
  - 当前 worktree：`/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260316-feature-dogfood-codex-auto`
  - `./bin/wt-status-all`：`Summary: total=7, dirty=1`
  - 结论：当前不在受保护分支，允许继续在 dedicated worktree 内写入；但 worktree 仍为 dirty，不能宣告 promote / cleanup
- scanned_pools:
  - `milestones`: `I-20260317-1005` 与 `I-20260317-1002` 都在 committed 队列，但 backend bridge blocker 已由前者承接
  - `progress/recovery`: 当前仓库无规范目录，continuation 证据仍以 `docs/pre-brainstorms/CONVERGENCE.md` 为等价落点
  - `review/test`: 本轮真实可执行的验证信号集中在 frontend build 与 Rust preflight/cargo check
  - `human chat / session evidence`: 只有当前会话，没有新的 discovery 需求
  - `github issue`: 无本地新落点
  - `PROJECT_INTENT`: 仍提供原始发现面，但当前不能覆盖已稳定 issue continuation
- verification:
  - `bun run typecheck` -> passed
  - `bun run build` -> passed
  - `bun run rust:preflight` -> failed (`cargo/rustc/rustup` missing)
  - `bun run rust:preflight:test` -> passed
  - `bun run cargo:check:probe` -> failed (`cargo/rustc/rustup` missing)
- updated_artifacts:
  - `docs/milestones.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_conclusion:
  - 当前问题保持为 `issue continuation`
  - 当前下一跳保持为 `dev-loop-execution`
  - 当前 blocker 仍是 Rust toolchain 缺失，而不是 issue 边界不稳
  - `I-20260317-1002` 的 milestone `next_action` 需要同步到“先继续 `I-20260317-1005`，再回前端 host integration”的新事实

## 变更（2026-03-17 Rust 命令层已解锁，blocker 收窄到 partial toolchain）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: 需求池优先级没有变化，当前仍是 `docs/milestones.md` 中 committed + `in_dev` 的 `I-20260317-1005` 最接近可执行；新的环境尝试没有把问题改写成 discovery
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是同一会话内继续解决 dev-loop 的执行环境阻塞，并把更高分辨率的 blocker 写回 issue/milestone/continuity，`codex` 仍最匹配
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005。Rust 命令层已安装，优先修复 stable-aarch64-apple-darwin toolchain 的 partial install / missing manifest，再回跑 bun run cargo:check:probe。`

### execution evidence
- environment_progress:
  - 已执行 `curl ... rustup-init` 与 `rustup default stable`
  - `~/.cargo/bin` 已出现 `cargo` / `rustc` / `rustup`
  - `bun run rust:preflight` -> passed
- current_blocker:
  - `bun run cargo:check:probe` -> failed
  - 失败点已从“缺少 cargo/rustc/rustup”收窄为 `rustc -vV`
  - stderr: `Missing manifest in toolchain 'stable-aarch64-apple-darwin'`
- updated_artifacts:
  - `docs/milestones.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
  - `docs/pre-brainstorms/CONVERGENCE.md`
- current_conclusion:
  - 当前 route 仍是 `milestones -> issue continuation -> codex -> dev-loop-execution`
  - 当前 blocker 已从“缺命令”升级为“partial toolchain / missing manifest”
  - 还不需要 reroute；下一步仍是继续修复 Rust toolchain 完整性

## 变更（2026-03-17 context-ratio warn 后的 dev-loop continuity refresh）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: context ratio 预警不会改变需求池优先级；当前仍是 `I-20260317-1005` 这条 committed + `in_dev` issue 最接近可执行
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: `selected_tool` 与当前 `AI_TOOL` 相同，且当前动作是先补 continuity 再继续修复执行环境，必须在本会话内继续第二跳
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005。已按 warn 阈值先刷新 continuity artifact；下一步直接修复 stable-aarch64-apple-darwin toolchain 的 partial install，再回跑 cargo check。`

### continuity refresh
- context_ratio_warn:
  - previous_ratio: `0.5550`
  - local_warn_threshold: `0.50`
- phase_appropriate_artifact:
  - 当前研究阶段尚无正式 `docs/progress/**`
  - 依宪法与法律允许，dev-loop continuity 继续落到 `docs/pre-brainstorms/CONVERGENCE.md`
- next_focus:
  - 先修复 `~/.rustup/toolchains/stable-aarch64-apple-darwin` 的 partial install / missing manifest
  - 再回跑 `bun run cargo:check:probe`

## 变更（2026-03-17 context-ratio warn 二次 refresh）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: 新一轮 warn 只要求先补 continuity，不改变当前最高优先池；`I-20260317-1005` 仍是 committed + `in_dev` 且最接近可执行的条目
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前仍是在同一会话内先补 continuity，再继续修复 dev-loop blocker；`codex` 与当前 `AI_TOOL` 一致，不能只做 handoff
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005。已按新的 warn 阈值再次刷新 continuity；下一步先核对 stable-aarch64-apple-darwin 实际缺的是 rustc 组件、manifest 元数据，还是 rustup 状态漂移，再决定继续用 rustup 还是切到 Homebrew fallback。`

### continuity refresh
- context_ratio_warn:
  - previous_ratio: `0.5776`
  - local_warn_threshold: `0.50`
- phase_appropriate_artifact:
  - 当前研究阶段尚无正式 `docs/progress/**`
  - 本轮 dev-loop continuity 继续落到 `docs/pre-brainstorms/CONVERGENCE.md`
- next_focus:
  - 先核对 `~/.rustup/toolchains/stable-aarch64-apple-darwin` 现状
  - 再决定继续 rustup 修复还是切到本机更稳的安装路径

## 变更（2026-03-17 rustup 安装路径出现震荡）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: 当前问题仍是 `I-20260317-1005` 的 dev-loop continuation；只是环境 blocker 的分辨率又提高了一层
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作仍是修复当前会话内可操作的执行环境并回写 continuity，不需要切工具
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005。不要把当前状态误写成代码编译失败；先记录 rustup toolchain 安装路径震荡，再评估是否切到 Homebrew 作为更稳的本机 Rust fallback。`

### execution evidence
- observed_state:
  - 先前 `rustup run stable-aarch64-apple-darwin rustc -vV` 一度可用
  - 重新执行 `bun run cargo:check:probe` 后，cargo 进入真实构建并最终报 `No such file or directory (os error 2)`
  - 随后再次检查时，`~/.rustup/toolchains/stable-aarch64-apple-darwin/bin` 已为空
  - `rustup run stable-aarch64-apple-darwin rustc -vV` 重新退回 `toolchain 'stable-aarch64-apple-darwin' is not installed`
- current_conclusion:
  - 当前 blocker 不是仓库 Rust 代码本身
  - 当前 blocker 是 rustup 安装路径在 partial install 与 uninstalled 之间震荡
  - 若继续使用 rustup 路径无法稳定，下一步应评估 Homebrew 提供稳定 `cargo/rustc` 作为本机 fallback

## 变更（2026-03-17 context-ratio warn 三次 refresh）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: warn 预警继续只要求先补 continuity；不改变当前最高优先池。`I-20260317-1005` 仍是 committed + `in_dev`，且 blocker 仍停留在执行环境层
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前仍在同一 `codex` 会话内维护 dev-loop continuity 和 blocker 解析，不需要改工具
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005。当前不要把状态回退成 discovery；先保持 continuity artifact 最新，再以有界方式验证本机 Rust 安装路径，而不是无节制重试。`

### continuity refresh
- context_ratio_warn:
  - previous_ratio: `0.6503`
  - local_warn_threshold: `0.50`
- phase_appropriate_artifact:
  - 当前研究阶段仍无正式 `docs/progress/**`
  - dev-loop continuity 继续写入 `docs/pre-brainstorms/CONVERGENCE.md`
- current_state_snapshot:
  - 首跳结论未变：`milestones -> issue continuation -> codex -> dev-loop-execution`
  - `rustup` 路径最近一次表现为安装状态震荡
  - `brew` fallback 只完成了可用性探测，尚未形成稳定可验证结果
- next_focus:
  - 保持 `I-20260317-1005` 为当前 issue
  - 后续本机 Rust 安装修复应采用单一路径、单次验证、单次回写，避免继续制造新的环境漂移

## 变更（2026-03-18 context-ratio warn 四次 refresh）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: 新一轮 warn 仍不改变需求池优先级，`I-20260317-1005` 继续是当前唯一需要收束的 `in_dev` backend bridge issue
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是同一会话内先补 continuity，再做一次有界的 Rust 环境稳定性验证；`codex` 适合直接完成
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005。既然当前 rustup stable toolchain 已重新稳定可见，就只做一次 cargo check 验证，确认问题是否已经从环境层推进到代码/依赖层。`

### continuity refresh
- context_ratio_warn:
  - previous_ratio: `0.6601`
  - local_warn_threshold: `0.50`
- phase_appropriate_artifact:
  - 当前研究阶段仍无正式 `docs/progress/**`
  - dev-loop continuity 继续写入 `docs/pre-brainstorms/CONVERGENCE.md`
- bounded_verification_gate:
  - `rustup show active-toolchain` -> `stable-aarch64-apple-darwin (default)`
  - `cargo --version` -> `1.94.0`
  - `rustc --version` -> `1.94.0`
  - 结论：当前本机 Rust 路径处于可见状态，允许执行一次有界的 `cargo check`

## 变更（2026-03-18 Rust bridge cargo check 解阻）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `I-20260317-1005` 仍是当前最高优先的 backend bridge continuation；环境已经回到可验证状态，最有价值的动作就是完成一次真正的 `cargo check`
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是仓库内继续修复 dev-loop blocker 并回写 issue/milestone/continuity，`codex` 适合直接完成
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005。Rust toolchain 和 compile-time icon blocker 已解除；下一步转向真实 Tauri 宿主联调，并按需收掉当前 cargo check 的 dead-code warning。`

### execution evidence
- verification:
  - `rustup show active-toolchain` -> `stable-aarch64-apple-darwin (default)`
  - `cargo --version` -> `1.94.0`
  - `rustc --version` -> `1.94.0`
  - `bun run rust:preflight` -> passed
  - `bun run cargo:check:probe` -> passed
- implementation_delta:
  - `src-tauri/icons/icon.png`：补成有效 RGBA PNG，解除 `generate_context!()` 的 compile-time icon 错误
  - `src-tauri/src/event_payload.rs`：移除未使用的 `json` 导入
- residual_gap:
  - `cargo check` 仍有少量 `dead_code` warning
  - 下一阶段重点应是 Tauri 宿主联调，而不是继续处理环境安装问题

## 变更（2026-03-18 Rust bridge contract drift 收口）

### lead-agent routing
- selected_pool: `milestones`
- why_selected_pool: `docs/progress/**` / `docs/recovery/**` 仍未启用；`review/test` 池这轮新暴露的最高价值信号来自 `I-20260317-1005` 自身的 Rust 单测失败与 compile warning，因此当前最高优先仍是 milestone 中 committed + `in_dev` 的 backend bridge continuation
- current_problem_kind: `issue continuation`
- selected_tool: `codex`
- why_selected_tool: 当前动作是同一仓库内直接修复 Rust bridge、重跑本地验证并回写 issue/milestone/continuity；`codex` 比把执行权交回 runtime 或切到偏研究型工具更合适
- target_skill_or_loop: `dev-loop-execution`
- next_prompt: `继续承接 I-20260317-1005。当前 cargo check / test 与 frontend build 基线都已通过，下一步直接进入真实 Tauri 宿主启动联调，确认 Transport=tauri 不再停在 bridge offline。`

### execution evidence
- implementation_delta:
  - `src-tauri/src/bridge_manifest.rs`：新增 Rust 侧可消费的 contract 入口，并用公开 manifest JSON 做一致性测试
  - `src-tauri/src/event_payload.rs`：统一复用 `ProbeEventKind`，把事件名事实源收口到单处
  - `src-tauri/src/bridge_logic.rs`：修正两条已落后于当前 snapshot 行为的单测断言
  - `src-tauri/src/lib.rs`：在运行入口显式读取 bridge contract，确保运行路径消费同一份命令/事件绑定
- verification:
  - `bun run cargo:check:probe` -> passed
  - `cargo test -p freely-probe-bridge` -> passed (`24 passed`)
  - `bun run typecheck` -> passed
  - `bun run build` -> passed
- residual_gap:
  - 仍未实际启动桌面 Tauri 宿主，因此还不能声称 `Transport=tauri` 已完成真实 backend 联调
  - 下一跳应继续留在 `I-20260317-1005` 的 `dev-loop`，直接验证真实宿主路径，而不是回退到 doc-loop 或继续只做本地 contract/warning 清理
