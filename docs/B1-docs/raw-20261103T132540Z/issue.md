---
schema_version: '1'
local_id: raw-20261103T132540Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132540Z-A
platform_ids:
  github:
    issue_id: '4150'
    url: https://github.com/chatterzhao/freely/issues/4150
    synced_at: ''
  gitee:
    issue_id: IKSPQ4
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQ4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T13:25:40Z'
updated_at: '2026-11-07T10:36:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-07T10:40:00Z'
closeout_note: ''
---

# fix: pr-merge-guarded 读取 verdict 而非查文件存在

workflow_kind: fix

## 根因
合并门禁把「评审产物文件存在」当成「评审通过」，从不打开文件解析 verdict 字段；评审侧又把「无法判定」默认成 pass。两层叠加后，「通过」不携带任何信息。

## 证据
- `docs/system/workspace/scripts/worktree/pr-merge-guarded:622-629`：`_review_file="$(find docs/B2-docs -name "pr-review-raw-${_raw_key}.md" ...)"`，非空即 `echo "[MERGE-GUARD] PR review: pass ✓"`，无任何 verdict 解析（本次逐行复核确认）。
- 评审侧默认值即 pass：`bin/pr-review-guarded:333` `_review_verdict="pass"`，只有 `freely-review` 退出码非 0 或输出命中 `verdict.*fail` 才改判；`needs_changes`、超时、空输出全部落 pass（`:329-339`）。
- 结论可被显式覆盖：`--verdict pass --reason <任意文本>`。
- 治理门豁免：`docs/system/workspace/scripts/quality/governance-merge-gate`（offset `1744-1747`）`phase == "completed"` 直接 `continue`，跳过 `verification_artifact_dir` 与 owner review 要求；而 `bin/pr-review-guarded:711` 在评审通过后把 `done_b2_ibm` 改成 `completed` → 「审查过」这件事本身关闭了「必须有审查产物」的开关。

## 影响
review 文件写 `verdict: fail` 也照合并；作者一句 `--verdict pass --reason "急"` 可自放行；`completed` 豁免让治理门在评审通过后失效。合并门禁对 develop 的全部强制力都建立在一个恒为真的判断上。

## 修复方案
1. `pr-merge-guarded:622-629` 改为解析 `_review_file` 的 verdict 字段（字段名与 `pr-review-guarded` 写入侧一致，建议 `verdict: pass|fail|needs_changes`），仅 `pass` 放行；无法解析按 fail 处理并打印原文片段。
2. `pr-review-guarded:329-339` 的默认值改 `needs_changes`：「无法判定」不再等同 pass；`--verdict` 覆盖必须带 `--reason` 且落痕到 review 文件。
3. `governance-merge-gate:1744-1747` 的 `completed` 豁免至少保留「review 产物存在 + verdict=pass」这一条，不再全豁免。

## 验收标准
- RED：造一个 `pr-review-raw-<key>.md` 内容为 `verdict: fail`，执行 `pr-merge-guarded`：当前打印 `pass ✓` 并继续；修复后必须非零退出并打印 fail 结论。
- RED：review 文件缺 verdict 字段时不得放行（当前放行）。
- GREEN：`freely-review` 超时/空输出时 `pr-review-guarded` 写出 `verdict: needs_changes`；`grep -n '_review_verdict="pass"' pr-review-guarded` 无命中。
- GREEN：`governance-merge-gate` 对 `phase_state=completed` 且无 review 产物的输入返回非零。
- GREEN：`--verdict` 覆盖必须伴随 reason 落痕到 review 文件，测试断言 reason 缺失时被拒。
- GREEN：`pr-review-guarded` 生成的 review 文件必含 `verdict:` 行（`grep -c '^verdict:'` = 1）；当前无任何强制。
- 注：`verdict` 字段名一旦确定即为 `pr-review-guarded`（写）与 `pr-merge-guarded`（读）之间的唯一契约，须在 #4154 的契约收口里登记，避免再产生第二份副本。
