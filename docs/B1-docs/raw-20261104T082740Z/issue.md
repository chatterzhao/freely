---
schema_version: '1'
local_id: raw-20261104T082740Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T082740Z-A
platform_ids:
  github:
    issue_id: '4185'
    url: https://github.com/chatterzhao/freely/issues/4185
    synced_at: ''
  gitee:
    issue_id: IKSWS7
    url: https://gitee.com/zhaoquan/freely/issues/IKSWS7
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-04T08:27:41Z'
updated_at: '2026-11-05T13:27:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-05T12:51:28Z'
closeout_note: ''
---

# fix: pretests-gate 字段解析不接受反引号，误判字段缺失

workflow_kind: fix

## 根因
`pretests-gate` 的字段解析正则把反引号当作值的边界：`rf"^- {key}:\s*`?([^`\n]+)`?\s*$"`。字段值中一旦出现 Markdown 行内代码反引号，正则无法匹配整行，字段被判定为缺失。

## 证据
- `docs/system/workspace/scripts/quality/pretests-gate` 的 `parse_fields()`：`([^`\n]+)` 不允许值中出现反引号。
- 实测 1：`- requirement: `--output` 指向 `/` 时拒绝` → 报 `testcase_derivation_missing: acceptance-1 missing requirement`。
- 实测 2：`- required_evidence: 打包产物与 `.freely_version`` → 报 `pre_tests_missing: section 'End-to-End' missing 'required_evidence'`。
- 去掉值内反引号后两条均通过，证明是解析器问题而非文档缺失。

## 影响
- pre-tests 是 Markdown 文档，行内代码是合法且必要的表达方式；当前规则逼迫作者删掉反引号，降低可读性。
- 门禁报错指向「字段缺失」，与真实原因（值格式）不符，排查成本高。
- 同类问题会影响 `case_design`、`not_applicable_explanation` 等所有字段。

## 修复方案
1. 字段值解析改为「取 `- key:` 之后整行剩余内容」，不再用反引号做边界；仅去掉首尾成对的反引号。
2. 保留对空值的检查；值为空才判定缺失。
3. 补单测：值含单个/多个反引号、含冒号、含 `$HOME` 时均能正确解析。

## 验收标准
- RED：requirement 值含反引号时，gate 断言字段存在；当前报缺失。
- GREEN：上述两种实测写法均通过 gate，且字段值完整保留反引号。
- GREEN：新增 ≥4 条解析单测覆盖反引号、冒号、美元符号、空值。
