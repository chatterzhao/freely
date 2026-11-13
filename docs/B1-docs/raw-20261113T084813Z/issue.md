---
schema_version: '1'
local_id: raw-20261113T084813Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T084813Z-A
platform_ids:
  github:
    issue_id: '4328'
    url: https://github.com/chatterzhao/freely/issues/4328
    synced_at: ''
  gitee:
    issue_id: IKV5QS
    url: https://gitee.com/zhaoquan/freely/issues/IKV5QS
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T084813Z/issues/I-20261113T084813Z-A.md
last_synced_comment_at:
  github: '2026-11-13T10:11:56Z'
  gitee: '2026-11-13T10:11:56Z'
hash: ''
created_at: '2026-11-13T08:48:13Z'
updated_at: '2026-11-13T10:12:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T084813Z-A
source_candidate: ''
completed_at: '2026-11-13T10:11:55Z'
closeout_note: ''
severity: P1
---

# fix: 恢复 test-pre-merge 保护门禁，改由 companion cleanup 回收沙箱

workflow_kind: fix

## fix: 恢复 test-pre-merge 保护门禁，改由 companion cleanup 回收沙箱

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T084813Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T08:48:13Z |
| updated | 2026-11-13T08:48:13Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T084813Z`。实现前请用 `wt-create --raw-key 20261113T084813Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 背景：门禁的设计意图（已核实）

- `docs/system/workspace/scripts/tests/test-wt-close-protected-branch-guard` 的 Test 1–3 明确断言：`main` / `develop` / **`test-pre-merge-*` 一律 blocked**；Test 4 断言只有 fix/feature/hotfix 允许。这是既有验收契约。
- `docs/system/workspace/AGENTS.md.example`：`test-pre-merge-*` 是「临时测试面，用完即删，不可 commit/push」的丢弃型沙箱。
- `wt-close` Phase 6b（`Cleanup companion test-pre-merge via raw-key`）才是设计上删除 test 沙箱的路径：它从 `fix/raw-{key}-{slug}` 推导出同 key 的 `test-pre-merge-{key}-{slug}` 并一起删除。也就是说 test 沙箱**不是独立的收口目标**，它随 dev 分支一起退休。
- `_is_protected_branch`（main|develop|test-pre-merge-*）与守卫 `Error: '...' is a protected branch, cannot close` 由 `4d01714f6 feat: wt-close — unified worktree retirement with phase_state validation` 引入，与上述契约配套。

## 缺陷（R33.9 / R33.10 改错了门禁）

1. R33.9 给 `_resolve_branch_from_raw_key` 加了 `test-pre-merge-<key>-*` 回退解析，使 test 沙箱成为 `wt-close --raw-key` 的主 branch。
2. R33.10 进一步在 protected 守卫上开了窄例外：`test-pre-merge-*` + `--force` + `--discard-unmerged` 时放行。
   合并后真机跑这条路径，输出里出现了 `closing platform issue for raw-...`、`syncing develop across platforms` 等**本不该由丢弃型沙箱触发的完整生命周期副作用**。
3. 结果是：既有验收测试所断言的「test-pre-merge-* 一律 blocked」被事实推翻，Phase 7 的 develop 同步从死代码变成被错误路径触发，且 `wt-close` 现在对同一类分支有两套语义。

真正的问题是**实现不达标**：当 fix 分支已经先被删除、只剩 test 沙箱时，Phase 6b 的 companion cleanup 覆盖不到（它只在 `branch == fix/raw-* || feature/raw-*` 时运行）。这是 cleanup 的实现缺口，不是 protected 门禁设计错误。

## 期望（恢复门禁强度，修实现而不是改门禁）

1. **恢复** `_is_protected_branch` 守卫对 `test-pre-merge-*` 的一律拒绝，撤销 R33.10 的 `--force --discard-unmerged` 例外；R33.9 的 test-pre-merge 回退解析一并撤销（`_count` 数值守卫保留，那部分是真 bug 修复）。
2. 让 Phase 6b companion cleanup 覆盖「dev 分支已不存在、只剩 test 沙箱」的场景：在 `wt-close --raw-key <key>` 中，若找不到 fix/feature 分支但存在对应 `test-pre-merge-<key>-*`，走专门的 companion 回收分支（只删工位+分支，不触发平台关单、不触发 Phase 7 develop 同步），并显式打印。
3. `test-wt-close-protected-branch-guard` 的 Test 1–4 保持原样并通过；新增 AT：无 dev 分支但有 test 沙箱时 `wt-close --raw-key <key>` 能回收沙箱，且断言**没有**平台关单/develop 同步副作用；负向控制断言直接对 test-pre-merge 分支调用仍被拒。

## 边界

- 不放宽 main/develop 保护；不改 `--force` 的 reason 前缀与 closeout-gate 活跃 agent 检查；
- 不改 R33.9 修好的 `_count` 数值守卫（`grep -c . || true` + 首行 + 正则校验）；
- 不删 Phase 7 的 develop 同步逻辑，但不得由沙箱回收路径触发。

### comment-20261113T101156Z
- source: system
- event: promote_finalized
- children: ["I-20261113T084813Z-A"]

拆解为以下任务:
1. [I-20261113T084813Z-A](will-be-updated)
