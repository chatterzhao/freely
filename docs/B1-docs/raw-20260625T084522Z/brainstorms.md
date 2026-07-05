---
b1_id: B1-20260625T084522Z
phase_state: completed
source_raw: raw-20260625T084522Z
source_url: https://github.com/chatterzhao/freely/issues/3495
produced_candidate: C-20260625T084522Z-A
created_at: 2026-06-25
---

# B1_IBM: test-execution skill 反 ghost pass

## Input
- source: raw-20260625T084522Z (GitHub #3495)

## Problem
- AI 可能写 test_command="echo pass" 等占位符，test-execution 照跑不误

## Decision: 在 test-execution SKILL.md 增加步骤 4（可执行性检查）
- 执行前逐条检查 test_command 真实性、expected_output 可验证性
- 不通过 → 硬拦截，回 B2_IBM
- 与 B2_IBM 反糊弄铁律 + pretests-retirement-gate 形成三道防线

## Candidate
- candidate_id: C-20260625T084522Z-A
- status: promoted
- milestone: M-20260625T084522Z-A
