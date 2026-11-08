---
schema_version: '1'
local_id: raw-20261104T084406Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4187'
    url: https://github.com/chatterzhao/freely/issues/4187
    synced_at: ''
  gitee:
    issue_id: IKSX1A
    url: https://gitee.com/zhaoquan/freely/issues/IKSX1A
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-04T08:44:06Z'
updated_at: '2026-11-04T08:44:11Z'
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

# fix: freely feedback --severity 校验后不落盘，优先级信息丢失

workflow_kind: fix

## 根因
`freely feedback --severity P0|P1|P2` 只做参数校验，随后既不写入本地 frontmatter，也不写入平台 body 或 label。优先级在创建后完全丢失。

## 证据
- `runtime/freely:25122-25124` 只校验取值合法（P0/P1/P2），校验后无任何落盘或平台写。
- 生成的 raw frontmatter 字段为 local_id/kind/phase_state/absorbed_into/platform_ids/...，没有 severity。
- 平台 issue 的 body 与 labels 中均无 severity；labels 目前为空。
- 实测：分别以 `--severity P0`、`P1` 创建的 issue，创建后无法区分。

## 影响
- 无法按优先级分诊与排序，只能依靠外部清单（如 goal 文件）人工维护。
- 自动化无法挑选「下一条该做什么」。
- P0 与 P2 在平台上完全同权，紧急项容易被淹没。

## 修复方案
1. raw frontmatter 增加 `severity: P0|P1|P2`，纳入 raw_metadata_contract 的字段与取值校验。
2. 平台 issue 增加 `severity/P0` 等 label，与 kind/raw、phase/proposed 并列。
3. `scan` 与状态输出按 severity 排序。
4. 存量回填：无 severity 的 raw 默认 P2，并在 scan 报告中单列。

## 验收标准
- RED：`--severity P0` 创建后，frontmatter 含 `severity: P0`；当前缺失。
- GREEN：平台 issue 带 `severity/P0` label，可按 label 过滤。
- GREEN：scan 输出按 P0 到 P2 排序。
- GREEN：存量回填后所有 raw 都有合法 severity。
