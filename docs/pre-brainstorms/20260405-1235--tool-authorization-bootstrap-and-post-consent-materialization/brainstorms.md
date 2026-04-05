# Brainstorm - 20260405-1235--tool-authorization-bootstrap-and-post-consent-materialization

## Problem

Freely 已经冻结了 `default autonomy activation consent`，也已经具备一部分 tool boundary materialization，但还没有一条单独 contract 回答下面这组产品问题：

- 用户在 `freely init` 或后续显式设置里，到底在同意什么
- 哪些属于项目接管 / activation consent，哪些属于外部工具 trust / permission / writable-root 配置
- 用户同意之后，Freely 对每个工具能自动做什么，不能自动做什么
- 若工具没有稳定 project-local config surface，Freely 应如何降级为 wrapper、launch-time injection 或 manual steps

当前缺口不是“再补一个提示”，而是缺一个分层真源，把 `consent`、`trust`、`adapter`、`materialization`、`manual followthrough` 分开。

## Confirmed Facts

- `docs/system/workspace/scripts/runtime/freely` 已在 `init` 中要求 `--accept-default-autonomy`，并记录 `activation_consent_status/recorded_at/recorded_via`。
- 同一实现已在 `init` / `set-tool` / `sync-tooling` 路径里 materialize 当前受管 tooling：
  - `codex`: `.codex/config.toml` + `.freely/bin/codex`
  - `claude` / `iflow`: `.freely/bin/<tool>` wrapper
  - `kiro-cli`: passthrough wrapper
- `write_project_codex_config()` 当前会写项目级 `approval_policy`、`sandbox_mode`、`network_access=false`、`writable_roots=["{project}-worktrees"]`，但仍只打印 manual hint：若 Codex 尚未 trust 当前项目，需要用户在 `~/.codex/config.toml` 完成 trust。
- `docs/system/workspace/tools.md` 已明确：
  - `codex` 当前 strongest path 仍是 `direct`
  - `acp` 是 adapter 轴，不等于 direct parity
  - `cc` / `cc-use-codex-cli` 主要依赖 launch-time `--permission-mode bypassPermissions`
  - `iflow` 主要依赖 `--add-dir`
  - `kiro-cli` 当前只有 `--trust-all-tools` 一类 launch-time posture，未验证 sibling worktree project config surface
- 现有测试还暴露一个现阶段不一致：配置层允许 `cc + adapter=acp` 写入 project truth，但 runtime `supported_adapters` 仍只把 `cc` 视为 `direct`。这说明“用户可设置”与“runtime 可稳定执行”还未完全等价，后续 contract 必须把这种差异显式化。
- 已有 owner / pre-brainstorm 已覆盖相邻问题，但没有直接覆盖这条组合边界：
  - `default-autonomy-activation-consent-and-tool-policy-governance`
  - `freely-tool-autonomy-policy-materialization-governance`
  - `worktree-tool-boundary-bootstrap-governance`
  - `runtime-adapter-axis-and-per-tool-adapter-selection`
  - `acp-client-agent-protocol-runtime-adoption`
  - `interactive-init-bootstrap-and-force-governance`
  - `default-project-resolution-and-authorized-project-memory`

## External Facts Worth Folding In

- Claude Code 官方 settings/documentation 暴露了 `defaultMode`、`additionalDirectories` 等项目/目录访问相关能力；这说明 Claude 不是完全没有 config surface，但当前 Freely 仍未验证出与现有 runtime contract 对齐的 project-local managed path。
- ACP 官方语义更接近 permission/update/tool-call transport 统一层，不负责替 Freely决定 approval policy、sandbox、resume target 或 project trust。
- `codex-acp` 当前是 adapter bridge，不是 Codex direct config/trust 的替代物。

## Layer Split That Looks Necessary

### 1. Activation Consent

- 这是 Freely 产品层的“默认高自治是否允许开启”
- 它已经存在，且应继续 blocking
- 它不是某个具体外部工具的 trust 开关

### 2. Project Authorization Bootstrap

- 这是用户显式同意 Freely 为当前项目 materialize 受管配置、wrapper、boundary bootstrap、tool-local files 的动作
- 它应是用户主动触发的 `init` / `set-tool` / future settings mutation，而不是 runtime 在看见项目后静默自启动
- 它需要明确告诉用户：若不做，后面哪些能力会退化

### 3. Tool Trust / Permission Surface

- 这是每个外部工具自己的真相面
- 有的可 project-local materialize
- 有的只能 launch-time 注入
- 有的仍需要 home-level trust 或用户自己执行 CLI/config

### 4. Adapter Surface

- `direct` / `acp` / `prefer_acp_fallback_direct` 改变的是接入路径，不自动改变 consent/trust ownership
- ACP 可统一 permission transport，但不能冒充“授权/bootstrap 已完成”

## Current Per-Tool Reading

### codex

- Freely 当前已能自动做：
  - 写项目级 `.codex/config.toml`
  - 写 wrapper
  - 在 launch-time 注入 `--dangerously-bypass-approvals-and-sandbox`
  - sibling worktree `--add-dir` / `writable_roots`
- Freely 当前不能安全自动完成的部分：
  - 用户 home 级 project trust
- 这说明 Codex 需要显式拆成：
  - project-local materialization
  - home-level trust followthrough

### cc / cc-use-codex-cli

- 当前主要是 launch-time posture materialization
- project-local Claude config surface 尚未被 Freely 冻结成 canonical managed truth
- 若未来要自动写 Claude project settings，必须先验证：
  - 能否 project-local version
  - 与 current session-id / prompt / worktree boundary contract 是否一致
  - 是否会和 global / enterprise policy 混线

### iflow

- 当前主要是 wrapper + `--add-dir`
- 尚未看到 verified project-local permission/trust config 真源

### kiro-cli

- 当前只有 passthrough wrapper
- 现有 contract 仍主要依赖 launch flags，例如 `--trust-all-tools`
- sibling worktree writable-root / project trust 仍未冻结为 Freely-managed project config

### acp path

- ACP 只能减少 bridge duplication
- 它不会自动给出 “这个项目已经授权/已 trust/可安全写入哪些根目录” 的长期真源

## What The New Contract Likely Needs

1. 冻结一套 `authorization bootstrap matrix`
   - per tool:
     - project-local managed config
     - launch-time managed posture
     - home-level manual requirement
     - unsupported / unknown
2. 冻结“用户不同意时的退化说明”
   - 例如：
     - Codex 可能仍无法 trust 当前项目
     - sibling worktree 可能不可达，只能回到 root
     - protected branch 上的 owner development 无法正确 materialize
3. 冻结“用户同意后的执行方式”
   - 直接写项目配置
   - 调用工具官方 CLI 非交互子命令
   - 仅能输出明确 manual instructions
4. 冻结“后续修改授权”的入口
   - CLI / UI settings mutation 应走同一真源，而不是 init-only 一次性逻辑

## Key Tensions

- 不能把 activation consent、tool trust、runtime approval、adapter policy 混成一个总开关。
- 不能因为某工具存在部分配置面，就伪造“Freely 已能完整自动授权这个工具”。
- 不能通过修改用户 home 级全局配置来越权完成项目接管，除非用户显式选择且该工具官方支持。
- 不能把 ACP 误当成 tool trust 方案；它只是 transport/adaptation 方案。

## Boundary Judgment

- 这条问题是新的 product/capability boundary，不应再塞回已收口的 `AGENTS.md` contract owner。
- 也不只是现有 security baseline followthrough，因为它更具体地面向“项目接管后如何做 per-tool authorization bootstrap”。
- 下一跳更像新的 owner family，但在 materialize 之前还要先把 matrix 和 automation boundary 读透。

## Next Routing

这轮预研已经足够支持独立 owner materialization，原因如下：

1. 边界已经稳定到可写 issue contract：
   - activation consent 不是 project authorization bootstrap
   - tool trust 不是 adapter policy
   - project-local config、launch-time injection、manual followthrough 必须分层
2. 现有实现与测试已经暴露具体 drift，不再只是抽象讨论：
   - `init` / `set-tool` / `sync-tooling` 已能修改 tool-local surfaces
   - `cc + acp` 仍存在 config/runtime drift
   - `cmd_init()` 已混入过多职责，未来 GUI/TUI 不能再复制一套语义
3. 这条问题跨越产品治理、runtime contract、tool bootstrap matrix 与 future settings surface，已超出已有 owner 的窄 followthrough 范围。

因此下一跳改为：

- 新开 `tool-authorization-bootstrap-and-post-consent-materialization-governance` owner
- 第一轮 phase 只冻结 contract、matrix、degradation semantics 与 refactor seam
- 不在这轮 owner 内直接改 runtime 或新增 tool automation
