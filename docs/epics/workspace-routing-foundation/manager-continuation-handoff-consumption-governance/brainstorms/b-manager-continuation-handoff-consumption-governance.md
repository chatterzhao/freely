# Brainstorm: manager-continuation-handoff-consumption-governance

## Core Decision

这条 issue 不再讨论“manager continuation 有没有被正确 triage”。

该问题已经由历史 issue 收敛：
- broad manager chat 不应误吸到 cleanup
- 应回到 `handoff://continuation`

本 issue 只处理后半段：
- delegated continuation handoff 生成后
- runtime 如何在 prompt build / rotation / failure 边界上稳定记录它是否已被消费

## Dogfood Truth

真实 develop manager runtime 中观察到：

1. human chat -> intake -> interruption resolution 已正确生成 manager continuation handoff
2. 其中至少一条 handoff 已被写入下一轮 prompt 的 `Delegated continuation handoff`
3. 后续另一条 handoff 又命中了 local continuation re-entry
4. 下一轮 runtime 进一步命中 `context_compacted`，转入 `fresh_with_handoff`
5. 随后又因 `auth_failure` 停止

所以真实缺口不是“完全没消费”，而是：
- consumed 这件事没有 durable evidence
- failure boundary 之后看不清 pending / consumed / superseded

## Product Shape

最小产品形态应是 CLI-first：

- session-state 记录：
  - last delegated continuation pending ids
  - last delegated continuation consumed ids
  - last delegated continuation consumed at
- `live-status` 显示：
  - pending_manager_continuation_handoffs
  - last_consumed_manager_continuation_handoffs
- prompt build 负责把“consumed into prompt”写回状态
- `fresh_with_handoff` 只作为 rotation，不允许破坏 evidence

## Runtime Boundary

- 不把 intake item 从 `delegated` 自动改成 `absorbed`
- “consumed into prompt” 只表示：
  - runtime 已把 handoff 注入当前轮 prompt
- 真正的 canonical absorption 仍要靠后续 manager/worker resolution 完成

## Shell Safety

`write_session_handoff()` 的 here-doc 当前混入 markdown backticks，shell 会做 command substitution。
这类 handoff / prompt builder 文本必须避免未转义反引号。
