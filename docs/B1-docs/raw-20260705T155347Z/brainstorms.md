---
b1_id: B1-20260705T155347Z
phase_state: completed
source_raw: raw-20260705T155347Z
produced_candidate: C-20260705T155347Z-A
---

# B1: docs/ 目录结构重构 + 8 epic 收敛

## Input
- `docs/B1-docs/raw-20260705T155347Z/issue.md`
- 8 层 epic 设计（acp/a2a/runtime/git-worktree/ibm/gate/human/config）
- B1/B2 skill 现有结构

## Problem
1. B1 产物散落在 `docs/B1-docs/{key}--{slug}/`，无 raw key 目录包裹
2. B2 产物散落在 `docs/epics/` 下 245 个伪 epic，大多实为 story
3. skill/代码中硬编码旧路径（`docs/epics/`, `docs/B1-docs/`），新 raw issue 会放错位置
4. B1/B2 产物互不可追溯——同一个 raw key 在两个地方

## Discovery

### 现状路径 vs 目标路径

| 当前 | 目标 |
|------|------|
| `docs/B1-docs/{key}--{slug}/` | `docs/B1-docs/raw-{key}/` |
| `docs/epics/{old-epic}/{old-story}/` | `docs/B2-docs/{new-epic}/{new-story}/raw-{key}/` |
| `docs/B1-docs/raw-{key}/` | → `docs/B1-docs/raw-{key}/`（迁入 B1） |
| `docs/epics-map.svg` | 指向 `docs/B2-docs/`，删除重建 |
| `docs/milestones.md` | 保留，路径引用更新 |
| `docs/brainstorms/`, `docs/candidates/`, `docs/reviews/` | 废弃 |

### 需要更新的代码文件（按优先级）

**P0 — skill/模板。改了之后新 issue 才能写对位置：**
- `docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md` — brainstorms/candidates/milestones 写入路径
- `docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md` — 全部产物路径 + 示例
- `docs/system/workspace/skills/freely-doc-B2_IBM-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md`

**P1 — 门禁/命令。改错之后新 issue 创建/合并被拦截：**
- `bin/check-epics-map` — 改为扫描 `docs/B2-docs/`
- `bin/pr-review-guarded` — `find docs/B2-docs` + `verification_artifact_dir` 路径
- `bin/issue-sync` — issue 同步路径
- `bin/issue-sync-batch.py` — `os.walk('docs/B2-docs')`
- `.githooks/pre-commit.sh` — milestones.md 路径

**P2 — 运行时。feedback/issue-sync 读写路径：**
- `docs/system/workspace/scripts/runtime/freely` — `cmd_feedback`, `issue-sync` 相关路径
- `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py`

**P3 — 治理文档。AGENTS/LAWS 中的引用：**
- `AGENTS.md`, `docs/LAWS.md`, `docs/CONSTITUTION.md`
- `docs/system/workspace/ibm-framework.md`
- `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md`

### 历史文档迁移策略

历史文件（epics/ 下 240 个旧目录、pre-brainstorms/ 下 609 个）只需搬到正确目录结构——**不修改历史文件内部的路径引用**。原因：
1. 历史文档是已完成工作的记录，内部引用的是当时的上下文
2. 修改 1000+ 个历史文件会引入大量噪音
3. skill/代码更新后，新 issue 自然写到新路径

## Decision: 分阶段实施

| 阶段 | 内容 | 产出 |
|------|------|------|
| P0 | 更新 skill（B1/B2/workflow）路径引用 + 示例 | 修改 ~6 个文件 |
| P1 | 更新门禁/命令路径引用 | 修改 ~5 个文件 |
| P2 | 更新运行时路径引用 | 修改 ~2 个文件 |
| P3 | 更新治理文档路径引用 | 修改 ~5 个文件 |
| P4 | 删除重建 epics-map.svg（→ B2-docs/） | 1 个新文件 |
| P5 | 运行迁移脚本，搬移历史文件 | ~1000 个文件移动 |
| P6 | 清理废弃目录 | 删除 3 个目录 |

## Candidate
- candidate_id: C-20260705T155347Z-A
- status: promoted
- milestone: M-20260705T155347Z-A
