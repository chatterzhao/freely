---
name: A2A No-Fallback Implementation Decision Note
owner_issue: I-20260615T001626Z-A
owner_issue_path: docs/issues/I-20260615T001626Z-A/issue.md
implementation_decision_note: true
phase_state: completed
review_id: a2a-no-fallback-review
decision: Execute Phase 1+2 — fix signal file WORKERS field + unify all prompts to a2a-exit instruction
why_this: |
  Dual-path architecture (a2a-exit + text JSON parsing) creates confusion and
  maintenance burden. The A2A protocol is now the standard; text fallback is
  redundant legacy. Phase 1+2 fixes the most urgent signal file bug and removes
  the root cause (JSON block instructions in prompts).
alternatives_considered:
  - "Phase 1-6 all at once: larger scope, harder rollback, higher risk"
  - "Phase 1 only without Phase 2: doesn't fix root cause (prompt inconsistency)"
  - "No change: accumulates tech debt from dual-path maintenance"
boundary_non_goals:
  - "Does not change A2A Task state machine behavior"
  - "Does not modify Manager-Worker responsibility boundaries"
  - "Does not delete parse_a2a_task_json_reply (Phase 3-6)"
  - "Does not remove persistence files (Phase 3-6)"
residual_risk: |
  FREELY_A2A_TEXT_PARSING_FALLBACK=1 env var provides break-glass rollback.
  If a2a_task.py has bugs, fallback path can be re-enabled during transition.
  Phase 3-6 follow-up worktrees will complete the cleanup.
---

# Implementation Decision Note: 移除 A2A 文本 JSON 解析 Fallback (Phase 1+2)

## Decision

**执行 Phase 1+2：修复信号文件 WORKERS 字段 + 统一所有 Prompt 为 a2a-exit 指令**

## Why This

### 根因分析

父 Epic `a2a-replace-handoff` 已完成 A2A 协议替换 Handoff 的核心实现，但代码中仍存在双路径：

```
a2a-exit (标准路径)      ────→   A2A Task State Machine
                               ↗
文本JSON解析 (fallback)  ────→   旧 handoff exit_kind 映射
```

### 为什么要先做 Phase 1+2（不做 Phase 3-6）

1. **信号文件修复是最急迫的**：WORKERS 字段缺失导致下游功能异常，是最直接影响
2. **Prompt 统一消除 root cause**：AI 输出旧格式的根本原因是 prompt 中仍有 JSON block 指令
3. **可独立验证**：Phase 1+2 的改动可以通过 grep 和 env 变量独立验证
4. **渐进式迁移**：Phase 3-6 涉及代码删除，适合在验证稳定后再进行

### 为什么不是其他方案

- **全部 Phase 1-6 一次性完成**：改动范围大，回退复杂，风险较高
- **只做 Phase 1 不做 Phase 2**：不解决 root cause（prompt 指令仍不一致）
- **不做任何修改**：双路径持续累积技术债务

## Alternatives Considered

### 方案 A: Phase 1+2 优先 (选中)

- 优点: 解决最急迫的问题，改动范围可控，独立可回退
- 缺点: 遗留代码（Phase 3-6）仍然存在

### 方案 B: 全部 6 Phase 一次性完成

- 优点: 彻底清除所有 fallback 代码
- 缺点: 一次性改动范围大，回退困难

### 方案 C: 保持现状

- 优点: 零改动风险
- 缺点: 持续维护双路径

## Boundary & Non-Goals

### In Scope (Phase 1+2)
- `a2a_task.py` WORKERS 字段写入修复
- manager-agent.md prompt 更新
- worker-agent.md prompt 更新
- 系统 prompt 更新
- WORKER_STATE_INJECT 更新
- repair prompt 更新
- delta prompt 更新

### Out of Scope (Phase 3-6)
- 删除 `parse_a2a_task_json_reply` 的 tail+regex 路径
- 删除 `last-workers-csv.txt`/`last-exit-kind.txt` 持久化
- 废弃 `a2a_task_parser.py`
- Worker handoff 改用 DB 查询

### Non-Goals
- 不改变 A2A Task 状态机的行为
- 不修改 Manager-Worker 职责边界
- 不改变现有 worktree 模型

## Residual Risk

| 风险 | 缓解措施 | 残余风险 |
|------|----------|----------|
| Prompt 变更影响 AI 输出 | FREELY_A2A_TEXT_PARSING_FALLBACK=1 可恢复 | 低 |
| 遗漏某些 prompt 文件 | 全仓 grep 审计 T10 | 低 |
| WORKERS 格式不兼容 | 保持与下游期望一致的 JSON 格式 | 低 |
| AI 临时输出旧格式 | fallback env 可在过渡期开启 | 中 |

## Implementation Notes

### 渐进式迁移

1. Phase 1: 先修信号文件（改动小，影响大）
2. Phase 2: 再改 prompt（需谨慎，影响 AI 行为）
3. 验证: 全仓 grep + fallback 恢复测试
4. 后续: Phase 3-6 在独立 feature 中完成

### 关键决策点

- `FREELY_A2A_TEXT_PARSING_FALLBACK` 环境变量作为 break-glass
- 全仓 grep 是验证 prompt 完整性的必要手段
- Phase 1+2 与 Phase 3-6 解耦，互不阻塞

## Status

- **Date**: 2026-06-15
- **Status**: Proposed
- **Reviewers**: 待定
