# Candidates

## C-20260507T0200Z-A: Promoted candidate M gate bypass 漏洞修复

- candidate_format_version: v2
- title: Promoted candidate M（Milestone）门禁绕过漏洞修复
- status: promoted
- promoted_issue_path: docs/issues/I-20260507T0200Z-A/issue.md
- decision_reason: M gate 是 milestone 治理的核心门禁，bypass 会导致里程碑状态不一致并影响 release 质量保证体系；问题边界明确，需优先修复以防止进一步的状态污染
- milestone: M-20260507T0200Z-A
- acceptance_criteria:
  - candidate_issues 队列检查在 promoted 状态下正确执行 M gate 验证
  - 未满足里程碑条件的 promoted candidate 无法通过门禁
  - 修复不破坏现有正常 M gate 检查流程
