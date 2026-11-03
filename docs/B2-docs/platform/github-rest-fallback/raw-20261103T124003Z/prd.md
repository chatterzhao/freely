# PRD: GitHub open 列表 GraphQL 504 → REST 回退

- issue_id: I-20261103T124003Z-A

## Goal
GraphQL 504 时 GitHub open 列表仍可用（REST 回退），parity/scan 不再把空列表误判为"没有 open issue"。

## Modules
- `platform-adapter.py` GitHubHandler：新增 `_open_issue_records_via_rest`；`list_open_issue_records` 重试 + 回退；`list_open_issues` 派生。
- 新增 `test-platform-adapter-github-rest-fallback.py`（mock GraphQL 504 + REST 两页）。

## Invariants
- 返回结构不变：{number: state} / {number: {platform,title,body,state}}。
- REST 分页结果过滤 pull_request。
- GraphQL 正常时仍走 GraphQL（保持现有性能）。

## Non-Goals
- 不改 scan/parity 代码；不引入第三平台。

## Eval Plan
- unit：GraphQL 504 → REST 回退；两页合并；PR 过滤。
- integration：parity 测试连续 3 次通过。

## Dev-Loop Handoff
RED：单测失败（返回 {}）；实现后 GREEN。
