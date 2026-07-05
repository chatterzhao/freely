# Brainstorm: frontend-runtime-baseline-for-probe

## Focus

把 `Frontend Probe v0` 的宿主缺口收敛成可独立实现的 frontend runtime baseline。

## Key Questions

1. 最小宿主入口应该在哪里？
2. React renderer 与 root mounting 应如何对接？
3. Tauri runtime 注入与 host wiring 的最小要求是什么？
4. 最小 build/test baseline 应该有哪些文件或命令？

## Working direction

- 先冻结宿主与 runtime 基线，再继续 Probe v0 的真实接线。
- 不把 build/runtime baseline 混回 Probe 交互 issue。
