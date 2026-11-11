---
candidate_id: C-20261111T083905Z-A
status: promoted
source_raw: raw-20261111T083905Z
created_at: 2026-11-11
milestone: M-20261111T083905Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261111T083905Z-A: skill 删并的别名兼容期（第一阶段）

- candidate_format_version: v2
- title: 引用普查 + alias 兼容层 + 3 组语义删并（37→33）+ supersedes 回填 + 路由/lint 守护
- status: promoted
- decision_reason: 四个候选 skill 无运行时引用且语义可归入三个保留入口；只删目录会丢知识，因此以「合并自」章节承接原文并保留 alias 解析，给历史引用一个可机检的兼容期。
- next_action: AT-001（16 静态 + 2 行为）→ develop `faab26c14` 基线 RED `2 ok / 16 failed` → 实现 → GREEN `18 ok / 0 failed` → R28 AT 回归 21/0 + CI 16/0 → PR。
- revisit_trigger: 剩余 8 个删并（目标 ≤25）需重新做引用普查，不得照抄本轮名单；删并时同步 routing / aliases / supersedes / README / epics-map。
- acceptance_criteria:
  - RED：无 aliases 段、无 `bin/skill-route`、4 个目录仍在、supersedes 全空、README 仍列全、lint 不校验 alias、AT 未进 CI、epics-map 无 story。
  - GREEN：4 个 retired 名字各有 alias 指向存在的保留入口；retired 名字不再出现在 matrix skills；4 个目录消失；skill 总数下降且 ≤35。
  - GREEN：`bin/skill-route` 能把每个 alias 解析到入口、能按 loop 返回 routing 入口。
  - GREEN：3 个保留入口 frontmatter 的 `supersedes` 回填对应 retired 名字；SKILL.md 有「## 合并自」章节并含原文。
  - GREEN：README 索引不再列 retired skill 且有别名迁移说明；lint 拒绝悬空 alias、接受合法 alias；可执行真源（AGENTS/.githooks/bin/agents/hooks）无 dangling 引用。
  - GREEN：AT 进 CORE/CI_CORE；epics-map 注册 story；R28 AT 21/0、`test-all --ci` 16/0。
  - 不退化：workflow 全链路、RED→dev→GREEN 三阶段、dispatcher 三条 claim 路径、`runtime/freely` 均不变；核心高引用 skill 一个不删。
- promotion_gate: AT-001 RED → GREEN + R28 AT 回归 + CI + epics-map 对齐
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 全仓 7567 文件扫描引用分布；逐个读 4 个候选 SKILL.md 确认有真实知识；用 `git archive develop` 快照复现 RED；用临时 fixture 验证 lint 对悬空/合法 alias 的退出码。
  - verdict: pass
- promoted_issue_id: I-20261111T083905Z-A
- promoted_issue_path: docs/B2-docs/skills/skill-merge-compat/raw-20261111T083905Z/issues/I-20261111T083905Z-A.md
- milestone: M-20261111T083905Z-A
- session_refs: []
