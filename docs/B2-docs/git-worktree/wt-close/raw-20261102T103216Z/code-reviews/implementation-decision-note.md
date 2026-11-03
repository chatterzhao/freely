- issue_id: I-20261102T103216Z-A
- issue_path: docs/B2-docs/git-worktree/wt-close/raw-20261102T103216Z/issues/I-20261102T103216Z-A.md

## Implementation Decision Note

- decision: 用封装命令设置的显式标记替代 ps 进程树探测：reference-transaction 认 FREELY_WT_CREATE/FREELY_WT_CLOSE，pre-push 认 FREELY_ALLOW_REMOTE_BRANCH_DELETE；wt-create/wt-close 在调用 git 时设置，直接命令仍默认拦截。
- why_this: 本机沙箱禁用 ps，两个 hook 的调用方识别恒失败，连授权命令也被拦；分支建不出、远程分支删不掉。标记方案改动小、可测、保留原门禁语义。
- alternatives_considered: 用 /proc（macOS 无）、用 sysctl 解析（脆弱）、去掉调用方检查（等于放弃门禁，拒绝）。
- boundary_non_goals: 不改合并 receipt、develop/main 保护、分支命名校验；不做 ps 的跨平台替代。
- residual_risk: 标记可由用户手工 export 伪造，属于显式越权，审计可查；hook 仍保留 ps 作为第二判据。测试直接调用 hook 脚本而非 git，覆盖的是 hook 逻辑本身，真实 wt-create 另由 AT-003 日志佐证。
