# Brainstorm: feature-owned-test-pre-merge-family-promotion-model-governance

## Decision

先冻结一个 promote model owner，而不是立刻改 gate 实现或再拆多个 implementation owner。

这条 owner 的目标不是实现某个 hook，而是把下面几件事说清：

1. `feature/*`、`test-pre-merge-*`、`develop` 分别是什么。
2. single-feature lane 与 explicit multi-bundle lane 分别承担什么职责。
3. 哪些语义属于后续必须 machine-enforced，但当前先不承诺具体实现。

## Why This

1. 旧模型把 `test-pre-merge-*` 写成 shadow batch / replay 证据面，已经不能支撑“develop 只接收经过 develop-like 预集成测试的树”这个目标。
2. 现在直接改 `pr-merge-guarded` / hook / `governance-check`，会把未冻结的 promote model 反向固化到实现里。
3. 现在直接拆多个 owner，也会让 gate enforcement issue 和 lifecycle automation issue各自带着不同的前提开工。

## Current Model Tension

当前真正未冻结的不是命名本身，而是 promote unit：

1. `feature/*` 是否仍然是 develop 的默认 promote 单位。
2. `test-pre-merge-*` 是否只是验证环境，还是会在某些情形下成为最终 promote 单位。
3. explicit multi-bundle 究竟是：
   - 额外验证证据；还是
   - bundle promote 单位。

这三点不先收口，执行层就无法写出稳定 gate。

## Frozen Boundaries For This Owner

本 owner 先冻结这些边界：

1. canonical 前缀只保留 `test-pre-merge-*`。
2. multi 只能作为 `test-pre-merge-*` family 的 subtype 表达，不再新造第二前缀。
3. single-feature lane 是 develop-bound feature 的默认讨论入口。
4. explicit multi-bundle lane 只能作为显式声明的组合验证/组合提升模型讨论，不得默认替代 single-feature lane。
5. source features、feature shas、merge order、base develop sha、stale/rebuild trigger 是 multi-bundle 最小可追溯概念。

## Forward Split

等这条 owner 冻结后，后续再拆：

1. `enforce test-pre-merge family promotion gate`
2. `automate test-pre-merge family lifecycle`

在这之前，任何“顺手改一下 hook / pr-merge-guarded / wrapper”都不算合规完成路径。
