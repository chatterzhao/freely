---
schema_version: '1'
local_id: raw-20261113T110656Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4338'
    url: https://github.com/chatterzhao/freely/issues/4338
    synced_at: ''
  gitee:
    issue_id: IKV7AS
    url: https://gitee.com/zhaoquan/freely/issues/IKV7AS
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-13T11:06:56Z'
updated_at: '2026-11-13T11:07:02Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
severity: P2
---

# feat: 分批迁移 13 条 implementation-in-bin 到 workspace/scripts 投影

workflow_kind: feature

## feat: 分批迁移 13 条 implementation-in-bin 到 workspace/scripts 投影

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T110656Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T11:06:56Z |
| updated | 2026-11-13T11:06:56Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T110656Z`。实现前请用 `wt-create --raw-key 20261113T110656Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 背景

R32.5 / #4302 的 C-A 已合并（`52b095892`）：把 `docs/system/workspace/scripts/bin-projections.yaml` 里 35 条 `implementation-in-bin` 按项目设计意图逐条判定，22 条自包含 lint/聚合/one-shot 标为 `standalone-tool`（**不是豁免**，coverage/staleness/shrink 三条门禁规则照常生效），13 条判定为真实业务实现、应迁移。

`pr-create-guarded` Step 0b 要求 raw `phase_state: absorbed`（必须先 `promote-finalize`），因此同一 raw 无法跨多个 PR 保持 open；按项目惯例「部分完成 → 另立新 raw」，13 条迁移由本 raw 承接。

## 待迁移清单（13 条）

| 文件 | 行数 | 建议真源域 |
|---|---|---|
| `bin/agent-table-query` | 336 | `scripts/agents/`（或 `runtime/`） |
| `bin/freely-package` | 270 | `scripts/packaging/` |
| `bin/deploy-skills` | 216 | `scripts/skills/` |
| `bin/freely-review` | 202 | `scripts/worktree/` |
| `bin/test-pre-merge-selfhost` | 170 | `scripts/tests/` |
| `bin/raw-issue-pull` | 145 | `scripts/sync/` |
| `bin/issue-index` | 137 | `scripts/lifecycle/` |
| `bin/freely-cycle` | 129 | `scripts/runtime/` |
| `bin/cache-baseline` | 125 | `scripts/runtime/` |
| `bin/git-worktree-guard` | 111 | `scripts/worktree/` |
| `bin/freely-watchdog` | 88 | `scripts/runtime/` |
| `bin/pre-init-runtime` | 71 | `scripts/runtime/` |
| `bin/issue-sync-bootstrap` | 62 | `scripts/sync/` |

## 期望（按域分批，每批独立 PR）

1. 实现移到 `docs/system/workspace/scripts/<domain>/`，`bin/<cmd>` 变 ≤8 行 `exec` 投影；行为逐字不变（输入输出、退出码、错误文案）。
2. 变成投影后**删除注册表中对应条目**——`bin/check-bin-projection` 的 shrink 规则会强制，这正是债务收缩机制；不得保留条目或新增豁免。
3. 建议三批：① `sync/` + `skills/`（`raw-issue-pull`、`issue-sync-bootstrap`、`deploy-skills`）；② `runtime/` + `agents/`（6 条）；③ `worktree/` + `tests/` + `lifecycle/`（4 条）。每批独立 RED→GREEN、独立 wt-close。
4. **回归重点**：`bin/raw-issue-pull` 在 R33.11 刚修过「平台 comments 镜像 + 终态 phase 保护」，迁移后必须用 `test-raw-issue-pull-parity.py` 与 `raw-reconciliation-gate.py --require-local` 回归；`bin/deploy-skills` 在 R33.5 有 sha256 不变的验收。
5. 改到 `scripts/runtime/` 的批次同轮补 `tests/unit/t-*.sh`（R27 契约）。
6. 每批 AT 必须断言：投影文件 ≤8 行且 `exec` 真源、真源可执行且通过原有测试、注册表条目已删除、`bin/check-bin-projection` 全绿、行为与 develop 基线一致（可用快照对比）。

## 边界

- 不放宽 `bin/check-bin-projection` 的任一规则；不改 `threshold_lines`；
- `standalone-tool` 22 条不动；3 个 dispatcher 与 14 个 leaf 不动；
- 不改平台 adapter / 生命周期 / wt-close；
- 禁止一个 PR 夹带所有批次（R32.5 的修复方案明确「每批独立可合并」）。
