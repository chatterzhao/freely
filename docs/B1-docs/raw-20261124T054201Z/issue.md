---
schema_version: '1'
local_id: raw-20261124T054201Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261124T054201Z-A
platform_ids:
  github:
    issue_id: '4670'
    url: https://github.com/chatterzhao/freely/issues/4670
    synced_at: ''
  gitee:
    issue_id: IKXKY9
    url: https://gitee.com/zhaoquan/freely/issues/IKXKY9
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261124T054201Z/issues/I-20261124T054201Z-A.md
last_synced_comment_at:
  github: '2026-11-24T09:19:22Z'
  gitee: '2026-11-24T09:19:22Z'
hash: ''
created_at: '2026-11-24T05:42:01Z'
updated_at: '2026-11-24T09:19:27Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261124T054201Z-A
source_candidate: ''
completed_at: '2026-11-24T09:19:21Z'
closeout_note: ''
severity: P1
---

# fix: test-all 丢弃测试输出，CI 失败无断言诊断

workflow_kind: fix

## fix: test-all 丢弃测试输出，CI 失败无断言诊断

| Field | Value |
|-------|-------|
| local_id | `raw-20261124T054201Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-24T05:42:01Z |
| updated | 2026-11-24T05:42:01Z |

---

> **Freely 治理**：这是 raw issue `raw-20261124T054201Z`。实现前请用 `wt-create --raw-key 20261124T054201Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

`bin/test-all:147/149` 执行测试时 `python3 "$path" >/dev/null 2>&1 || rc=$?` / `bash "$path" >/dev/null 2>&1 || rc=$?`，stdout 与 stderr 全部丢弃。CI 只能打印 `[FAIL] name (rc=1)` 与 `SUMMARY: 41 ok, 2 failed`，看不到断言细节。

实证：CI run 43827151395 的 verify job（PR #4668 merge ref `1df6a39`）两个失败测试只留 `[FAIL]` 行；同一 tree sha `f5fd10c1…` 在本地 develop HEAD 跑 `bin/test-all --ci` = 43 ok / 0 failed，根因无法从 CI 输出判断。

## 影响

Freely 的目标是让 AI 自主发现→修复→验证。CI 不提供失败诊断，AI 只能盲改或人工重跑，直接损害自举闭环。

## 修复方向

- 每个测试独立保存 stdout/stderr 到日志；成功只输出摘要，失败打印完整日志或 stderr 尾部。
- CI 上传失败日志为 artifact；记录每测试退出码与耗时。
- 默认零输出需求用 flag 控制，不改变现有 SUMMARY 行格式（下游门禁依赖）。

## 验收

- RED：构造必然失败的测试，CI 输出含其断言信息而非只有 `[FAIL]`。
- GREEN：43 ok 时 SUMMARY 格式不变。

### comment-20261124T091922Z
- source: system
- event: promote_finalized
- children: ["I-20261124T054201Z-A"]

拆解为以下任务:
1. [I-20261124T054201Z-A](will-be-updated)
