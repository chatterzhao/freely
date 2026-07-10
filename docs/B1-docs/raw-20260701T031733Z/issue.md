---
local_id: raw-20260701T031733Z33Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260701T031733Z-A
platform_ids:
  github:
    issue_id: '3680'
    url: https://github.com/chatterzhao/freely/issues/3680
    synced_at: ''
  gitee:
    issue_id: IJY0HM
    url: https://gitee.com/zhaoquan/freely/issues/IJY0HM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T03:17:53Z'
updated_at: '2026-07-01T03:17:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n
## 问题

每次 PR 在门禁阶段反复失败，需多轮修复才能通过。根因是 skill 指导与 gate 实现不同步：

### 反复出现的问题
- absorbed_into missing — 每个 raw issue 都需要
- promoted_issue_path missing — candidate 模板缺字段
- epics-map.svg 不对齐 — B2 skill 从未提及需要更新
- pre-tests.md 格式问题 — skill 示例含反引号但 parser 不支持
- evidence .log 文件被 gitignore — 实践问题未文档化
- dev↔test 不同步 — skill 没有明确提醒 merge 时机

## 修复方案

### 1. pr-create-guarded 增加 pre-flight self-check
在执行 gate 之前，先跑一遍已知的常见检查：
- absorbed_into / promoted_issue_path 字段存在性
- epics-map.svg 对齐
- pre-tests.md acceptance items 格式
- dev↔test 一致性
- evidence 文件是否可 staged
不通过直接给修复建议，不等 gate 报错。

### 2. 更新 skill 模板
- B1 candidates.md 模板加上 promoted_issue_path 示例
- B2 pre-tests.md 模板去掉反引号，加上 .log 证据文件 force-add 提醒
- B2 完成自检清单加上 epics-map.svg 更新
- test-execution 和 dev-loop skill 加上 dev 提交后 merge 到 test 的提醒

### 3. dev↔test 同步提醒
在以下 skill 中增加明确提醒：
- freely-dev-loop-execution: 提交代码后提醒 merge 到 test
- freely-test-execution: 执行测试前先 merge dev 到 test
