---

schema_version: '1'
local_id: raw-20261103T055554Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T055554Z-A
platform_ids:
  github:
    issue_id: '4131'
    url: https://github.com/chatterzhao/freely/issues/4131
    synced_at: ''
  gitee:
    issue_id: IKSK7I
    url: https://gitee.com/zhaoquan/freely/issues/IKSK7I
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T05:55:54Z'
updated_at: '2026-11-03T05:55:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---
# fix: raw replica 搜索需按 [RAW-key] 标题前缀精确匹配


workflow_kind: fix

## 现象
platform-adapter.py 的 search_raw_issue 在 title 与 body 两处做子串搜索（raw-{key} in:title / in:body），只要其它 issue 的正文/证据路径提到同一 raw key，就返回多个匹配。discover_raw_replicas 将多匹配视为 ambiguous 并 block，raw-reconciliation-gate 永远无法通过，PR 流程被硬阻断。

## 根因
raw issue 的平台身份是 [RAW-{key}] title 前缀；body 中的引用（例如其它 issue 证据路径 fix-raw-{key}/...）不是身份声明。当前搜索把 body 子串也当身份来源，导致身份解析不唯一。

## 修复方向
1. search_raw_issue 优先按标题前缀 [RAW-{key}] 精确匹配；仅当标题无命中时回退 body 匹配。
2. 多个精确标题匹配仍视为 ambiguous（fail-closed）。
3. 补单测：标题命中优先、body 交叉引用不产生额外匹配、重复标题匹配仍 ambiguous。

## 影响
当前被阻断的工位：fix/raw-20260807T114900Z-scan-platform-adapter-import（scan import 修复）因另一个 issue 的证据路径引用该 key 而 ambiguous。
