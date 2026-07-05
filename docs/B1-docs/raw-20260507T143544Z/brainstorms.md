# Brainstorm: raw-issue-pull 工位拦截

## 来源
- `docs/issues/raw-20260507T143544Z/issue.md` — GitHub #247
- 实际操作中发现：从 `develop` 分支直接调用 `raw-issue-pull` 可拉取任意 issue，绕过工位隔离

## 问题边界
- `bin/raw-issue-pull` 无调用者身份校验
- `bin/freely raw-issue-pull` CLI 路由未实现（help 有但 dispatch 无）
- `local` bash 关键字在函数外使用导致 `local: can only be used in a function`

## 研究结论
1. **受保护分支拦截**：develop/main 上禁止执行 raw-issue-pull
2. **分支名匹配校验**：当前分支必须包含 raw-key
3. **CLI dispatch**：补充 `cmd_raw_issue_pull()` 函数和 case 路由
4. **Bash bug**：将 `local local_id` 改为普通变量赋值

## 推荐下一跳
- Candidate promote → B2_IBM materialize I-* → 实现
