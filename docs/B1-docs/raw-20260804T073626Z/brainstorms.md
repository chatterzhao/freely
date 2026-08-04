---
b1_id: B1-20260804T073626Z
phase_state: completed
source_raw: raw-20260804T073626Z
source_url: https://github.com/chatterzhao/freely/issues/4077
produced_candidate: C-20260804T073626Z-A
created_at: 2026-08-04T08:30:00Z
---

# B1_IBM: platform-adapter pull KeyError 阻塞 wt-create

## Input

- 来源：`raw-20260804T073626Z`（GitHub #4077 / Gitee IK6EKQ）。
- 现象：`freely wt-create --source platform` 在 raw-issue-pull 阶段失败，`platform-adapter.py pull` 抛 `KeyError: issue_number`。
- 根因（raw issue 已记录）：GitHub `search_raw_issue` needle 大小写不对称 + 顶层把 `{"matches": []}` 当有效结果 + pull 直接取 `info["issue_number"]`。

## Discovery

- 2026-08-04 验证：`feature/raw-20260725T030511Z-raw-replica-reconciliation`（I-20260725T030511Z-A）已合并进 develop，包含：
  - GitHub/Gitee `search_raw_issue` needle 改为 `f"raw-{raw_key}".lower()`（platform-adapter.py L234/L426）。
  - `pull_raw_issue` 重构为 `discover_raw_replicas` 契约，统一 `issue_id`，不再直接取 `issue_number`（L710/L954）。
  - 残留调用点 `_comment_via_local_issue`（L917）与 `_resolve_issue_state`（L942）均用 `.get("issue_number", "")` 防御，无 KeyError 路径。
- 行为验证：`freely wt-create --raw-key 20260804T073054Z` 与 `20260804T073626Z` 均成功创建工位（此前全部失败）。

## Brainstorm

### Option A：在本 issue 内重写 search/契约

重复实现已被 reconciliation 工位修复的逻辑，产生重复代码与潜在回归。拒绝。

### Option B：验证已合并修复并标记 absorbed

逐项核对 raw issue 的四条修复建议是否全部落地，验证 wt-create 真实可用；若无残留，标记 absorbed，指向吸收者 I-20260725T030511Z-A。采用。

## Decision

采用 Option B。raw-20260804T073626Z 的全部修复点已由 I-20260725T030511Z-A 的合并实现覆盖并经真实命令验证，无需新开实现。

## Candidate

- candidate_id: `C-20260804T073626Z-A`
- status: absorbed
- milestone: `M-20260804T073626Z-A`
- absorbed_into: `I-20260725T030511Z-A`
