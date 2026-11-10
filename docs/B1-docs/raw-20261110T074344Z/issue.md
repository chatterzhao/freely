---
schema_version: '1'
local_id: raw-20261110T074344Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T074344Z-A
platform_ids:
  github:
    issue_id: '4258'
    url: https://github.com/chatterzhao/freely/issues/4258
    synced_at: ''
  gitee:
    issue_id: IKUB9Q
    url: https://gitee.com/zhaoquan/freely/issues/IKUB9Q
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T074344Z/issues/I-20261110T074344Z-A.md
last_synced_comment_at:
  github: '2026-11-10T08:11:29Z'
  gitee: '2026-11-10T08:11:29Z'
hash: ''
created_at: '2026-11-10T07:43:44Z'
updated_at: '2026-11-10T08:16:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T074344Z-A
source_candidate: ''
completed_at: '2026-11-10T08:11:28Z'
closeout_note: ''
severity: P1
---

# fix: 状态文件读写点逐组迁移到安全协议（输入边界三）

workflow_kind: fix

## 背景

从 #4252 / IKU9MB（状态文件 source 可执行化）拆分。本轮（R23.9 第一阶段）已完成并验证：

- 新增 `runtime/state_file.py`：单一所有者读写协议。新格式 `KEY<TAB>json-encoded string`；兼容旧 `KEY="value"` 但**绝不展开** `$()`/反引号/引号；显式 `ALLOWED_KEYS` 白名单（77 键，来自 develop 全量扫描）；`to-shell` 用 `shlex.quote` 生成惰性赋值。
- 新增 `bin/check-state-file-sources`：登记基线 55 处 `source` 状态文件调用，只降不升，并禁止安全模块出现 `eval`/`exec`/`subprocess`。
- AT-001 RED 1/7 → GREEN 9/0（含旧格式 `source "$(touch marker)"` 注入 PoC、恶意值逐字节 round-trip、未知键拒绝、旧格式不展开、`to-shell` 惰性）。

本 issue 承接**第二阶段：逐组迁移读写点**。

## 实测规模（develop ea9f5b38c）

- `source ".*state` 在 `runtime/freely` 命中 **55 处**（issue 原报 20，已增长）：`source "$state_file"` 22、`source "$(workcell_state_file "$project")"` 20、`source "$(manager_worker_launch_state_file "$project")"` 7、带 `2>/dev/null || true` 4、`session_state_file` 2。
- 另有 39 处非状态 `source`（库加载、identity 文件等），**不得误改**。
- 写入点 `cat >"$state_file" <<EOF` / `printf 'KEY=%s\n'` 至少 15 处；77 个状态键已在白名单中。
- 部分状态文件是位置格式（`printf '%s|%s\n'`），不是 KEY=value，需单独判定。

## 修复方案（按族分组，每组独立提交）

1. 在 `freely` 定义 `runtime_state_load()`：文件不存在返回 0；调用 `state_file.py to-shell` 生成安全赋值，写入 `${path}.loaded.$$` 临时文件后 source（值已 shlex.quote，不可注入），随即删除。
2. 把 55 处 `source` 按 5 种形态机械替换为 `runtime_state_load`，保留 `2>/dev/null || true` 等语义。
3. 每组迁移后跑对应 `test-freely-*` 状态回归（manager-worker-launch / workcell / session / cooldown / preemption）。
4. 逐组把写入点改用 `state_file.py write`（新格式）；兼容期 reader 同时读旧格式，迁移完成后可收紧。
5. `check-state-file-sources` 的基线数字随每组下降，最终归零；归零后可把 lint 改为「0 处命中」。

## 验收标准

- GREEN：`grep -n 'source ".*state' docs/system/workspace/scripts/runtime/freely` 无命中。
- GREEN：每组迁移后对应状态回归全绿，且 `bin/test-all --ci` 不退化。
- GREEN：含双引号/换行/tab/`$()` 的状态值经写读两侧逐字节相等，且不执行。
- GREEN：滚动升级期间旧状态文件可读，不要求人工清空 `.freely/run/`。

## 不做

- 不改 39 处非状态 `source`。
- 不改 `load_meta_env_snapshot` 对 `meta.env` 的既有解析。
- 不一次性重写全部状态文件（会丢 daemon 恢复信息）。

### comment-20261110T081128Z
- source: system
- event: promote_finalized
- children: ["I-20261110T074344Z-A"]

拆解为以下任务:
1. [I-20261110T074344Z-A](will-be-updated)
