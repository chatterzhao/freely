# Pre-tests: project-scoped-network-proxy-configuration-and-launcher-inheritance-governance

## Acceptance target

1. `freely init` 会把 proxy defaults 写进 `.freely/config.env`，而不是依赖 runtime shell 里的默认值。
2. resolver 至少支持：
   - `inherit`
   - `explicit`
   - `disabled`
3. codex launcher 与 watchdog 的 OAuth/curl path 使用同一份 resolver。
4. runtime 里不再依赖 hardcoded localhost proxy defaults。

## Testing layers

1. Script regression gate
   - `test-freely-init-codex-project-config-force`
   - `test-freely-network-proxy-resolver`
2. Runtime inheritance gate
   - `test-freely-network-proxy-launcher-inheritance`
   - `test-freely-network-proxy-oauth-inheritance`
3. Governance gate
   - `./bin/governance-check`

## Required evidence

1. `freely init` 的默认输出包含 proxy config defaults。
2. `inherit` mode 不改写现有 proxy env。
3. `explicit` mode 会把 `.freely/config.env` 的 proxy 真源导出到 codex launcher。
4. OAuth/curl path 也会读取同一份 project-scoped proxy env。
5. runtime scripts 中不再出现 `127.0.0.1:7890` 这类硬编码 proxy fallback。

## Non-goals

1. 不要求在这个 lane 里做前端 UI。
2. 不要求在这个 lane 里迁移用户全局代理配置。
3. 不要求改动 OAuth inventory sweep 的业务分类语义。
