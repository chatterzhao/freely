---
issue_id: I-20260704T004227Z-A
issue_path: docs/B2-docs/config/agent-table/raw-20260704T004227Z/issues/I-20260704T004227Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260704T004227Z-A
- issue_path: docs/B2-docs/config/agent-table/raw-20260704T004227Z/issues/I-20260704T004227Z-A.md

## Implementation Decision Note

- decision: |
  对齐 monitor-ai-acp.sh 的 `_bridge_ensure_running` 到 freely 的 `_ensure_acp_bridge_running` 标准:
  1. tool name 对比统一用 base_tool (%%-*)
  2. 增加 registry → config.toml → PATH 三层 ACP binary 解析
  3. 传 --acp-bin + --acp-args 给 acp-bridge.py
  4. 写 .bin 文件
  5. bridge 启动前清理 ANTHROPIC_*/CLAUDE_CODE_*/AI_AGENT 环境变量

- why_this: |
  monitor-ai-acp.sh 是 bridge 的另一个启动入口（由 supervisor 循环调用）。
  当前有 tool name 误杀 + 不传 --acp-bin + 不写 .bin 三连 bug。
  对齐 freely 的实现是最小改动、最低风险方案——复用已被验证正确的三层解析逻辑。

- alternatives_considered: |
  1. 删除 monitor-ai-acp.sh 的 bridge 管理职责，完全交给 freely
     → 不可行: monitor-ai-acp.sh 需要在 cycle 开始时确保 bridge 存活
  2. monitor-ai-acp.sh source freely 获取函数
     → 不可行: monitor-ai-acp.sh 是独立 subprocess，source 20K+ 行的 freely 太重
  3. 创建共享 library
     → 过大 scope，当前改动只需 awk 读 config.toml + registry query

- boundary_non_goals: |
  - 不修改 acp-bridge.py 的 session 管理逻辑
  - 不改变 bridge 的 socket/pid 文件路径协议
  - 不调整 tool-registry.toml 的结构
  - 不在 daemon start 时运行 _init_acp_tool_setup（那是 init 职责）

- residual_risk: |
  - 如果 config.toml 中 FREELY_ACP_*_BIN 路径存在但不指向正确的 ACP binary
    （例如被人手动改错），系统会使用错误 binary。mitigation: command -v 最终回退
    保证至少能找到一个 binary
  - 如果新增工具不需要 acp args（空数组），当前逻辑正确处理
  - awk 读 config.toml 依赖 TOML key = "value" 格式。如果格式变化需同步更新
