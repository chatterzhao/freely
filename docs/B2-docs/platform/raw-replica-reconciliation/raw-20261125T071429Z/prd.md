---
prd_id: PRD-20261125T071429Z-A
issue_id: I-20261125T071429Z-A
source_raw: raw-20261125T071429Z
epic: platform
story: raw-replica-reconciliation
created_at: 2026-11-25
---

# PRD: I-* 终态平台取证与关闭对账

## 1. 问题陈述

`wt-close` 删除工位前要求 I-* 终态，但判定依据是本地 `platform_state`。该字段可能因四种原因与平台不一致：

| 来源 | 机制 | 现状 |
|------|------|------|
| 未映射副本 | `close_linked` 只关闭 `platform_ids` 内的副本 | 孤儿/重复副本永久 OPEN |
| 部分失败 | `cmd-batch.sh:118`、`pr-merge-guarded:573` 的 `|| true` | 失败不影响退出码 |
| 跳过同源 | `cmd-batch.sh:64` 以 `platform_state=closed` 判定「双方一致」 | 漂移永不复查 |
| 重复创建 | `_already_on_platform` 只读本地映射 | `platform_ids: {}` 时每次 batch 造新副本 |

## 2. 目标行为

### 2.1 门禁（wt-close，只读）

- 对 raw 下每个 `promoted_children` / `absorbed_into` 的 I-*：
  - `phase_state` 必须 `completed`（既有规则不变）；
  - 调 `platform-adapter verify-local-id <I-id>`：返回的 OPEN 副本必须为空；
  - 平台不可读（degraded / error）→ 拒绝，错误信息包含重试命令。
- 全程无平台写；`--skip-platform` 仍保留但必须带 `--reason`（记录为审计行）。

### 2.2 关闭（issue-sync，写）

- `close_linked` 改为调用 adapter `close-local-id <I-id> <platform_ids_json>`：
  1. 在每个 configured platform 上按标题枚举该 local_id 的 OPEN 副本；
  2. 与 `platform_ids` 并集去重；
  3. 逐平台关闭；任一平台非 closed → 退出码 3/1，不写 `platform_state`；
  4. 全部 closed → 写 `platform_state: closed`。
- `batch` 不再对 `cmd_close_linked` 使用 `|| true`；汇总失败并在末尾以非零退出。

### 2.3 合并门禁（pr-merge-guarded）

- `batch` 返回非零 → 打印失败摘要并中止合并（不落 merge commit），提示修复命令。

### 2.4 去重

- `batch` 在 `create` 前用 `verify-local-id` 判定平台是否已有该 local_id 的 **OPEN** 副本；有则跳过 create 并输出「unmapped replica，交给 close-local-id 对账」提示。已关闭但未映射的副本不在此判定内（无重复创建风险，且全文枚举成本高）。

## 3. 兼容性

- `platform-adapter` 现有子命令不变；新增 `verify-local-id`（只读）与 `close-local-id`（写）。
- 既有 AT `test-wt-close-children.py` 的断言（platform_state != closed 即拒绝）保留，新增断言在其前执行。
- 历史遗留 OPEN 副本不在本 PR 清理。

## 4. 风险

| 风险 | 缓解 |
|------|------|
| 平台读延迟导致误拒 | 仅在收口时读一次；失败信息给出重试命令，允许人工确认后重跑 |
| 标题枚举误伤 | 只匹配标题含 `local_id` 且含 `[I-` 的 issue；raw 标题不含 `I-` |
| `--skip-platform` 破坏既有脚本 | 保留 flag，只新增 `--reason` 要求；同步更新提示 |
| batch 失败导致合并被阻断 | 这正是目标；错误信息给出可执行修复命令 |
