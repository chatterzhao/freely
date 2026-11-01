# Implementation Decision Note

## decision

新增 `agent_protocol.py` 和 `prompt_manifest.py`；`a2a-report` CLI 写同一 `freely.db`。prompt 用 `<!-- FREELY_SEGMENT:name -->` 标记；无标记退化为 `full_prompt`，不伪造 11 段。

## why_this

- A2A task 行不适合塞 JSON；新表 append-only，旧查询不受影响。
- report/attention 必须先校验再落库，避免自由文本。
- manifest 只有真实 marker 才算段；没有 marker 如实记录，不制造假 prefix。
- 不改 Manager 批量路由，先提供可验证的库/CLI。

## alternatives_considered

- 扩 a2a_tasks 列：迁移风险高。
- 重写 prompt 11 段：范围过大，先 marker + 渐进。
- 把 JSON 塞 summary：不可查询，拒绝。

## boundary_non_goals

- 不做 Manager batch 接线、UI、真实 patrol。
- 不保证 provider cache 命中；只区分 reported/estimated/absent。

## residual_risk

- prompt marker 只覆盖当前 bootstrap/fleet；agent_role/exit_contract 可能由 runtime 前置，manifest 会少段。
- 真实 patrol 对照需 test 阶段；fixture 不能冒充。
