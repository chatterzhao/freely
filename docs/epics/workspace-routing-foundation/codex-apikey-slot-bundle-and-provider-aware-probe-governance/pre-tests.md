# Pre-tests

## Pre-merge acceptance

1. `save codex` 在 API-key/provider 模式下保存的 slot，必须包含足够恢复 provider/base-url/auth-mode 的 slot-local truth，而不是只保存 `auth.json`。
2. `switch codex <slot>` 在以下四种方向上必须有明确可测试 contract：
   - `account -> account`
   - `account -> apikey`
   - `apikey -> account`
   - `apikey -> apikey`
3. 从 `apikey-*` 切回 `account-*` 时，live `~/.codex/config.toml` 中 API-key-only provider residue 必须被清理或被目标 account fragment 覆盖。
4. `apikey-*` slot 的可用性判断不得再以 OAuth/curl inventory sweep 为 gate；它必须以 non-interactive `codex exec` probe 为 canonical truth。
5. legacy unprefixed Codex slot 仍可被读取；若无 manifest 明确声明，应按 legacy/account semantics 处理。
6. 非 Codex 工具在本轮 IBM 文档和后续实现中不得被写成已经拥有 verified live auth materializer 或 proactive probe，除非有新的 verified evidence。
7. `ai-switch-cli` 的最小命令面必须冻结为 `list/current/login/save/switch/delete/probe/best/status`，并明确 `switch auto` 与 `best` 的职责差异。
8. `ai-switch-cli --json` 的顶层 envelope 必须至少冻结以下字段：`ok`、`backend`、`tool`、`requested_action`、`capability_tier`、`slot_id`、`slot_kind`、`current_slot_id`、`provider_id`、`probe_method`、`mutated_live_surfaces`、`reason_code`、`message`。
9. `login <tool>` 必须允许 interactive 选择 `account` 与 `apikey`，也必须允许 non-interactive `login <tool> <auth-mode>`。
10. `freely init` 的长期 contract 必须明确：检测 `ai-switch-cli` 是否安装、询问是否使用或安装、并把 backend 选择写入项目本地配置。
11. `freely ai login <tool> <auth-mode>` 的长期 contract 必须明确：登录完成后若工具不在 priority list 中，默认回车插到最前面。
12. `ai-switch-skill` 的职责边界必须冻结为 AI-facing CLI guide，而不是把 tool-specific live-file knowledge 继续散落在 Freely prompt 内部。

## Post-merge acceptance

1. 在 canonical `develop` 上，Codex account slot 与 apikey slot 都能进入同一 generic slot inventory surface，但 probe routing 会按 slot kind 正确分流。
2. 当当前 active slot 为 `apikey-*` 且不可用时，watchdog 的恢复路径不会错误依赖 OAuth inventory truth 来判定其可用性。
3. `freely ai status` / `freely ai switch codex auto` / watchdog recovery 对 slot-kind-aware probe contract 的解释保持一致。
4. canonical dogfood recheck 应能证明：
   - switching account/apikey cross-kind 不会把旧 provider/base-url 留在 live config
   - all-tools generic slot inventory 仍可工作
   - 只有 Codex 在本轮拥有 proactive strong contract
5. 当 `ai-switch-cli` 已安装时，Freely 的后续实现应能只依赖其 JSON surface 完成 probe/switch/select 决策，而不是重新内嵌每个工具的私有 live-file 推断。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `save codex in apikey/provider mode persists enough slot-local truth to restore provider-aware auth surfaces`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`

### PT-2
- id: `PT-2`
- requirement: `cross-kind account/apikey switching clears stale provider residue while preserving unrelated config tables`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`

### PT-3
- id: `PT-3`
- requirement: `kind-prefixed codex login/save defaults remain stable for repeated account logins`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-login-creates-incremented-slot`

### PT-4
- id: `PT-4`
- requirement: `oauth inventory remains authoritative for account slots, including oauth_unreachable blocking when no apikey fallback exists`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`

### PT-5
- id: `PT-5`
- requirement: `apikey slots can still be selected through exec-based truth when oauth inventory is unreachable`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`

### PT-6
- id: `PT-6`
- requirement: `watchdog and ai switch preserve prior account-slot behavior while the new apikey path is added`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
