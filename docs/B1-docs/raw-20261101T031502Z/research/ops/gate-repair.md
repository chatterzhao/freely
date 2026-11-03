---
adr_id: ADR-010-20261101T031502Z
phase_state: accepted
created_at: 2026-11-01
---

# B1 promotion gate 修复：研究证据 vs B2 运行时验收

## 0. 问题

独立评审发现：C-C/C-E 的 `promotion_gate` 要求“真实 patrol 前后对照”“P0/P1 runtime spike”，但这些只能在实现后取得；B1 promotion 又必须先于 B2。逻辑循环，导致 candidate 永远无法 promote。

这不是“降低标准”，而是**gate 放错阶段**：

- B1 gate 应验证：问题是否研究透、方案/协议/接口是否可执行、是否有研究级回放。
- B2/TDD 应验证：运行时行为、真实环境、前后对照。

## 1. 拆分规则

每个 candidate 增加 `b2_acceptance`，原 `acceptance_criteria` 保留为完整目标；`promotion_gate` 只保留 B1 可关闭的研究证据。

| Candidate | B1 promotion_gate（研究） | B2 acceptance（运行时） |
| --- | --- | --- |
| C-F | 六类 event schema/准入/选型 + 真实 issue/PR/CI 回放 + 独立 review | adapter 方法、events 表、scan/queue、CI 事件、去重 |
| C-B | 五类行为矩阵 + protocol v0 + 状态机/真实线程回放 + 独立 review | new/fork 修复、handoff 表、真实 PR/issue 回放 |
| C-C | report/attention schema + manifest + 可观测性基线 + fixture 对照 + 独立 review | 真实 patrol 前后对照、usage/cache reported |
| C-D | Protocol/RoleConfig + 三角色 probe 输出 + 独立 review | `--role`、apply/validate、UI/CLI 后端 |
| C-E | 静态插件契约 + 真实 host P0/P1 spike + 独立 review | Python bridge、首次 session、gate E2E、完整 issue→PR |

C-E 的 runtime spike 仍在 B1，因为“插件能否加载/调用”是可行性问题，不是实现验收；没有 spike 不 promote。

## 2. 研究债账本同步

- `research-debt.md` 的“研究缺口”列只记研究债；“实现/验证缺口”列记 B2 债。
- `phase_state` 改为 `research_closed` 时，表示研究债关闭，不表示 candidate promoted。
- `research/README.md` 的 `phase_state: completed` 只表示研究包整理完成；B1 loop 仍按 candidate 状态。

## 3. 不改变的东西

- 原 acceptance_criteria 不删；B2 用它。
- C-E 的 runtime spike 不降级；没跑不 promote。
- 不因为 gate 修复而跳过独立 review；review 仍要按完整文档判。
