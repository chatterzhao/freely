# Brainstorm: worktree 路径架构修正

## Discovery

### Source
- raw-20260618T015503Z (GitHub #2956)
- 发现链：develop 反复被弄脏 → 追踪到 _absorb_close_frontmatter → 发现全链路路径问题

### 问题全貌

Freely 的多条命令在操作治理文档时，路径解析存在系统性错误：

1. **ROOT_DIR 双轨制**：项目中有两种互不兼容的 ROOT_DIR 解析方式
2. **raw issue 放在 develop**：wt-create 把 raw issue 物化到 develop 的 `docs/B1-docs/`，而非 worktree
3. **wt-close 硬编码 develop**：ROOT_DIR 通过脚本路径推导，永远指向主仓库
4. **_absorb_close_frontmatter 是补救代码**：因为 raw issue 不在 worktree 中，merge 后需要事后 amend develop

### 影响

- develop 反复被弄脏（raw issue frontmatter 被直接修改）
- `_absorb_close_frontmatter` + `git commit --amend 2>/dev/null || true` 静默失败
- 多 worktree 并发时可能互相覆盖 raw issue
- 增加了不必要的复杂度（amend、force-close trace、issue-sync 在 develop 上执行）

## Research

### ROOT_DIR 解析方式

| 方法 | 机制 | 使用者 |
|---|---|---|
| A | `git rev-parse --show-toplevel` | wt-create, pr-create-guarded |
| B | `$(dirname $0)/../../../../..` | wt-close, worktree-common.sh, ~10 个 quality 脚本 |

方法 A 在 worktree 内执行返回 worktree 路径 ✓，在 develop 执行返回 develop。
方法 B 永远返回 develop ✗（无论从哪里执行）。

### 受影响文件清单

| 文件 | 问题 | 修复 |
|---|---|---|
| wt-create | 7 处 `$ROOT_DIR/docs/B1-docs/` → develop | `$target_path/docs/B1-docs/` |
| wt-close | ROOT_DIR 硬编码 + 所有 `$ISSUES_DIR` 引用 | `git rev-parse --show-toplevel` |
| pr-merge-guarded | `_absorb_close_frontmatter` 整段 | 删除 |
| pr-create-guarded | 缺少 worktree 内 phase_state 检查 | 增加 worktree 路径检查 |
| worktree-common.sh | ROOT_DIR 硬编码 | `git rev-parse --show-toplevel` |
| config.toml | PROJECT_ROOT 硬编码绝对路径 | 支持自动推导 |

### 边界

- 所有 worktree 与主仓库的相对位置受 `{project}-worktrees/` 约束保证
- `git worktree list` 可查询任意 worktree 的路径
- 向后兼容：develop 上已有大量历史 raw issue，不能丢失

## Decision

**Promote**。这是一个架构性修复，涉及 6 个文件但每处修改都是路径修正，不改变业务逻辑。

### 执行顺序（按依赖关系）

1. **worktree-common.sh**：修正 ROOT_DIR 定义（被其他脚本 source）
2. **wt-create**：`$target_path/docs/B1-docs/` 替换 `$ROOT_DIR/docs/B1-docs/`
3. **pr-create-guarded**：增加 worktree 内 phase_state 检查
4. **pr-merge-guarded**：删除 `_absorb_close_frontmatter`（raw issue 由 merge 自然带入）
5. **wt-close**：ROOT_DIR 改用 `git rev-parse --show-toplevel`
