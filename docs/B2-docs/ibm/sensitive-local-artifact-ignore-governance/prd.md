# PRD: sensitive-local-artifact-ignore-governance

## Problem

Freely 当前仓库会忽略 `.env*`，但不会忽略真实世界常见的本地敏感副产物，例如根目录 `auth.json`、常见包管理器认证文件，以及私钥/证书扩展名。现场已经出现过一次真实 `auth.json` 误落到 `develop` 根目录，说明这不是假设风险。

## Product Decision

第一阶段只冻结一个最小 contract：

1. 忽略最常见的根目录本地凭证文件名。
2. 忽略常见私钥/证书扩展名。
3. 保持规则尽量窄，不额外扩大到目录黑名单或敏感内容扫描器。
4. 用 focused regression 锁住 ignore 行为。

## User Value

- 降低误把本地凭证加进 Git 的概率
- 减少 `git status` 暴露敏感副产物的机会
- 给 Freely 这种高频本地工具自举仓库补上最低安全护栏

## Acceptance Narrative

当本地工具、登录流程或人工操作把常见凭证/私钥文件误落到仓库里时，Git 默认应将其视为 ignored，而不是普通未跟踪文件。与此同时，正常源码与文档路径不能被误伤；未来若确实需要跟踪证书夹具，应通过显式例外恢复。
