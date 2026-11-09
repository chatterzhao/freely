---
schema_version: '1'
local_id: raw-20261109T070744Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261109T070744Z-A
platform_ids:
  github:
    issue_id: '4236'
    url: https://github.com/chatterzhao/freely/issues/4236
    synced_at: ''
  gitee:
    issue_id: IKTZOM
    url: https://gitee.com/zhaoquan/freely/issues/IKTZOM
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/governance/raw-20261109T070744Z/issues/I-20261109T070744Z-A.md
last_synced_comment_at:
  github: '2026-11-09T07:17:02Z'
  gitee: '2026-11-09T07:17:02Z'
hash: ''
created_at: '2026-11-09T07:07:45Z'
updated_at: '2026-11-09T07:22:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261109T070744Z-A
source_candidate: ''
completed_at: '2026-11-09T07:17:01Z'
closeout_note: ''
---

# fix: 治理门禁死锁——已损坏 frontmatter 的 issue 文档无法被任何工位修复

workflow_kind: fix

## 根因

`governance-merge-gate` 把「本分支 diff 触及的每个 issue 文档」都当作本次 merge 的 owner，要求其 key 与分支 key 一致（GATE 1），并进一步用它做 phase-vs-code、review-artifact、milestone 归属等校验。

而 raw issue #4148（SDD frontmatter 解析所有权）要求一次性修复 23 份历史坏文档（12 份 B1 + 11 份 B2）。这些文档的 key 各不相同，任何修复分支都会同时命中：

- GATE 1：timestamp mismatch（19 条）
- phase_state is 'dropped'/'absorbed' but ...（B1 18 条）
- phase_state 'completed' but no bound review artifact（B2 10 条）
- missing valid source_candidate 等

结果：**坏文档在门禁下永远无法被修复**——修复它的分支必然被判定为「一工位多 issue」。这不是纪律，是死锁。

## 实测证据

分支 `fix/raw-20261103T132517Z-sdd-frontmatter-ownership` 的 `pr-merge-guarded develop` 在 develop 侧被挡：
```
[MERGE-GUARD] merge blocked. PR #4235 left open for retry.
── B1_IBM 相关错误 (18) ── / ── B2_IBM 相关错误 (10) ──
```
同一分支在自身工位跑 `governance-merge-gate --range develop..HEAD`，未豁免时同样是 18+10 条错误。

## 修复方案

在 `governance-merge-gate` 中引入「结构修复豁免」，判定标准是**基线副本本身不可解析**：

1. 对 diff 触及的每个 issue 文档，读 `--range` 左端（staged 模式下为 `HEAD`）的版本；
2. 若该版本无法被单一所有者（`raw_metadata_contract.parse_issue_text`）解析，则视为「修复既有损坏」，把该路径从 owner 集合中剔除并降级为 warning；
3. 基线可解析但 key 不匹配时，仍然报 error（不放宽真实的多 issue 混入）；
4. legacy bullet-only 文档（无 YAML 块）不算损坏，不豁免。

语义依据：一份 frontmatter 无法解析的文档，其 phase/candidate/issue 链从未读到过它的状态，因此修它的结构不可能改变任何人的治理状态。

## 验收标准

- RED：夹具里放一个 glued `---` 的 issue 文档（key 与分支不同），旧门禁报 GATE 1 mismatch；新门禁降级为 warning 且整体放行。
- RED：staged 模式（`git diff --cached`）同样生效——当前 `pr-merge-guarded` 走的就是 staged 路径，若只在 `--range` 模式生效则死锁仍在。
- GREEN：基线可解析、key 不匹配的 issue 文档仍然被拦截（反向守护）。
- GREEN：legacy bullet-only 文档不被当作损坏。
- GREEN：`raw-20261103T132517Z` 的 PR 在 develop 侧能通过合并门禁。

### comment-20261109T071702Z
- source: system
- event: promote_finalized
- children: ["I-20261109T070744Z-A"]

拆解为以下任务:
1. [I-20261109T070744Z-A](will-be-updated)
