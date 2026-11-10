---
schema_version: '1'
local_id: raw-20261110T081029Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T081029Z-A
platform_ids:
  github:
    issue_id: '4261'
    url: https://github.com/chatterzhao/freely/issues/4261
    synced_at: ''
  gitee:
    issue_id: IKUBSG
    url: https://gitee.com/zhaoquan/freely/issues/IKUBSG
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T081029Z/issues/I-20261110T081029Z-A.md
last_synced_comment_at:
  github: '2026-11-10T08:48:08Z'
  gitee: '2026-11-10T08:48:08Z'
hash: ''
created_at: '2026-11-10T08:10:29Z'
updated_at: '2026-11-10T08:48:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T081029Z-A
source_candidate: ''
completed_at: '2026-11-10T08:48:07Z'
closeout_note: ''
severity: P1
---

# fix: 状态文件迁移第二族起（剩余 54 处 source 逐步归零）

workflow_kind: fix

## 背景

从 #4258 / `raw-20261110T074344Z`（状态文件逐组迁移）的 continuation。`fix/raw-20261110T074344Z-migrate-state-family` 已完成**第一族 cooldown-state.env**：

- `state_file.py` 增加 `values` 行接口与 `write --kv` argv 接口；
- `_read/_write_cooldown_state` 去掉 `source` 与 `printf`，改走安全协议；
- AT-001 RED 2/6 → GREEN 8/0（旧实现注入 PoC 真的创建 marker）；
- `bin/check-state-file-sources` 计数 **55 → 54**。

本 issue 承接**剩余 54 处状态 `source` 与对应写入点**，按族逐轮迁移。

## 剩余族（按形态/文件族）

| 族 | 读点数 | 备注 |
|---|---|---|
| `workcell_state_file` | 20 | `source "$(workcell_state_file "$project")"` |
| `manager_worker_launch_state_file` | 7 | 有较多 `test-freely-manager-worker-launch-*` 回归可作护栏 |
| `session_state_file` 系 `$state_file` | 22 | 分散在多个函数，需逐个确认所属状态文件 |
| 带 `2>/dev/null \|\| true` 的状态 source | 4 | 保留容错语义 |
| `session_state_file` 直接调用 | 2 | — |
| 位置格式文件（`printf '%s\|%s'`） | 若干 | 不是 KEY=value，需单独判定是否适合 `state_file.py` |

另有 **39 处非状态 source**（库加载、identity 文件）不得误改；`load_meta_env_snapshot` 对 `meta.env` 的解析不动。白名单 `ALLOWED_KEYS` 现有 77 键，若新族出现新键须先扩充。

## 复制第一族的做法

1. 读侧用 `state_file.py values <path> <keys...>` + `{ read -r ...; } < <(...)`（macOS bash 3.2 无 `mapfile`）；含换行的值改用 JSON `read` 接口。
2. 写侧用 `write --kv KEY=VALUE ...`（argv 安全）或 `write --data`。
3. 兼容期保留：reader 仍可读旧 `KEY=value`，但不展开 `$()`/反引号。
4. 每族一组独立提交 + 对应 `test-freely-*` 回归；`check-state-file-sources` 计数应逐轮下降。

## 验收标准

- GREEN：每轮 `check-state-file-sources` 计数严格下降，最终 `grep -n 'source ".*state' docs/system/workspace/scripts/runtime/freely` 无命中。
- GREEN：归零后把 lint 基线改为 0，禁止任何新增状态 source。
- GREEN：每族旧格式文件可读，注入文本不执行，值逐字节相等；`bin/test-all --ci` 与状态回归全绿。
- GREEN：不改键名与语义，不改 39 处非状态 source，不要求人工清空 `.freely/run/`。

## 不做

- 不一次性替换全部（77 键白名单与位置格式需逐族判定）。
- 不改 `load_meta_env_snapshot`。
- 不删除既有状态文件。

### comment-20261110T084808Z
- source: system
- event: promote_finalized
- children: ["I-20261110T081029Z-A"]

拆解为以下任务:
1. [I-20261110T081029Z-A](will-be-updated)
