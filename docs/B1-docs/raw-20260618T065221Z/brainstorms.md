# Brainstorm: pr-merge-guarded local merge 替代 gh pr merge

## Discovery

### Source
- raw-20260618T065221Z (GitHub #2981)
- 发现链：origin 持续落后 → 追踪到 git pull 被 receipt hook 拦截 → 发现 gh pr merge --merge --body 无效

### 根因验证

gh pr merge --merge --body 不生效：
- GitHub 文档明确：--body 仅在 --squash/--rebase 时附加
- --merge 时 GitHub 生成 "Merge pull request #XXXX from ..." 消息，忽略 --body
- 所有通过 gh pr merge 的 merge commit 均无 Freely-Merge-Path receipt
- reference-transaction hook 拦截 pull → 手动 reset → origin 落后

### 连锁影响

1. origin 持续落后 github → wt-create 从 origin 同步 → 工位拿到旧代码
2. 开发者手动 FREELY_SKIP_IBM_GATE=1 reset 绕过 hook → 无 receipt 的 merge 进入历史
3. governance gate 拦截 origin push → 跨 PR 累积变更无法推送
4. 整个开发链断裂

## Research

### 方案对比

| 方案 | receipt | 多平台一致 | GitHub PR 状态 | 复杂度 |
|---|---|---|---|---|
| A: gh pr merge --merge | ❌ 无效 | ❌ 分叉 | ✅ MERGED | 低 |
| B: gh pr merge --squash | ✅ body 可用 | ❌ 分叉 | ✅ MERGED | 低 |
| C: gh pr merge --rebase | ✅ body 可用 | ❌ 分叉 | ✅ MERGED | 低 |
| D: local git merge --no-ff | ✅ 带 receipt | ✅ 统一 commit | ✅ 自动检测 | 中 |
| **E: local merge + gh pr close** | ✅ | ✅ | ✅ CLOSED | 中 |

方案 B/C: squash/rebase 改变 commit 历史，不适合 Freely 的 merge 策略。

方案 D: 用 FREELY_GUARDED_MERGE_COMPLETION=1 做 local merge，commit message 带 receipt，push 到所有 remote。GitHub 检测到分支已合并后自动关闭 PR。

方案 E: local merge + 显式 gh pr close，更可靠。

### 选择：方案 D + E 混合

```
do_initial_merge:
  1. git fetch github develop
  2. FREELY_GUARDED_MERGE_COMPLETION=1 git merge --no-ff source_branch
     -m "Merge branch 'xxx' into develop\n\nFreely-Merge-Path: pr-merge-guarded"
  3. git push github develop && git push origin develop
  4. gh pr close (确保 PR 状态更新)
  5. attempt_develop_push_followthrough_if_needed
```

关键：FREELY_GUARDED_MERGE_COMPLETION=1 告诉 hook 这是合法的 guarded merge，允许 receipt 写入。

### 同时修复：wt-create 平台一致性检查

wt-create 行 627：
```bash
git fetch origin develop 2>/dev/null && git update-ref ... 2>/dev/null
```

改为：
```bash
# 获取所有平台 develop HEAD，验证一致
git fetch github develop && git fetch origin develop
github_head=$(git rev-parse refs/remotes/github/develop)
origin_head=$(git rev-parse refs/remotes/origin/develop)
if [[ "$github_head" != "$origin_head" ]]; then
  echo "ERROR: platforms out of sync. github=$github_head origin=$origin_head"
  echo "Run: freely develop-push attempt --project <path>"
  exit 1
fi
git update-ref refs/heads/develop "$github_head"
```

## Decision

**Promote**。两个修复：
1. pr-merge-guarded 改用 local git merge（方案 D+E）
2. wt-create 增加平台一致性检查（阻塞 + 清晰错误信息）
