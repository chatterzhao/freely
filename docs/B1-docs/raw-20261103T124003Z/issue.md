---
schema_version: '1'
local_id: raw-20261103T124003Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T124003Z-A
platform_ids:
  github:
    issue_id: '4144'
    url: https://github.com/chatterzhao/freely/issues/4144
    synced_at: ''
  gitee:
    issue_id: IKSPI7
    url: https://gitee.com/zhaoquan/freely/issues/IKSPI7
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T12:40:03Z'
updated_at: '2026-11-03T12:43:37Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-03T12:45:00Z'
closeout_note: ''
---
# fix: platform-adapter GitHub open 列表在 GraphQL 504 时返回空


workflow_kind: fix

## 现象
test-platform-open-parity.py 间歇 FAIL，报 GitHub 侧 open 为空（gitee-only 13 个），但 GitHub REST 实际有 13 个 open。

## 根因
GitHubHandler.list_open_issues / list_open_issue_records 使用 gh issue list --json（GraphQL）。GraphQL 返回 HTTP 504 时 handler 捕获后 return {}，调用方（parity 测试、scan）把空结果当成“真的没有 open issue”。

## 影响
- parity 校验不可靠，误报双平台不一致。
- scan 在 GraphQL 504 期间漏掉全部 GitHub open issue。
- 2026-11-03 已因此产生一次错误 parity FAIL（实际 13=13）。

## 修复方向
1. list_open_issues / list_open_issue_records 增加重试（2 次，短暂退避）。
2. gh issue list 失败时回退 REST：gh api --paginate repos/{owner}/{repo}/issues?state=open&per_page=100。
3. 单测：mock subprocess 使 GraphQL 504、REST 返回 2 条 open，断言汇总正确。
4. 返回结构不变。

## 验收
- 单测 RED→GREEN。
- parity 测试可重复通过（或明确报 transport 错误而非误判不一致）。
- scan platform_health=ok。
