---
b1_id: B1-20260701T024449Z
phase_state: completed
source_raw: raw-20260701T024449Z
source_url: https://github.com/chatterzhao/freely/issues/3676
produced_candidate: C-20260701T024449Z-A
created_at: 2026-07-01
---

# B1_IBM: pr-review-guarded _review_guide unbound variable crash

## Input
- **Raw issue**: raw-20260701T024449Z
- **Platform**: GitHub #3676 / Gitee IJY01L
- **Source**: daemon 启动后观察 pr-review-guarded 执行时发现

## Problem

`bin/pr-review-guarded` L506 引用未定义变量 `$_review_guide`，配合 `set -euo pipefail`（L2），当 ACP bridge 不可用、回退到 `manual_required` 路径时，脚本直接 crash：

```
line 506: _review_guide: unbound variable
```

## Root Cause Analysis

`_review_guide` 在整个脚本中仅被引用一次（L506 echo），但从未被赋值。这是遗漏：原本意图是通过变量输出审查指南内容，但忘记定义。

`review_file` 等其他变量均已正确定义（L164）。只有 `_review_guide` 缺失。

影响范围：
- ACP 可用时无影响（走正常流程，不进入 manual_required 分支）
- ACP 不可用时（daemon 未启动），人工审查路径完全不可用——脚本在打印指南前崩溃

## Brainstorm

### Option A: 在脚本前部定义 `_review_guide` 变量
```bash
_review_guide="skill:freely-tdd-review"
```
避免 crash，但增加一个只用一次的变量。
- 风险：低

### Option B: 将 echo 行替换为字符串字面量
```bash
echo "  审查指南: skill:freely-tdd-review"
```
- 最简方案，零维护负担

### Option C: 删除该 echo 行
- 减少信息输出，不推荐

## Decision: Option B — 字符串字面量

理由：
1. 最简修复，一行改动
2. 不需要额外变量定义
3. 信息完整保留
4. 与其他 echo 行风格一致

## Candidate

- candidate_id: C-20260701T024449Z-A
- status: promoted
- milestone: M-20260701T024449Z-A
- promoted_issue_id: I-20260701T024449Z-A
- decision_reason: 将 `$_review_guide` 替换为字符串字面量 `skill:freely-tdd-review`，消除未定义变量
- next_action: B2 → dev 应用修复 → test → PR
