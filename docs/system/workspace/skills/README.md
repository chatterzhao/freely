# 系统工作区技能

本目录是 Freely 自主工作流的执行来源。

规则：
- `CONSTITUTION.md` 定义边界与原则（What/Why）。
- `LAWS.md` 定义检查、证据和路由（Check/Accept/Route）。
- `docs/system/workspace/three-loop-capability-lifecycle.md` 定义三个 loop 下的能力归宿、owner 边界与生命周期细节真源。
- Skills 仅定义可执行步骤（How）。
- Hooks / `bin/*` 脚本是 skills 的运行时承载；若它们执行门禁，必须与宪法、法律和 skills 保持同源对齐。
- Skills 不得扩展宪法范围或替代法律验收。
- Skills 可以补充更细执行细节（如包安装、配置预检、修复步骤），但一旦与宪法/法律冲突必须立即回退并修正文档。
- 当冲突发生时，优先语义意图而非提交时间顺序。
- 不要在多个文档中重复完整执行过程。
- 流程标识词典与状态联动矩阵以 `docs/LAWS.md` 第 2C 章为唯一事实源。
- Worktree 卫生门禁命令：`freely wt-status-all`（合并/提升/发布前必须全部 `CLEAN`；cleanup 需保证 target 自身安全，并显式跳过 unrelated dirty / busy worktree）。
- 交叉引用顺序应遵循宪法/法律章节顺序 `1..16` 以减少阅读摩擦。

## 技能角色归属

每个技能标注所属角色：`M` = Manager, `W` = Worker, `A` = All。

| 角色 | 技能 | 用途 |
|------|------|------|
| A | `freely-constitution-guard` | 宪法硬性约束门禁（预检） |
| A | `freely-laws-enforcer` | 法律级验收检查 |
| A | `freely-context-source-skill` | 输入来源判定与下一跳路由 |
| A | `freely-auto-loop-orchestrator` | 自主持续交付循环编排 |
| A | `freely-agent-execution-safety-review` | 执行边界安全评审 |
| A | `freely-config-backup-guard` | 配置修改前强制备份 |
| M | `freely-multi-worktree-supervision` | 同时监督多个 worktree |
| M | `freely-worktree-maintenance-governance` | worktree 状态核单与 merge 顺序 |
| M | `freely-worktree-hygiene-supervision` | 单个 worktree 卫生与提交边界 |
| M | `freely-premerge-reconcile` | 合并冲突高风险协调 |
| M | `freely-milestone-planning-state-maintenance` | 里程碑状态维护与排序 |
| M | `freely-branch-management` | 完整自主分支生命周期 |
| M | `freely-workflow-guarded-execution` | 新功能完整开发流程编排 |
| M | `freely-candidate-acceptance-review` | candidate acceptance 独立评审 |
| M | `freely-watchdog-control-plane` | 外层监督与恢复控制面 |
| M | `freely-continuity-watchdog` | 上下文连续性监督 |
| M | `freely-ai-cli-availability-manager` | AI CLI 工具可用性管理 |
| M | `freely-signal-intent-understanding` | signal 意图收敛 |
| M | `freely-human-interruption-manager-triage` | 插话的主管级 routing |
| M | `freely-human-interruption-handling` | 插话深度处理 |
| M | `freely-human-interruption-direct-answer` | 插话直接回答(低价值) |
| M | `freely-chat-issue-routing` | chat 消息路由到正确 issue |
| M | `freely-recovery-subagent-governance` | 恢复耦合与子代理治理 |
| M | `freely-module-interface-governance` | 模块接口版本治理 |
| W | `freely-dev-loop-execution` | scan-selected / handoff-continued issue 的实现与测试 |
| W | `freely-doc-B1_IBM-execution` | raw issue → brainstorm → candidate |
| W | `freely-doc-B2_IBM-execution` | scan/A2A/continuity 选出的 issue → prd/tasks/code-review |
| W | `freely-workflow-guarded-execution` | bug 快速修复流程 |
| W | `freely-url-content-intake` | URL 内容抓取与结构化 |
| W | `freely-rust-tauri-toolchain-bootstrap` | Rust/Tauri toolchain 引导 |
| W | `freely-tool-cc-codex-mcp-runtime` | Codex MCP 运行时安装配置 |
| W | `freely-workspace-skill-governance` | skill 新增/拆分/重构/校准 |
| W | `freely-mem9-continuity-bridge` | mem9 连续性后端接入 |

执行顺序（默认）：
1. `freely-constitution-guard`（预检门禁）
2. `freely-laws-enforcer`（验收门禁）
3. 领域工作流技能（`auto/doc/dev/branch/multi-worktree`）
4. 异常技能（`freely-premerge-reconcile`）按需使用
