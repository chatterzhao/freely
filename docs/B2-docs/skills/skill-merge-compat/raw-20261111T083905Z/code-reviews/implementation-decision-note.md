# Implementation Decision Note
- issue_id: I-20261111T083905Z-A
- issue_path: docs/B2-docs/skills/skill-merge-compat/raw-20261111T083905Z/issues/I-20261111T083905Z-A.md
- decision: 全仓引用普查后按语义分 3 组删并 4 个低引用 skill（37→33），用 `skill-map.yaml` 的 aliases/merge_groups 建索引兼容期，原正文以「## 合并自」章节并入保留入口，supersedes 回填，新增 `bin/skill-route` 与 lint alias 校验，README/AT/epics-map 同步。
- why_this: 直接删目录会永久丢失 mem9 边界、signal 意图、Codex MCP 配置、chat 路由四份知识，也会让历史引用悬空；别名兼容期让名字仍可解析，知识不丢，且每一点都能被 lint 与 AT 机检。
- alternatives_considered: ①一次删到 ≤25——剩余候选引用数迅速上升且含核心 skill，风险不可控；②只加 alias 不删目录——总数不降，没解决问题；③把原正文压缩成一句摘要再删——知识失真，无法追溯。
- boundary_non_goals: 不删任何引用数 ≥5 的 skill；不改 R28 判定的三组分工；不改 workflow 全链路 / TDD 三阶段 / dispatcher claim 路径；不改 `runtime/freely`；不批量改写历史 B1/B2 文档中的研发留痕引用。
- residual_risk: ①总数 33 未达 ≤25，剩余 8 个需重新普查后另立一轮；②合并章节原文照搬未去重；③alias 目标若再被删并，lint 会抓到但需人工决定新落点；④安装态下降由 followthrough 打包验证，本轮不改打包白名单。

## 为什么是这 4 个

全仓 7567 文件扫描「自身目录外引用」后，这 4 个引用数 3–4 且引用点只有
README / skill-map / 历史 B1，无运行时、hooks、tests 引用；其余 skill 引用数
≥5 且包含 `AGENTS.md.example`、CONSTITUTION、LAWS、agents 配置或专门测试。
删并名单由扫描结果决定，不是凭印象挑选。

## 补记：references 语料一并承接

提交前发现 `freely-tool-cc-codex-mcp-runtime/references/` 另有 4 份参考文档，只搬 SKILL.md 会丢知识；已以 `merged-*.md` 搬入保留入口 `freely-ai-cli-availability-manager/references/`，并新增 AT 断言守护（否则删并后无人发现）。
