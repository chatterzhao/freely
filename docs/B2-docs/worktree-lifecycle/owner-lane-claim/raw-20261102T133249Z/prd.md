# PRD: 认领判定下沉

## Goal

`_resolve_current_agent_id` 只负责“问一次”，不再在 bash 里判断“该不该认领”。

## Modules

- `runtime/freely::_resolve_current_agent_id`：删除路径不等守卫；捕获 claim 的 stderr，失败时记录 reason。
- `runtime/freely::_start_freely_db`：启动前 `mkdir -p .freely/run`（新工位没有该目录）。
- `tests/test-owner-lane-claim-wiring.py`（新）：锁死“不得重新引入路径守卫”“不得吞 stderr”。
- `tests/test-owner-lane-claim.py`：补 `project == path` 两条锁定用例。

## Invariants

- 认领安全条件全部由 `owner_lane.claim` 承担：零行、唯一 manager、真实 worktree、分支可解析。
- bash 不得出现 `_current_path` 与 `project` 的不等比较。
- claim 失败必须留 reason（stderr 不得丢弃）。
- 项目根（分支 develop）永远不会被认领。

## 非目标

- 不改 claim 的四条守卫。
- 不改 agent_working 表结构。
- 不处理 test-gate.env 在启动失败后仍被写 completed 的问题（另立 raw）。

## Dev-loop handoff

先补 wiring 测试（当前必红），再改 bash；随后补两条 `project == path` 单测，最后在全新工位做一次真实的 daemon start。
