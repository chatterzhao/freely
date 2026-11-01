---
pre_brainstorm_id: PB-20261101T231000Z
phase_state: completed
topic: Freely vs DeepSeek Super-agent
created_at: 2026-11-01
---

# B1 预研索引：Freely vs Super-agent

> 状态：completed（研究阶段）。本阶段不 promote、不写实现；下面的“未解”是下一阶段的设计决策，不是未研究的面。每篇文档只负责一个面，避免把结论埋在大文件里。

## 一句话结论

**没有全局更优的系统。** Super-agent 强在“事件 → 准入 → 交接 → 注意力”的运行时；Freely 强在“规格 → TDD → 独立评审 → 合并治理”的交付链。Freely 应保留自己的 SDD/TDD/Reviewer/gates，只借 Super-agent 的运行时协作 primitive。

## 文档地图

| 文档 | 回答什么 | 状态 |
| --- | --- | --- |
| [pre-brainstorm-review.md](pre-brainstorm-review.md) | 独立 B1 评审：verdict、findings、是否进入 candidate | completed |
| [synthesis.md](synthesis.md) | 逐项判定：问题/方案/谁更优/为什么/代价；adopt/adapt/reject | 初稿 |
| [delivery-model.md](delivery-model.md) | B1/B2、SDD/TDD、三角色、阶段评审/PR 评审、3 loop + 2 门禁、工具层 | 初稿 |
| [research.md](research.md) | 理念、五平面、逐维对比、场景判定、实证、取舍 | 初稿 |
| [super-agent-article.md](super-agent-article.md) | IT之家文章四特征/五模块、Router/Worker/Reviewer 映射纠偏 | 初稿 |
| [failure-modes.md](failure-modes.md) | 漏单、重复、越权、交接丢失、缓存误判、文档漂移 | 初稿 |
| [event-admission.md](event-admission.md) | 事件准入放哪层、平台 actor 数据缺口 | 初稿 |
| [state-authority.md](state-authority.md) | 分域真相、字段级单写者、I-* 双解析 | 初稿 |
| [tdd-policy.md](tdd-policy.md) | TDD 强制边界、按改动面分级、全 not_applicable 风险 | 初稿 |
| [attention-metrics.md](attention-metrics.md) | 注意力指标、现有数据采样、最小埋点 | 初稿 |
| [context-cache.md](context-cache.md) | prompt 顺序、ACP 传输、cache 日志、prefix hash 建议 | 初稿 |
| [observability.md](observability.md) | live/fleet/harness 实测、DSH panel/health 对比、只读面 fail-closed | 初稿 |
| [harness-port.md](harness-port.md) | HarnessPort 接口、ACP 四家、DSH adapter 三种模式 | 初稿 |
| [dsh-adapter-decision.md](dsh-adapter-decision.md) | DSH adapter 会阉割什么；B1/B2 两种插件形态 | 初稿 |
| [dsh-freely-plugin-design.md](dsh-freely-plugin-design.md) | Freely-host 插件架构、handoff envelope、迁移/验收 | 初稿 |
| [deployment-forms.md](deployment-forms.md) | Freely 主应用 vs DSH 插件：谁拥有 loop、角色选择、配置真源 | 初稿 |
| [harness-selection.md](harness-selection.md) | 三角色 harness 选择 UI/CLI/TUI、写 agent-table 还是 DSH settings | 初稿 |
| [agent-handoff.md](agent-handoff.md) | Manager/Worker/Reviewer 交接缺陷、A2A/AHP/ACP、DSH delegation 对照 | 初稿 |
| [readme-architecture-audit.md](readme-architecture-audit.md) | README 图为什么改、主图/辅图取舍 | 初稿 |
| [docs-directory-audit.md](docs-directory-audit.md) | 预研目录归位、遗留目录审计与规则 | completed |

## 关键事实（可复核）

1. **B1 不是 SDD，B2 不是 TDD**：B1 产出 candidate（问题规格），B2 产出 I-*/PRD/pre-tests/tasks（SDD/TDD 合同）。
2. **Manager 不做 B1/B2/dev/test**：它巡检、建 raw issue/工位、派工、收口；B1→B2→dev→test 由 Worker 在 skill 下执行。
3. **Reviewer 是阶段评审 + PR 评审**：B1/B2/RED/dev/test 可 `needs-review`，由 watchdog 起独立 session；PR 前 `pr-review-guarded` 再做四问 review。
4. **阶段评审是反馈环，PR 评审是硬门禁**：前者通过 session/prompt 给 Worker；后者由 `pr-merge-guarded` 检查 review 文件，缺失拒绝合并。
5. **Super-agent 没有独立 Reviewer**：文章里的“代码审查评论”是 Trigger；内部实例是“响应 review”。Reviewer 是 Freely 的额外设计。
6. **Router ≈ Manager 只是部分成立**：Manager 还巡检/建工位/收口；Router 不做实现、不管 merge。
7. **状态是分域真相**：docs（规格/生命周期）、A2A（谁在做）、git/worktree（环境）、test-gate（证据）、平台（对外副本）；scan 是派生，不是权威。
8. **I-* 被两套解析器读**：pretests-gate 只认正文 bullet，pr-merge 只认 YAML frontmatter；当前必须双写。
9. **TDD 的 GREEN 硬、RED 软**：pretests-gate 强制终态 green/not_applicable；RED 主要靠 skill；全 not_applicable 只由 skill 约束。
10. **cache 多为估算**：主项目 21 条 `[CACHE]` 全是 estimated、hit/miss=0；Reviewer 的 Cline 是 degraded fork。
11. **MCP 不由 Freely 编排**：ACP 会话传 `mcpServers: []`；可用性取决于底层 CLI。
12. **多项目有 registry，但无统一调度台**：`~/.freely/projects.tsv` 真实存在；`fleet-status` 只是本项目工位视图。
13. **scan 有实测缺陷**：station=收口但 next_action=wt-create/B1；同一 raw 因 dev/test 工位重复；platform_adapter 缺失已有在修工位。
14. **注意力度量缺失**：chats=0、reviews 表空、input-required 4 条；现有数据不足以证明谁更省注意力。
15. **DSH 不做 harness adapter**：那会把 Router/Thread/Mandate 阉割成执行器；插件现实形态是 Source + skill + `freely` CLI，不是全套能力原样插件化。

## 还没研究透

- 状态 schema 与字段级单写者：canonical 格式选 YAML 还是 bullet？phase transition 表由谁维护？
- 事件准入：scan 前/Manager 前/raw issue 创建时？平台 actor/event id 必须先补。
- TDD 分级：`change_surface` 字段、docs-only 替代校验、全 not_applicable 的硬拦截。
- 注意力指标：人工动作数、打断精度、升级率、返工率、漏报率如何采样。
- HarnessPort：fork degraded 是否算 `--require` 满足？DSH adapter 走插件桥还是 Node bridge？
- 多项目：registry 是否要产品化，还是保持单项目深度？
- 当前 PR 的 raw replica 不一致：需要单独收口，不能绕过 pr-create-guarded。

## 非目标

- 不在本阶段 promote candidate、不写新实现。
- 不把 Super-agent 的领域模型整体搬进 Freely。
- 不把当前仓库的 issue/phase/工位状态画进产品架构。

## 交付状态

- 本阶段只提交研究文档，不合并、不保留 PR。
- GitHub PR #4111、Gitee PR #33 均已关闭。
- 研究提交在 `feature/raw-20261101T031502Z-super-agent-collab-study` 分支；B1 独立评审 verdict=`pass-with-gaps`，可起草 candidate，不 merge。
