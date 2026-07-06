# PRD: worker-reactivation-and-local-reentry-residual-runtime-governance

## Goal

让 worker reactivation 与 local continuation reentry 的 worker-side boundary 再次变得可信：runtime 不再对缺失 AI child 的 attach reuse 写出假成功 truth，active-worker local reentry 也有明确、可验证的 canonical predicate。

## Why Now

- 当前安全/materialization lane 已经只剩这两条红测。
- 这两条都不是 Freely 默认自治产品姿势问题，而是 worker runtime residual。
- 若不单独收口，completed workspace-routing owners 的完成性表述会继续漂移。
- 本条现已完成 focused 收口，后续只保留必要的 side repro 跟进。

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- existing issue/progress/verification docs under `workspace-routing-foundation`

## Non-Negotiables

- 保持 Freely 默认高自治姿势，不把问题降级成交互人工批准。
- worker residual 必须由 runtime truth 和 focused tests 收口，而不是让 security lane 吞掉。
- attach reuse 的 truth 不能再依赖 optimistic write-only semantics。
- local continuation reentry 的 predicate 必须 machine-readable、可复现、可解释。

## Decomposition

1. attach-reuse residual
   - freeze exact failure path
   - decide allow-reuse vs repair boundary after `operator_stop`
2. local reentry residual
   - freeze canonical active-worker predicate
   - align test fixture and runtime behavior
3. documentation truth
   - narrow or supersede old completion claims
4. verification
   - focused regressions for both paths

## Outcome

1. attach reuse 已收敛为 confirmed-running AI truth required。
2. local continuation reentry 已收敛为 worker-owned active runtime truth required。
3. owner closure 不再依赖 security lane，也不再要求 generic runtime redesign。
