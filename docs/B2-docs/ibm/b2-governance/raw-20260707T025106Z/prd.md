# PRD: pr-review-guarded 工位清洁检查 + pr-merge-guarded 兜底

## Goal

确保每个阶段结束时工位是 clean 的（全部修改已提交），不允许带着 uncommitted changes 进入下一个阶段。

## 三层检查架构

```
pr-review-guarded (入口: Step 0)
    ↓ 检查1: dirty → 阻塞，给出修复方案
    [review 执行... review 可能生成文件]
    ↓ 检查2: dirty → 阻塞，要求提交 review 产物
pr-merge-guarded (兜底: 合并前)
    ↓ 检查3: dirty → 阻塞，提示可能遗漏 review 修改
merge
```

## 实现方案

### 1. bin/pr-review-guarded — 审查前检查（入口闸门）

位置：紧接参数解析后、review 开始前（约 L108 后）

```bash
# ── Step 0: Worktree cleanliness check (入口闸门) ──
_dirty_files=$(git status --porcelain 2>/dev/null | grep -v '^?' | head -20 || true)
_untracked=$(git ls-files --others --exclude-standard 2>/dev/null | head -20 || true)
if [[ -n "$_dirty_files" ]] || [[ -n "$_untracked" ]]; then
  cat >&2 <<DIRTY
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  [PR-REVIEW] 工位不干净 — 审查前必须先提交所有修改       ║
╠══════════════════════════════════════════════════════════════╣
║  带着未提交的修改做审查 = 审查的代码可能和最终合并的不一致     ║
║                                                              ║
║  Tracked 修改:                                                ║
${_dirty_files:-  (none)}
║                                                              ║
║  Untracked 文件（需要提交或 .gitignore）:                      ║
${_untracked:-  (none)}
║                                                              ║
║  修复方案（三选一，不要直接丢弃）:                              ║
║    git add <files> && git commit -m "..."  — 提交修改         ║
║    git stash                                — 暂存稍后恢复    ║
║    echo <pattern> >> .gitignore             — 明确忽略        ║
║                                                              ║
║  ❌ 不要用 git reset --hard 或 git clean -f（会丢失工作）     ║
╚══════════════════════════════════════════════════════════════╝
DIRTY
  exit 1
fi
echo "Step 0/5: worktree clean ✓"
```

### 2. bin/pr-review-guarded — 审查后检查（出口闸门）

位置：review verdict 写入后、提示 pr-merge 前

```bash
# ── Step 5: Post-review cleanliness check (出口闸门) ──
_dirty_files=$(git status --porcelain 2>/dev/null | grep -v '^?' | head -20 || true)
_untracked=$(git ls-files --others --exclude-standard 2>/dev/null | head -20 || true)
if [[ -n "$_dirty_files" ]] || [[ -n "$_untracked" ]]; then
  cat >&2 <<DIRTY
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  [PR-REVIEW] Review 产生了未提交的修改                     ║
╠══════════════════════════════════════════════════════════════╣
║  Review 过程中生成的文件未提交——不提交 = 这些修改会丢失。       ║
║                                                              ║
║  Uncommitted 修改:                                            ║
${_dirty_files:-  (none)}
║                                                              ║
║  Untracked 文件:                                              ║
${_untracked:-  (none)}
║                                                              ║
║  请提交 review 产物再继续:                                     ║
║    git add <files> && git commit -m "review: ..."            ║
║                                                              ║
║  提交后重新运行:                                               ║
║    freely pr-review-guarded <branch>                          ║
║    freely pr-merge-guarded develop <branch>                   ║
╚══════════════════════════════════════════════════════════════╝
DIRTY
  exit 1
fi
echo "Step 5/5: post-review worktree clean ✓"
```

### 3. pr-merge-guarded — 合并前兜底（最后防线）

位置：merge 执行前

```bash
# ── Worktree cleanliness check (最后防线) ──
_dirty_files=$(git status --porcelain 2>/dev/null | grep -v '^?' | head -20 || true)
_untracked=$(git ls-files --others --exclude-standard 2>/dev/null | head -20 || true)
if [[ -n "$_dirty_files" ]] || [[ -n "$_untracked" ]]; then
  cat >&2 <<DIRTY
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  [MERGE-GUARD] 工位不干净 — 合并前必须先提交所有修改       ║
╠══════════════════════════════════════════════════════════════╣
║  可能是 review 阶段产生了未提交的修改。                         ║
║                                                              ║
║  Uncommitted 修改:                                            ║
${_dirty_files:-  (none)}
║                                                              ║
║  Untracked 文件:                                              ║
${_untracked:-  (none)}
║                                                              ║
║  修复方案:                                                     ║
║    git add <files> && git commit -m "review: ..."            ║
║    git stash                                — 暂存            ║
║    echo <pattern> >> .gitignore             — 忽略            ║
╚══════════════════════════════════════════════════════════════╝
DIRTY
  exit 1
fi
```

## Dev-Loop Handoff

- 修改 2 个脚本文件（bin/pr-review-guarded + pr-merge-guarded 脚本）
- 全部为 shell 脚本的文本插入
- 检查逻辑完全复用 pr-create-guarded Step 0a 的模式
- 验证方式：制造 dirty 状态后运行命令，确认被阻塞且错误消息正确
