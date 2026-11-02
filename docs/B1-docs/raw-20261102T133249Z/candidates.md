---
candidate_id: C-20261102T133249Z-A
status: promoted
source_raw: raw-20261102T133249Z
created_at: 2026-11-02
milestone: M-20261102T133249Z-A
---

# Candidates

## C-20261102T133249Z-A: 认领判定下沉到 owner_lane，bash 只负责调用与记录

- candidate_format_version: v2
- title: 去掉 bash 守卫，让 project == path 成为可单测的普通输入
- status: promoted
- decision_reason: 守卫 `"$_current_path" != "$project"` 在 daemon 于工位内启动时恒为假，claim 从未执行；失败表现与修复前一致，导致误判为“已修复”。规则写在 bash 里既不可单测，又与 claim 内部守卫重复。
- next_action: B2 物化 `I-20261102T133249Z-A`；先补 `project == path` 的两条 RED（有 raw key 应认领 / develop 分支不认领），再改 bash。
- revisit_trigger: 若出现“项目根被认领为 manager”的日志，恢复更严格的路径判定并补用例。
- acceptance_criteria:
  - `claim(project=path)` 且分支含 raw key → created=true
  - `claim(project=path)` 且分支为 develop → `raw_key_unresolved`，不写库
  - 已绑定工位重复调用不写库
  - bash 侧不再存在“路径不等”判定；失败时日志包含 reason
  - 新建工位直接 `daemon start` 能够成功并留下 `owner-lane claim` 日志
- promotion_gate: RED→GREEN + 既有 owner-lane / replica 测试全绿 + `governance-merge-gate` 通过
- open_questions:
  - 认领成功后是否要立即写一条 runtime event（当前只写日志）
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 读 `runtime/freely:341-375`（守卫 + claim 调用）、`owner_lane.py::claim`（四条守卫）、两个工位的实测日志（13:13/13:14 两次失败）
  - verdict: pass
- promoted_issue_id: I-20261102T133249Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/owner-lane-claim/raw-20261102T133249Z/issues/I-20261102T133249Z-A.md
- milestone: M-20261102T133249Z-A
- session_refs: []
