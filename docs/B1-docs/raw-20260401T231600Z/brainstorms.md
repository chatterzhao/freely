# Brainstorms - 20260401-2316--cc-acp-init-autonomy-consent-test-followthrough

## Context

`develop` 上已经把默认高自治和 tool materialization contract 冻结到 product truth：

- `cc:auto` init 现在默认要求显式 activation consent
- `cc` 允许配置 `--tool-adapter acp`
- focused test `test-freely-init-cc-config` 本来就是这条 contract 的回归锁

但 canonical `develop` 上这条测试仍保留了旧调用形态：`cc:auto + --tool-adapter acp` 路径没有补上 `--accept-default-autonomy`。结果不是 runtime contract 错，而是测试夹具没有跟随已经 canonical 的 activation-consent contract 更新。

## Problem

当前缺口非常窄：

1. `test-freely-init-cc-config` 在 `cc:auto + adapter=acp` 这条 init 路径上仍按旧前提调用。
2. develop-bound merge hook 不允许直接把这类 completed-family followthrough 当作“无 owner 的小修”；它要求新的 candidate / issue 生命周期，并记录 reopen 来源。
3. 如果不补最窄 reopen owner，这条一行修复会一直被 merge gate 拦住，哪怕修复本身已经正确。

## Boundary

本条只处理：

1. `cc:auto + --tool-adapter acp` init 夹具补齐 `--accept-default-autonomy`
2. 为这条修复补齐最小 candidate / milestone / issue / progress / verification writeback
3. 明确这是一条已冻结 contract 的测试对齐，不是重新协商 runtime 语义

本条不处理：

1. `freely init` runtime 行为改写
2. ACP adapter 新能力
3. broader security-review capability
4. `cc` / `cc-use-codex-cli` 更广义 materialization contract 扩展

## Working Direction

1. 新开一条 narrow follow-on lifecycle，而不是改写已收口 owner。
2. 挂回 `I-20260401T130300Z-A-2` 这一家族，因为缺口属于 tool autonomy policy materialization 的已冻结 activation-consent contract。
3. 让 owner 直接处于 `in_verification`：
   - 代码只是一行测试修复
   - focused test 与 `governance-check` 即可形成 feature-lane verification
4. merge 进 `develop` 后再把这条 follow-on closeout 掉，不反向扩大原 owner。

