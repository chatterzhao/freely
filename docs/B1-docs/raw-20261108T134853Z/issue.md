---
schema_version: '1'
local_id: raw-20261108T134853Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4230'
    url: https://github.com/chatterzhao/freely/issues/4230
    synced_at: ''
  gitee:
    issue_id: IKTSSM
    url: https://gitee.com/zhaoquan/freely/issues/IKTSSM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-08T13:48:53Z'
updated_at: '2026-11-08T13:49:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

# fix: feedback 建单传 severity/Pn 标签但 GitHub 无此标签，导致双平台 PARTIAL 且自举立项阻塞

workflow_kind: fix

workflow_kind: fix

## 根因

R15（#4187，merge `c1949aa24`）让 `freely feedback create` 把 `severity/Pn` 作为 `gh issue create --label` 的参数传给平台。但 GitHub 仓库里只预置了 `kind/*` 与 `phase/*` 两组标签，**`severity/P0|P1|P2` 从未创建**；`gh issue create --label` 不会自动建标签，遇到不存在的标签会整单失败。

## 证据（2026-11-08 13:47Z 真机）

- 执行 `./bin/freely feedback create --kind fix --severity P2 ...`（为 R16 的文档缺口立项）返回：
  `"github": {"status":"error","error":"could not add label: 'severity/P2' not found"}`、`"gitee": {"status":"created","issue_id":"IKTSRS"}`、`[feedback] PARTIAL: 1 platform(s) created, 1 failed.`
- `gh label list` 当时只有 `kind/raw`、`kind/linked`、`phase/*`，无 `severity/*`。
- 因此新建的 `raw-20261108T134701Z` **只有 Gitee 副本，GitHub 无单**，且 `raw-issue-pull` 在 develop 上被门禁拒绝，补建需要用 `issue-sync create` 在工位里做。
- R15 的 AT-001 用 stub 替换了平台 CLI，只断言 argv 里有标签，没有真机验证「标签是否已存在」；该风险当时已写进 IDN 残余风险①，但未被处理。

## 影响（P0 级自举阻塞）

- **所有** `freely feedback create`（默认 P2 也会传标签）在 GitHub 侧必然失败 → 无法按自举约定用 feedback 立项新缺陷；
- 每次产生 PARTIAL raw：只有 Gitee 单，本地 `platform_ids` 缺 GitHub，后续副本一致性 / wt-close 都可能被卡；
- 平台标签体系与本地 `_labels()` 输出不再是同一套词汇。

## 修复方案（推荐 A）

- A：在 `docs/system/workspace/scripts/sync/platform-adapter.py` 的 GitHub handler `create_issue` 中，先确保 `labels` 里的每个标签存在（`gh label create ... 2>/dev/null || true`，幂等），再建单；若建单因 `not found` 失败则重试一次。Gitee handler 保持现状。
- B（否决）：建单时不传 label，建完用 `gh issue edit --add-label` 补 —— 仍需要标签存在，且失败后留下无标签的半成品单。
- C（否决）：只在文档里要求人工预建标签 —— 换台机器就会复发，不是机制保证。

## 验收标准

- RED：构造一个 stub `gh`，让 `issue create --label severity/P0` 返回 `could not add label: ... not found`，断言当前 handler 直接返回 error、没有尝试 `label create`、也没有重试建单。
- GREEN：同一 stub 下 handler 自动创建缺失标签并重试，最终返回 `created`，且 `label create` 对每个标签只调用一次。
- GREEN：标签已存在时不额外调用 `label create`（幂等）。
- GREEN：真机 `./bin/freely feedback create --severity P0` 双平台均 `created`（可用后立刻用一条真实 raw 验证，验证完按流程收口）。
- GREEN：补建 `raw-20261108T134701Z` 的 GitHub 副本，使其 `platform_ids` 双平台齐全。
- 回归：feedback-severity / platform-write-channel / handler-probe / open-parity 等与 develop 基线退出码一致。

## 证伪（现有 open issue 未覆盖）

- #4187（R15，已关闭）是实现 severity 数据链本身，AT-001 断言的是 argv，不含「标签必须已存在」；其 IDN 明确把这条列为残余风险。
- #4194（R16，已关闭）是安装态版本同步，与平台标签无关。
- #4183 / #4216 / #4221 分别是 B2 文档解析、test-gate 记录命令、wt-close 评论判定，均不涉及平台建单标签。
- 其余 open issue 无「gh label / 标签不存在 / feedback PARTIAL」相关项。
