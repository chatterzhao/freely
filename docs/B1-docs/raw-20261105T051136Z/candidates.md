---
candidate_id: C-20261105T051136Z-A
status: promoted
source_raw: raw-20261105T051136Z
created_at: 2026-11-05
milestone: M-20261105T051136Z-A
---

# Candidates

## C-20261105T051136Z-A: 保留兼容判定、修好达标动作与本地身份

- candidate_format_version: v2
- title: 保留 created_at 兼容分支，把本地身份锚定到调用方 key，并把平台标题自动修正收敛为单一真源
- status: promoted
- decision_reason: 根因不是「反推」而是「反推被当成改写本地身份的授权」+「标题修正动作是 no-op」+「双层静默吞错」。Option A（禁止反推）会删除用户明确要求保留的兼容能力；Option B 用六项动作分别修复判定/动作/规则/可观测性，且四处既有能力一个不删。scope 判定为一个独立问题：五处改动同因同源，拆多个 candidate 会破坏「单一真源」目标。
- next_action: 先写 AT-001 回归测试确认 RED（复现漂移目录与 no-op 修正），再实现六项动作，跑 GREEN 并做全量退化审计。
- revisit_trigger: 若后续要把 raw 身份改为平台侧全局唯一 ID（而非本地时间戳），另开 issue；本 PR 只统一「调用方 key 即本地真源」与标题达标规则。
- acceptance_criteria:
  - 标题不含 canonical 前缀时，物化目录名、返回 `local_id`、frontmatter `local_id` 三者全部仍等于调用方 key；不产生任何漂移目录。
  - 平台标题被修正为 `[RAW-<调用方 key>] <原用户标题>`，去掉已有重复前缀、保留 `fix:` 等类型前缀、遵守 100 字符上限，并同步到所有已配置平台。
  - `_created_at_to_key()` 兼容分支与诊断日志保留；`_resolve_raw_identity()` 对无前缀历史 issue 的单条兜底仍可用；`cmd_feedback` create 的校验与 `[RAW-stamp]` 前缀不改。
  - `wt-create._pull_raw_issue()` 在 `local_id` 不匹配或目标 `issue.md` 缺失时返回失败，由既有清理分支移除 dev 工位。
  - `bin/raw-issue-pull` 不再静默吞掉 `issue-sync create` 失败，至少输出可诊断告警。
  - `feedback edit --title` 对 raw issue 自动补全达标前缀，且不回写任何历史标题。
  - 全量退化审计：`_platform_title()` 对 803 份真实 B1 issue.md 的输出差异必须全部可归因为「去重复前缀」或「100 字符上限」两类修正；相关回归测试零新增失败。
- promotion_gate: AT-001 RED → GREEN + 全量退化审计 + 相关回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对 `platform-adapter.py:1201-1206/1247-1256`、`wt-create:456-471/850-865`、`bin/raw-issue-pull`、`bin/issue-sync:216-245`、`runtime/freely:24869-24979`；在未修改基线复现漂移目录 `raw-20261105T051142Z` 与 no-op 标题修正；核对 #4148 已覆盖冲突标记发现，确认不重复建 issue。
  - verdict: pass
- promoted_issue_id: I-20261105T051136Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-parity/raw-20261105T051136Z/issues/I-20261105T051136Z-A.md
- milestone: M-20261105T051136Z-A
- session_refs: []
