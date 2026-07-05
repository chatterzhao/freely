# Brainstorm: pr-merge-guarded local merge 替代 gh pr merge

## Discovery

### Source
- raw-20260618T071502Z02Z (GitHub #2981 继续)
- 发现链：origin 持续落后 → 追踪 git pull 被 receipt hook 拦截 → 确认 gh pr merge --merge --body 无效

### 问题
gh pr merge --merge --body 不生效。--body 仅在 --squash/--rebase 时有效，--merge 时 GitHub 忽略 --body，生成自己的 merge 消息。Freely-Merge-Path receipt 从未进入 GitHub merge commit。

### 影响
- receipt hook 拦截 git pull
- origin 落后 github
- wt-create 从落后 origin 创建工位拿到旧代码
- 整个开发链断裂

## Research

### 方案对比
| 方案 | receipt | 多平台一致 | 
| gh pr merge --merge | ❌ | ❌ |
| local git merge --no-ff | ✅ | ✅ |

### 选择
Local git merge --no-ff with Freely-Merge-Path receipt。attempt_develop_push_followthrough_if_needed 自动推送到所有平台。

## Decision
**Promote**。替换 do_initial_merge 中的 gh pr merge 为 local git merge。
