---
schema_version: '1'
local_id: raw-20261125T094104Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261125T094104Z-A
platform_ids:
  github:
    issue_id: '4702'
    url: https://github.com/chatterzhao/freely/issues/4702
    synced_at: ''
  gitee:
    issue_id: IKXYNX
    url: https://gitee.com/zhaoquan/freely/issues/IKXYNX
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-25T09:41:04Z'
updated_at: '2026-11-25T11:05:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: 2026-11-25 10:42:00+00:00
closeout_note: ''
severity: P1
---

# fix: pr-merge-guarded issue-sync 自动提交后 push 吞错且虚假回执

workflow_kind: fix

## fix: pr-merge-guarded issue-sync 自动提交后 push 吞错且虚假回执

| Field | Value |
|-------|-------|
| local_id | `raw-20261125T094104Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-25T09:41:04Z |
| updated | 2026-11-25T09:41:04Z |

---

> **Freely 治理**：这是 raw issue `raw-20261125T094104Z`。实现前请用 `wt-create --raw-key 20261125T094104Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象
pr-merge-guarded 的 _sync_issues_changed_in_merge 在合并前自动 commit issue-sync 变更（chore: issue-sync before merge）后执行 push，但用 `|| true` 吞掉 push 失败，并无条件打印 `[MERGE-GUARD] issue-sync committed + pushed to <branch>`。若 push 失败（网络抖动 / 平台拒绝 / pre-push hook），回执仍声称已推送，本地与远程源分支产生静默漂移。

## 实证（raw-20261125T071429Z 合并现场）
- pr-merge 自动提交 `0b56bc5f5`（issue-sync before merge，更新 I-* 的 platform_ids）后打印 `issue-sync committed + pushed`。
- 合并后 git branch -vv 显示：`all/origin/fix/*` 指向 `0b56bc5f5`，但 `github/fix/*` 仍停在 `2905bdf67`——GitHub 远程源分支落后一个 commit，而回执未报告任何失败。
- remote 'all' 含两个 pushurl（github + gitee），`git push all <branch>` 顺序推送，任一失败被 `|| true` 吞掉后无法区分是部分成功还是全部成功。

## 根因
docs/system/workspace/scripts/worktree/pr-merge-guarded:623-629 的 push 块：
```bash
if git -C "" remote | grep -q "^all$"; then
  git -C "" push all "" 2>/dev/null || true
else
  git -C "" push origin "" 2>/dev/null || true
fi
echo "[MERGE-GUARD] issue-sync committed + pushed to "   # 无条件打印
```
同一文件 401-423 行的 develop-push 段是正确范式（逐 remote 校验、汇总 failed_remotes），issue-sync 段未沿用，属于范式不一致。

## 期望
1. 逐 configured remote（github + gitee）push 源分支，校验每个结果，汇总失败。
2. 任一平台 push 失败 → 非零退出 / 中止合并或明确告警，绝不打印无条件 'pushed'；给出可执行的重试命令（如 `git push <remote> <branch>` 对应的封装入口）。
3. 回执区分 success / partial / failure，与 develop-push 段和 issue-sync update/batch 的汇总语义一致。
4. 保持封装命令自动 push 的必要性（源分支需含 issue-sync commit 才能保持 PR 与各平台一致、wt-close 才能干净删分支），只修失败可见性，不去掉自动 push。

## 非目标
- 不改 pr-create-guarded 的建 PR 链路；不改 develop-push 段；不改 wt-close 删除分支逻辑；不夹带 #4698/#4687。

## 与既有 raw 的关系
raw-20261124T054217Z 覆盖 issue-sync update 吞 Gitee 失败；本条覆盖 pr-merge-guarded 源分支 push 吞错 + 虚假回执，边界不重叠。
