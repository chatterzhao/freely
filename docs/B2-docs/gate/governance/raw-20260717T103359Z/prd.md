# PRD: 工位所有权三道硬防线
- issue_id: I-20260717T103359Z-A
## Goal
零交付删工位与异主删工位默认被拦;develop 运行中污染可观测;fallback worker 带边界铁律。
## 实现方案
b-I 三点。顺序:guard → export+prepend → dirty 检测。
## Dev-Loop Handoff
RED 4 → 实现 → GREEN。
