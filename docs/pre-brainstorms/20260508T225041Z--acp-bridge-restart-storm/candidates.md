# Candidates

## C-20260508T225041Z-A: ACP bridge restart cooldown

- candidate_format_version: v2
- title: acp-bridge.py 重启加 cooldown 防 storm
- status: promoted
- decision_reason: storm 根因是 claude-agent-acp 快速退出时 bridge 连续重启。加 cooldown 最直接有效，不依赖外部 daemon 参数调整。
- promoted_issue_path: docs/issues/I-20260508T225041Z-A/issue.md
- milestone: M-20260508T225041Z-A
- next_action: B2_IBM → dev-loop → merge
- revisit_trigger: 如果 cooldown 后仍有 storm，再考虑 daemon 层策略调整
- acceptance_criteria:
  - bridge 在 server 快速退出时等待 cooldown 而非立即重启
  - cooldown 期间 socket 保持可用，新请求触发重启
  - 3次/30s 快速退出不再触发
- promotion_gate:
  - 不改变 ACP 协议交互
  - 不修改 claude-agent-acp 行为
  - cooldown 参数可配置（环境变量），默认 10s
- open_questions:
  - cooldown 是否应该指数退避？
  - 是否需要区分正常 end_turn vs 异常退出？
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - verdict: pass
