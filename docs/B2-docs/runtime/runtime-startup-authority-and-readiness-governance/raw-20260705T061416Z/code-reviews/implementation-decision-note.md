---
issue_id: I-20260705T061416Z-A
issue_path: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/issues/I-20260705T061416Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260705T061416Z-A
- issue_path: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/issues/I-20260705T061416Z-A.md

## Implementation Decision Note

- decision: 去掉 `docs/system/workspace/scripts/runtime/freely:21982` 行 log_error 消息中的反引号，将 `\\\`freely-workflow-guarded-execution\\\`` 改为纯文本 `freely-workflow-guarded-execution`
- why_this: 双引号内 `\\` + 裸反引号在 bash 展开时触发命令替换，最简修复是去掉反引号。纯文本语义不变，且避免了转义链脆弱性。
- alternatives_considered: (1) 用单引号替代反引号 — 不必要的视觉区分；(2) 正确转义反引号 `\\\`` — 转义链仍脆弱，易在后续编辑中再次出错
- boundary_non_goals: 不修改 Bug 1（__manager__ slot empty）—— 已由 M-20260703T080443Z-A 独立修复；不修改其他文件的 log_error 消息；不改变 dirty check 逻辑
- residual_risk: 无。单行字符串修改，不影响任何功能逻辑。
