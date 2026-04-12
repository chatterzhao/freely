# PRD: launch-time-verification-contract-hard-gate-governance

## Goal

把 verification contract 的第一道硬门禁前移到 manager dispatch / runtime launch 边界，避免 worker 在缺少最小 verification metadata 时继续启动。

## Why Now

当前上层真源已经要求 worker handoff 带完整 verification metadata，但 runtime 仍允许缺字段 prompt 继续 launch。结果是：

- 缺口被记录，却不在 launch 时阻断
- 问题经常拖到 completion / merge gate 才暴露
- 审计容易把执行层缺口误判成提示层没写清楚

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`

## Non-Goals

- 不在本 owner 中扩 adequacy item schema v2
- 不在本 owner 中实现 cleanup / retirement pre-tests enforcement
- 不新增 `tests.md` 或任何第二测试真源
- 不把 merge / completion gate 重写成 launch gate

## Non-Negotiables

- `pre-tests.md` 继续是唯一 canonical success-standard / test-task 真源
- 缺少必填 verification metadata 时，worker launch 必须被拒绝
- 拒绝结果必须 machine-readable，并明确列出 missing fields
- 完整 metadata 路径不能回退
- branch-only / 自然语言 prompt 的兼容策略必须显式决定，不能继续依赖隐式宽松

## Prototype Path

最小原型是：

1. manager continuity 产出 worker prompt
2. runtime 在 launch 前解析 verification metadata
3. 若缺 `Owner-Issue` / `Pre-Tests-Path` / `Verification-Artifact-Dir` / `Required-Test-Lanes` / `Required-Acceptance-Item-Ids` / `Minimum-Evidence-Level` / `Target-Environment` / `Closeout-Gate`
4. launch 被拒绝，并落一份 machine-readable blocked state
5. 完整 metadata prompt 仍可正常 launch

## Eval Plan

成功：

- 缺字段 prompt 不再启动 worker supervisor
- state / intake 仍能保留缺口诊断，便于恢复
- 现有完整 metadata 测试继续通过

失败：

- runtime 仍允许 partial prompt launch
- 诊断只剩模糊文本，没有 missing field 列表
- 成功路径被误伤，导致已有完整 handoff 回退

## Dev-Loop Handoff

本 owner 先做 launch hard gate。adequacy schema、retirement gate、stale pre-brainstorm reconcile 作为独立 follow-on 保持拆分。
