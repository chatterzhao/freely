# PRD: replace ./bin/ with freely in hook scripts and start-lead-agent

- issue_id: I-20260629T132042Z-A

## Goal

将 6 个 .sh 文件中残留的 `./bin/xxx` CLI 命令引用统一替换为 `freely xxx` 子命令格式，与全仓 216 个已规范化的文件保持一致。

## Motivation

- `./bin/` → `freely` 替换在 216 个文件中已执行完成
- 这 6 个 .sh 文件因 gate 判定为代码而撤销了修改
- 命令引用不一致导致维护困惑和 CI/hook 行为不可预测

## Scope

6 个文件，全文机械替换：

1. `.githooks/pre-commit.sh`
2. `docs/system/workspace/hooks/pre-commit.sh`
3. `docs/system/workspace/hooks/pre-merge-commit.sh`
4. `docs/system/workspace/hooks/pre-push.sh`
5. `docs/system/workspace/hooks/reference-transaction.sh`
6. `docs/system/workspace/scripts/start-lead-agent.sh`

## Non-Goals

- 不修改 `worktree-common.sh` 库引用（`source ./bin/worktree-common.sh`）
- 不改变任何 hook 门禁逻辑
- 不引入新的 CLI 命令

## Dev-Loop Handoff

1. 在 6 个文件中执行机械替换（按 B1 brainstorm 决策的替换规则）
2. 确认 `source ./bin/worktree-common.sh` 和对应 `[[ -f ]]` 检查保留
3. 确认 `[[ -x "./bin/xxx" ]]` 存在性检查改为 `which freely >/dev/null 2>&1`
4. 确认用户面向的提示消息同步更新

## Success Criteria

- 6 个文件中所有 CLI 命令引用统一为 `freely xxx` 格式
- `worktree-common.sh` 引用保留不变
- 通过 RED-GREEN 验证
- 通过 governance-merge-gate + governance-promotion-gate
