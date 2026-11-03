---
adr_id: ADR-20261101T031502Z
phase_state: accepted
created_at: 2026-11-01
---

# 跨切面 ADR：实现前必须定死的决策

## ADR-001 I-* 单一格式

**决策**：YAML frontmatter 是 canonical；正文 bullet 是投影。

- 现在 `pretests-gate` 只读正文 bullet `- phase_state:`；`pr-merge-guarded` 只读 YAML。两边必须过渡。
- B2 物化时同时写 YAML + bullet（兼容）；新增/修改只写 YAML，bullet 由脚本生成。
- 后续改 `pretests-gate` 读 YAML，再删除 bullet 投影。
- 不在同一次改动里同时改两个 parser 和所有历史文档；先兼容，后收敛。

## ADR-002 phase 单写者

**决策**：新增 `freely phase transition --issue <I-*> --to <state> --reason ...`；禁止 sed 直改。

状态转移表：

```
proposed → in_progress → done_b2_ibm → red → in_dev → in_verification → completed
任何非终态 → blocked/canceled
completed 不可回退；新工作新 issue
```

- 只有该命令写 `phase_state`；wt-create/pr-review/pr-merge 调它，不各自 sed。
- 每次转移写 `lifecycle-trace.log`（from/to/reason/actor/evidence）。
- 旧工位/历史文档允许保留旧值；新改动必须走命令。
- 实现前先加测试：非法转移拒绝、终态不可回退、重复转移幂等。

## ADR-003 TDD change_surface

**决策**：pre-tests 增加 `change_surface`，gate 按面分级。

| change_surface | 最低证据 |
| --- | --- |
| docs | 链接/结构/引用校验；可全 not_applicable |
| config | 解析/一致性校验；可全 not_applicable |
| script/runtime | 至少一个 test_command + passed |
| agent/skill/prompt | 行为回放/结构校验 |
| ui | 交互/截图/E2E |

- 代码类 issue 至少一个 `test_command` + `expected_output`；全 not_applicable 不能覆盖整个代码类 issue。
- `change_surface` 写在 I-* 或 pre-tests 头部；B2 声明，gate 校验。
- 与现有 `red-green-status` 兼容：仍要求 green，但增加面级最低证据。

## ADR-004 MCP 归属

**决策**：MCP 由 harness 拥有；Freely 只声明/传递，不内嵌 MCP server。

- `HarnessPort.capabilities.mcp` 标记 native/unsupported/unknown。
- 配置新增 `FREELY_ACP_MCP_SERVERS`（JSON 数组，可选）；`run-acp-prompt.py` 把它传给 `session/new|resume|fork` 的 `mcpServers`，不再固定 `[]`。
- 角色可覆盖（`{role}_mcp_servers`）作为后续；先全局。
- 没有配置时保持 `[]`，并在 `harness-status` 显示 `mcp=unsupported`，不假装已遵循。
- 不在 Freely runtime 内实现 MCP client/server；避免与 harness 的 MCP 双份。

## ADR-005 语义 Watchdog 边界

**决策**：不做第二个常驻 Agent；做一个 Manager 可调用的轻量 supervisor reviewer。

- 触发：每 N 个 patrol 或 Worker 超过 T 无进展/重复失败。
- 输入：A2A task、scan、progress、最近 events；不读全量代码。
- 输出：`progress|stuck|off_track|needs_human` + 证据 + 建议动作。
- 权限：只读；不能直接改任务/杀进程；由 Manager 决策。
- 失败：Watchdog 自身失败不影响主 loop；记录并降级。
- 不做：文章里的独立 Watchdog Session/云端控制面；先用 skill/subagent 实现。

## ADR-006 absorbed raw 下的 candidate promote

**决策**：C-B~F 直接从现有 raw 的 candidates 提升为 I-*；raw 保持 `absorbed_into I-A` 历史，不重开。

- B1 candidate 的 `source_raw` 仍指向 `raw-20261101T031502Z`；`promoted_issue_id` 用 `I-20261101T031502Z-{B..F}`。
- B2 物化到 `docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/issues/`。
- 不新建 raw，除非 scope 变成新问题；避免重复 raw/双状态。
- `pr-create-guarded` 若因 raw absorbed 拒绝，按 gate 错误修 gate/文档，不绕过。

## ADR-007 注意力度量

**决策**：先埋点，后算指标；没有 baseline 不报“提升”。

- 最小事件：`human_action`（chat/issue comment/PR review/approval）、`agent_attention`（input-required/needs_human）、`review_round`。
- 指标：人工动作数/issue、打断精度、决策时延、升级率、返工率、漏报率。
- 基线：选一个真实项目跑 2 周或 20 个 issue；在此之前只报计数，不报比率。
- 不在文档里写“注意力提升 X%”除非有日志。

## ADR-008 事件准入边界

**决策**：准入放 intake（scan 前），只做权威判断；价值判断归 B1。

- 规则：source enabled、actor allowed、bot policy、addressed、dedupe、rate/loop。
- 结果：`accept|observe|ignore|unavailable`，写 `events.disposition`。
- 不做 per-ticket Mandate；不做默认 observe（与 Freely 自主目标冲突）。
- 数据不够时 actor=`unknown` → 只 observe，不自动开工。

## ADR-009 DSH 插件边界

**决策**：只做 Freely-host 插件；不做 DSH-as-harness adapter；不加载 `dsh-superagent`。

- Freely 保留 Manager/Worker/Reviewer、A2A、scan、gates、worktree、PR。
- DSH 提供 Session/Agent/模型/preset/tools/skills。
- 配置真源 DSH settings；`.freely/harness.toml` 只镜像。
- 先 spike（静态契约已过），再 P0/P1；不先产品化。

## ADR-010 B1 promotion gate

见 [gate-repair.md](gate-repair.md)：B1 gate 只收研究证据；运行时验收进 `b2_acceptance`。

## 关闭证据

- 本文是 B2 的设计输入；实现后逐条回填测试/日志。
- 任何与本文冲突的实现，先改 ADR 再改代码，不能静默漂移。
