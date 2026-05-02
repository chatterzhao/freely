# Pre-tests: project-scoped-network-proxy-configuration-and-launcher-inheritance-governance

## Acceptance Structure

### Pre-merge acceptance

1. `freely init` 会把 project-scoped proxy defaults 写进 `.freely/config.env`，不再依赖 runtime shell 里的 hardcoded localhost fallback。
2. resolver 必须稳定支持：
   - `inherit`
   - `explicit`
   - `disabled`
3. codex launcher 与 watchdog 的 OAuth/curl path 必须继承同一份 project-scoped proxy env。
4. 无参 `freely ai switch codex` 必须先刷新保存的 auth inventory，再根据最新结果决定是否切换到 `usable` slot。
5. runtime 真源中不再保留 `127.0.0.1:7890` 这类代理硬编码 fallback。

### Post-merge acceptance

1. 合入 `develop` 后，后续 worktree 只要从新 `develop` 继续推进，就会默认继承同一套 project-scoped proxy contract。
2. 这一批不要求同时完成前端配置入口；前端后续只需改 `.freely/config.env` 即可驱动同一能力。

### Non-goals

1. 不要求在这个 lane 里完成前端 UI。
2. 不要求迁移用户级全局代理配置。
3. 不要求在这个 lane 里重写 watchdog 的完整 limit recovery 状态机。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `freely init writes project-scoped proxy defaults into .freely/config.env`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/code-reviews/20260327-project-scoped-network-proxy-verification.md`

### PT-2
- id: `PT-2`
- requirement: `network proxy resolver preserves inherit mode and exports explicit and disabled modes consistently`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/code-reviews/20260327-project-scoped-network-proxy-verification.md`

### PT-3
- id: `PT-3`
- requirement: `codex launcher and OAuth sweep inherit the same project-scoped proxy env and never fall back to hardcoded localhost defaults`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/code-reviews/20260327-project-scoped-network-proxy-verification.md`

### PT-4
- id: `PT-4`
- requirement: `no-arg freely ai switch codex refreshes saved auth inventory before selecting a usable slot`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/code-reviews/20260327-project-scoped-network-proxy-verification.md`

### PT-5
- id: `PT-5`
- requirement: `governance-check stays clean aside from the repository's existing legacy naming warnings`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/code-reviews/20260327-project-scoped-network-proxy-verification.md`
