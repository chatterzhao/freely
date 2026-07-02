# Brainstorms: fix-execution SKILL.md branch naming uses feature/ instead of fix/

## Discovery

### 来源
- Raw issue: `raw-20260507T0100Z`
- GitHub issue #278 — zhaoquan
- created_at: 2026-05-07 01:00 UTC
- platform_state: open

### 问题陈述
fix-execution SKILL.md 分支规范表中普通 fix 的分支前缀错误地使用了 `feature/` 而不是 `fix/`。需要将 7 处 `feature/` 统一替换为 `fix/`，并使用 `raw-{raw key}-{slug}` 格式。

### 当前状态
Raw issue 已确认，但未进入 B1 预研阶段。需要正式记录问题边界和影响范围。

### 价值与时效性判断
- fix-execution skill 是日常修复流程的核心，分支命名规范直接影响工位创建的正确性
- 命名错误会导致分支管理治理混乱，影响 pr-merge-guarded 的门禁判断
- 当前项目阶段 fix-execution 已投入使用，此命名问题需要优先解决

**结论**: 价值确认，进入 B1 预研流程。

## Status

discovery (needs B1 research)

## Next Action

complete B1 pre-brainstorm — 分析分支命名规范在各 skill 中的一致性，确认修复范围和副作用。
