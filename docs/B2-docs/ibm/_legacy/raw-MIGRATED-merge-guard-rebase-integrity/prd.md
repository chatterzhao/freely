# PRD: Merge Guard + Rebase Integrity

## Goal

杜绝两类代码丢失路径：
1. GitHub UI merge 绕过 pr-merge-guarded 门禁
2. git rebase 冲突解决静默丢弃变更

## Design

### 架构

```
PR opened → CI creates governance/pr-merge-guard check (in_progress)
                ↓
          GitHub branch protection requires this check → merge button greyed
                ↓
          pr-merge-guarded runs → all gates pass → set check to success
                ↓
          gh pr merge (no --admin) → check passes → merge allowed


git rebase → pre-rebase hook saves snapshot
           → rebase executes (conflict resolution may drop changes)
           → post-rewrite hook compares snapshot → lost files? → write marker

pr-merge-guarded → check_rebase_integrity gate → marker present? → BLOCK
```

### 行业对标
- **Branch protection + required check**: GitHub 原生能力，Merge Gatekeeper (starkware-libs) 开源参考
- **post-rewrite hook**: Apache Mesos 等项目用于 rebase 后风格/完整性检查

### 关键决策
- 使用 git hooks 而非 wrapper 脚本：hooks 自动触发，不依赖开发者记忆
- 使用 GitHub check runs API 而非保持 `--admin`：让 branch protection 真正生效
- pre-rebase 保存文件列表（非完整 diff）：轻量、可靠、避免误报

## Dev-Loop Handoff

- 代码已实现（5 个 commit，3 个 scope：hooks, workflow, pr-merge-guarded）
- pre-rebase hook 已验证：快照成功保存到 `.freely/run/pre-rebase-diffs/`
- post-rewrite + pre-rebase hook 通过 bash syntax check
- pr-merge-guarded 语法正确

## Acceptance

- [ ] pre-rebase hook 在 `git rebase develop` 前自动保存快照
- [ ] post-rewrite hook 在 rebase 后自动对比，丢文件时写入 marker
- [ ] pr-merge-guarded `check_rebase_integrity` 读 marker 拒绝 merge
- [ ] CI workflow 创建 `governance/pr-merge-guard` check (in_progress)
- [ ] pr-merge-guarded `_set_governance_check_pass` 将 check 更新为 success
- [ ] `gh pr merge` 无 `--admin` 正常合并
