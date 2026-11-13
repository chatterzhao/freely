---
schema_version: '1'
local_id: raw-20261113T084851Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T084851Z-A
platform_ids:
  github:
    issue_id: '4329'
    url: https://github.com/chatterzhao/freely/issues/4329
    synced_at: ''
  gitee:
    issue_id: IKV5QZ
    url: https://gitee.com/zhaoquan/freely/issues/IKV5QZ
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform-sync/close-merged/raw-20261113T084851Z/issues/I-20261113T084851Z-A.md
last_synced_comment_at:
  github: '2026-11-13T09:10:36Z'
  gitee: '2026-11-13T09:10:36Z'
hash: ''
created_at: '2026-11-13T08:48:51Z'
updated_at: '2026-11-13T09:10:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T084851Z-A
source_candidate: ''
completed_at: '2026-11-13T09:10:36Z'
closeout_note: ''
severity: P1
---

# fix: raw-issue-pull 应镜像平台评论并保护终态，避免造数据绕过副本门禁

workflow_kind: fix

## fix: raw-issue-pull 应镜像平台评论并保护终态，避免造数据绕过副本门禁

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T084851Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T08:48:51Z |
| updated | 2026-11-13T08:48:51Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T084851Z`。实现前请用 `wt-create --raw-key 20261113T084851Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 背景：副本一致性门禁的设计意图

`docs/system/workspace/scripts/lifecycle/raw_reconciliation.py` 的 `canonical_projection` 把 raw 的 title/body/state/**comments** 一起做 canonical hash；`_comments()` 同时读平台返回的 comments 与本地文档里的 `### comment-*` / `#### resolution-*` 块。`raw-reconciliation-gate.py --require-local` 与 `wt-close` / `pr-create-guarded` 用它做写入前的 fail-closed 校验。

也就是说：**平台上的 comment 必须在本地文档有对应 comment 块**，这是设计上的双向镜像，不是可以手工补的装饰。

## 缺陷（R33.8 收口时暴露，且我当时用造数据绕过了门禁）

1. `bin/raw-issue-pull` 只从平台物化 issue 的 title/body/frontmatter，**不物化平台评论**（文件里没有任何 comment 处理）。
2. `issue-sync promote-finalize` 通过 `cmd_comment` 把 `拆解为以下任务: ...` 推到平台，并在本地 raw 文档追加 `### comment-<ts>` 块；但之后任何一次 `raw-issue-pull`（例如 AT 的 B3 在 fix 工位真调它）都会用平台 body 重写本地文档，**把本地 comment 块冲掉**，而平台 comment 仍在。
3. 于是 `raw-reconciliation-gate` 判 `content_diverged`，`pr-create-guarded` 拒「raw replicas are inconsistent」。
   R33.8 当时的处理是**手工编辑文档补回 `### comment-` 块**再重跑门禁——这是造数据绕过门禁，不是修实现：下一次 pull 会再次丢，问题可稳定复现（R33.6 同一轮也出现过 `docs: restore raw absorption state after pull re-materialized it`）。

## 期望（修数据链路，不动门禁）

1. `raw-issue-pull` 物化时把平台 comments 一并镜像为本地 `### comment-<ts>` 块（保持 `_comments()` 可解析的格式），使「pull 之后本地与平台天然一致」；或让 `cmd_comment` 把 comment 同时写入可由 pull 还原的规范位置，保证单一真源。
2. `raw-issue-pull` 不得把已 `absorbed/closed` 的本地 phase 回退成 `proposed`（R33.8 另一次被 `pr-create-guarded` 拒的根因）；物化应保护本地已有的终态，或明确要求显式 `--reopen`。
3. AT：构造一个带 platform comment 的 fixture raw，`raw-issue-pull` 之后直接跑 `raw-reconciliation-gate.py --require-local` 必须 `ok=True / allow`，且本地 frontmatter 的 `phase_state=absorbed` 不被回退；负向控制：不物化 comments 的实现必须判红。

## 边界

- 不放宽 `raw_reconciliation` 的 comment 比较；不改 canonical projection；
- 不改 `promote-finalize` 的 comment 内容；
- 不引入「手工补 comment 块」的流程说明（那正是要消除的绕过手法）。

### comment-20261113T091036Z
- source: system
- event: promote_finalized
- children: ["I-20261113T084851Z-A"]

拆解为以下任务:
1. [I-20261113T084851Z-A](will-be-updated)
