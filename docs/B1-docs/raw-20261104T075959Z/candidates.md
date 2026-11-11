---
candidate_id: C-20261104T075959Z-A
status: promoted
source_raw: raw-20261104T075959Z
created_at: 2026-11-11
milestone: M-20261104T075959Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T075959Z-A: skill 重叠矩阵 + frontmatter 契约 + fail-closed lint

- candidate_format_version: v2
- title: `skill-map.yaml` 单一真源 + 37 份 `loop`/`owner`/`supersedes` frontmatter + lint + 路由测试
- status: promoted
- decision_reason: 37 个 skill 没有机器可读的路由真源，agent 只能逐个读 SKILL.md 猜入口；同时「三组重叠」经普查是分工而非重复，直接删并会破坏 dispatcher 与 TDD 顺序。先用零语义变化的契约把路由固定下来，删并另立 raw。
- next_action: AT-001（19 静态 + 2 行为）→ develop `49958c1d9` 基线 RED `0 ok / 21 failed` → 实现 → 工位 GREEN `21 ok / 0 failed` → 回归 + CI → PR。
- revisit_trigger: 若后续删并型 raw 落地，`skill-map.yaml` 的 `routing` / `overlap_groups` / `supersedes` 必须随删除同步，lint 的孤儿检查会抓到。
- acceptance_criteria:
  - RED：无 `skill-map.yaml`、无 lint、37 个 frontmatter 无 `loop`/`owner`/`supersedes`、重复枚举措辞仍在、AT 未进 CI、epics-map 无 story。
  - GREEN：矩阵覆盖全部 37 个 skill（无遗漏无孤儿），每个条目含 loop/owner/inputs/outputs/triggers。
  - GREEN：三组重叠各有合法 `decision` / `entrypoint` / `reason`；12 个 loop 各有唯一路由入口。
  - GREEN：每个 SKILL.md frontmatter 含 `loop`/`owner`/`supersedes` 且与矩阵逐条一致、值来自枚举。
  - GREEN：`bin/check-skill-frontmatter` 对缺字段 rc≠0、对合规 fixture rc=0、对缺失真源 rc=2；真实语料 37/0。
  - GREEN：能力目录 `docs/system/workspace/` 下 `从 gate 源码提取` 为 0；AT 进 `CORE`/`CI_CORE`；epics-map 注册 story。
  - 不退化：不删任何 skill、不改 skill 正文语义、不改 workflow 全链路顺序、不改 `runtime/freely` 一行。
- promotion_gate: AT-001 RED → GREEN + `bin/test-all --ci` 15/0 + `check-epics-map` 对齐
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐个读三组 9 个 SKILL.md 的 description 与职责，核对 workflow 全链路；用 `git archive develop` 快照注入最终版 AT 复现 RED；用临时 fixture 验证 lint 的 refuse/accept 行为。
  - verdict: pass
- promoted_issue_id: I-20261104T075959Z-A
- promoted_issue_path: docs/B2-docs/skills/skill-overlap-matrix/raw-20261104T075959Z/issues/I-20261104T075959Z-A.md
- milestone: M-20261104T075959Z-A
- session_refs: []
