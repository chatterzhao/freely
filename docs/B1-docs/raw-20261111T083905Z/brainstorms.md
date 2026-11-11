# Brainstorms: 为 skill 删并建索引兼容期并收敛总数

- source_raw: raw-20261111T083905Z（由 R28 / #4164 拆出）
- 覆盖域：引用普查、alias 兼容层、≥2 组删并、supersedes 回填、路由测试、打包验证、总数 ≤25。

## 引用普查（7567 个文件全仓扫描，排除 .git/.freely/安装态）

按「自身目录外引用数」排序，引用最少的四个 skill 只有 `skills/README.md`、
`skill-map.yaml` 与历史 B1/B2 文档引用，**无运行时、hooks、tests 引用**：

| skill | 外部引用 | 主要引用点 |
|---|---|---|
| freely-mem9-continuity-bridge | 3 | README / skill-map / 历史 B1 |
| freely-signal-intent-understanding | 3 | README / skill-map / 历史 B1 |
| freely-tool-cc-codex-mcp-runtime | 3 | README / skill-map / 历史 B1 |
| freely-chat-issue-routing | 4 | README / skill-map / 历史 B1 |

引用高的核心 skill（workflow 138、B2 92、B1 69、dev-loop 57、test-execution 50、
tdd-review 50）**一律不动**；R28 已证伪的三组「重叠」也保持原样。

## 关键判断：不能只删目录

四个候选都有真实知识（mem9 连续性边界、signal 意图收敛、Codex MCP 注册验证、
chat 消息路由）。只删目录 + 指个别名会永久丢知识。因此按语义分三组，把原正文
以「## 合并自」章节并入保留入口：

| 组 | 保留入口 | 删并 skill |
|---|---|---|
| intake-routing | freely-human-interruption-manager-triage | signal-intent-understanding / chat-issue-routing |
| continuity | freely-continuity-watchdog | mem9-continuity-bridge |
| toolchain | freely-ai-cli-availability-manager | tool-cc-codex-mcp-runtime |

## 方案对比

1. 一次性删到 ≤25：会碰核心 skill（引用 50+），风险不可控 → 否决。
2. 只加 alias 不删目录：总数不降，问题没解决 → 否决。
3. 别名兼容期 + 三组语义删并 + 知识并入 + supersedes 回填 + 路由/lint 守护（本轮）→ 采用。

## 范围诚实标注

本轮 37 → **33**（下降 4），完成 **3 组**删并（≥2 组达标）；**「≤25」未达成**。
剩余 8 个的删并需要逐个核对历史引用与运行时行为，按项目惯例另立一轮，
不在本轮用臆测的安全名单硬删。R28 的矩阵/README/lint 契约全部保留并同步。
