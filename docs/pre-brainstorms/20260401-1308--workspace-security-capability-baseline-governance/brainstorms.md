# Brainstorms - 20260401-1308--workspace-security-capability-baseline-governance

## Context

与 Freely 自身产品治理并行，还存在另一条能力面问题：

如果 Freely 最终要把这套安全治理提供给 Freely runtime / agent / skills / CLI 长期消费，那么仅靠 `init` / `doctor` 的内建逻辑不够，还需要可复用的安全能力单元。

本轮还应明确与产品 lane 的分工：

- Freely 默认仍按免交互、自动批准实现
- “是否允许交互批准”不是本条要设计的默认主路
- 本条能力面主要服务于检测、复核、解释、建议与决策增强，而不是重新把用户拉回逐步批准链路
- 主目标是提升 owner-grade AI autonomy 的可信度，而不是削弱自治本身
- 本条也不把 safeguard completeness 当作默认阻塞条件；能力面主要帮助 runtime 更好地提示、建议、评估、复核并继续推进

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
5. 执行边界、自动批准、网络和可写范围 posture 检查
6. agent prompt injection / MCP / external content trust-boundary 评估
7. 事件发生后的 credential rotation / cleanup / verification 指引

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
4. product-facing consent 文案本身的最终 owner

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
- downstream tool runtime flags versus actual execution-boundary verification
- project-local tool config versus launch-time injected policy verification
- safeguard recommendation helpers for non-interactive runtime decisions
- security review helpers for non-interactive runtime decisions

### 4. Security decision support

- one or more security-focused subagents review current posture and detected risks
- produce risk summaries and suggested Freely policy / adapter adjustments
- support a “decision committee” style internal review when a single agent should not decide alone
- write back canonical review evidence without replacing product-owned consent surfaces
- help the runtime continue through an internal decision ladder before falling back to minimal-risk stop
- when safeguards are missing, prefer producing clearer recommendations, boundary assessments, and reviewer-backed continuation guidance before concluding that runtime must stop

### 5. Response and remediation

- credential rotation checklist
- cleanup and re-validation path
- focused regression hints after remediation

## Candidate Skill Shape

一个可行的最小拆分是：

- `skill:supply-chain-audit`
- `skill:secret-and-artifact-exposure-audit`
- `skill:agent-execution-safety-audit`
- `skill:security-decision-support`
- `skill:security-incident-remediation`

也可以先收成一个聚合入口，再逐步细分，但不应一开始就让一个超大 skill 同时承担发现、判断、修复、验证全部职责。

## Relation To Existing Governance

这条线应吸收但不重复：

- `sensitive-local-artifact-ignore-governance` 的现场事实
- `project-scoped-network-proxy-configuration-and-launcher-inheritance-governance` 的网络配置真相
- `tool-cc-codex-mcp-runtime` 的工具接入约束
- `url-content-intake` 的“外部内容进入系统能力前应先经过专门 intake”模式

这些能力后续还需要回到 `docs/system/workspace/three-loop-capability-lifecycle.md` 说明其 loop owner 与消费位置，避免只列 skill 名而不落 owner truth。

这里还应保持一个原则：

- security capability 的目标是让 runtime 更会判断、更会复核、更会继续推进
- 不是把“遇到风险就停”固化成默认产品行为
- 也不是把“未满足所有安全建议”误判成默认不可运行；推荐 safeguard 是支持面，不是默认前置门槛

## Open Questions

1. source map 审计应归到 secret/artifact skill，还是独立 build-exposure skill
2. incident remediation 是否应保持纯文档/清单型 skill，还是允许带自动修复脚本
3. agent execution safety 是否需要先沉淀为 references，再升格成独立 skill
4. security decision support 应是独立 skill，还是作为 agent-execution-audit 的固定子流程
