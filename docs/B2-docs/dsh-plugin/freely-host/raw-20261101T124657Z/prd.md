# PRD：dsh-freely E2E driver

## Goal

证明 DSH 侧 Manager/Worker/Reviewer session 与 Freely gate 能串成确定性链路；不复制 loop。

## Components

- `packaging/dsh-freely/e2e/driver.js`
- `packaging/dsh-freely/e2e/cordis.patch.yml`
- `packaging/dsh-freely/e2e/test/driver.test.mjs`

## Flow

1. `workspaceRegistry.create(config.repo)`。
2. 创建 `freely-e2e-worker` session，restrict `read/write/edit/bash/grep/glob`，steer 写 DONE + git commit。
3. poll status 到 idle（30s）。
4. `git log -1` 验证 commit；失败则 result fail。
5. 创建 `freely-e2e-reviewer` session，restrict `read/grep/glob`，steer 审查；poll idle。
6. 跑 `pretests-gate --project <repo-parent> --issue <issue>`（config 可选）。
7. 写 `<repo>/result.json`，含 sessions/commit/verdict/exitCode。

## E2E preset

- `freely-e2e-worker`：fs + fs-search + bash-sandbox/tool-bash；仅测试 profile 使用。
- `freely-e2e-reviewer`：fs + fs-search。

## Non-goals

- 不改 P1 `freely-worker`；不做 Panel/多项目；不做模型自由编排。

## Acceptance

见 pre-tests。
