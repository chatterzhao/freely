# Candidates

## C-20260507T0730Z-A: wt-create 添加 --source 必填参数

- candidate_format_version: v2
- title: wt-create 添加 --source 必填参数，支持 chat-inbox 和 platform 两种来源
- status: promoted
- promoted_issue_path: docs/issues/I-20260507T0730Z-A/issue.md
- decision_reason: --source 必填确保 AI 在调用 wt-create 前必须明确 issue 来源；scan 匹配验证防止来源误判导致工位创建错误；platform_ids 补齐确保多平台一致性；此功能是 wt-create 完整工作流的关键一环
- milestone: M-20260507T0730Z-A
- acceptance_criteria:
  - wt-create 添加 --source 必填参数（chat-inbox | platform）
  - 参数校验逻辑完整，非法来源值提示错误
  - scan 匹配验证防止来源误判
  - 物化后自动调 issue-sync create 补齐 platform_ids
