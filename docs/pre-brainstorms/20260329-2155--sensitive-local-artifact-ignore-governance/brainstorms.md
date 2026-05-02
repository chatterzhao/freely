# Brainstorms - 20260329-2155--sensitive-local-artifact-ignore-governance

## Context

`2026-03-29` 在 `develop` 根目录发现了一个未跟踪的 `auth.json`。它不是测试夹具，也不是 Freely 正常运行应产生的仓库内产物，而是带真实授权结构的本地凭证文件。

已确认事实：

- `git status --short` 只显示一个未跟踪文件：`auth.json`
- 文件结构包含：
  - `OPENAI_API_KEY`
  - `tokens.access_token`
  - `tokens.id_token`
  - `tokens.refresh_token`
- Freely 当前账号真源约定在：
  - `$HOME/.codex/auth.json`
  - `$HOME/.ai-auth/codex-*/auth.json`
- 仓库当前 `.gitignore` 没有任何规则会忽略根目录 `auth.json` 或其他常见敏感凭证文件名

这说明当前缺口不是“某个文件不小心没删掉”，而是仓库缺少一层针对本地敏感文件误落的最低保护。

## Reproduced Facts

### 1. `develop` 确实出现过仓库根敏感文件

根目录 `auth.json` 已被实际观察到，并且在删除前是唯一未跟踪文件。

### 2. 当前忽略规则没有保护这类文件

`git check-ignore` 对以下路径都没有命中：

- `auth.json`
- `.npmrc`
- `foo.pem`

因此只要这些文件误落到仓库里，它们就会作为普通未跟踪文件暴露给 `git status`，并存在被误加进提交的风险。

### 3. 仓库内当前没有已跟踪的证书/私钥夹具与本提案冲突

对以下常见敏感文件名/扩展名做了仓库扫描：

- `auth.json`
- `secrets.json`
- `credentials.json`
- `.npmrc`
- `.pypirc`
- `id_rsa`
- `id_dsa`
- `id_ecdsa`
- `id_ed25519`
- `*.pem`
- `*.key`
- `*.p12`
- `*.pfx`
- `*.crt`
- `*.cer`
- `*.der`
- `*.csr`

当前仓库没有命中结果。这意味着本轮最小忽略保护不会立刻遮住现有已跟踪资产。

## Problem

Freely 当前对本地敏感文件的防护只覆盖了 `.env*` 一类环境变量文件，没有覆盖：

- 误落到仓库根的账号凭证文件
- 常见证书/私钥扩展名
- 常见包管理器或账号工具的本地认证文件

在 Freely 这种会频繁执行本地账号切换、登录、工具自举的仓库中，这类误落不是理论风险，而是已经出现过的现场事实。

## Boundary

本条研究只处理：

1. 仓库级别的最低敏感文件忽略保护
2. 误落到本地仓库中的常见凭证/私钥文件名
3. 一个可验证的 ignore contract

本条不处理：

1. 登录流程为什么会把文件写到错误目录
2. 账号凭证真实存储架构 redesign
3. 历史已提交 secrets 的清理审计
4. 一切可能包含敏感内容的文件类型的无限扩张式黑名单

## Root Cause Hypothesis

当前更深层的缺口是仓库对“本地开发工具会产生敏感副产物”这件事缺少治理表达：

- `.env*` 被明确视为不应提交
- 但 `auth.json`、证书、私钥等同类高风险本地文件没有同等级别的默认保护

也就是说，问题不是某个账号命令今天偶然写错，而是仓库没有把“敏感本地产物误落”定义成一条能力/治理 contract。

## Proposed Direction

第一阶段应采用保守且可解释的策略：

1. 先忽略最常见、最危险、最容易误落的文件名和扩展名
2. 保持模式尽量窄，不去一口气忽略整类业务目录
3. 如果未来测试需要跟踪证书/密钥夹具，使用显式 `!` 规则或专门 fixture 路径来恢复，而不是默认裸奔
4. 同时补一个 focused regression，锁住这些路径应被 `git check-ignore --no-index` 命中

## Initial Decision

这条线值得 materialize 成独立 issue，原因是：

1. 现场已经出现真实敏感文件误落
2. 缺口可以用很小的治理和实现切口修复
3. 它与账号登录、slot 管理、runtime 恢复等问题正交，不应混入其他 owner issue
4. 修复可以做到低风险且可测试
