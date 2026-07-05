---
b1_id: B1-20260705T231131Z
phase_state: in_progress
source_raw: raw-20260705T231131Z
---

# B1: 全项目旧路径引用清理

## Input

- 上一个 PR `feature/raw-20260705T155347Z-docs-structure-refactor` 的 brainstorms + candidates
- wt-close 设计缺陷审查中发现的 `governance-closeout-gate` 仍用 `docs/issues`
- 全仓搜索发现 bin/ + scripts/ 层大量遗漏

## Problem

上一个 PR 的 acceptance criteria 只覆盖了 skill 文档、门禁脚本、治理文档（P0-P3），**完全遗漏了 `bin/` 和 `docs/system/workspace/scripts/` 下的执行层脚本**。

### 全量遗漏统计

| 类别 | 文件数 | 引用数（约） |
|------|--------|------------|
| 核心执行脚本 | 19 | ~100 |
| 测试文件 | ~40 | ~400 |
| 配置文件 | 1 | 1 |

### 涉及的核心脚本（按严重度）

| 文件 | 引用数 | 影响 |
|------|--------|------|
| `scripts/runtime/freely` | 23 | CLI 主程序，chat→issue 写入、intake 更新、issue 查询 |
| `scripts/quality/governance-closeout-gate` | 13 | 收口门禁，`_issue_file()` 路径构建 |
| `scripts/worktree/wt-create` | 10 | 工位创建，读 raw issue、创建 issue 目录 |
| `bin/freely-review` | 8 | Review 入口，读 raw issue + I-* issue |
| `bin/issue-sync` | 5 | ISSUES_DIR 中枢变量 |
| `scripts/worktree/wt-close` | 4 | 工位关闭，ISSUES_DIR + I-* 查找 |
| `scripts/worktree/pr-merge-guarded` | 4 | issue diff + add |
| `scripts/worktree/pr-create-guarded` | 4 | 读 issue file + find 扫描 |
| `bin/raw-issue-pull` | 4 | raw issue 物化路径 |
| `bin/pr-review-guarded` | 4 | I-* issue 查找 |
| `scripts/quality/checkpoint-guard` | 4 | checkpoint 检查 |
| `bin/check-epics-map` | 3 | epics-map 对齐检查 |
| `bin/issue-migrate-intake` | 3 | ISSUES_DIR |
| `bin/issue-index` | 2 | ISSUES_DIR + find 扫描 |
| `scripts/runtime/interruption-manager-handler` | 2 | issue 文件读取 |
| `bin/freely-watchdog` | 2 | issue 路径 |
| `bin/issue-sync-bootstrap` | 1 | --issues-dir 参数 |
| `scripts/quality/governance-merge-gate` | 1 | merge 门禁 |
| `.gitignore` | 1 | scan-state 路径 |

### 测试文件（~40 个）

大量测试硬编码了旧路径作为期望值/测试数据。典型：
- `test-governance-merge-gate` (191 处) — 最大的期望值文件
- `test-pretests-gate` (94 处)
- `test-pre-merge-commit-hook` (31 处)
- `test-pretests-retirement-gate` (20 处)
- …等

## Discovery

### 新旧路径完整映射

```
docs/issues/              → docs/B1-docs/          (raw-*  issue)
docs/issues/              → docs/B2-docs/          (I-*  issue — 需搜索)
docs/epics/               → docs/B2-docs/          (epic/story)

docs/issues/raw-{key}/issue.md          → docs/B1-docs/raw-{key}/issue.md
docs/issues/I-{key}-A/issue.md          → docs/B2-docs/{epic}/{story}/raw-{raw_key}/issues/I-{key}-A.md
docs/issues/ISSUES.md                   → 废弃
docs/issues/.scan-state                 → docs/B1-docs/.scan-state
docs/epics/{epic}/{story}/...           → docs/B2-docs/{epic}/{story}/...
```

### B2-docs I-* 文件结构关键发现

B1-docs 和 B2-docs 的文件命名不同：

| | B1-docs (raw issues) | B2-docs (I-* issues) |
|---|---|---|
| 结构 | `raw-{key}/issue.md` (目录+文件) | `I-{key}-A.md` (扁平 .md 文件) |
| 示例 | `docs/B1-docs/raw-20260701T085407Z/issue.md` | `docs/B2-docs/ibm/workflow/raw-20260701T051138Z/issues/I-20260701T051138Z-A.md` |

**两种 Pattern：**
- Pattern A: `docs/B2-docs/{epic}/{story}/raw-{raw_key}/issues/I-{key}.md`（标准，新格式 key）
- Pattern B: `docs/B2-docs/{epic}/{story}/issues/I-{key}.md`（老格式，无 raw- 目录）

### 两种旧路径类型的修复策略

**`docs/epics` → `docs/B2-docs`**: 简单 `sed` 替换即可（纯目录名替换）

**`docs/issues` → ?**: 需要逐引用分析：
- 引用 `raw-{key}` → `docs/B1-docs/raw-{key}`
- 引用 `I-{key}` → `find docs/B2-docs -path "*/issues/I-{key}*.md"`（搜索，不是目录）
- 引用 `$ISSUES_DIR` 变量 → 改为 `docs/B1-docs` 基路径
- 引用 `find docs/issues` 扫描 → 需同时扫 B1-docs + B2-docs

### 自举问题

`wt-create` 本身引用旧 `docs/issues` 路径。用 `--source platform` 可绕过（platform-adapter.py 已更新），但 `--source local` 永远失败。已确认：新设计只有 platform。

### 上一个 PR 的做法

上一个 PR 使用了分阶段的 commit（P0→P6），但实际执行中：
- 更新了 skill/门禁/治理文档（P0-P3）✅
- 迁移了历史文件（P5）✅
- 删除了 `docs/issues/` 目录（P6）✅
- **遗漏了 bin/ 和 scripts/ 执行层** ❌

上一个 PR 的 `candidates.md` acceptance_criteria 没有包含这些文件，属于 scope 设计缺陷。

### 关键规则

1. B1-docs 的 raw issue 是 `raw-{key}/issue.md`（目录+文件结构）
2. B2-docs 的 I-* issue 是 `I-{key}.md`（扁平 .md 文件，非目录！）
3. 查找 I-* 文件必须用 `find -path "*/issues/I-{key}*.md"` 而不是构造目录路径
4. 测试文件可以批量 `sed`（纯字符串替换）
5. 核心脚本必须逐文件逐引用分析

## Decision

**一刀切 sed 不可行**——B1-docs 和 B2-docs 的文件结构不同（目录+issue.md vs 扁平 I-*.md）。

**分两阶段实施：**

| 阶段 | 策略 | 文件数 |
|------|------|--------|
| 阶段1 | 核心脚本：逐文件分析每个引用，根据 raw/I-* 类型选择正确目标 | 19 个 |
| 阶段2 | 测试文件：批量 sed `s|docs/issues|docs/B1-docs|g` + `s|docs/epics|docs/B2-docs|g`（测试数据是字符串常量，不涉及 I-* 扁平结构） | ~40 个 |

**阶段1 中 `docs/issues` 引用的分类处理规则：**
- `docs/issues/raw-` 模式 → `docs/B1-docs/raw-`（直接替换）
- `docs/issues/I-` 模式 → `find docs/B2-docs -path "*/issues/I-{key}*.md"`（搜索）
- `docs/issues/$var/issue.md`（var 是 raw-*）→ `docs/B1-docs/$var/issue.md`
- `docs/issues/$var/issue.md`（var 是 I-*）→ `find docs/B2-docs ...`
- `find docs/issues -name "issue.md"` → 分两个 find（B1-docs 找 issue.md，B2-docs 找 I-*.md）
- `$ISSUES_DIR` 变量定义 → `docs/B1-docs`

## 待验证

- [ ] git diff 确认无遗漏
- [ ] `bash -n` 所有修改的 .sh 文件通过
- [ ] 所有文件 `grep -c 'docs/issues\|docs/epics'` 归零（除 B1/B2 内容文件）
