# Brainstorms: raw-20261125T094104Z

## 0. 设计意图审计（先于方案）

### B0 前置：关键词广搜 + 多文档交叉

| 关键词族 | 搜索词 | 主要命中 |
|---|---|---|
| 功能名 | `pr-merge-guarded` / `issue-sync before merge` | `scripts/worktree/pr-merge-guarded:599-631`、:776-781 |
| 机制名 | `push all` / `failed_remotes` / `committed + pushed` | 同文件 :625、:629、:401-423 |
| 字段名 | `|| true` / 回执 / partial | 同文件 :625；raw-20261124T054217Z（update 吞 Gitee 失败） |
| 命令名/门禁名 | `develop-push` / `all remotes synced` | 同文件 :401-423（正确范式） |

**多份文档声明**：push 相关逻辑在同文件有两处实现（develop-push 段 vs issue-sync 段），加上 commands.md 的意图描述与 734-735 行错误提示。当前生效实现是 :623-629；历史/局部是 734-735 的提示文本；权威契约是 commands.md「pr-merge → 双平台同步」。

**三类分层**：
- 当前生效实现：`:623-629`（push all + || true + 无条件回执）；`:401-423`（develop 逐 remote 校验）。
- 历史局部：`:734-735` 错误提示里手写 `git push github/origin`（说明设计意图本就是逐平台）。
- 当前权威恢复点：goal v6 P0-1（本条立项）。

**矛盾清单**：
1. `:401-423` 逐 remote 校验汇总 vs `:623-629` 单 remote + `|| true` + 无条件成功——同一文件两种范式，后者是缺陷。
2. `:734-735` 提示用户手动 `git push github/origin` vs `:625` 封装只 `push all`——提示与实现不一致。
3. raw-20261124T054217Z 已确立「部分成功不得伪装整体成功」，本段违反该既有契约。

**二元决策**：**继续（修实现）**——设计正确（逐平台 push + 汇总），实现偏差（issue-sync 段未沿用 develop-push 范式），非 dropped。

### 四行实质结论

1. **外部锚点**：`pr-merge-guarded:401-423`「Push to all configured remotes, not just @{upstream}... failed_remotes」；raw-20261124T054217Z「update 汇总 github/gitee/overall，任一失败非零退出」；`CONSTITUTION.md` §5 bypass 永久禁止。
2. **判定（五选一）**：**实现偏差**——同文件已有正确范式（develop-push 逐 remote），issue-sync 段漏用；不是设计错误。
3. **与既有断言冲突**：无冲突；修法是让 issue-sync 段对齐 develop-push 段，不改任何既有断言。
4. **影响面**：仅 `pr-merge-guarded:_sync_issues_changed_in_merge` 的 push 块（:623-629）；不改 develop-push 段、不改 pr-create/pr-review、不改 adapter。

## 0.1 全局适配四问

- Q1 类别：流程能力（封装命令的写回可靠性）。
- Q2 职责边界：与 develop-push 段共享「push 到双平台」职责——两者应统一到同一 helper 或同一范式；最终判定归 pr-merge-guarded。
- Q3 结构性冲突：无——修实现不改变任何上层设计，不要求额外工位或额外 IBM 流程。
- Q4 门禁失配：现有门禁测「merge 是否成功」，本缺陷在「merge 前的源分支 push」——判据缺失但不需要放宽任何门禁，只需让 push 结果可见并 fail-closed。

## 1. 根因分析

`_sync_issues_changed_in_merge` 在 commit issue-sync 变更后：
```bash
if git -C "$_wt_path" remote | grep -q "^all$"; then
  git -C "$_wt_path" push all "$_src_branch" 2>/dev/null || true
else
  git -C "$_wt_path" push origin "$_src_branch" 2>/dev/null || true
fi
echo "[MERGE-GUARD] issue-sync committed + pushed to $_src_branch"   # 无条件
```
三重缺陷：① `2>/dev/null` 丢弃 stderr；② `|| true` 吞掉失败；③ 无条件打印 "pushed"。remote 'all' 有 github+gitee 两个 pushurl，顺序推送，任一失败被吞后无法区分部分/全部成功。

实证（#4699 合并现场）：`github/fix/*` 停 `2905bdf67`、`all/origin/fix/*` 在 `0b56bc5f5`，回执未报失败。

## 2. 方案评估

| 方案 | 结论 |
|---|---|
| A：删掉 `|| true`，保留 `push all` | 否决——多 pushurl 仍无法区分哪一平台失败，且 `push all` 失败时可能只推了一半 |
| B：逐 configured platform push + 汇总 failed_remotes，对齐 develop-push 段 | **采纳**——同文件已有范式，改动最小，失败可见且可定位 |
| C：抽出公共 helper 供两段复用 | 部分采纳——若改动面可控则抽 helper；但为避免触碰 develop-push 段（已稳定），本轮先只在 issue-sync 段内联同范式，helper 抽取另议 |
| D：合并失败即回滚 commit | 否决——过度设计；commit 本身正确，只需让 push 失败可见并可重试 |

## 3. 收敛决策

采用 B：逐 remote（遍历 `git remote`、跳过 `all`）push 源分支，汇总每个结果；失败 → 非零退出 + 列出失败 remote + 可执行重试命令；成功才打印 pushed。保留自动 push 的必要性（源分支需含 issue-sync commit 以保持 PR 与各平台一致、wt-close 才能干净删分支）。
