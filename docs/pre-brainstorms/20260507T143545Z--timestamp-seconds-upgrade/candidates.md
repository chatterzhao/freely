# Candidates

## C-20260507T143545Z-A: 时间戳格式带秒升级

- candidate_format_version: v2
- title: YYYYMMDDTHHMMSSZ 带秒格式升级，全局正则兼容旧格式
- status: promoted
- decision_reason: #247 开发中实测确认 `_extract_issue_key` 正则 `\d{4}` 截断 6 位秒，同分钟操作存在 key 碰撞风险，改动边界清晰
- next_action: B2_IBM materialize → 在 feature 工位逐一修改正则 + 增强 normalize_key_variants + 全局 grep 验证
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `_normalize_key_variants("20260507T143544Z")` 返回变体含 `20260507T143544Z`、`20260507-143544`
  - `_normalize_key_variants("20260507-1435")` 返回变体含 `20260507T143500Z`（后补 00 秒）
  - `_normalize_key_variants("20260430222144")` 返回变体含 `20260430T222144Z`（bare→new）
  - 旧格式 `20260503-0915` 分支名仍可正确提取 issue key
  - `grep -rn "\\\\d\{4\}[^,]" docs/system/workspace/scripts/` 零命中（无遗漏旧正则）
  - `pre-push.sh` 分支名校验接受 4 位和 6 位
- promotion_gate:
  - 所有 12 处正则已改为 `\d{4,6}`
  - `_normalize_key_variants` 三格式互转测试通过
  - global grep 确认旧 `\d{4}` 零遗留
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 全局搜索确认 12 处正则定位准确，`_normalize_key_variants` 增强方案覆盖三格式互转
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260507T143545Z-A/issue.md
- milestone: M-20260507T143545Z-A
- session_refs: []
