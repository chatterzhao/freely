---
b1_id: B1-20260705T010030Z
phase_state: completed
source_raw: raw-20260705T010030Z30Z
source_url: https://github.com/chatterzhao/freely/issues/3734
produced_candidate: C-20260705T010030Z-A
created_at: 2026-07-05
---

# B1_IBM: wt-close --raw-key 唯一入口重构

## Input
- raw-20260705T010030Z30Z (GitHub #3734)

## Problem

wt-close 当前支持 --raw-key 和 --branch 两个入口，还存在 test-pre-merge 分支直接传入的 disposable 路径。用户容易用错——直接传 test 分支名导致报错后用 --force 绕过。

## Brainstorm

### 唯一方案: --raw-key 为唯一必填参数

- 移除 --branch 参数和 BRANCH_INPUT 变量
- 移除 _extract_issue_id 函数（issue_id 始终 = raw-${_raw_key}）
- 移除 test-pre-merge 分支 disposable 路径
- usage 和错误提示全部指向 --raw-key
- --force 也必填 --raw-key

## Decision: 逐项重构

改动集中在 wt-close 单文件：arg 解析、输入判定、usage、错误提示、注释。

## Candidate
- candidate_id: C-20260705T010030Z-A
- status: promoted
- milestone: M-20260705T010030Z-A
