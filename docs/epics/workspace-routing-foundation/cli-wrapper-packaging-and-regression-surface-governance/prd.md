# PRD: cli-wrapper-packaging-and-regression-surface-governance

## Problem

Freely 已经是 CLI-first，但当前 CLI 审计证明部分真实入口不稳定：

- 若干 wrapper 不能直接执行
- `freely ai --help` 在最基础的帮助面就会泄漏 shell 错误
- 一个已存在 regression test 在不同 worktree 上结果不稳定

这会削弱所有后续 develop-bound 测试的可信度。

## Product Decision

先收束 CLI 包装层与回归入口，再继续 project-target bootstrap/status 与 runtime control-plane follow-on。

## Requirements

1. 目标 wrapper 必须 direct-exec。
2. 帮助输出必须 deterministic 且无 shell 噪音。
3. 测试 fixture 必须在不同 worktree 上稳定产出同一结果。
4. 修复范围保持最小，不顺手扩大为通用 CLI 重构。
