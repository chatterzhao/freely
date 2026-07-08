---
candidate_id: C-20260708T222454Z-A
status: absorbed
source_raw: raw-20260708T222454Z
milestone: M-20260708T222454Z-A
---
## C-20260708T222454Z-A: scan platform detection fix
- status: absorbed
- milestone: `M-20260708T222454Z-A`
- acceptance_criteria:
  - _sync_platform_direct: update content → check per-platform → close OPEN
  - platform-only detection: 扫平台 OPEN issues → 比对本地
  - 4 个测试场景全部通过
  - dropped/closed/absorbed 统一 terminal 同步
- promoted_issue_id: I-20260708T222454Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260708T222454Z/issues/I-20260708T222454Z-A.md
- decision_reason: _sync_platform_direct 先update后close + extract_raw_key 大小写 + platform-only 检测
