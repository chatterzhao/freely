---
local_id: raw-20260719T045949Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T045949Z-A
platform_ids:
  github:
    issue_id: '3997'
    url: https://github.com/chatterzhao/freely/issues/3997
    synced_at: ''
  gitee:
    issue_id: IK20PG
    url: https://gitee.com/zhaoquan/freely/issues/IK20PG
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T05:00:16Z'
updated_at: '2026-07-19T05:00:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
freely-doc-B1_IBM-execution 和 freely-doc-B2_IBM-execution 两个核心 skill 缺少对三环能力生命周期总图的交叉引用，也没有说明自身在 doc-loop 中的位置。

## 改动
1. B1 skill 末尾新增能力生命周期参考：B1 是 doc-loop 第一阶段，raw→brainstorm→candidate→milestone→promote→B2
2. B2 skill 末尾新增关键参考：聚合 PRD 质量门槛、设计派生约束、三环生命周期引用，B2→dev 交付关系

## 影响
纯文档改进，不涉及代码逻辑。评审确认方向正确、质量达标。
