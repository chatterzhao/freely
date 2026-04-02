# PRD: freely-tool-autonomy-policy-materialization-governance

## Goal

把 Freely 默认高自治 posture 如何被下游工具真正消费，冻结成清晰、分层、可实现的 contract。

## Why Now

如果 Freely 继续同时保留：

- `tools.md` / launcher 的 auto posture
- `.codex/config.toml` 的 guarded posture

那么后续无论实现 `init`、launcher、status 还是 ACP adapter，都还是会建立在 split truth 上。

## Product Surface

- `freely init`
- `docs/system/workspace/tools.md`
- runtime launcher path
- project-local tool bootstrap artifacts such as `.codex/config.toml`
- future adapter follow-up such as ACP

## Non-Goals

- 不重新定义 activation consent 的产品文案
- 不默认自动改写用户 home 目录里的工具配置
- 不把 ACP 变成前置 blocker
- 不扩成 reusable security capability umbrella

## Non-Negotiables

- Freely canonical policy 是上位真源
- project-local config、launch-time injection、manual-only home guidance 必须分层
- 当前 split truth 必须被明确收口，不能继续依赖口头解释
- ACP 只能消费这份 contract，不能倒过来定义 owner

## Decomposition Tree

1. Reproduce current split truth
2. Define canonical policy layer
3. Define adapter injection layer
4. Define project-local config layer
5. Define manual-only home-config boundary
6. Define ACP follow-on seam

## Eval Plan

成功：
- 读者可以一眼看懂每个工具 posture 是怎么被消费的
- 不再需要靠会话解释来分辨 project-local config 和 launcher flags 谁说了算
- ACP 的位置被清楚压回 optional adapter follow-up

失败：
- 仍看不清 launcher 和 project config 的优先级
- user-global config mutation 还在模糊地带
- ACP 又被误解成 blocker 或 owner

## Dev-Loop Handoff

这条 owner 的下一跳应优先实现 issue-bound contract 写回，再选择最小实现切片去改 `freely init`、launcher、`tools.md` 和 focused tests。
