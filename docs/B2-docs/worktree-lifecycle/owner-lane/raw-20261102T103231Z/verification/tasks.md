# Tasks: I-20261102T103231Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | claim 判定与守卫（零行 / 唯一 manager / 真实 worktree / 分支可解析） | `runtime/owner_lane.py` | — | AT-001 / AT-002 / AT-003 |
| T2 [x] | 接入 `_resolve_current_agent_id`，保留 fail-closed | `runtime/freely` | T1 | AT-005 |
| T3 [x] | 工位缺 agent-table.toml 时从 FREELY_HOME 解析 | `runtime/owner_lane.py` | T1 | AT-004 |
| T4 [x] | test 车道分支缺 raw- 前缀也能解析 | `runtime/owner_lane.py` | T3 | AT-004 |
| T5 [x] | 新工位自动带 agent-table.toml（daemon slot 解析） | `scripts/worktree/wt-create` | — | AT-005 |
| T6 [x] | 证据与门禁 | `verification/test-evidence/*` | T1–T5 | 六份日志/输出 |

## 备注

- T3/T4/T5 不在最初的 candidate 范围内，是端到端验证时逐层暴露的：先 `manager_not_unique`（无 agent-table.toml），再 `raw_key_unresolved`（test 车道分支没有 raw- 前缀），最后 `AGENT_AI_TOOL not set`（daemon 解析 slot 仍读工位本地表）。三者都是同一个缺陷的不同断面——“工位被假定拥有项目级配置”，因此并入本 issue 而不是另开。
- 未改动 `agent_working` 表结构；未恢复 `agent-id.env`；未给 worker/reviewer 自动认领通道。
