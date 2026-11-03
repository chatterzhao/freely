---
schema_version: '1'
local_id: raw-20261102T103231Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261102T103231Z-A
platform_ids:
  github:
    issue_id: '4120'
    url: https://github.com/chatterzhao/freely/issues/4120
    synced_at: ''
  gitee:
    issue_id: IKSE3M
    url: https://gitee.com/zhaoquan/freely/issues/IKSE3M
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-02T10:32:32Z'
updated_at: '2026-11-02T13:02:45Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-02T12:41:08Z'
closeout_note: ''
---

# [RAW-20261102T103231Z] fix: owner-lane 工位 daemon 启动要求 agent_working 绑定

workflow_kind: fix

## 现象
在 wt-create 出来的 test-pre-merge 工位执行 freely daemon start --task-mode wait，A2A server 启动即退出，daemon 报 unable to resolve agent identity — agent_working has no entry，fail-closed。

## 根因
daemon 启动要求 agent_working 已有 manager/worker 行；owner 直接创建、未经 Manager 委派的工位没有该行，形成鸡生蛋。同一原因让 test-gate.env 无法由 daemon 自动写。

## 影响
owner lane 无法跑 daemon 与自动测试证据；只能人工写 test-gate.env，evidence 链不完整。pr-review 也因此需要 owner-lane 回退才能收口。

## 修复方案
wt-create 时 seed 一条 manager 绑定；或 daemon 在 agent_working 为空时从 agent-table 解析 manager 身份并落库，仅对 manager 角色放行，其他角色仍 fail-closed。

## 验收
1. 新建 test-pre-merge 工位可直接 daemon start。
2. daemon stop 能自动写 test-gate.env（completed + HEAD）。
3. 未知角色仍 fail-closed。
