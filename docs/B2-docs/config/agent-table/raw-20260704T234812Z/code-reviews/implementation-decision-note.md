---
issue_id: I-20260704T234812Z-A
issue_path: docs/B2-docs/config/agent-table/raw-20260704T234812Z/issues/I-20260704T234812Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260704T234812Z-A
- issue_path: docs/B2-docs/config/agent-table/raw-20260704T234812Z/issues/I-20260704T234812Z-A.md

## Implementation Decision Note

- decision: |
  逐项修复 9 个 #3731 遗漏问题。acp-bridge.py 加 --base-tool CLI 参数；
  bash 路径函数与 Python conditional suffix 对齐；硬编码路径替换为函数调用；
  语法错误（缩进/未闭合 docstring）修正；agent_assign → acp_session_register；
  hook 提示改进。

- why_this: |
  #3731 虽已合并但在 acp-bridge.py 中只传了 ""（空字符串）等于没改，
  CLI 无 --base-tool 参数导致多 bridge 无法工作。其余为语法错误和路径不一致。

- alternatives_considered: |
  1. 仅在 freely shell 侧绕过 → acp-bridge.py 不配合的话，stop/status 命令失败
  2. 保持 bash 函数无条件加 - → 与 Python 路径不一致，未来排查困难

- boundary_non_goals: |
  - 不修改 acp_session_connect 决策树
  - 不修改 agent-table 结构
  - 不添加新功能

- residual_risk: |
  无。全部为单文件内机械性修改，不影响运行时行为。
