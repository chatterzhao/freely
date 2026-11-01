---
analysis_id: DSH-PACKAGING-20261101T120027Z
phase_state: completed
created_at: 2026-11-01
---

# @freely/dsh-freely：P1 打包边界

## 0. 结论

`@freely/dsh-freely` 是 **Freely 的 DSH 打包形态**，不是 Super-agent 对比 candidate，也不是新的 loop。

P1 只交付：

- DSH bundle plugin（`packaging/dsh-freely`）
- manager/worker/reviewer preset + persona + 工具白名单
- `freely_status` / `freely_worker_start` / `freely_reviewer_start` / `freely_gate` 的 subprocess bridge
- 缺服务 fail-closed，不加载 `dsh-superagent`

**handoff envelope、A2A 落库、真实 issue→PR 不在本 raw 的 P1**；它们依赖 C-B/C-D 的上游结果，另开 slice。

## 1. 包结构

```
packaging/dsh-freely/
  package.json          # @freely/dsh-freely, dsh.bundle.patch
  cordis.patch.yml      # insert plugin + 三角色 preset
  index.js              # apply/session/restrict/tools/bridge
  test/plugin.test.mjs  # fake ctx 单测
```

## 2. apply

```js
export const name = 'dsh-freely'
export const inject = ['sessionController','workspaceRegistry','subprocess','tools']
export async function apply(ctx, config) { ... }
```

流程：

1. `workspaceRegistry.create(root)`，创建 `freely-manager` Session。
2. 注册工具：`freely_status`、`freely_worker_start`、`freely_reviewer_start`、`freely_gate`。
3. 对 manager/worker/reviewer 分别 `agent.ctx.tools.restrict({allow})`。
4. `FreelyBridge` 通过 `ctx.subprocess` 跑 `root/bin/freely`。
5. 缺服务/启动失败 fail-closed，不静默降级。

## 3. Presets

| preset | persona | tools |
| --- | --- | --- |
| `freely-manager` | Freely Manager | read/grep/glob + 四个 freely_* 工具 |
| `freely-worker` | Freely Worker | read/write/edit/bash/grep/glob |
| `freely-reviewer` | Freely Reviewer | read/grep/glob |

工具白名单由 `agent.ctx.tools.restrict` 实测：

- manager/reviewer：`glob,grep,read`
- worker：`edit,glob,grep,read,write`

## 4. Bridge

- `bin/freely fleet-status --project <root>`
- `bin/freely pretests-gate --project <root> --issue <issue>`
- argv 显式，不拼 shell；stdout 64KB、stderr 16KB、grace 5s。
- 返回 `{ok, exitCode, stdout, stderr}`；失败结构化返回，不抛到模型。

## 5. DSH API 稳定性

- pin：`dsh 0.2.1-rc.5`，web profile。
- 可用：`sessionController`、`workspaceRegistry`、`subprocess`、`tools`。
- headless：缺 `sessionController/workspaceRegistry`，插件 pending；不支持。
- desktop/tui：未测，不假设。
- 性质：pinned private API，不承诺跨 minor；升级必须重跑 runtime-load spike。

## 6. 证据

- 静态契约：`research/ops/spike/dsh-plugin-contract.ts` 编译通过。
- web profile 真加载：`[dsh-freely] applied ...`。
- Worker session 在 `/tmp/freely-e2e` 写 `DONE.txt` 并 commit `fa9c06e`，`worker_status=idle`。
- `pretests-gate` 对缺失 issue 返回 `gate_exit=1`。
- 三角色 preset/白名单/persona 已验。

## 7. 出界

- 不加载 `dsh-superagent`；DSH Router/Ticket 不接管 loop。
- 不做 Panel、DSH Source、多项目、headless/desktop。
- 不做 handoff envelope/A2A 落库/真实 issue→PR；这些是后续 slice，前置 C-B merge。

## 8. 后续 slice（另开 raw/issue）

1. handoff envelope v1 落库 + Reviewer verdict 不覆盖 Worker summary（依赖 C-B）。
2. Manager→Worker→Reviewer→PR 的完整 E2E（依赖 C-B/C-D）。
3. 真实 issue→PR 后再谈 Panel/多项目。

## 9. 风险

| 风险 | 缓解 |
| --- | --- |
| DSH private API 变化 | pin rc.5；feature detect；升级重跑 spike |
| headless 缺服务 | 明确不支持，不静默降级 |
| 双 loop | 不加载 dsh-superagent |
| 工具白名单失效 | fake ctx + 真实 profile 双测 |
