---
candidate_id: C-20260717T124926Z-A
status: promoted
source_raw: raw-20260717T124926Z
created_at: 2026-07-17
milestone: M-20260717T124926Z-A
---

# Candidates

## C-20260717T124926Z-A: wt-close 自治化重构

- candidate_format_version: v2
- title: 免交互门禁 + 活跃 worker 先收工后关 + agent_working 前置 + 分支消歧 + test 免静默
- status: promoted
- decision_reason: 六个设计缺陷单体收敛于 wt-close 脚本,替换判定语义不删步骤。见 brainstorms Option A
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - AC1: 自属未完成 key 被拒且输出 machine-readable 阻塞原因(含下一步 action)；他属未完成 key 被拒
  - AC2: 他属已完成 key(有 merge 证据)允许关闭(scan 收尾场景)
  - AC3: 活跃 worker 存在时：先 A2A shutdown→poll completed→超时降级(不直接 kill)；--force 保留 kill-and-continue
  - AC4: agent_working 有活跃 reviewer 时拒关
  - AC5: test 工位有未提交证据时 emit event 但继续关闭
  - AC6: 分支匹配多条 time→取最短;多条同级→拒绝+输出候选列表
  - AC7: 所有既有 closeout 步骤无缺失(平台 close/远程分支/worktree/branch/agent_working release)
- promotion_gate: 六缺陷 file:line 勘察完毕;每项保留既有功能不删步骤
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-code-anchor
  - mode: inline
  - summary: 六缺陷与六 fix 点 1:1 映射,文件位置逐行确认
  - verdict: pass
- promoted_issue_id: I-20260717T124926Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/issues/I-20260717T124926Z-A.md
- milestone: M-20260717T124926Z-A
- session_refs: []
