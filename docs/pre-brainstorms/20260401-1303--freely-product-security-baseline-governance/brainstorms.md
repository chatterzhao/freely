# Brainstorms - 20260401-1303--freely-product-security-baseline-governance

## Context

近期开发链路安全事件已经从“某个依赖有 CVE”转向“发布身份、CI tag、install hook、agent 外连、源码暴露面”被直接利用。

对 Freely 自身而言，这不是单纯的用户项目建议，而是产品默认安全基线缺口：

- `init` 目前主要负责项目注册、AI 规格和 hooks 初始化
- `doctor` 目前只覆盖文档门禁和 hook 门禁
- runtime 已经有网络代理、watchdog、slot/tool 编排等能力，但没有独立的 security baseline contract

最近对话中已经收敛出的高优先级缺口包括：

1. 凭证治理不能只看“是否被 git 跟踪”
2. 依赖安全不能只看“固定版本号”
3. 供应链策略需要考虑 minimum package age、provenance、GitHub Actions 可变 tag、install script
4. source map / 调试工件即使不进 git，也可能通过打包、静态托管、预览目录、runtime 产物或工具副产物外流
5. AI agent / MCP / Claude Code / Codex 这类执行面需要默认最小权限，而不是让每个项目临时发明自己的安全姿势

## Existing Governance To Reuse

已有最接近的前史是：

- `docs/pre-brainstorms/20260329-2155--sensitive-local-artifact-ignore-governance/**`
- `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/**`

这条线已经证明：

- Freely 仓库里真实出现过敏感本地产物误落
- 当前治理可以承接“最小默认保护”这一类问题
- 但它只覆盖 narrow ignore contract，不覆盖更高层的 security baseline

另有可复用输入：

- project-scoped proxy / launcher inheritance 已经是已完成能力
- `tool-cc-codex-mcp-runtime` 已经定义了工具接入策略
- `url-content-intake` 说明了外部内容抓取类能力可沉淀成 skill

## Problem

Freely 自身现在缺少一层明确的产品级安全默认值，导致以下判断容易散落在对话里而不是进入 canonical truth：

1. 什么安全检查必须在 `init` 时落默认配置
2. 什么安全检查必须在 `doctor` 时变成 baseline gate
3. runtime 默认应限制哪些外部访问、工具权限、输出落盘行为
4. 哪些风险属于 Freely 自身产品治理，而不是交给单个 repo 的 ad hoc 习惯

## Boundary

本条预研只讨论 Freely 自身产品治理和默认基线，不直接定义独立可复用 skill 的完整执行细节。

本条应优先回答：

1. Freely 自身应内建哪些默认安全 contract
2. 它们更适合落在 `init`、`doctor`、runtime config、hooks、还是 status surface
3. 哪些只需要 warning，哪些应该 gate

本条不直接处理：

1. 具体某个 security skill 的详细工作流
2. 外部生态全量 threat intelligence ingestion
3. 历史所有 secrets / artifacts 的回溯清理

## Working Hypothesis

Freely 自身至少应形成四块 baseline：

1. secret materialization baseline
   - tracked / staged / untracked 高风险路径
   - runtime 日志、continuity、prompt、artifact 的敏感内容约束

2. dependency and release baseline
   - lockfile / immutable pin / minimum package age
   - provenance / trusted publishing / install script 风险

3. artifact exposure baseline
   - source map
   - 调试符号
   - 不应外发的 build side products

4. agent execution baseline
   - 网络最小权限
   - MCP / tool approval / domain allowlist
   - 外部内容到工具调用之间的 trust boundary

## Initial Direction

优先把 Freely 自身产品面的安全默认值冻结为：

- `init` 负责写入默认安全配置与最小忽略/模板
- `doctor` 负责做 baseline security audit
- runtime 负责执行时最小权限
- `baseline-status` / `live-status` 负责暴露关键安全 posture，而不是把它藏在内部脚本

## Open Questions

1. minimum package age 应该是 Freely 全局默认，还是 per project override
2. source map 应只做 warning，还是对 production-facing output 做 hard gate
3. secret 扫描应只扫描文件系统，还是也扫描 runtime 产物与 continuity artifacts
4. agent 网络权限应默认为 deny-all 还是 allow-minimal
