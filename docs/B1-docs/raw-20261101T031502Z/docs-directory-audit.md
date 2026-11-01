---
audit_id: DIR-20261101T031502Z
phase_state: completed
created_at: 2026-11-01
---

# 文档目录审计：预研该放哪、还有哪些遗留目录

## 0. 结论

- **`docs/pre-brainstorms/` 是废弃遗留目录**，本轮已删除；研究文档已迁到 `docs/B1-docs/raw-20261101T031502Z/`。
- 原 `docs/pre-brainstorms/20260720T055358Z--wt-create-silent-exit/` 的 `brainstorms.md`/`candidates.md` 已迁到它对应的 `docs/B1-docs/raw-20260720T055358Z/`。
- 顶层 docs 目录现在只剩：`assets/`、`B1-docs/`、`B2-docs/`、`system/`，以及 `CONSTITUTION.md`、`LAWS.md`、`PROJECT_INTENT.md`、`milestones.md`、`epics-map.svg`。
- 仓库根目录 `code-reviews/` 也是遗留目录；本轮已移除。
- **B1 下不应有 `code-reviews/`**；本轮把 B1 的两个 review 都迁到 B2，B1 只保留 brainstorms/candidates/研究。
- 仍存在两类“看起来像遗留”的目录，但性质不同：一类是显式归档（`_legacy`），一类是历史路径仍被引用，不能直接搬。

## 1. 本轮修复

| 原路径 | 新路径 | 动作 |
| --- | --- | --- |
| `docs/pre-brainstorms/20261101T231000Z--freely-vs-super-agent/*` | `docs/B1-docs/raw-20261101T031502Z/*` | 16 个文件迁入 B1 raw 目录；`README.md`→`research-index.md`，`b1-review.md`→`pre-brainstorm-review.md` |
| `docs/pre-brainstorms/20260720T055358Z--wt-create-silent-exit/brainstorms.md` | `docs/B1-docs/raw-20260720T055358Z/brainstorms.md` | 历史 B1 文档归位 |
| `docs/pre-brainstorms/20260720T055358Z--wt-create-silent-exit/candidates.md` | `docs/B1-docs/raw-20260720T055358Z/candidates.md` | 历史 B1 文档归位 |
| `docs/pre-brainstorms/` | 删除 | 已空，废弃目录移除 |
| `code-reviews/pr-review-raw-20260701T030358Z.md` | `docs/B2-docs/ibm/_legacy-issues/raw-20260701T030358Z/code-reviews/pr-review-raw-20260701T030358Z.md` | 无 active B2 story 的 legacy review，归 B2 `_legacy-issues` 的 raw；根目录 `code-reviews/` 删除 |
| `docs/B1-docs/raw-20260710T171329Z/code-reviews/pr-review-raw-20260710T171329Z.md` | `docs/B2-docs/config/test-gate/env/raw-20260710T171329Z/code-reviews/pr-review-raw-20260710T171329Z.md` | B1 误放；对应 B2 issue 已存在，review 归该 raw 的 `code-reviews/` |

## 2. 仍需保留/单独处理的历史目录

| 路径 | 性质 | 判断 | 建议 |
| --- | --- | --- | --- |
| `docs/B2-docs/ibm/_legacy/` | 显式归档（2.5M） | 有意保留的历史迁移归档 | 不搬；如要清理，单独开 issue |
| `docs/B2-docs/ibm/_legacy-issues/` | 显式归档（2.0M） | 旧 I-* issue 归档 | 不搬；新 issue 不再写入 |
| `docs/B2-docs/config-toml-complete/` | 顶层旧 story 残留（仅 1 个 review 文件） | 内容已归档到 `_legacy/raw-MIGRATED-config-toml-complete`，但历史 issue 的 `verification_artifact_dir` 仍指向它 | **冻结**；不要直接搬，先做路径重写 issue |
| `docs/B2-docs/config/test-gate/env/raw-20260710T171329Z/` | 比 canonical 多一层 `env` | 自身引用一致，但不符合 `{epic}/{story}/raw-*` 深度 | **标记**；不搬，等 owner 确认是否 story 分组 |
| `docs/B1-docs/.scan-state` | runtime 扫描状态（未跟踪） | 不是文档目录 | 不提交，不迁移 |
| `docs/B1-docs/raw-20260701T030358Z/issue.md` | 历史 metadata 异常 | `local_id`/`absorbed_into` 多了 `58Z`，phase=`dropped` 且无 B2 I-*；review 仍属该 raw | **只记录，不顺手改**；如影响 scan，单独开 issue 修 metadata |

### 2.1 B1 内仍存在的非 canonical 目录

| 路径 | 性质 | 判断 |
| --- | --- | --- |
| `docs/B1-docs/raw-20260303T000000Z/` | 旧 pre-brainstorm 命名（无 issue.md），被 4 处历史文档引用 | 不重命名；重命名需 path rewrite issue |
| `docs/B1-docs/raw-20260503-0000/`、`raw-20260503/`、`raw-20260503-1235/`、`raw-20260501/` | 旧日期格式 | 历史只读，不搬 |
| `docs/B1-docs/raw-MIGRATED/` | 显式迁移归档 | 保留 |
| `docs/B1-docs/raw-20260710T171329Z/code-reviews` | 已迁到 B2；B1 下不再有 code-reviews | 已修复 |

`governance-check` 仍会报 5 个**仓库既有**缺陷：missing `protected-branch-breakglass-receipts.md`、missing `docs/B1-docs/{README.md,INDEX.md,CONVERGENCE.md}`、legacy `raw-20260303T000000Z` 命名。它们不是本轮引入的，不能靠改本轮文档绕过；需要单独治理 issue。

## 3. 规范（新文档）

1. B1 预研、candidate、对比研究：`docs/B1-docs/raw-{key}/`。
2. 支持性研究放同目录，命名避免 `README.md`/`b1-review.md` 这类会被误认为 B1 标准产物的名字；索引用 `research-index.md`，评审用 `pre-brainstorm-review.md`。
3. B2 只用 `docs/B2-docs/{epic}/{story}/raw-{key}/`；所有 PR review 放该 raw 的 `code-reviews/`。
4. B1 **只放** brainstorms/candidates/研究；B1 下不允许 `code-reviews/`。没有 active B2 story 的 legacy review，放 `docs/B2-docs/ibm/_legacy-issues/raw-{key}/code-reviews/`。
5. 不再新建 `docs/pre-brainstorms/`、`docs/epics/`、`docs/progress/`、`docs/recovery/`。
6. 历史归档只读；路径迁移必须单独 issue + 引用重写，不做“顺手搬”。

## 4. 验证

- `find docs -mindepth 1 -maxdepth 1 -type d` 只剩 `assets`、`B1-docs`、`B2-docs`、`system`。
- `docs/pre-brainstorms/` 不存在。
- 根 README 链接全部指向新路径。
- 仓库根 `code-reviews/` 不存在。
- `find docs/B1-docs -type d -name code-reviews` 为空。
- 20260701T030358Z 的 review 在 B2 `_legacy-issues/raw-20260701T030358Z/code-reviews/`；20260710T171329Z 的 review 在 B2 `config/test-gate/env/raw-20260710T171329Z/code-reviews/`。
- 依据：20260710 有对应 I-*；20260701 无 active B2 story，只能进 `_legacy-issues`，不能进 B1，也不凭空造 story。
