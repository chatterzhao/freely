# 系统工作区技能

本目录是 Freely 自主工作流的执行来源。

规则：
- `CONSTITUTION.md` 定义边界与原则（What/Why）。
- `LAWS.md` 定义检查、证据和路由（Check/Accept/Route）。
- `docs/system/workspace/three-loop-capability-lifecycle.md` 定义三层循环下的能力归宿、owner 边界与生命周期细节真源。
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
- `skill:constitution-guard` -> `constitution-guard/SKILL.md`
- `skill:laws-enforcer` -> `laws-enforcer/SKILL.md`
- `skill:auto-loop-orchestrator` -> `auto-loop-orchestrator/SKILL.md`
- `skill:doc-pre-brainstorm-execution` -> `doc-pre-brainstorm-execution/SKILL.md`
- `skill:doc-ibm-execution` -> `doc-ibm-execution/SKILL.md`
- `skill:dev-loop-execution` -> `dev-loop-execution/SKILL.md`
- `skill:workspace-skill-governance` -> `workspace-skill-governance/SKILL.md`
- `skill:branch-management` -> `branch-management/SKILL.md`
- `skill:multi-worktree-supervision` -> `multi-worktree-supervision/SKILL.md`
- `skill:worktree-hygiene-supervision` -> `worktree-hygiene-supervision/SKILL.md`
- `skill:worktree-maintenance-governance` -> `worktree-maintenance-governance/SKILL.md`
- `skill:premerge-reconcile` -> `premerge-reconcile/SKILL.md`
- `skill:recovery-subagent-governance` -> `recovery-subagent-governance/SKILL.md`
- `skill:module-interface-governance` -> `module-interface-governance/SKILL.md`
- `skill:config-backup-guard` -> `config-backup-guard/SKILL.md`
- `skill:rust-tauri-toolchain-bootstrap` -> `rust-tauri-toolchain-bootstrap/SKILL.md`
- `skill:watchdog-control-plane` -> `watchdog-control-plane/SKILL.md`
- `skill:continuity-watchdog` -> `continuity-watchdog/SKILL.md`
- `skill:ai-cli-availability-manager` -> `ai-cli-availability-manager/SKILL.md`
- `skill:human-interruption-handling` -> `human-interruption-handling/SKILL.md`
- `skill:human-interruption-direct-answer` -> `human-interruption-direct-answer/SKILL.md`
- `skill:human-interruption-manager-triage` -> `human-interruption-manager-triage/SKILL.md`
- `skill:signal-intent-understanding` -> `signal-intent-understanding/SKILL.md`
- `skill:url-content-intake` -> `url-content-intake/SKILL.md`
- `skill:mem9-continuity-bridge` -> `mem9-continuity-bridge/SKILL.md`

执行顺序（默认）：
1. `constitution-guard`（预检门禁）
2. `laws-enforcer`（验收门禁）
3. 领域工作流技能（`auto/doc/dev/branch/multi-worktree`）
4. 异常技能（`premerge-reconcile`）按需使用
