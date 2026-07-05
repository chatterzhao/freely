# 研究：治理职责到 Skills / Hooks / Bin Scripts 的落地对齐

## Context

- 日期：2026-03-05 23:38 UTC
- 触发：审查发现 `CONSTITUTION.md`、`LAWS.md`、`docs/system/workspace/skills/**` 在职责边界上基本对齐，但 hooks/bin 实际执行层仍绑定 legacy 文档路径，且 `wt-enter` 在主 worktree 挂接 feature 分支时无法自愈。
- 约束：遵循宪法第 2、10、11、13、15、16 章与法律附录 A/B；先进入 pre-brainstorms，再进入 doc/dev 落地。

## 现状问题

1. `bin/governance-check` 与 `bin/freely` 若仍依赖 `docs/brainstorms/`、`docs/planning/`、`docs/continuity/`、`docs/validation/`，就会与 `AGENTS.md` 当前活跃文档范围冲突。
2. `constitution-guard` / `laws-enforcer` 参考清单过薄，无法支撑 1..16 章的逐项执行检查。
3. `recovery-subagent-governance` 尚未把“并行开发领域模型”写成具体操作步骤，尤其缺少 worktree、ownership、hotspot 串行窗口三项落地说明。
4. `config-backup-guard` 提到命名约定，但宪法/法律没有定义可检查的备份命名格式。
5. `bin/wt-enter` + `.githooks/post-checkout` 在“分支已挂在主 worktree”场景缺少自愈路径，易把主 worktree 留在 feature 分支上。

## 收敛判断

本问题不是单纯文档修订，而是治理编译链问题：
- 宪法提供硬边界；
- 法律提供判定门与证据；
- skills 提供 How；
- hooks/bin 是 skills 的运行时承载。

因此落地时必须同时更新四层，否则会出现“文档正确、脚本仍旧错误”的伪对齐。

## 最小变更原则

1. 不新增新的治理层，仍保持 `宪法 -> 法律 -> skills -> hooks/bin`。
2. hooks/bin 只承载已存在的技能/门禁，不得自行发明新规则。
3. 当前研究阶段的脚本门禁必须对齐最小活跃 docs 集合；未来正式 `docs/B2-docs/**` / `docs/progress/**` 路径应作为后续阶段扩展，不得继续强依赖 legacy 目录。
4. 并行开发与配置备份的规则必须补成可执行、可验证、可留痕的链路。

## 结论

该问题已具备 issue-ready 条件，应晋升为 P0 候选并进入落地。
