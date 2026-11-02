# PRD: owner lane 显式认领 manager 身份

## Goal

让 owner 自建的工位可运行，同时不放松身份边界：

`pwd → agent_working(行存在?) → existing | claim(唯一 manager + 真实 worktree + 分支可解析) → 落库 → 返回`

## Modules

- `runtime/owner_lane.py`（新）：`claim(project, path)`，纯判定 + 一次写库。
- `runtime/freely::_resolve_current_agent_id`：在原逻辑失败、且当前路径不是项目根时调用 claim；成功则打印 `owner-lane claim: <path> → <agent>`。
- `tests/test-owner-lane-claim.py`（新）：注入 `rows / managers / worktrees / write` 五个决策用例。

## Invariants

- 已有绑定（任意角色）一律原样返回，不覆盖、不新增。
- 只有 `manager` 角色可以被自动认领；worker / reviewer 没有此通道。
- 认领要求项目只配置一个 manager；多个即 `manager_not_unique`，保持 fail-closed。
- 认领要求路径出现在 `git worktree list --porcelain` 中；否则 `not_a_worktree`。
- raw_key 必须由分支名 `raw-<YYYYMMDDTHHMM[SS]Z>` 解析；解析不到即 `raw_key_unresolved`，不用目录名兜底。
- 读不到 `agent_working`（无 DB socket / RPC 失败）时返回 `rows_unreadable` 并拒绝认领——不能在看不见绑定的情况下写绑定。
- 认领必须落库；只返回不写库的“回退”被明确禁止。

## 非目标

- 不恢复 `agent-id.env`。
- 不改 `agent_working` 表结构。
- 不在 `wt-create` 里写身份行（owner / worker 语义不能混在一个命令里）。
- 不做身份一致性巡检（C-20261102T103231Z-B）。

## Dev-loop handoff

先写五个决策用例并跑红（模块不存在），再实现 `owner_lane.py`，最后接 `_resolve_current_agent_id` 并在真实工位验证 daemon 能越过身份解析。
