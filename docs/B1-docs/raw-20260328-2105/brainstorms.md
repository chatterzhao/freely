# Brainstorms - 20260328-2105--resume-evidence-strength-and-false-positive-resume-governance

## Context

在 `2026-03-28` 的 `develop` 现场，Freely 出现了两条同时存在但性质不同的故障链：

- 真实账号 / 工作区故障：
  - `cycle-20260328-071149.log` 出现 `402 Payment Required` 与 `deactivated_workspace`
  - runtime 将其归类为 `auth_failure`
  - 这条链属于真实外部故障，watchdog / slot probe / restart handoff 应继续负责吸收
- 假 resume evidence 故障：
  - fresh 首轮失败时，runtime 从 cycle log 读到了 `session id`
  - 同一轮却已确认 `jsonl_path=unavailable`
  - supervisor 仍把这个 id 持久化为下轮 `resume_target`
  - 后续连续 `resume` 同一个不可恢复 id，直到 `restart_storm_pause`

这说明当前问题不是“resume 功能整体坏掉”，而是“Freely 把不够强的恢复证据误判成可恢复会话”。

## Related Prior Research

这条线与两个既有研究家族相关，但都不能直接代替本条：

- `20260321-2010--explicit-session-addressed-resume-over-last-and-pty`
  - 已经收敛出“显式 session-addressed resume 是正确方向”
  - 但没有继续定义“什么证据才足够强到可以 resume”
- `20260308-0145--state-sync-and-session-evidence-governance`
  - 已经把 `tool + session_id + jsonl_path + role` 立成跨环最小证据
  - 但没有把这套证据强度真正落进 runtime 的 launch-kind 判定

因此本条不是要推翻旧结论，而是要补齐：

- explicit session targeting 已确立之后
- verified resume evidence 应如何定义与消费

## Reproduced Facts

### 1. 现场链条已经完整落盘

`develop` 的 `.freely/logs/runtime-events.log` 已记录以下顺序：

- `fresh` 首轮结束，拿到 `session_id=019d374c-6743-7020-a420-14573edb41cd`
- 同时 `jsonl_path=unavailable`
- 后续多轮仍以 `launch_kind=resume` 重试该 id
- 最终进入 `restart_storm_pause`

这说明恢复路径不是根据“是否有 rollout/jsonl 证据”决定，而是根据“是否看到了某个 session id”决定。

### 1b. 这不是最近 auth/watchdog 提交直接引入的回归

git 历史检查表明：

- 当前“观察到 `session id` 后直接升格为 `resume_target`”的逻辑来自更早的显式 resume 改造
- `extract_tool_session_id_from_log()` 与 `tool_runtime_resume_target_after_cycle()` 都早于 `2026-03-28` 这轮 auth/watchdog 现场异常

所以这次故障更像：

- 旧恢复逻辑缺口被真实账号故障和 fresh 失败放大

而不是：

- 最近账号治理或 watchdog 修复直接把 resume 逻辑搞坏

### 2. 底层工具层复现已经成立

在隔离工位中，直接执行：

- `codex exec resume 019d374c-6743-7020-a420-14573edb41cd ...`

稳定报错：

- `thread/resume failed: no rollout found for thread id 019d374c-6743-7020-a420-14573edb41cd`

同样的错误也通过 `monitor-ai-cli.sh` 的 `resume` 路径复现，日志写入：

- `.freely/logs/invalid-resume.log`

这说明坏的是 resume target 本身，不是 status surface 的错觉。

### 3. 健康 resume 仍然存在，不能被修掉

另一个隔离工位已经观察到：

- 有效 session 上的 `resume` 可以连续工作
- 即使某次 `resume` 返回 `rc=1`，runtime 也会在达到轮换条件时转为 `fresh_with_handoff`

所以安全修复边界不是“禁用 resume”，而是“拒绝把假证据当成 resume evidence”。

## Root Cause Hypothesis

当前 runtime 的 continuity contract 存在一个深层缺口：

- `extract_tool_session_id_from_log()` 只要从 cycle log 读到 `session id:`，就接受该 id
- `tool_runtime_resume_target_after_cycle()` 会把这个 id 直接升格为下一轮 `resume_target`
- `tool_has_resume_evidence()` 对 `codex` 只检查 `resume_target` 非空，不检查 rollout/jsonl 是否真实存在

结果就是：

- `session_id` 被当成“强恢复证据”
- 但它实际上只是“弱观察信号”

对 `codex` 这类显式 session-addressed resume 工具而言，`session_id` 只说明某轮日志里提到过一个线程，不说明：

- 该线程当前仍可恢复
- 本地 rollout/jsonl 可被 runtime 追溯
- 下一轮应该继续 resume 而不是 fresh handoff

更准确地说，当前 runtime 混淆了三层事实：

- `observed`: 本轮日志里观察到某个 session id
- `persistable`: 这个 session id 值得写入 continuity state
- `resumable`: 下一轮 supervisor 应该真的对它执行 `resume`

这三层不应再被一个非空字符串折叠成同一个判断。

## Contract Drift

这次故障首先暴露的是当前 `codex` resume path 的 contract drift，而不只是一个 if 判断写漏了：

- `LAWS` 已要求跨环恢复至少保留 `tool + session_id + jsonl_path + role`
- 更强的恢复语义还建议附带 `branch`、`worktree_path`、`phase_state`、`runtime_state`、`resume_hint`
- 但 runtime 当前真正的 `resume` 判定仍然退化成了“`resume_target` 是否非空”

也就是说：

- 文档上的 continuity contract 已经更强
- 当前 `codex` resume path 的恢复证据判定却没有同步升级到这个强度

## Boundary

本条预研应保持边界清晰：

- 它不是账号池治理问题；账号 / workspace 故障仍应由 watchdog slot recovery 处理
- 它不是 `live-status` 观测面问题；观测不一致可以并行研究，但不能替代恢复证据修复
- 它不是要回退 `explicit session-addressed resume`；显式 session 寻址仍然正确
- 它也不是要让 runtime 重新依赖 `resume --last`、PTY 注入或更弱的 continuation 模型

本条只研究一件事：

- 什么才算“足够强、足以触发下一轮 resume 的证据”

## Candidate Directions

### Direction A: Tiered Resume Evidence

把 resume evidence 升级成显式分层，而不是布尔值：

- `strong`
  - `session_id` 存在
  - 且对应 rollout/jsonl 可追溯
  - 且满足当前工具的 resume precondition
- `weak`
  - 只有 `session_id`
  - 或只有不完整的历史线索
- `none`
  - 既没有可用 session，也没有可消费 handoff 证据

runtime 只允许 `strong` 进入 `resume`。
`weak` 必须降级为 `fresh_with_handoff` 或等价的 `missing_resume_evidence`。

### Direction B: Verified Resume Resolver

不要在不同函数里零散做“看到 session id 就记下来”的局部判断。
应该把以下步骤合并成一个统一解析器：

1. 提取观测到的 session id
2. 解析对应 rollout/jsonl 路径
3. 生成 evidence strength
4. 决定：
   - persist 哪些字段
   - 是否允许下轮 `resume`
   - 若不允许，应以什么 reason 降级成 `fresh_with_handoff`

### Direction C: Recovery-Grade Test Template

这次暴露了一个明确的测试空洞：

- 已有测试覆盖“没有 resume evidence”
- 已有测试覆盖“健康 explicit resume”
- 但缺少“有 session id、无 rollout/jsonl”的假阳性场景

这类场景至少应成为 `codex` 的标准恢复测试模板。
如果后续审计发现其他显式 session-addressed tool 也存在“session id 可见但 replay evidence 不可追溯”的情况，再把它上升为共享恢复测试模板。

## Initial Decision

更合理的第一跳不是直接改实现，而是先把以下结论固定下来：

1. `session_id` 不是对 `codex` 自动充分的 resume evidence
2. `observed session id + missing rollout/jsonl` 必须被视为弱证据或无效证据
3. runtime 必须在保持健康 resume 能力的前提下，把这类场景自动降级为 `fresh_with_handoff`
4. 这套判断应抽象成 Freely 的恢复能力，而不是只补一个现场特判
