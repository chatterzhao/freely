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
- Worktree 卫生门禁命令：`./bin/wt-status-all`（合并/提升/发布前必须全部 `CLEAN`；cleanup 需保证 target 自身安全，并显式跳过 unrelated dirty / busy worktree）。
- 交叉引用顺序应遵循宪法/法律章节顺序 `1..16` 以减少阅读摩擦。

入口技能：
- `skill:freely-freely-constitution-guard` -> `freely-constitution-guard/SKILL.md`
- `skill:freely-freely-laws-enforcer` -> `freely-laws-enforcer/SKILL.md`
- `skill:freely-freely-auto-loop-orchestrator` -> `freely-auto-loop-orchestrator/SKILL.md`
- `skill:freely-freely-candidate-acceptance-review` -> `freely-candidate-acceptance-review/SKILL.md`
- `skill:freely-freely-milestone-planning-state-maintenance` -> `freely-milestone-planning-state-maintenance/SKILL.md`
- `skill:freely-freely-doc-B1_IBM-execution` -> `freely-doc-B1_IBM-execution/SKILL.md`
- `skill:freely-freely-doc-B2_IBM-execution` -> `freely-doc-B2_IBM-execution/SKILL.md`
- `skill:freely-freely-dev-loop-execution` -> `freely-dev-loop-execution/SKILL.md`
- `skill:freely-freely-workspace-skill-governance` -> `freely-workspace-skill-governance/SKILL.md`
- `skill:freely-freely-branch-management` -> `freely-branch-management/SKILL.md`
- `skill:freely-freely-multi-worktree-supervision` -> `freely-multi-worktree-supervision/SKILL.md`
- `skill:freely-freely-worktree-hygiene-supervision` -> `freely-worktree-hygiene-supervision/SKILL.md`
- `skill:freely-freely-worktree-maintenance-governance` -> `freely-worktree-maintenance-governance/SKILL.md`
- `skill:freely-freely-premerge-reconcile` -> `freely-premerge-reconcile/SKILL.md`
- `skill:freely-freely-recovery-subagent-governance` -> `freely-recovery-subagent-governance/SKILL.md`
- `skill:freely-freely-module-interface-governance` -> `freely-module-interface-governance/SKILL.md`
- `skill:freely-freely-config-backup-guard` -> `freely-config-backup-guard/SKILL.md`
- `skill:freely-freely-rust-tauri-toolchain-bootstrap` -> `freely-rust-tauri-toolchain-bootstrap/SKILL.md`
- `skill:freely-freely-watchdog-control-plane` -> `freely-watchdog-control-plane/SKILL.md`
- `skill:freely-freely-continuity-watchdog` -> `freely-continuity-watchdog/SKILL.md`
- `skill:freely-freely-ai-cli-availability-manager` -> `freely-ai-cli-availability-manager/SKILL.md`
- `skill:freely-freely-agent-execution-safety-review` -> `freely-agent-execution-safety-review/SKILL.md`
- `skill:freely-freely-human-interruption-handling` -> `freely-human-interruption-handling/SKILL.md`
- `skill:freely-freely-human-interruption-direct-answer` -> `freely-human-interruption-direct-answer/SKILL.md`
- `skill:freely-freely-human-interruption-manager-triage` -> `freely-human-interruption-manager-triage/SKILL.md`
- `skill:freely-freely-signal-intent-understanding` -> `freely-signal-intent-understanding/SKILL.md`
- `skill:freely-freely-url-content-intake` -> `freely-url-content-intake/SKILL.md`
- `skill:freely-freely-fix-execution` -> `freely-fix-execution/SKILL.md`
- `skill:freely-freely-mem9-continuity-bridge` -> `freely-mem9-continuity-bridge/SKILL.md`
- `skill:freely-freely-tool-cc-codex-mcp-runtime` -> `freely-tool-cc-codex-mcp-runtime/SKILL.md`
- `skill:freely-freely-agent-execution-safety-review` -> `freely-agent-execution-safety-review/SKILL.md`

执行顺序（默认）：
1. `freely-constitution-guard`（预检门禁）
2. `freely-laws-enforcer`（验收门禁）
3. 领域工作流技能（`auto/doc/dev/branch/multi-worktree`）
4. 异常技能（`freely-premerge-reconcile`）按需使用
