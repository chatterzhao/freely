# Brainstorm - 20260405-0027--codex-apikey-slot-bundle-and-provider-aware-probe

## Problem

Freely 现有 Codex slot contract 仍以 `~/.codex/auth.json` copy-in/copy-out 为核心，这足以覆盖 ChatGPT account 登录，但不足以覆盖用户已经真实在使用的 API-key/provider 模式。

当前新需求已经收口到一个更窄且更可实现的 runtime owner：

- `apikey` 也必须成为一种一等 slot
- 它的 key / provider / base URL / auth-mode 信息必须落在 slot 目录里，而不是只漂浮在 live `~/.codex/config.toml`
- `switch` / `login` / `save` / `delete` 必须兼容 `account-*` 与 `apikey-*` 两类 slot
- Freely 仍要保持自己已有的 stronger contract：
  - probe first
  - classify failure reason
  - auto-switch only when rotation is justified
  - no-launch when every slot is unavailable

## Confirmed Facts

- 当前本机 `~/.codex/auth.json` 只有 `OPENAI_API_KEY`，没有 account email/session 字段。
- 当前本机 `~/.codex/config.toml` 同时包含：
  - `model_provider = "custom"`
  - provider-scoped `base_url`
  - `requires_openai_auth = true`
- OpenAI Codex 官方 schema 已定义：
  - `model_providers`
  - `base_url`
  - `env_key`
  - `openai_base_url`
  - `requires_openai_auth`
- `cc-switch` 已证明一个重要实现事实：Codex live state 应按 `auth.json + config.toml` 成对处理，`base_url` 也应优先写到当前 provider section，而不是误写到别的 TOML section。
- Freely 已有 stronger runtime truth：
  - Codex slot switch lock
  - watchdog-owned probe-first recovery
  - no-launch truth
  - cooldown / availability cache

## Boundary

这不是重新打开 architecture-only authorization owner，也不是回塞到已完成的 unified-slot / oauth-sweep owner。

它是一个新的 runtime capability follow-on，负责：

1. Codex API-key slot bundle contract
2. account/apikey cross-kind switch semantics
3. provider-aware probe and classification
4. atomic live auth+config materialization

## Proposed Direction

### 1. Slot inventory contract

- 保留 canonical root：`~/.ai-auth/<tool>-<slot_id>/`
- Codex slot id 改成 kind-prefixed：
  - `account-<normalized-name>`
  - `apikey-<normalized-name>`
- 旧的未带前缀 Codex slot 保持兼容读取，但在下一次 save/rewrite 时允许 lazy migration

### 1a. Generic all-tools contract

- 这次不要把 `apikey` bundle 做成 Codex-only filesystem special case
- 应先冻结一份 generic slot bundle vocabulary，供所有当前受支持工具复用：
  - `tool`
  - `slot_id`
  - `slot_kind`
  - `auth_source`
  - `capability_tier`
  - optional tool payload files
- `cc`、`opencode`、`iflow`、`kiro-cli` 也应能继续挂在同一 inventory root 下，并兼容 `list/save/switch/delete/status`
- 但不能假装它们第一轮就与 Codex 拥有同级 probe parity

推荐 capability tier：

- `inventory_only`
- `switchable`
- `probeable`
- `auto_rotatable`

首批判断：

- `codex`: target `auto_rotatable`
- `cc` / `cc-use-codex-cli` / `opencode` / `iflow` / `kiro-cli`: preserve generic compatibility first, then upgrade probe parity tool by tool

### 1b. Required abstraction layers

只抽象 slot 目录还不够，因为不同工具 live state 落在不同文件和不同行为面上。

建议拆成三层：

1. generic slot manifest layer
   - 负责统一 inventory root、slot id、metadata、payload file naming
2. per-tool live materializer adapter
   - 负责把 slot bundle 应用到该工具的真实 live surfaces
   - 例如：
     - `codex` -> `auth.json + config.toml`
     - `cc` / `iflow` / `opencode` -> wrapper/env/config fragment or other verified tool-local files
3. per-tool probe adapter
   - 负责判断该工具/slot 当前是否 usable，以及失败分类

因此泛化的重点应是：

- 统一 slot bundle contract
- 统一 slot command semantics
- 为每个工具保留自己的 materialize/probe implementation

而不是：

- 强行要求所有工具都改同一个 live file
- 强行要求所有工具都遵守 Codex provider semantics

### 1c. Preferred long-term split: standalone `ai-switch-cli`

如果 Freely 自己长期内嵌所有工具的 live-file writer / probe logic，维护成本会越来越像重新做一个 `cc-switch`，这不符合 Freely 的 CLI-first orchestration 定位。

更合理的长期拆分应是：

1. `ai-switch-cli`
   - 独立负责 tool auth slot inventory、save/switch/delete/probe/status
   - 每个工具自己的 live file mutation、provider config patch、tool-native login flow 都归它
2. Freely
   - 负责 runtime/watchdog/fallback/tool priority/control-plane orchestration
   - 不直接以“读写各工具 live 文件”作为长期 contract
   - 优先调用 `ai-switch-cli --json ...` 获取：
     - 当前 slot
     - 可用 slot
     - probe 结果
     - switch 执行结果

因此建议把当前 owner 分成两个阶段：

- Phase 1
  - 先在 Freely 内冻结 generic slot manifest、Codex slot bundle、slot-kind-aware probe contract
  - 用它证明正确性
- Phase 2
  - 把 tool-specific materializer/probe adapter 提炼成独立 `ai-switch-cli`
  - Freely runtime 改为 CLI-first 集成，只保留薄 orchestration layer

这能保留当前研究成果，同时避免 Freely runtime 永久背负所有工具的 auth/config 细节

### 2. Slot bundle contents

- `manifest.json`
- optional `auth.json`
- optional provider/config slice
- optional env metadata stub

最低 manifest 字段：

- `slot_kind`
- `auth_source`
- `provider_id`
- `base_url`
- `openai_base_url`
- `requires_openai_auth`
- `preferred_auth_method`
- `probe_strategy`

### 2a. Codex first-slice bundle contract

Codex 第一轮不应把整个 `~/.codex/config.toml` 原样塞进 slot 目录，也不应继续只保存 `auth.json`。

建议冻结为：

- `manifest.json`
  - `tool = "codex"`
  - `slot_id`
  - `slot_kind = account|apikey|legacy_account`
  - `capability_tier = auto_rotatable`
  - `probe_strategy = oauth_inventory_then_exec|exec_only`
  - `saved_from_version`
- optional `auth.json`
  - account slot: 保存 OAuth/session truth
  - apikey slot: 保存 key-bearing auth truth
- optional `config-auth.toml`
  - 只保存 auth/provider materialization 所需字段，而不是整个 live config
  - 例如：
    - `model_provider`
    - selected provider section 的 `base_url` / `env_key` / `wire_api` / `query_params`
    - `preferred_auth_method`
    - `requires_openai_auth`
    - `openai_base_url`
- optional `probe.json`
  - 最近一次 probe 结果摘要，可选缓存，不是 live truth

这样做的原因：

- slot 目录必须足够恢复 provider/auth 行为
- 但 live `config.toml` 可能还承载与 auth 无关的用户偏好，不能被 slot restore 粗暴覆盖
- 因此切换规则应是“slot 提供 auth/config fragment，materializer 以 syntax-preserving 方式写回 live file，并清理上一种 auth kind 留下的 stale fields”

### 2b. Generic manifest contract

为支持 `codex`、`cc`、`cc-use-codex-cli`、`opencode`、`iflow`、`kiro-cli` 共享 command surface，generic manifest 至少需要：

- `tool`
- `slot_id`
- `slot_kind`
- `auth_mode`
- `capability_tier`
- `materialization_strategy`
- `probe_strategy`
- `payloads`
  - tool-specific payload file list，例如 `auth.json`、`config-auth.toml`、`settings.json`、`env.json`
- `last_verified_at`
- `last_verified_status`

其中：

- generic layer 只理解这些元数据
- 是否存在 `auth.json` / `settings.json` / env overlay，由 tool adapter 自己决定
- `switch` 命令应先读目录名，再以 manifest 作为更强真相校正；目录名负责快速路由，manifest 负责向后兼容和 future migration

### 3. Switch direction matrix

- `account -> apikey`
  - apply API-key slot auth/config pair
  - overwrite or clear stale account-only live truth
- `apikey -> account`
  - restore account auth payload
  - clear or overwrite stale provider/base-url overrides from API-key slot
- `apikey -> apikey`
  - atomically replace provider/auth/config bundle
- `account -> account`
  - keep current account behavior, but no longer assume auth-only is always enough

### 3a. Cross-kind materialization rules for Codex

| from | to | required live writes | stale truth that must be cleared |
| --- | --- | --- | --- |
| `account-*` | `account-*` | replace `auth.json`; apply saved account config fragment if present | prior API-key provider override fields if they are not present in target slot |
| `account-*` | `apikey-*` | replace `auth.json`; apply API-key `config-auth.toml` fragment; update selected provider + base URL | OAuth-only identity assumptions, stale account-derived provider defaults |
| `apikey-*` | `account-*` | replace `auth.json`; apply account fragment or explicit account defaults | selected custom provider section, API-key-only `base_url`, `env_key`, `preferred_auth_method = "apikey"` when target does not require them |
| `apikey-*` | `apikey-*` | replace `auth.json`; replace effective auth fragment; re-point selected provider | old slot's provider section values and auth-mode residue |

补充规则：

- `switch` 成功判定不能只看文件 copy 成功，而要看 post-switch probe 是否匹配目标 slot kind 的 truth source
- `delete` 一个 active slot 前，要么先 probe/switch 到另一个 usable slot，要么显式 `--force`
- active-slot pointer 继续走 generic `~/.ai-auth/.<tool>-current-slot`
- 对 legacy unprefixed Codex slot：
  - 默认当作 `legacy_account`
  - 若 manifest 声明 `slot_kind = apikey`，则以 manifest 为准

### 4. Probe contract

Freely should not treat “files copied successfully” as availability truth.

The first narrow probe taxonomy should distinguish:

- `usable`
- `auth_invalid`
- `quota_or_rate_limited`
- `provider_endpoint_invalid`
- `provider_network_transient`
- `provider_network_persistent`
- `config_invalid`

### 4a. Probe adapter must branch by slot kind

`switch` 不只是“把目录拷回 live state”，还要根据 `slot_id` / `slot_kind` 选择正确的 probe path。

对 Codex 第一轮应冻结为：

- `account-*`
  - 继续优先走现有 OAuth inventory truth
  - 即当前 watchdog 里的 `wham/usage` / curl sweep family
  - 只在最终 launch-time confirmation 时再进入真实 `codex exec` probe
- `apikey-*`
  - 不再把 OAuth/curl inventory sweep 当成 canonical usability truth
  - 应直接走现有 non-interactive execution probe
  - 也就是 watchdog 里已经存在的：
    - 写入只含 `hi` 的 prompt
    - `codex exec --dangerously-bypass-approvals-and-sandbox`
    - 基于真实输出分类 `usable / unauthorized / rate_limited / timeout / error`

原因：

- `apikey-*` 的可用性取决于 live provider/config/auth bundle，而不再只是 OAuth account inventory
- 对这类 slot，旧的 curl/OAuth check 可能根本不是正确 truth source

### 4b. Switch-time selection rule

Codex `switch` / auto-switch / watchdog probe 应先按目录名或 manifest 决定 probe adapter：

1. if `slot_id` matches `account-*`
   - inventory probe: OAuth/curl path
   - launch confirmation: existing `codex exec hi` path
2. if `slot_id` matches `apikey-*`
   - inventory/probe truth: `codex exec hi` path
   - do not gate on OAuth sweep result
3. if legacy unprefixed slot
   - default to legacy account semantics unless manifest says otherwise

这样可以保持：

- 旧 account slot 行为不被打断
- 新 apikey slot 有正确 truth source
- 同一套 generic scheduler 仍可工作，只是 probe adapter 被 slot kind 分流

### 5. Delete contract

- deleting a slot deletes only that saved slot bundle
- deleting the active slot must either:
  - refuse without explicit force, or
  - auto-switch to another verified usable slot first

## Freely Per-Tool Auth Materialization Matrix

| tool | likely auth kinds | current Freely slot state | authoritative live surface | save/switch maturity | probe maturity | recommended tier now |
| --- | --- | --- | --- | --- | --- | --- |
| `codex` | `account`, `apikey`, `legacy_account` | real saved slots today, but still auth.json-centric | `~/.codex/auth.json` + `~/.codex/config.toml` | partial and needs redesign for auth+config bundle | strong, already has OAuth sweep + exec probe | `auto_rotatable` target |
| `cc` | likely `account`, maybe `apikey` via Claude/provider setup | generic slot container only | mostly launch-time flags today; no frozen Freely-managed auth truth yet | inventory only in current Freely runtime | no verified slot probe path in Freely | `inventory_only` |
| `cc-use-codex-cli` | same as `cc` top-level auth | generic slot container only | same as `cc`; Codex MCP policy is launch-time, not auth storage | inventory only in current Freely runtime | no separate slot probe path | `inventory_only` |
| `opencode` | likely `apikey` first | generic slot container only | research evidence suggests `~/.config/opencode/opencode.json`, but current Freely runtime has no verified writer or launcher parity | no current save/switch materializer in Freely; current runtime support is inconsistent | no probe adapter yet | `inventory_only` now, `switchable` only after verified writer + launcher |
| `iflow` | `apikey` and maybe account artifacts | generic slot container only; current runtime explicitly treats slot container as scheduler compatibility only | local machine evidence suggests `~/.iflow/settings.json`, but current Freely runtime does not yet freeze it as authoritative writable truth | no current save/switch materializer in Freely | no probe adapter yet | `inventory_only` now, `switchable` only after verified writer |
| `kiro-cli` | unknown / unverified | generic slot container only | no verified stable auth/config truth in current research | no real save/switch beyond slot pointer | no probe adapter yet | `inventory_only` |

解读：

- 这次预研不能把“已纳入统一 slot inventory”误写成“所有工具都支持真正 auth 切换”
- generic compatibility 的意思是：
  - 都能挂到 `~/.ai-auth/<tool>-<slot>/`
  - 都能复用 `list/status/current-slot/delete` 的 command surface
- 但只有当某工具的 live auth truth 与 probe truth 都被核实后，才能升级成 `switchable` / `probeable` / `auto_rotatable`

## Command Surface Implications

## CLI-First Integration Direction

一旦 `ai-switch-cli` 独立出来，Freely 推荐只消费稳定 JSON contract，例如：

- `ai-switch-cli list --tool <tool> --json`
- `ai-switch-cli current --tool <tool> --json`
- `ai-switch-cli login --tool <tool> --auth-mode <mode> --slot <slot> --json`
- `ai-switch-cli save --tool <tool> --slot <slot> --json`
- `ai-switch-cli probe --tool <tool> [--slot <slot>] --json`
- `ai-switch-cli switch --tool <tool> --slot <slot> --json`
- `ai-switch-cli best --tool <tool> --json`

Freely control plane 则只负责：

- 何时 probe
- 何时 rotate
- 何时跨工具 fallback
- no-launch when all tools unavailable
- 读取 / 更新项目级工具优先级列表

也就是说：

- 可用性判断与切换执行可交给 `ai-switch-cli`
- “何时该切、切哪个工具、是否该停机等待” 仍归 Freely

这正是 Freely 与 `cc-switch` 的边界差异：

- `cc-switch`: 以工具切换产品为主体
- Freely: 以 runtime/watchdog/orchestration 为主体，并通过 CLI-first 集成消费切换能力

## Init And Login UX Implications

### `freely init`

若检测不到 `ai-switch-cli`，可以继续以内置能力运行；但一旦独立 CLI 稳定，推荐把 `freely init` 冻结为：

1. 检查本机是否已安装 `ai-switch-cli`
2. 若未安装：
   - 提示是否安装/引导安装
   - 用户拒绝时，Freely 继续以内置 fallback 能力运行
3. 若已安装：
   - 写入 project config truth，例如：
     - `AI_SWITCH_BACKEND=cli`
     - `AI_SWITCH_CLI_BIN=ai-switch-cli`

### `freely ai login <tool> <auth-mode>`

新增一个与工具优先级联动的 command 语义：

1. 先调用 tool switch backend 完成 login/save
2. 完成后检查项目级工具优先级列表是否已包含该工具
3. 若未包含：
   - 询问是否加入优先级列表
   - 默认回车即插入最前面
4. 若已包含：
   - 不改顺序，除非用户显式要求提升

这样做的原因：

- 用户刚登录一个工具，通常就是希望 Freely 能优先用它
- 但仍保留项目自主控制，不强行静默改动工具顺序

### Priority list semantics

Freely 的工具优先级列表应同时扮演两层角色：

1. routing preference
2. availability fallback order

需要明确：

- 被加入列表的工具，不代表当前一定可用
- 可用性仍要通过 `probe` / `best` / cached status 判断
- 但若一个新登录工具不在列表里，Freely 默认不会优先考虑它

因此 `login` 联动 priority list 是合理的首轮 UX

### `login`

- interactive:
  - `login <tool>` 进入 auth-mode picker
  - Codex 至少提供：
    - `account`
    - `apikey`
- non-interactive:
  - `login <tool> --auth-mode <mode> --slot <slot>`
- 首轮 Codex 语义：
  - `--auth-mode account`: tool-native login flow，随后 capture `auth.json` + account fragment
  - `--auth-mode apikey`: guided capture or direct `save`-style onboarding，把当前 live `auth.json + config-auth.toml` 保存成 slot

### `save`

- 必须从 tool live truth 抽取 bundle，而不是假设只有一个 auth file
- Codex `save` 需要：
  - 识别当前 slot kind
  - 生成 kind-prefixed slot id
  - 抽取 auth/provider fragment

### `switch`

- 先按目录名前缀分流：
  - `account-*`
  - `apikey-*`
  - legacy
- 再读取 manifest 校正最终 materializer / probe adapter

### `delete`

- 删除逻辑保持 generic
- 若 tool 有 live materializer，则 active-slot delete 要额外经过 tool-aware safety check

## Reference Boundary

`cc-switch` 在本 owner 中只能作为“哪些工具改哪些 live 文件”的旁证，不能成为 Freely 的 architecture template。

明确不复制：

- 它的产品边界
- 它的 UI / flow
- 它的配置管理层级
- 它缺少 Freely watchdog-owned probe-first / auto-rotate / no-launch contract 的地方

可复用的只有研究事实：

- Codex live truth 不是 `auth.json` 单文件
- OpenCode / Claude / Gemini / iFlow 各自确实存在不同 live surfaces
- 不同工具需要不同 writer/materializer

## Generic Command Semantics With Tool Adapters

为保持 `login/save/switch/delete` 一致，建议命令面保持 generic，但分发到 tool adapters：

1. `login <tool>`
   - 调用 tool-specific login or capture flow
   - 产出 generic slot bundle
2. `save <tool> [slot]`
   - 从当前 live tool state 抽取 slot bundle
3. `switch <tool> <slot>`
   - generic layer 负责 inventory / locking / active-slot pointer
   - tool adapter 负责 live materialization
   - probe adapter 负责 post-switch verification
4. `delete <tool> <slot>`
   - generic layer 负责 slot inventory deletion and active-slot governance
   - tool adapter 只在需要清理当前 live state时介入

## Why New Owner

- architecture owner already froze the boundary and explicitly calls for a narrower follow-on instead of widening itself into runtime churn
- completed unified-slot owner should not be reopened for per-tool probe parity
- completed oauth-sweep owner is too OAuth/auth-json centric to own provider-aware config bundle switching
- generic all-tools compatibility should be preserved by reusing the existing slot root/manifest discipline, not by forcing every tool into Codex-specific provider semantics

## Next Routing

This candidate is ready for milestone visibility under `workspace-routing-foundation`.

Next step:

- materialize a dedicated issue for `codex api-key slot bundle and provider-aware probe governance`
- keep the first implementation slice narrow:
  - slot bundle format
  - switch semantics
  - config mutation helpers
  - focused probe/status regressions
  - do not promise non-Codex probe parity in the first landing
