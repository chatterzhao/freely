# Candidates

## C-20260507T0600Z-A: 平台 raw issue 同步到本地

- candidate_format_version: v2
- title: 从平台（GitHub/Gitee）拉取 raw issue 到本地 docs/issues/ 目录
- status: promoted
- promoted_issue_path: docs/issues/I-20260507T0600Z-A/issue.md
- decision_reason: 平台 issue 本地化是 B1_IBM 流程的前提条件，当前大部分 issue 创建在 GitHub 但本地 docs/issues/ 中缺乏对应条目；缺少此功能会导致平台与本地 issue 体系脱节，影响治理一致性
- milestone: M-20260507T0600Z-A
- acceptance_criteria:
  - 实现从 GitHub/Gitee 拉取 raw issue 到本地 docs/issues/ 的功能
  - 拉取后的 raw issue 格式与本地 issue 规范一致
  - 支持增量同步，避免重复拉取
  - 与现有 issue-sync 体系集成
