# Issue: project-scoped-network-proxy-configuration-and-launcher-inheritance-governance

- issue_id: `I-20260327-0651`
- title: Project-scoped network proxy configuration and launcher inheritance governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `project-scoped-network-proxy-configuration-and-launcher-inheritance-governance`
- issue-name: `project-scoped-network-proxy-configuration-and-launcher-inheritance-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260327/candidates.md#c-20260327-0651-b`
- source_brainstorm: `docs/B1-docs/raw-20260327/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/B2-docs/ibm/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely runtime 里和代理有关的默认值目前仍然分散在脚本内部，典型问题是把 localhost 代理写死成运行时 fallback。这样会造成三个直接后果：

1. codex exec、curl/OAuth、watchdog 和 launcher 不能共享同一份 proxy truth。
2. 后续前端如果只改 project config，也无法把所有调用面一起带起来。
3. 代理行为被藏进代码默认值后，任何真实环境下的网络出口变化都会被测试假象掩盖。

这条 issue 的目标是把 proxy 变成 Freely 的项目级能力，而不是散落在 runtime shell 里的隐式假设。

## Scope

1. 把 `.freely/config.env` 作为 project-scoped proxy config truth source。
2. 新增一个最小、可复用的 resolver，统一处理 `inherit` / `explicit` / `disabled`。
3. 让 codex exec launcher 和 watchdog 里的 OAuth/curl path 共用同一个 resolver。
4. 清理 runtime 里的硬编码 localhost proxy defaults。
5. 让无参 `freely ai switch codex` 每次都刷新保存的 auth inventory，再基于最新 sweep 结果选 usable slot。
6. 增加 focused tests，锁住 config write、resolver 行为、launcher inheritance 与 switch refresh contract。

## Non-Goals

1. 不做前端 UI。
2. 不做全局用户级代理配置迁移。
3. 不改 OAuth inventory sweep 的业务语义，只改它取 proxy 环境的方式。
4. 不扩写与 proxy 无关的 watchdog / scheduler / state machine 逻辑。

## Acceptance

1. `freely init` 会在 `.freely/config.env` 中写入 project-scoped proxy defaults。
2. resolver 支持：
   - `inherit`：不改写现有 proxy env
   - `explicit`：从 `.freely/config.env` 的配置导出 proxy env
   - `disabled`：清空 proxy env
3. codex launcher 与 watchdog 的 OAuth/curl path 都从同一个 resolver 继承 proxy env。
4. runtime 里不再出现 hardcoded `127.0.0.1:7890` 作为代理默认值。
5. 无参 `freely ai switch codex` 不会偷吃新鲜 cache，而是先刷新所有保存的 auth inventory，再决定是否切换。
6. focused tests 覆盖：
   - init config defaults
   - resolver mode handling
   - codex launcher inheritance
   - OAuth/curl inheritance
   - no-arg switch refreshes inventory before selecting a usable slot

## Completion

- `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/issues/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance.md`
- `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/prd.md`
- `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/pre-tests.md`
- `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/tasks.md`
- `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/code-reviews/`
- `docs/progress/workspace-routing-foundation/p-project-scoped-network-proxy-configuration-and-launcher-inheritance-governance.md`
- `docs/system/workspace/scripts/runtime/network-proxy-resolver.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
- `docs/system/workspace/scripts/tests/test-freely-network-proxy-resolver`
- `docs/system/workspace/scripts/tests/test-freely-network-proxy-launcher-inheritance`
- `docs/system/workspace/scripts/tests/test-freely-network-proxy-oauth-inheritance`
- `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
- `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-resolver`
- `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-launcher-inheritance`
- `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-oauth-inheritance`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `./bin/governance-check`
