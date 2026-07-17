# PRD: bridge 生命周期三点收口
- issue_id: I-20260717T004654Z-A

## Goal
任何模式下 bridge 进程数有界（每工具 ≤1，无孤儿）；未委派工具不被 eager 启动。

## 实现方案
b-I 三点。顺序：孤儿回收 → 暖机宽限 → lazy 守卫。

## Dev-Loop Handoff
RED 3 项 → 实现 → GREEN（E2E 在 test 工位）。
