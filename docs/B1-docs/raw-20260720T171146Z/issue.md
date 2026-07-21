---
local_id: raw-20260720T171146Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260720T120329Z-C
parent_story: M-20260720T120329Z-A / I-20260720T120329Z-A,B,C
  github:
    issue_id: '4068'
    url: https://github.com/chatterzhao/freely/issues/4068
    synced_at: ''
  gitee:
    issue_id: IK2FO8
    url: https://gitee.com/zhaoquan/freely/issues/IK2FO8
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T17:12:09Z'
updated_at: '2026-07-20T17:12:09Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
raw-20260720T120329Z 只迁移了部分 runtime 路径，未统一 raw_key 契约；原子分配 API 未贯通真实 launch 调用链，测试又只直调 daemon handler 且回归门禁漏扫 bin，导致假绿。

## 影响
生产 review、scan、close、handoff 可能查询不同 agent_working 行；DB 不可用时静默错绑 manager_01/worker_01；并发或重复分配可能覆盖既有 worker；agent-id.env 已停写但仍被读取。

## 修复方案
移除全部生产 agent-id.env 读写；建立统一 raw_key 规范化边界；真实 launch 必须使用 next_free_and_assign 并按返回 agent 选择 slot；DB/RPC 失败 fail-closed；同 raw 重复分配幂等；修复 reviewer 占用解析与 RPC 错误传播。

## 治理归属

这是 `raw-20260720T120329Z` 的 continuation，不创建新的 candidate、milestone 或 `I-*` issue。残差按职责吸收到父 story：真实分配链和幂等归 `I-20260720T120329Z-A`，生产路径与 raw_key 契约归 `I-20260720T120329Z-B`，真实 socket 验收、bin 门禁和 fail-closed 归 `I-20260720T120329Z-C`。父 milestone 在残差验证完成前保持 `active`。

## 验收
RED 测试先行；覆盖 bin 与 runtime 的零引用门禁、真实 socket 客户端三角色闭环、并发分配、同 raw 幂等、raw key 跨 assign/scan/review/close 一致、close 后 review 持久化、DB 不可用 fail-closed；在 test-pre-merge 工位全绿并独立评审。
