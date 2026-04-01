# Brainstorms - 20260401-1308--workspace-security-capability-baseline-governance

## Context

与 Freely 自身产品治理并行，还存在另一条能力面问题：

如果 Freely 最终要把这套安全治理提供给 Freely runtime / agent / skills / CLI 长期消费，那么仅靠 `init` / `doctor` 的内建逻辑不够，还需要可复用的安全能力单元。

当前仓库里已有的能力形态包括：

- `tool-cc-codex-mcp-runtime`
- `url-content-intake`
- `watchdog-control-plane`
- `workspace-skill-governance`

这说明 Freely 已经接受“稳定、可复用、会被长期消费的工作流应该进入能力目录”的模式。

## Problem

目前没有一组统一的 security capability contracts 来处理以下工作：

1. 供应链 intake 审计
2. 依赖/Action pin、minimum age、provenance 检查
3. secret / artifact exposure 审计
4. source map / build side-product 暴露检查
5. agent prompt injection / MCP / external content trust-boundary 评估
6. 事件发生后的 credential rotation / cleanup / verification 指引

如果这些能力全部硬塞进 runtime：

- runtime 变成难以演化的大杂烩
- 不同场景无法按需复用
- 用户项目也难以显式调用或 override

## Boundary

本条预研只处理 Freely 的可复用安全能力面，不定义 Freely 自身产品默认是否启用这些能力。

本条应回答：

1. 哪些安全问题适合成为独立 skill
2. 哪些能力更适合作为 scripts + skill references
3. 能力之间的最小拆分应该是什么

本条不处理：

1. Freely 自身 `init/doctor` 最终默认策略
2. 单个具体事件的完整 incident response 文档
3. 外部 SaaS 平台绑定的专有工作流

## Initial Capability Families

### 1. Supply-chain audit

- package lock / pin completeness
- GitHub Actions mutable tag detection
- minimum package age policy
- install hook / postinstall risk detection
- provenance / trusted publishing checks

### 2. Secret and artifact exposure audit

- tracked / staged / untracked secret scanning
- runtime artifact scanning
- source map / debug artifact scanning
- static/public/release directory exposure checks

### 3. Agent execution safety

- prompt injection / untrusted content boundary checks
- MCP trust policy and tool invocation guardrails
- network allowlist / denylist posture checks

### 4. Response and remediation

- credential rotation checklist
- cleanup and re-validation path
- focused regression hints after remediation

## Candidate Skill Shape

一个可行的最小拆分是：

- `skill:supply-chain-audit`
- `skill:secret-and-artifact-exposure-audit`
- `skill:agent-execution-safety-audit`
- `skill:security-incident-remediation`

也可以先收成一个聚合入口，再逐步细分，但不应一开始就让一个超大 skill 同时承担发现、判断、修复、验证全部职责。

## Relation To Existing Governance

这条线应吸收但不重复：

- `sensitive-local-artifact-ignore-governance` 的现场事实
- `project-scoped-network-proxy-configuration-and-launcher-inheritance-governance` 的网络配置真相
- `tool-cc-codex-mcp-runtime` 的工具接入约束
- `url-content-intake` 的“外部内容进入系统能力前应先经过专门 intake”模式

## Open Questions

1. source map 审计应归到 secret/artifact skill，还是独立 build-exposure skill
2. incident remediation 是否应保持纯文档/清单型 skill，还是允许带自动修复脚本
3. agent execution safety 是否需要先沉淀为 references，再升格成独立 skill
