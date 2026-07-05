---
local_id: raw-20260621T090002Z02Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T090002Z-A
platform_ids:
  github:
    issue_id: '3210'
    url: https://github.com/chatterzhao/freely/issues/3210
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T09:00:22Z'
updated_at: '2026-06-21T09:26:10Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`freely` L10642-10655 的 worker launch verification gate 对所有 worker 无差别检查 12 个 verification metadata 字段。但 `a2a-exit --state submitted --role worker` 创建的常规 worker prompt 只包含 `write_scope` 和 `intent_kind` 两个元数据头——这触发了 `has_any_verification_metadata=true`，但其余 10 个字段（owner_issue、pre_tests_path、verification_artifact_dir、required_test_lanes 等）全部缺失。

结果：所有 a2a-exit 委派的 worker 全部被 verification_blocked 拦截，无一启动。A2A task 累积在 submitted 状态，跨 session 变成僵尸。

## 根因

verification gate 是为 test-pre-merge family 设计的（提示工程阶段注入完整 12 字段）。但 gate 没有区分 worktree 类型——它对 fix/raw-* 工位的常规 worker 也执行相同的检查。

当前逻辑（L10642-10655）:
```bash
missing_fields_csv="$(worker_prompt_verification_metadata_missing_fields_csv "$prompt_file")"
if worker_prompt_has_any_verification_metadata "$prompt_file"; then
  has_any_verification_metadata="1"
fi
if [[ -n "$missing_fields_csv" && "$has_any_verification_metadata" == "1" ]]; then
  # BLOCK - return 1
fi
```

问题：`has_any_verification_metadata` 为 true（因为 prompt 里有 write_scope/intent_kind），但 12 字段不齐 → gate 拦截。

## 修复方案

**范围化 gate**：只在 test-pre-merge 工位（`test-pre-merge-*` 分支）上执行完整 12 字段检查。常规 fix/feature 工位的 worker 跳过此 gate。

具体：在 L10642 前加分支类型判断：
```bash
# verification gate 仅适用于 test-pre-merge 工位
if [[ "$branch" != test-pre-merge-* ]]; then
  # 常规 worker: 跳过 verification metadata 检查
  :
else
  # test-pre-merge worker: 执行完整 12 字段检查
  ...existing gate logic...
fi
```

## 影响范围

- 修复后：a2a-exit 委派的常规 worker 能正常启动（恢复 Manager 的委派能力）
- test-pre-merge worker：不受影响（继续执行完整 verification contract）
- 不引入新 bug：改动是纯减法（缩小 gate 适用范围），不修改 gate 内部逻辑
