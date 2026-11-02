# PRD: 受控调用方显式标记

## 1. Goal

让 `wt-create` 与 `wt-close` 在 `ps` 不可用的环境里仍能通过自己的门禁；直接命令继续被拦。

## 2. 实现方案

### 2.1 hook 侧

`docs/system/workspace/hooks/reference-transaction.sh`：

- `_caller_is_wt_create` 开头：`[[ "${FREELY_WT_CREATE:-}" == "1" ]] && return 0`
- `_caller_is_wt_close` 开头：`[[ "${FREELY_WT_CLOSE:-}" == "1" ]] && return 0`

`docs/system/workspace/hooks/pre-push.sh`：

- 进入删除分支判定后：`[[ "${FREELY_ALLOW_REMOTE_BRANCH_DELETE:-}" == "1" ]] && continue`

### 2.2 调用方

- `wt-create`：`FREELY_WT_CREATE=1 git worktree add -b ...`
- `wt-close`：`FREELY_ALLOW_REMOTE_BRANCH_DELETE=1 git push <remote> --delete <branch>`

### 2.3 测试

新增 `docs/system/workspace/scripts/tests/test-guarded-caller-markers`：

1. reference-transaction：带标记放行、无标记拦截。
2. pre-push：带标记不拦删除、无标记拦截。

## 3. 非目标

- 不改 develop/main 保护与合并 receipt。
- 不做进程探测的跨平台重写。

## 4. Dev-Loop Handoff

- 改动：两个 hook + `wt-create` + `wt-close` + 一个测试脚本。
- 测试入口：`bash docs/system/workspace/scripts/tests/test-guarded-caller-markers`。
- 证据：`verification/test-evidence/test-guarded-caller-markers.log`。
