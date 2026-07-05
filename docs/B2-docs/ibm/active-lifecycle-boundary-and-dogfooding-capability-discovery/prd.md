# PRD: active-lifecycle-boundary-and-dogfooding-capability-discovery

## Goal

让 Freely 在方法论真源中明确区分：

- 哪些产物已进入历史追溯面
- 哪些产物仍在当前活跃生命周期，可继续做应用产物收敛重构
- Freely 狗粮中暴露的共性问题何时应进入能力发现流程

## Product Outcomes

1. 生命周期边界稳定：
- AI 不再仅根据文件时间误判“不能再改”
- AI 也不会继续把新讨论回写到已闭环的历史 issue

2. 狗粮发现被产品化：
- Freely 开发 Freely 时暴露的可复现共性问题，优先进入能力发现判断
- 若可复用，进入三层循环的正式生命周期，而不是只停留在聊天记录

## Scope

### In

- `three-loop-capability-lifecycle.md` 的生命周期边界 wording
- `PROJECT_INTENT.md` 的狗粮能力发现原则
- 当前 issue 生命周期内的 IBM / verification / milestone 对齐

### Out

- runtime 脚本化 drift detector
- 自动 capability classifier
- 历史已完成 issue 的回写修订

## Acceptance Slice

### Slice A: active/historical boundary

- 明确 `historical = completed + worktree closure`
- 明确 `active lifecycle` 可继续重构当前应用产物

### Slice B: dogfooding capability discovery

- 高层原则明确：
  - 可泛化的狗粮问题默认先判断为 Freely 能力缺口

### Slice C: consistency

- wording 与既有三层 loop / manager / worktree 治理不冲突
