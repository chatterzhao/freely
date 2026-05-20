# Brainstorms: Promoted candidate M gate bypass

## Discovery

### 来源
- Raw issue: `raw-20260507T0200Z`
- GitHub issue #282 — zhaoquan
- created_at: 2026-05-07 02:00 UTC
- platform_state: open

### 问题陈述
Promoted candidate 的 M（Milestone）门禁检查存在绕过漏洞。当 candidate 已被标记为 promoted 时，对应的 M gate 检查未正确执行，导致未满足里程碑条件的 candidate 能够通过门禁。

### 当前状态
Raw issue 已确认，问题边界明确但未进入正式预研。需要分析 bypass 的具体路径和影响范围。

### 价值与时效性判断
- M gate 是 milestone 治理的核心门禁，bypass 会导致里程碑状态不一致
- 影响 release 质量保证体系
- 需要优先修复以防止进一步的状态污染

**结论**: 价值确认，进入 B1 预研流程。

## Status

discovery (needs B1 research)

## Next Action

complete B1 pre-brainstorm — 分析 M gate bypass 的具体路径、触发条件和修复方案。
