# PRD: issue-sync update 失败传播
- issue_id: I-20261124T054217Z-A

## Goal
双平台写操作的结果必须真实反映到命令退出码与输出，不做部分成功伪装整体成功。

## 实现方案
1. `cmd-update.sh`：GitHub 与 Gitee 写均检查返回值，记录每平台 status。
2. 打印汇总：`[issue-sync] result: github=<success|failure|skipped> gitee=<success|failure|skipped> overall=<success|partial_failure>`。
3. 任一平台 failure → `return 1`；全成功/skipped → 保持原 `update complete` 输出并 return 0。
4. 不改 create/close/comment 等其它写命令（scope 限制）。

## 不退化边界
- 双平台成功时输出含原 `update complete` 行（下游可能依赖）。
- 不改变幂等性、不引入自动重试、不改 issue 生命周期。

## Dev-Loop Handoff
见 pre-tests.md。RED：基线 mock Gitee 失败仍返回 0；GREEN：失败返回非 0 且有汇总。
