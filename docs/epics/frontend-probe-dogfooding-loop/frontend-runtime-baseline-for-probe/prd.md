# PRD: frontend-runtime-baseline-for-probe

## Goal

建立 Frontend Probe 可运行所需的最小 frontend build/runtime baseline。

## Requirements

1. 定义宿主入口与 React renderer 挂载路径。
2. 定义 Tauri runtime 注入的最小约束。
3. 定义最小 build/test baseline。
4. 明确与 `Frontend Probe v0` 的依赖关系。

## Product rules

1. baseline 是独立基础设施，不继续伪装成 Probe v0 的 UI 细节。
2. 宿主入口、renderer、runtime wiring 必须可追溯。
3. 没有 baseline 时，Probe v0 不得被误判为可继续顺滑实现。

## Exit criteria for `done_ibm`

1. host entry、renderer、runtime wiring、build/test baseline 的最小边界已冻结。
2. `Frontend Probe v0` 如何依赖该 baseline 已明确。
3. 后续实现阶段不需要再回退讨论“baseline 是不是独立问题”。
