---
schema_version: '1'
local_id: raw-20261125T071429Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261125T071429Z-A
platform_ids:
  github:
    issue_id: '4699'
    url: https://github.com/chatterzhao/freely/issues/4699
    synced_at: ''
  gitee:
    issue_id: IKXWCQ
    url: https://gitee.com/zhaoquan/freely/issues/IKXWCQ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-25T07:14:30Z'
updated_at: '2026-11-25T08:57:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: 2026-11-25 08:10:00+00:00
closeout_note: ''
severity: P0
---

# fix: wt-close 以本地 platform_state 放行，平台 I-* 未关仍能收口

workflow_kind: fix

## fix: wt-close 以本地 platform_state 放行，平台 I-* 未关仍能收口

| Field | Value |
|-------|-------|
| local_id | `raw-20261125T071429Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `none` |
| created | 2026-11-25T07:14:30Z |
| updated | 2026-11-25T08:10:00Z |

---

> **Freely 治理**：这是 raw issue `raw-20261125T071429Z`。实现前请用 `wt-create --raw-key 20261125T071429Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象
`wt-close` 能成功删除工位，但平台上的 I-* 仍然 OPEN。当前 GitHub 有 17 个 OPEN 的 `[I-*]` issue，仅对应 10 个 distinct local_id（7 个 local_id 各挂着 2 个 OPEN 副本）；这些 local 文档的 `platform_state` 要么缺失、要么已是 `closed`。

## 根因（三层叠加）
1. **门禁读缓存，不向平台取证**。`wt-close:1119-1126` 的 I-* 终态判定只读 frontmatter 的 `platform_state`，全程没有任何平台读。对比同文件 raw 路径 `wt-close:937` 走 `close-raw`（按 raw key 在所有 configured platform 解析），`--platform-only` 路径 `wt-close:953` 走 `close-multi`——只有 I-* 正常收口路径是纯本地判断。
2. **写 closed 的通道只覆盖映射内的副本**。`raw_lifecycle_effects.close_linked()` 只用 `platform_ids`；`platform-adapter.close_issue():903-916` 逐平台取映射里的 issue_id，从不按 local_id 枚举。未映射、重复、或 `platform_ids: {}` 的历史副本永远 OPEN，却仍被判定为"已关"。不对称证据：`close_dropped():925+` 用 `_unique_raw_issue` 按 raw key 在每个平台解析——**drop 路径会对账，正常路径不会**。
3. **失败被吞 + 跳过谓词同源，漂移永久不可见**。`cmd-batch.sh:118` `cmd_close_linked "$local_id" || true`；`pr-merge-guarded:573` `batch "$_raw_key" || true`；`cmd-batch.sh:64` 直接以 `platform_state=closed` 当作 "both sides agree" 跳过。于是同一个自述字段既是 batch 的跳过条件，又是 wt-close 的放行条件，平台真实状态无人校验。

## 重复副本工厂
`lib-state.sh:45 _already_on_platform()` 只读本地 `platform_ids`，从不查平台。因此 `platform_ids: {}` 但平台上已有未跟踪副本时，每次 `batch` 都会 `cmd_create` 出一个新副本：原副本永久 OPEN，新副本被映射并关闭，本地写 `platform_state: closed` → wt-close 放行。这正是双副本的来源。

## 历史定位（git 证据）
- `f1be6b5c3`（2026-11-13）：让 wt-close 直接关闭 I-*（真实平台写）。
- `8bc4773cf`（2026-11-13）：改成 "single closeout predicate"，放行判据换成 `platform_state` —— **回归点：真关被替换成读自述字段**。
- `8745a7345`（2026-11-13 19:48）：merge 钩子加入 `batch ... || true`，关闭失败不再阻断合并。
- `234c12c52`（2026-11-13）："keep the platform_state pre-check"，把该判据固化。
- `raw-20260621T185519Z`（2026-06-21）已列出 `wt-close --skip-platform` = "无验证"，并要求为每个绕过机制补 `--reason` / 调用者验证 / AI 拦截 —— **从未实现**。

## 结论
既是回归也是未完成功能。设计意图（wt-close 做只读终态门禁 + 不可逆清理）正确；错在"终态"以本地自述字段判定，而非向平台取证；且缺硬拦截层（`git-worktree-guard` 拦截 `git worktree remove` 有先例，平台写没有对应 guard）。

## 期望
1. **wt-close I-* 终态改为平台取证**：按 local_id 在所有 configured platform 枚举副本，任一 OPEN 即拒绝收口；仍保持 read-only，不写平台。
2. **关闭通道加对账**：`close_linked` / `close-multi` 按 local_id 解析全部副本（含未映射的孤儿），任一平台失败即非零且不写 `platform_state`。
3. **去掉吞错**：`cmd-batch.sh:118` 与 `pr-merge-guarded:573` 的 `|| true` 改为 fail-closed（batch 失败阻断合并），并给出可直接执行的修复命令。
4. **消除重复工厂**：`_already_on_platform` 增加平台侧存在性判定（按标题/local_id），禁止重复 create。
5. **硬拦截**：平台写只能经封装命令。直接 `gh issue close`、`python3 platform-adapter.py close-*`、unscoped `issue-sync batch` 必须被拒绝并打印正确封装命令（参考 git-worktree-guard 的 PATH wrapper + 进程树判定）。
6. **语义降级**：`platform_state` 明确为缓存，任何门禁不得单独作为事实来源。

## 与既有 raw 的关系
- `#4698`（wt-close 职责边界与提示语漂移）：文档/提示语/frontmatter schema，不含平台取证。
- `#4687`（stale linked 孤儿副本无封装关闭入口）：只覆盖"关闭入口缺失"。
- 本 raw 覆盖"判据真源 + 失败吞噬 + 重复创建 + 硬拦截"，不重复上述两条。
