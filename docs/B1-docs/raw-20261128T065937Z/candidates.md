---
candidate_id: C-20261128T065937Z-A
status: promoted
source_raw: raw-20261128T065937Z
created_at: 2026-11-28
milestone: M-20261128T065937Z-A
---

## C-20261128T065937Z-A: 打包 parity 回归收口
- candidate_format_version: v2
- title: 测试型 checker 退出运行时目录，入口注释去非打包路径
- status: promoted
- design_verdict: 实现偏差
- anchor_refs:
  - docs/system/workspace/package-allowlist.txt:49-51
  - docs/system/workspace/scripts/quality/package-runtime-file-parity.py:36-41
  - docs/B1-docs/raw-20261106T100938Z/brainstorms.md
- decision_reason: commands.md 明确不随包发布；扩 allowlist 或放宽 parity 都是设计漂移。
- acceptance_criteria:
  - RED 证明 develop 上 parity 检查 rc=1 且指出 commands.md。
  - GREEN: parity rc=0；`freely-package --version auto --activate` 成功。
  - 原命令名契约 AT 与函数级单测保持全绿，checker 反例仍 fail-closed。
  - 不改 allowlist、不改 parity 判据。
- promotion_gate: B0 判定为实现偏差，且扩 allowlist 被历史设计判决排除。
- next_action: 进入 B2，写 pre-tests 后跑 RED。
- revisit_trigger: 若未来 commands.md 被正式决定随包发布，需废止 raw-20261106T100938Z 判决并单独立项。
- open_questions: []
- acceptance_reviews:
  - reviewer: main-agent
  - mode: B0-five-layer-audit
  - summary: 实证 parity 失败由 bin/freely 注释与 quality checker 的字面引用引起。
  - verdict: pass
- promoted_issue_id: I-20261128T065937Z-A
- promoted_issue_path: docs/B2-docs/command-wrapper/install-command-parity/raw-20261128T065937Z/issues/I-20261128T065937Z-A.md
- milestone: M-20261128T065937Z-A
- session_refs: []
