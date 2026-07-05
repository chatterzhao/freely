# Brainstorms - 20260401-2245--build-artifact-exposure-and-release-allowlist-capability

## Context

最近这轮安全评审已经收敛出一个明确缺口：

- 原始 product security baseline 已经明确把 `source map`、`artifact exposure`、`secret materialization` 视为 first-class baseline topic。
- 已合并的 security owner 只先收了 default autonomy posture 与 tool policy materialization。
- “用自动化工具和强制流程取代人工记忆和手工操作”是正确方向，但还没有 materialize 成当前 repo 可执行的 capability。

当前 Freely 自身也已经有一个真实、可立即承接的实现面：

- repo 有前端 build 输出 `dist/`
- Tauri build 会消费 `dist/`
- `doctor` 目前还没有任何 build artifact / source-map / secret exposure audit
- 当前 build 脚本也没有强制 release allowlist 或 build-output forbidden-artifact scan

这使得“开发阶段默认方便”与“release-facing output 不应外发敏感/调试工件”之间仍然依赖人工记忆，而不是被 Freely 自动拦住。

## Problem

当前缺少一条 narrow capability owner，专门回答：

1. 哪些 build / release-facing artifacts 绝不能进入输出面。
2. 哪些输出文件必须显式在 allowlist 中声明，否则默认不准带出。
3. 哪些环境差异应由构建配置直接隔离，例如 production sourcemap 默认关闭。
4. 这些检查应如何进入 `doctor` / build 脚本 / CI，而不是停留在“记得检查一下”。

如果不把这条能力先落成最小 slice，剩余 security baseline 仍会继续依赖：

- 人工记忆哪些文件不能发
- 人工肉眼检查 `dist/`
- 人工确认 production build 没把 source map 带出去

## Boundary

本条只处理 build artifact exposure 的第一刀，不一次吞掉全部 security baseline。

本条应回答：

1. forbidden artifact scan 的最小默认集合是什么。
2. release allowlist 的最小真源应该落在哪里。
3. `doctor` 是否应把这类问题作为 baseline gate。
4. 当前 repo 的 build 脚本是否应自动执行这类审计。

本条不处理：

1. supply-chain minimum package age / provenance 的完整策略
2. runtime secret scanning 的全量能力
3. 生产发布平台专有的 SaaS 集成
4. incident remediation automation 的完整闭环

## Working Direction

先收一个最小 capability slice：

1. 新增可复用的 build artifact exposure audit 脚本
   - 扫描 `dist/` 之类输出目录
   - 发现 `.map`、`.env*`、密钥/证书类文件、常见 secret artifact 时直接失败
2. 引入 repo-scoped release allowlist
   - 输出文件若不在 allowlist，默认失败
   - 不靠“构建完人工看一眼”
3. 把这条审计接入 `freely doctor`
   - `doctor` 从文档/hook gate 扩成第一条 security baseline audit
4. 当前 repo 的 `build` 脚本自动执行这条审计
   - 让 build / Tauri build 默认携带这条 gate
5. 显式写出 production build 的 source-map posture
   - 不是依赖 Vite 默认值碰巧正确

## Relation To Broader Security Work

这条 owner 是 wider security baseline 的一个 sibling slice，不回灌：

- `I-20260401T130300Z-A` default autonomy posture
- `I-20260401T130300Z-A-2` tool materialization
- `I-20260401T130800Z-A` execution-boundary review and security decision support

它更接近：

- secret / artifact exposure capability 的第一条 materialization
- “automation + enforced workflow over operator memory” 的第一条可执行证明

## Open Questions

1. allowlist 真源应只用于当前 repo，还是设计成将来可复用 contract
2. forbidden patterns 是否先收窄成明显高风险文件，再逐步扩展
3. `doctor` 应在没有 `dist/` 时跳过，还是要求显式说明构建输出位置
4. 后续是否拆出独立的 source-map / public artifact capability，而不是继续堆到一个 audit 脚本中
