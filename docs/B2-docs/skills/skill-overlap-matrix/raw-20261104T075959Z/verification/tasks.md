# Tasks: skill 重叠矩阵与 frontmatter 单一契约
- issue_id: I-20261104T075959Z-A
- pre_tests_path: docs/B2-docs/skills/skill-overlap-matrix/raw-20261104T075959Z/verification/pre-tests.md

## 任务分解

- [x] T1: `wt-create --raw-key raw-20261104T075959Z --source platform --kind feature` 建 dev/test 工位；普查 37 个 skill、frontmatter 现状、1 处重复枚举措辞、`epic-skills` 结构。
- [x] T2: 前置评审证伪三组「重叠」（实为阶段/owner 分工）；按 AGENTS.md 仓库分层修正验收标准 4 的自指矛盾；写 AT-001（19 静态 + 2 行为）。
- [x] T3: develop `49958c1d9` 基线 RED `0 ok / 21 failed`（`git archive` 快照 + 最终版 AT）。
- [x] T4: `skill-map.yaml`：37 条 loop/owner/输入输出/触发词、3 组重叠判定、12 个 loop 唯一路由入口；JSON 兼容 YAML 1.2 子集。
- [x] T5: 37 个 SKILL.md 注入 `loop`/`owner`/`supersedes: []`；新增 `bin/check-skill-frontmatter`（0/1/2）。
- [x] T6: 消除 B2 skill 里重复的 gate 枚举标题，改为引用 `pretests-gate` 真源；AT 接入 `CORE`/`CI_CORE`。
- [x] T7: `docs/epics-map.svg` 的 `epic-skills` 注册 `skill-overlap-matrix` story（其后 epic 整体 +26）；GREEN `21 ok / 0 failed`、`test-all --ci` 15/0。
- [x] T8: 删并型重构（≥2 组合并、总数 ≤25）证伪后用 `freely feedback` 新建 raw 并排入 goal 队列，不夹带进本 PR。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2, T3 | AT-001（RED fidelity） |
| T4 | AT-001（静态 1–8、16） |
| T5 | AT-001（静态 9–15、行为 20–21） |
| T6, T7 | AT-001（静态 17–19）+ 回归/CI |
| T8 | 另立 raw（goal 队列） |
