---
b1_id: B1-20261101T120027Z
phase_state: completed
source_raw: raw-20261101T120027Z
source_url: https://github.com/chatterzhao/freely/issues/4112
produced_candidate: C-20261101T120027Z-A
created_at: 2026-11-01
---

# B1_IBM: @freely/dsh-freely DSH 打包形态

## Input

独立 raw `raw-20261101T120027Z`（GitHub #4112 / Gitee IKS33V）。从 Super-agent 对比 raw 中拆出：DSH 打包是 Freely 的分发形态，不是 Super-agent candidate。

## Problem

Freely 需要在不复制 loop 的前提下进入 DSH 生态：DSH 提供 Session/Agent/模型/工具，Freely 保留 scan、Manager/Worker/Reviewer、A2A、gates、worktree、PR。

## Discovery

- DSH `0.2.1-rc.5` web profile 可加载第三方 bundle plugin。
- `sessionController/workspaceRegistry/subprocess/tools` 可用；headless 缺服务。
- P1 插件已创建 Manager session、工具白名单、`freely_status` bridge。
- Worker session 已在 `/tmp/freely-e2e` 真写文件并 commit `fa9c06e`。
- 三角色 preset/persona/白名单已验证。
- 仍缺完整 issue→PR E2E。

## Decision

- 只做 Freely-host 插件，不做 DSH-as-harness adapter，不加载 `dsh-superagent`。
- 独立 raw、独立 B1/B2/PR；Super-agent raw 只保留底层 runtime 能力。
- 宿主基线锁 `dsh 0.2.1-rc.5` + web；headless/desktop 出界。

## Candidate

`C-20261101T120027Z-A`：实现 `packaging/dsh-freely` P1 插件与 E2E；milestone `M-20261101T120027Z-A`。
