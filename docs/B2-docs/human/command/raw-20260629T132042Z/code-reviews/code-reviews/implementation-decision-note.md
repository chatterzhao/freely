---
issue_id: I-20260629T132042Z-A
issue_path: docs/B2-docs/human/command/raw-20260629T132042Z42Z/issues/I-20260629T132042Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260629T132042Z-A
- issue_path: docs/B2-docs/human/command/raw-20260629T132042Z42Z/issues/I-20260629T132042Z-A.md

## Implementation Decision Note

- decision: 对 6 个 .sh 文件执行全文机械替换，将 `./bin/xxx` CLI 命令引用统一改为 `freely xxx` 子命令格式，同步替换存在性检查（`[[ -x "./bin/xxx" ]]` → `which freely >/dev/null 2>&1`），保留 worktree-common.sh 库引用不变
- why_this: 216 个文件的同类替换已验证策略正确。6 个文件被 gate 撤回仅因 gate 将其识别为代码文件走检查，不是替换策略有问题。统一替换保持全仓命令引用格式一致
- alternatives_considered:
  - 仅替换命令执行行保留检查：会导致存在性检查仍指向旧路径，与 freely 体系不对齐
  - 分文件逐个处理：增加不一致性风险，且与 216 文件处理方式脱节
- boundary_non_goals:
  - 不修改 worktree-common.sh 库引用（source 和 [[ -f ]] 检查）
  - 不改变任何 hook 门禁逻辑
  - 不引入新 CLI 命令
  - 不移除或重构 hook 功能
- residual_risk: 低。freely 在 PATH 中的前提假设已在 216 个文件中验证；hook 脚本在 git 操作中执行时 PATH 环境可能受限，但 develop 工位的 freely 已在 PATH 中（经 sync-tooling 配置）
