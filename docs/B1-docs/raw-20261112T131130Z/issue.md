---
schema_version: '1'
local_id: raw-20261112T131130Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261112T131130Z-A
platform_ids:
  github:
    issue_id: '4316'
    url: https://github.com/chatterzhao/freely/issues/4316
    synced_at: ''
  gitee:
    issue_id: IKUZ18
    url: https://gitee.com/zhaoquan/freely/issues/IKUZ18
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261112T131130Z/issues/I-20261112T131130Z-A.md
last_synced_comment_at:
  github: '2026-11-13T07:27:20Z'
  gitee: '2026-11-13T07:27:20Z'
hash: ''
created_at: '2026-11-12T13:11:30Z'
updated_at: '2026-11-13T07:27:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261112T131130Z-A
source_candidate: ''
completed_at: '2026-11-13T07:27:20Z'
closeout_note: ''
severity: P2
---

# fix: wt-close 无 fix/feature 分支时 grep -c 双写 0 报语法错误，工位无法收口

workflow_kind: fix

## fix: wt-close 无 fix/feature 分支时 grep -c 双写 0 报语法错误，工位无法收口

| Field | Value |
|-------|-------|
| local_id | `raw-20261112T131130Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-12T13:11:30Z |
| updated | 2026-11-12T13:11:30Z |

---

> **Freely 治理**：这是 raw issue `raw-20261112T131130Z`。实现前请用 `wt-create --raw-key 20261112T131130Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

`freely wt-close --raw-key <key>` 在**没有 fix/feature 分支**（只剩 test-pre-merge 或自证工位）时，分支解析阶段抛 shell 语法错误并静默跳过收口：

    .../scripts/worktree/wt-close: line 305: [[: 0
    0: syntax error in expression (error token is "0")
    .../scripts/worktree/wt-close: line 306: [[: 0
    0: syntax error in expression (error token is "0")

实测：`./bin/freely wt-close --raw-key 20261112T040108Z --discard-unmerged --force --reason "..."`（2026-11-12，develop 8ad2c2a83），该 raw 只剩 `test-pre-merge-20261112T040108Z-r336-selfproof` 工位，命令 exit 0 但工位与分支都还在。

## 根因（已定位到行）

`docs/system/workspace/scripts/worktree/wt-close:303`：

    _count=$(printf '%s\n' "$match_list" | grep -c . 2>/dev/null || echo 0)

`grep -c` 在无匹配时**自己已经输出 `0` 并以 1 退出**，`|| echo 0` 再追加一个 `0`，于是 `_count` 变成 `$'0\n0'`；随后 `[[ "$_count" -eq 0 ]]` 报 `syntax error in expression`。

同类写法在本仓还有多处（`grep -c ... || echo 0`），需一并收紧为「只取第一行数字」或 `|| true` 后默认值。

## 影响

- 任何缺少 fix|feature 分支的工位（自证工位、仅测试工位、异常中断残留）都无法用封装命令收口，只能手工 `git worktree remove` / `branch -D` —— 与「禁止手工删 worktree/分支」的铁律直接冲突。
- 命令退出码为 0，调用方（AI 或人）会误以为收口成功，残留静默累积。
- 本次 R33.6 收尾时留下 `freely-worktrees/test-pre-merge-20261112T040108Z-r336-selfproof`（raw 20261112T040108Z 已双平台关闭）无法清理。

## 期望

1. 修 `_count` 计算（例如 `_count=$(printf '%s\n' "$match_list" | grep -c . || true); _count=${_count:-0}; _count=$(printf '%s' "$_count" | head -1)`），并对仓内同类 `grep -c ... || echo 0` 做一次普查。
2. 分支解析失败时**非零退出**并给出可执行诊断（当前静默 pass 是最坏行为）。
3. 加 AT：无 fix/feature 分支、只有 test-pre-merge 工位时，`wt-close --discard-unmerged` 必须 rc=0 且工位/分支被真正清理；再补一条「分支解析失败必须 rc!=0」的负向断言。

## 边界

- 不改收口门禁（closeout-gate / pretests-retirement-gate / dev-test 一致性）的判定强度；
- 不放宽 `--force` 的语义与 reason 要求。

### comment-20261113T072720Z
- source: system
- event: promote_finalized
- children: ["I-20261112T131130Z-A"]

拆解为以下任务:
1. [I-20261112T131130Z-A](will-be-updated)
