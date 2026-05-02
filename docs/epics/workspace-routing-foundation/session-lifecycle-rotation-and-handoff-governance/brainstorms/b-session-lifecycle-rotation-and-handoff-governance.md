# Brainstorm: session-lifecycle-rotation-and-handoff-governance

## Problem framing

- Freely 之前只有“第一轮 fresh，后续一律 resume”的粗粒度 runtime 行为。
- 这与恢复优先原则不冲突，但不足以覆盖“原会话仍可 resume，却已不值得继续 resume”的情形。
- 具体退化信号已经在当前狗粮运行中出现：
  - `context compacted`
  - 同一首跳 / 第二跳输出重复
  - 没有显式 handoff 的 fresh session 无法承接上一轮有效结论

## Decision

1. 把 `resume` 与 `fresh_with_handoff` 区分为两个明确运行时动作。
2. 继续保持 `resume` 优先，但只在当前 session 仍值得续接时使用。
3. 当出现以下任一条件时，允许 supervisor 轮换到 `fresh_with_handoff`：
- 最近 cycle log 出现 `context compacted`
- 连续 resume 已达到本地阈值
4. `fresh_with_handoff` 不依赖外部人工总结；先由 runtime 生成最小交接文件，再拼接进下一轮首跳 prompt。

## Minimal handoff surface

- `rotation_reason`
- `previous_launch_kind`
- `previous_tool_session_id`（如可得）
- `previous_cycle_log`
- `branch`
- `worktree_path`
- recent output excerpt

## Resulting implementation boundary

- `runtime/freely`
  - 选择 `fresh | resume`
  - 维护 session state
  - 生成 handoff 文件
- `start-lead-agent prompt`
  - 继续作为首跳主提示
- runtime prompt assembly
  - 在 fresh-with-handoff 时追加 handoff 内容
- `monitor-ai-cli.sh`
  - 保持 AI CLI 监控职责不变，只补测试工具模拟器
