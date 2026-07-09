---
candidate_id: C-20260709T232630Z-A
status: absorbed
source_raw: raw-20260709T232630Z
absorbed_into: I-20260709T232630Z-A
milestone: M-20260709T232630Z-A
---

## C-20260709T232630Z-A: acp-bridge.log 按 base_tool 分离

- candidate_format_version: v2
- title: acp-bridge.log 按 base_tool 分离
- status: absorbed
- decision_reason: 三个 bridge 共用同一个日志文件导致互相 truncate 覆盖，按 base_tool 分离最简单有效
- acceptance_criteria:
  - 每个 bridge 写入独立的 `acp-bridge-{base_tool}.log`
  - truncate 仅影响自己的日志
  - 错误检测/健康检查能扫描所有 per-tool 日志
- promoted_issue_id: I-20260709T232630Z-A
- promoted_issue_path: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260709T232630Z/issues/I-20260709T232630Z-A.md
- milestone: M-20260709T232630Z-A
