# Brainstorm - 20260406-1851--codex-interactive-login-and-apikey-input-flow

## Problem

Freely 的 Codex bundle contract 已经把 `login/save/switch` 相关 truth 冻结到 canonical owner，但当前实现仍缺一个受治理约束的 first-hop interactive login flow：

- `freely ai login codex` 还没有稳定的交互式 auth-mode 选择语义
- `freely ai login codex apikey` 缺少 provider/base-url/api-key 的受控输入收集与 direct-arg parity
- 当前 dirty worktree 已经在 `ai-cli` 里实现了一套交互逻辑和 4 个对应测试，但它还没有 canonical owner，继续实现只会把 UX contract 漂在未归档代码里

这个问题不等于 current-live bootstrap，也不该回塞进已完成的 bundle/probe owner。它是一个更窄的 “Codex interactive login UX + apikey input/materialization first-hop” follow-on。

## Confirmed Facts

- dirty worktree `feature/codex-apikey-login-interactive` 当前只改了 `docs/system/workspace/scripts/runtime/ai-cli` 和 4 个交互式 login 测试。
- 这组改动做了三件事：
  - 给 `login codex` 增加 interactive auth-mode 选择
  - 给 `login codex apikey` 增加 provider/base-url/api-key 的 prompt 与 `--name/--url/--key` 参数
  - 在采集输入后写 live bundle，并立即保存为 slot
- 已完成 owner `I-20260405T002700Z-A` 明确说明后续 reopen 只针对 bundle/probe-routing/provider-residue regression；interactive login UX 不应伪装成原 owner 的“未完成部分”。
- 这条边界也不属于 `ai-switch-cli` extraction threshold，因为它还只是现有 `ai-cli` 的 bounded UX follow-on，不是抽离 backend 的时机判断。

## Direction

### 1. 交互式 login contract 只解决 first-hop UX，不扩大到底层 auth architecture

- 冻结 `login codex` 的 auth-mode selection
- 冻结 `login codex apikey` 的 prompt/default/direct-arg parity
- 冻结 empty-input/no-mutation failure semantics

### 2. 输入采集与 live bundle materialization 保持绑定，但不扩大为 generic multi-tool login framework

- Codex apikey flow 可以在完成输入后写 live auth/config 并立即保存 slot
- 该 owner 不为其他工具声明 interactive parity
- 该 owner 不顺手抽 `ai-switch-cli` backend

### 3. 与其他 follow-on 分开

- current-live bootstrap without saved-slot inventory 是另一条 owner
- reconnect fast-fail/network classification 是另一条 owner
- interactive login 不应承担 watchdog/bootstrap identity semantics

## Immediate Slice

- 冻结 `login codex` interactive mode selection
- 冻结 `login codex apikey` 的 `provider/base_url/api_key` prompt flow
- 冻结 `--name/--url/--key` 与 interactive defaults 的 parity
- 冻结 empty input failure 和 saved-slot/JSON continuity
- 用现有 4 个测试作为 issue-bound acceptance 的最小起点

## Follow-up Boundary

- 不把本 owner 扩成 current-live bootstrap owner
- 不在本 owner 内做 standalone `ai-switch-cli` extraction
- 不把本 owner 写成通用 “所有工具 interactive login” 的大而化之 contract
