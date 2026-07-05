---
local_id: I-20260321-1530
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '36'
    url: https://github.com/chatterzhao/freely/issues/36
    synced_at: '2026-04-27T11:15:26Z'
  gitee:
    issue_id: IJFO5Y
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5Y
    synced_at: '2026-04-27T13:14:31Z'
primary_platform: github
canonical_issue_path: docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/issues/agent-ready-prd-for-freely-flow.md
last_synced_comment_at:
  github: '2026-04-27T11:15:26Z'
hash: ''
created_at: '2026-04-27T11:15:26Z'
updated_at: '2026-04-27T11:15:26Z'
platform_state: closed
---

Freely 现有的 `prd.md` 普遍偏短，能表达“这轮要做什么”，但还不足以让 AI 在 doc-loop 和 dev-loop 中稳定继续工作。外部研究显示，AI 时代的 PRD 不应只是说明文，而应成为能驱动 prototype、eval、task slicing 和模型升级重判的执行控制面。

如果 Freely 自己不先把这个结构说明白，后续由 AI 生成 PRD 时就只能继续输出“Goal + Product Surface”一类的薄文档，难以支撑更强的 agentic loop。

canonical: docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/issues/agent-ready-prd-for-freely-flow.md
