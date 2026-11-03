---
b1_id: B1-20261103T124003Z
phase_state: completed
source_raw: raw-20261103T124003Z
produced_candidate: C-20261103T124003Z-A
created_at: 2026-11-03
---

# B1_IBM: GitHub open 列表在 GraphQL 504 时返回空

## Input
- parity 测试在 develop 上误报 FAIL：GitHub 侧 open 为空，实际 REST 有 13 个 open；同一时刻 `gh issue list --json number,title` 报 HTTP 504 GraphQL。
- 影响：parity 误判双平台不一致；scan 在 504 窗口会漏掉全部 GitHub open issue。

## Option A: 测试加重试（否决）
- 只治测试，scan/生产路径仍会拿到空列表。

## Option B: handler 层重试 + REST 回退（选定）
- `list_open_issue_records`：GraphQL 失败重试 1 次 → 回退 `gh api --paginate --slurp repos/{repo}/issues?state=open`（REST）。
- `list_open_issues` 改为从 records 派生，自动继承回退。
- 返回结构不变，调用方零改动。

## Option C: 完全改用 REST（否决）
- 改动面大，且 GraphQL 正常时更快；保留 GraphQL 优先更稳。

## Decision: Option B
- 边界：不改 scan/parity 语义，不改返回结构；REST 分页过滤 PR。

## Candidate
- candidate_id: C-20261103T124003Z-A；milestone: M-20261103T124003Z-A
