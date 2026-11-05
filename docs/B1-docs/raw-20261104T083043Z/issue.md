---
schema_version: '1'
local_id: raw-20261104T083043Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T083043Z-A
platform_ids:
  github:
    issue_id: '4186'
    url: https://github.com/chatterzhao/freely/issues/4186
    synced_at: ''
  gitee:
    issue_id: IKSWU2
    url: https://gitee.com/zhaoquan/freely/issues/IKSWU2
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-04T08:30:43Z'
updated_at: '2026-11-04T08:43:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: '2026-11-05T05:35:00Z'
closeout_note: ''
---

# fix: wt-create 中断后无法恢复，缺 test-pre-merge 工位时不补建

workflow_kind: fix

## 优先级
P0 — wt-create 是所有 issue 的入口命令；一旦在创建 test 工位前中断，该 issue 无法用官方命令恢复，test 与 PR 全链路阻断。

## 事实边界
- wt-create 本身可以一次走完，不是「跑不完」。
- 本次是调用侧给了 120 秒超时，进程在 Step 2（创建 test 工位）之前被 SIGTERM。
- 因此本 issue 只主张两件事：① 中断后重跑不可恢复；② legacy 帮助声称可补建、实现却不做。
- 不主张「wt-create 性能问题」；若要优化耗时，另开 issue。

## 根因
`wt-create` 的帮助声称 legacy 模式可"已有开发工位但缺 test-pre-merge-<raw-key>-<slug> 时补建测试工位"，但实现中 legacy 分支把 `test_pre_merge_branch` 置空，只创建 dev 工位，不会创建 test 工位。

## 证据
- 帮助文本：`docs/system/workspace/scripts/worktree/wt-create` 第 874 行。
- 实现：第 254-260 行，`if [[ "$using_new" -eq 1 ]]; then test_pre_merge_branch="test-pre-merge-${raw_key}-${slug}" ... else test_pre_merge_branch="" ...`。
- 实测：`freely wt-create "test-pre-merge-20261104T074512Z-package-output-guard" --base develop` 直接打印 usage，不创建任何工位。
- 关联：标准模式首次执行被超时中断后，dev worktree 与分支已存在，重跑输出 `Branch already exists` 并退出，不会补建 test 工位；结果 PR 门禁报 `pretests_not_tested` 且无工位可测。

## 影响
- 一旦 wt-create 在创建 test 工位前中断（超时、网络、手动取消），该 issue 无法通过官方命令补齐测试工位。
- 只能手工 `git worktree add`，违反"所有工位由 wt-create 创建"的约束。
- 帮助与实现不一致，按帮助执行必然失败。

## 修复方案
1. legacy 模式识别 `test-pre-merge-*` 分支名时，解析 raw key 与 slug，补建 test 工位（base 为对应 dev 分支）。
2. 标准模式增加幂等：dev 工位/分支已存在但 test 工位缺失时，只补建 test 工位并继续，而不是直接退出。
3. 帮助文本与实现保持一致，并补一条测试覆盖"dev 已存在、test 缺失"的场景。

## 验收标准
- RED：dev 工位存在、test 工位缺失时执行标准 wt-create，断言 test 工位被创建；当前直接退出。
- GREEN：legacy `wt-create test-pre-merge-<key>-<slug>` 创建对应 test 工位。
- GREEN：重复执行不产生重复工位，退出码 0 并输出已存在状态。
