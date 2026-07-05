# Tasks: replace ./bin/ with freely in hook scripts and start-lead-agent

- issue_id: I-20260629T132042Z-A

## Task List

### T-001: 替换 .githooks/pre-commit.sh
- status: todo
- description: 全文机械替换 ./bin/ CLI 命令引用为 freely xxx，保留 worktree-common.sh 引用

### T-002: 替换 docs/system/workspace/hooks/pre-commit.sh
- status: todo
- description: 全文机械替换 ./bin/ CLI 命令引用为 freely xxx，保留 worktree-common.sh 引用

### T-003: 替换 docs/system/workspace/hooks/pre-merge-commit.sh
- status: todo
- description: 全文机械替换 ./bin/ CLI 命令引用为 freely xxx，替换 [[ -x ]] 检查为 which freely

### T-004: 替换 docs/system/workspace/hooks/pre-push.sh
- status: todo
- description: 全文机械替换 ./bin/ CLI 命令引用为 freely xxx，替换 [[ -x ]] 检查为 which freely

### T-005: 替换 docs/system/workspace/hooks/reference-transaction.sh
- status: todo
- description: 全文机械替换 ./bin/ CLI 命令引用为 freely xxx

### T-006: 替换 docs/system/workspace/scripts/start-lead-agent.sh
- status: todo
- description: 全文机械替换 ./bin/ CLI 命令引用为 freely xxx

### T-007: 验证全部 4 个 acceptance items
- status: todo
- description: 执行 pre-tests.md 中的全部 acceptance items，确认全部 PASS
