# Tasks: skill 删并的索引兼容期
- issue_id: I-20261111T083905Z-A
- pre_tests_path: docs/B2-docs/skills/skill-merge-compat/raw-20261111T083905Z/verification/pre-tests.md

## 任务分解

- [x] T1: `wt-create --raw-key raw-20261111T083905Z --source platform --kind feature` 建 dev/test 工位；全仓 7567 文件引用普查。
- [x] T2: 判定 4 个低引用候选、按语义分 3 组；写 AT-001（15 静态 + 2 行为）；develop `faab26c14` 基线 RED `2 ok / 15 failed`。
- [x] T3: `skill-map.yaml` 增 `aliases`（4 条）+ `merge_groups`（3 组），删 4 个 skills 条目。
- [x] T4: 三个保留入口追加「## 合并自」章节承接原文、frontmatter `supersedes` 回填；删除 4 个目录（37 → 33）。
- [x] T5: 新增 `bin/skill-route`（名字/alias/loop，0/1/2）；`bin/check-skill-frontmatter` 增 alias 三项校验。
- [x] T6: README 索引移除 retired 行 + 别名迁移说明；AT 接入 `CORE`/`CI_CORE`；epics-map 注册 `skill-merge-compat` story（3 story、其后 +18）。
- [x] T7: GREEN `17 ok / 0 failed`；R28 AT 回归 21/0；lint 33/0；`test-all --ci` 16/0；epics-map 16/211。
- [x] T8: 范围诚实标注「≤25 未达成」，剩余 8 个删并留待重新普查后另立一轮。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity） |
| T3, T4 | AT-001（静态 1–6、10–11） |
| T5 | AT-001（行为 8–9、13–14） |
| T6 | AT-001（静态 12、16–17）+ 回归/CI |
| T7, T8 | 不退化边界与范围标注 |
