- issue_id: I-20260720T012820Z-A
- issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260720T012820Z/issues/I-20260720T012820Z-A.md
- phase_state: done_b2_ibm

## Implementation Decision Note

- decision: cross-tool worker launch_kind 从 "new" 改为 "fresh"
- why_this: run-acp-prompt.py --launch-kind 仅接受 fresh/resume/fork/prompt 四种枚举值。"new" 不在其中，导致 argparse error → worker 崩溃。改为 "fresh" 后语义正确：cross-tool 无法 fork（不同 base tool 无共享 session），需新 session。
- alternatives_considered: 在 run-acp-prompt.py 中添加 "new" 别名 — 驳回，侵入工具侧且语义与 "fresh" 重叠，应在调用侧修正
- boundary_non_goals: 不修改 run-acp-prompt.py 的 choices 枚举；不改变 same-tool fork 路径；不改变 manager 的 launch-kind 逻辑
- residual_risk: 无。一字改动，fresh 是合法值，语义明确
