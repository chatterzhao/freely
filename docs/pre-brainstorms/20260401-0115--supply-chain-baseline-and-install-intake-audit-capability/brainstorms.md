# Brainstorms - 20260401-0115--supply-chain-baseline-and-install-intake-audit-capability

## Context

前面的 product security baseline 已经收窄并拆成了几条已完成 owner：

- product-level autonomy / activation consent
- tool policy materialization
- execution-boundary review support
- build artifact exposure and release allowlist

但原始 security baseline 里仍然有一块真实且未过时的能力没有被 materialize：

- lockfile / install intake baseline
- install hook 风险
- mutable GitHub Action ref
- 非 registry 依赖来源

这块问题和 artifact exposure 一样，不该继续依赖人工记忆或临时对话提醒。

## Problem

当前仓库没有一个 canonical 的 supply-chain baseline audit 去回答：

1. `package.json` 存在时是否要求 lockfile
2. install-time lifecycle scripts 是否要被显式拒绝
3. 依赖来源是否允许 `git+` / `github:` / `http(s):` / `file:` / `link:`
4. GitHub Actions 是否允许 mutable tag

如果这些检查继续只靠人脑 review，就会重复“知道该查，但 merge 时忘了查”的问题。

## Narrow First Slice

第一刀保持窄边界：

1. root package manager lockfile presence
2. package manifest direct dependency specifier baseline
3. top-level install lifecycle script baseline
4. GitHub Actions external `uses:` ref must pin to immutable SHA
5. `freely doctor` replay of the same audit

## Non-Goals

第一刀不承接：

1. minimum package age
2. provenance / trusted publishing verification
3. transitive dependency CVE intelligence
4. generalized secret scanning
5. runtime state artifact remediation

## Direction

将这条能力冻结为 automation-first audit：

- standalone script in `docs/system/workspace/scripts/quality/`
- stable wrapper in `bin/`
- `freely doctor` runs it as part of baseline checking
- tests prove lockfile, dependency specifier, lifecycle script, and workflow pinning behavior

## Why This Split

这条线刚好承接原安全预研里“automation and enforced workflow replace operator memory”的一个具体剩余面，又不会和已完成的 build-artifact / execution-boundary owners 踩踏。
