---
schema_version: '1'
local_id: raw-20261112T131150Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261112T131150Z-A
platform_ids:
  github:
    issue_id: '4317'
    url: https://github.com/chatterzhao/freely/issues/4317
    synced_at: ''
  gitee:
    issue_id: IKUZ1D
    url: https://gitee.com/zhaoquan/freely/issues/IKUZ1D
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261112T131150Z/issues/I-20261112T131150Z-A.md
last_synced_comment_at:
  github: '2026-11-12T13:30:17Z'
  gitee: '2026-11-12T13:30:17Z'
hash: ''
created_at: '2026-11-12T13:11:50Z'
updated_at: '2026-11-12T13:30:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261112T131150Z-A
source_candidate: ''
completed_at: '2026-11-12T13:30:17Z'
closeout_note: ''
severity: P1
---

# fix: wt-close dry-run 真删测试工位，wt-create 恢复模式写脏 develop

workflow_kind: fix

## fix: wt-close dry-run 真删测试工位，wt-create 恢复模式写脏 develop

| Field | Value |
|-------|-------|
| local_id | `raw-20261112T131150Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-12T13:11:50Z |
| updated | 2026-11-12T13:11:50Z |

---

> **Freely 治理**：这是 raw issue `raw-20261112T131150Z`。实现前请用 `wt-create --raw-key 20261112T131150Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

预演与恢复两条「只读/补齐」路径都会产生不可逆副作用，且都不报错。2026-11-12 R33.6 收尾时连环命中，直接导致测试证据丢失与 develop 工作树被改脏。

## 现象 1：`wt-close --dry-run` 真的删了测试工位与分支

- develop `8ad2c2a83`，fix 工位与 test 工位都在，test-gate 证据为 `TEST_STATUS=completed / LAST_TESTED_COMMIT=8ad2c2a83`。
- 执行 `./bin/freely wt-close --raw-key 20261112T031638Z --dry-run`：输出里 `git worktree remove` / `branch -d` 都带 `[DRY-RUN]` 前缀，但随后打印
  `wt-close: cleaning up companion test-pre-merge: ...` → `Deleted branch test-pre-merge-... (was 8ad2c2a83)` → `test-pre-merge cleaned ✓`。
- 结果：`freely-worktrees/test-pre-merge-20261112T031638Z-*` 目录与分支**真的消失**（`git worktree list` 不再有它），test-gate.env 证据随之丢失。
- 后果：紧接着的正式 `wt-close` 直接拒绝：
  `[wt-close] 找不到对应的测试工位 test-pre-merge-20261112T031638Z-*`，必须用 `wt-create`（resume 模式）重建工位并**重跑 2 分钟 test-gate** 才能继续收口。

## 现象 2：`wt-create` 恢复模式把已 absorbed 的 raw 自动改回 proposed，并写脏 develop

- 为补齐上面被删的测试工位执行
  `./bin/freely wt-create --raw-key 20261112T031638Z --source platform --kind fix --slug issue-sync-ghost-skill-names`。
- 输出第一行即 `[wt-create] raw-20261112T031638Z phase_state=absorbed → proposed (auto-reopen)`。
- 该 raw 的代码早已合并进 develop、双平台 issue 已 CLOSED、goal 记录为 absorbed；auto-reopen 之后主仓（develop）`git status` 出现
  ` M docs/B1-docs/raw-20261112T031638Z/issue.md`（`phase_state: absorbed` → `proposed`），需要人工 `git checkout --` 还原。
- 后果：①在受保护分支的工作树上产生未提交改动，下一次 `pr-merge-guarded` / `pr-create-guarded` 会因 dirty 拒绝；②本地 phase 与平台状态被临时反转，任何并发校验会读到错误状态。

## 影响

- 「预演」不再是预演：一条 `--dry-run` 会删掉收口所需的唯一测试证据，属于流程级破坏，且没有任何警告。
- 「恢复」把只读的补齐动作变成状态写入（且写到受保护分支的工作树），与 wt-close 的 phase 门禁互相抵消。

## 期望

1. `wt-close --dry-run` 全程零副作用：companion test-pre-merge 的清理同样必须走 dry-run 分支（当前只对 `git worktree remove` / `branch -d` 做了 DRY-RUN 前缀，清理函数是实跑）。
2. `wt-create` 恢复模式不得改写已 `absorbed`/`closed` 的 raw 的 phase_state；确需重开工位时显式要求用户传开关（例如 `--reopen`），并把写入限制在工位内，禁止写主仓工作树。
3. 两条命令各补一条 AT：①dry-run 之后 `git worktree list` / `git branch` 与执行前完全一致；②恢复模式对 absorbed raw 执行后主仓 `git status --porcelain` 为空且 phase_state 不变。

## 边界

- 不改变 `wt-close` 正式路径（非 dry-run）的清理顺序与门禁；
- 不改变 `wt-create` 正常（非 resume）建工位的行为；
- 不引入新的 phase 状态枚举。

### comment-20261112T133017Z
- source: system
- event: promote_finalized
- children: ["I-20261112T131150Z-A"]

拆解为以下任务:
1. [I-20261112T131150Z-A](will-be-updated)
