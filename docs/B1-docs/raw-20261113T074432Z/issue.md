---
schema_version: '1'
local_id: raw-20261113T074432Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T074432Z-A
platform_ids:
  github:
    issue_id: '4324'
    url: https://github.com/chatterzhao/freely/issues/4324
    synced_at: ''
  gitee:
    issue_id: IKV4RX
    url: https://gitee.com/zhaoquan/freely/issues/IKV4RX
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T074432Z/issues/I-20261113T074432Z-A.md
last_synced_comment_at:
  github: '2026-11-13T07:54:51Z'
  gitee: '2026-11-13T07:54:51Z'
hash: ''
created_at: '2026-11-13T07:44:32Z'
updated_at: '2026-11-13T07:54:57Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T074432Z-A
source_candidate: ''
completed_at: '2026-11-13T07:54:51Z'
closeout_note: ''
severity: P2
---

# fix: wt-close 保护分支门禁阻止 test-pre-merge 残留工位回收

workflow_kind: fix

## fix: wt-close 保护分支门禁阻止 test-pre-merge 残留工位回收

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T074432Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T07:44:32Z |
| updated | 2026-11-13T07:44:32Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T074432Z`。实现前请用 `wt-create --raw-key 20261113T074432Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

R33.9 修好 `_resolve_branch_from_raw_key`（计数守卫 + test-pre-merge 回退）后，真机执行：

    ./bin/freely wt-close --raw-key 20261112T040108Z --discard-unmerged --force \
      --reason "违规绕过门禁中，理由充分，是：..."

输出：

    wt-close: raw key '20261112T040108Z' → branch 'test-pre-merge-20261112T040108Z-r336-selfproof'
    wt-close: branch = test-pre-merge-20261112T040108Z-r336-selfproof
    Error: 'test-pre-merge-20261112T040108Z-r336-selfproof' is a protected branch, cannot close

分支解析已经成功，但下一道门禁直接拒绝，残留工位仍无法用封装命令回收。

## 根因（已定位到行）

`docs/system/workspace/scripts/worktree/wt-close:433`（`_is_protected_branch` 定义在 144 行）：

    case "$branch" in
      main|develop|test-pre-merge-*) return 0 ;;
    esac
    ...
    if _is_protected_branch "$branch"; then
      echo "Error: '$branch' is a protected branch, cannot close" >&2
      exit 1
    fi

注释写的是「test-pre-merge is disposable, skip checks」，实现却是一律拒绝；Phase 7（`if [[ "$branch" == test-pre-merge-* ]]` 同步 develop）因此成为死代码。

## 影响

- 只剩 test-pre-merge 沙箱的残留（自证工位、异常中断）永远无法回收；`git worktree list` 会一直带一条 `test-pre-merge-20261112T040108Z-r336-selfproof`（971d4e2fb，仅一条 chore 临时提交，raw 已双平台 CLOSED）。
- 与「禁止手工删 worktree/分支」铁律冲突：唯一剩下的手段是手工 `git worktree remove` / `branch -D`。

## 期望

1. `--force --discard-unmerged --reason <合规前缀>` 且 raw 平台已 CLOSED、无活跃 agent 时，允许关闭 `test-pre-merge-*` 分支：跳过前置 frontmatter/issue 门禁（该分支是丢弃型沙箱），删除工位与分支；**main/develop 仍然一律拒绝**。
2. 保持 Phase 7 的 develop 同步语义（若仍需要），或明确删除死代码并说明。
3. 加 AT：真机（隔离仓库）跑 `wt-close --raw-key <key> --discard-unmerged --force --reason ...`，断言 rc=0、worktree/branch 消失；负向控制断言 `wt-close --raw-key <key>`（main/develop 分支）仍被拒绝、不加 `--force` 时被拒绝。

## 边界

- 不放宽 main/develop 的保护；
- 不放宽 `--force` 的 reason 前缀与 closeout-gate 的活跃 agent 检查；
- 不改 R33.9 已修好的分支解析与计数守卫。

### comment-20261113T075451Z
- source: system
- event: promote_finalized
- children: ["I-20261113T074432Z-A"]

拆解为以下任务:
1. [I-20261113T074432Z-A](will-be-updated)
