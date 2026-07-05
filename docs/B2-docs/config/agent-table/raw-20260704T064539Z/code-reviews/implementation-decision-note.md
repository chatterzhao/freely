---
issue_id: I-20260704T064539Z-A
issue_path: docs/B2-docs/config/agent-table/raw-20260704T064539Z39Z/issues/I-20260704T064539Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260704T064539Z-A
- issue_path: docs/B2-docs/config/agent-table/raw-20260704T064539Z39Z/issues/I-20260704T064539Z-A.md

## Implementation Decision Note

- decision: |
  agent_working.py 新增 acp_session_connect() 统一入口，内部实现 prompt>resume>fork>new 决策树。
  active detection (slot 检测) + fallback safety net (异常回退 new + 日志)。
  watchdog_sse.py 删除 6 个分散函数 (~140行)，handler 改为一行调用。
  bridge 签名预留 base_tool 参数（本期忽略）。

- why_this: |
  当前 12 个调用点各写各的 session 逻辑，参数不一致，agent_working 记录残缺。
  统一入口消除重复，slot 列使 resume 决策有据可依。
  bridge 签名预留保证下期多 bridge 无需重构调用方。

- alternatives_considered: |
  1. 壳封装 (shell wrapper): 跨语言不现实（Python watchdog + shell freely）
  2. acp-bridge.py 拦截: bridge 不知道 raw_key/role/slot 等业务语义
  3. 最小改动补参数: 5 个调用点各自补，无法阻止未来漂移

- boundary_non_goals: |
  - 本期不支持多 bridge（预留签名，行为不变）
  - 不改变 session/new, session/fork 的 ACP 协议
  - 不修改 agent-table.toml 结构
  - 不修改 start-lead-agent.sh 的 prompt 构建

- residual_risk: |
  - slot 列为空的历史行不影响正常运行（DEFAULT ''）
  - 同 base_tool 不同 slot 的 fork 可能因配置差异失败 → 自然回退 new + 日志
  - 删除 watchdog 函数可能导致 MRO/引用问题 → 逐函数 grep 确认无其他引用
