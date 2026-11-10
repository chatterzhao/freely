---
schema_version: '1'
local_id: raw-20261108T141300Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261108T141300Z-A
platform_ids:
  github:
    issue_id: '4231'
    url: https://github.com/chatterzhao/freely/issues/4231
    synced_at: ''
  gitee:
    issue_id: IKTSUN
    url: https://gitee.com/zhaoquan/freely/issues/IKTSUN
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/issue-parity/raw-20261108T141300Z/issues/I-20261108T141300Z-A.md
last_synced_comment_at:
  github: '2026-11-10T07:24:52Z'
  gitee: '2026-11-10T07:24:52Z'
hash: ''
created_at: '2026-11-08T14:13:00Z'
updated_at: '2026-11-10T07:24:55Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261108T141300Z-A
source_candidate: ''
completed_at: '2026-11-10T07:24:51Z'
closeout_note: ''
---

# fix: raw-issue-pull 物化时丢失 severity 字段，优先级在 B1 文档里退回 P2

workflow_kind: fix

workflow_kind: fix

## 根因

R15（#4187）让 `freely feedback create` 把 `severity` 写进 raw frontmatter，并给平台副本打 `severity/Pn` 标签。但 `wt-create` → `raw-issue-pull` 从平台物化本地文档时**没有把 severity 写回 frontmatter**，于是「优先级」在物化之后再次丢失：本地读视图按默认 P2，平台标签却是真实的 P0/P1。

## 证据（2026-11-08 14:05Z 真机，R16.5 轮次）

- `./bin/freely feedback create --kind fix --severity P0 ...` 创建 `raw-20261108T134853Z`：GitHub #4230 / Gitee IKTSSM 双平台 created，平台标签均为 `['kind/raw','phase/proposed','severity/p0']`。
- 工位内 `docs/B1-docs/raw-20261108T134853Z/issue.md` 的 frontmatter 只有 21 个字段，**没有 `severity`**（实测 `grep '^severity'` 为空）。
- 因此 `bin/issue-sync::_labels()` 与 `cmd_scan` 对该 raw 按 R15 的默认规则解析成 P2，与平台 P0 不一致；`raw_reconciliation` 的本地投影也无法断言 severity 标签。
- R16.5 为了让副本一致性门禁放行，只能把 `severity/*` 与 `phase/*` 一起从两侧标签比较中排除（见 R16.5 的 IDN `same_round_prerequisites`）—— 这是权宜，不是修复。

## 证伪（现有 open issue 未覆盖）

- #4187（R15，已关闭）实现「feedback 创建时写 severity」，AT-001 覆盖的是 `cmd_feedback` 路径，未覆盖 `raw-issue-pull` 物化路径。
- #4230（R16.5）修的是 GitHub 标签不存在导致建单失败，并把副本比较收口到 kind/*，明确把本条列为残余风险、未夹带实现。
- #4183 / #4216 / #4194 / #4221 均与物化 frontmatter 字段无关。
- open issue 标题过滤 `materializ|物化|severity` 无匹配（除本条）。

## 修复方案

1. `raw-issue-pull` / `wt-create` 物化时，从平台副本的 labels（或 feedback receipt）解析 `severity/Pn`，写入本地 frontmatter 的可选第 22 字段（`raw_metadata_contract.validate` 已支持 21/22 双形状）。
2. 双平台标签不一致时 fail-closed 报出，不静默猜一个；无 severity 标签的历史 raw 保持 21 字段不重写。
3. 恢复 `raw_reconciliation.canonical_projection` 对 `severity/*` 的比较（R16.5 暂时排除），让「本地 severity 与平台标签一致」成为可机器证明的事实。
4. 补 AT-001：RED（带 P0 标签的 raw 物化后 frontmatter 无 severity、scan 显示 P2）→ GREEN（物化后 `severity: P0`、scan 与平台一致、历史 raw 零改写）。

## 验收标准

- RED：构造带 `severity/P0` 标签的平台副本，走真实物化流程，断言本地 frontmatter 无 severity、`_labels()` 输出 P2。
- GREEN：同一流程后 frontmatter 有 `severity: P0`，`_labels()` / `cmd_scan` 与平台标签一致，副本一致性对 severity/* 的比较恢复且通过。
- GREEN：无 severity 标签的历史 raw 仍为 21 字段、零改写；21/22 字段 `validate()` 双形状不变。
- 回归：materialization / raw-metadata / feedback-severity / raw-reconciliation / replica-degraded / wt-create 相关测试与 develop 基线退出码一致。

### comment-20261110T072451Z
- source: system
- event: promote_finalized
- children: ["I-20261108T141300Z-A"]

拆解为以下任务:
1. [I-20261108T141300Z-A](will-be-updated)
