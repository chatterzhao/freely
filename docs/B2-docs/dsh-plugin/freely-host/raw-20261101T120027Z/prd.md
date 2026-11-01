# PRD：@freely/dsh-freely Freely-host 插件（P1）

## Goal

让 DSH 只做 Freely 的 harness：插件创建 Manager/Worker/Reviewer Session，提供工具白名单/persona/subprocess bridge；Freely 保留 scan、A2A、gates、worktree、PR。

## 包结构

```
packaging/dsh-freely/
  package.json          # name, type module, dsh.bundle.patch
  cordis.patch.yml      # insert plugin + 三角色 preset
  index.js              # name/inject/apply, FreelyBridge, tools
  test/plugin.test.mjs  # fake ctx 单测
```

## apply

```js
export const name = 'dsh-freely'
export const inject = ['sessionController','workspaceRegistry','subprocess','tools']
export async function apply(ctx) { ... }
```

流程：

1. 读 config：`freelyRoot`（默认 process.cwd()）。
2. 确保 manager session（preset `freely-manager`）；创建 worker/reviewer 时由 Freely runtime 触发（P1 只建 manager）。
3. 对每个 session 调 `agent.ctx.tools.restrict({allow})`。
4. 注册工具 `freely_status`：`ctx.subprocess` 跑 `bin/freely fleet-status --project <root>`，返回 stdout。
5. 记录 `applied` 日志；失败 fail-closed，不静默降级。

## Presets

`cordis.patch.yml` 定义：

- `freely-manager`：persona Manager；tools `read,grep,glob`。
- `freely-worker`：persona Worker；tools `read,write,edit,grep,glob`。
- `freely-reviewer`：persona Reviewer；tools `read,grep,glob`。

## 工具白名单

`agent.ctx.tools.restrict({allow})`；空 preset 先挂 `@deepseek-ai/dsh-tool-fs`/`tool-fs-search`。不把 DSH 全局工具直接暴露给 Reviewer。

## Bridge

- `FreelyBridge.status()` → `bin/freely fleet-status`。
- 输出限 64KB；timeoutMs 透传 subprocess；失败返回 `{ok:false, stderr}`，不抛到模型。
- 不通过 shell 拼接参数；argv 显式。

## Handoff

P1 不实现 handoff envelope；handoff/A2A 由上游 C-B 负责，后继 slice 见 successor raw `20261101T124657Z`。

## 非目标

- Panel、DSH Source、多项目、headless/desktop。
- DSH Router/Ticket、`dsh-superagent`。
- 完整 A2A RPC。

## 验收

- 插件被 DSH web profile 加载；三角色 preset 创建成功；白名单生效。
- `freely_status` 返回 fleet 输出。
- P1 验收：插件加载、三 preset/白名单/persona、bridge、gate exit 透传。
- 真实 issue→PR 由 successor raw `20261101T124657Z` 承接；未跑前不宣称插件产品完成。
