# Tasks

1. 冻结三条 canonical test lanes 及其 branch/worktree 匹配关系。
2. 收紧 `feature-local`，只允许 dedicated `feature/*`、`feature/premerge-*`、`release/*`、`hotfix/*` families。
3. 修复 `./bin/test-lane` 和 `./bin/test-test-lane` 的直接执行入口。
4. 补 focused regression，覆盖入口可执行性、lane mismatch、命令退出码保持。
5. 对齐直接消费 lane 语义的 skills、references、hook README 与 AGENTS 入口。
6. 完成 candidate / milestone / issue 写回，让后续执行 authority 以本 owner 为准。
