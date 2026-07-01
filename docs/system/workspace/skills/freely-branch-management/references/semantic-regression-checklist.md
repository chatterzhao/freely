# 语义回归检查清单

在进入 `develop` 前运行；若本轮启用了 `test-pre-merge-*`，则在该临时验证批次完成后执行：

1. 分支治理意图：
- `feature/*` 必须从 `develop` 创建。
- `main/develop` 必须保持 add/commit 禁止（仅接受 merge）。`test-pre-merge-*` 禁止手动 add+commit 原创提交、禁止 push；允许 merge、cherry-pick、直接修改文件。

2. Worktree 治理意图：
- Worktree 根目录必须是同级 `{project-name}-worktrees`。
- 在项目根目录内创建 worktree 必须保持禁止。

3. Pre-brainstorms 命名意图：
- 新记录 ID 使用 `YYYYMMDDTHHMM[SS]Z--<topic>`。

- 临时协调分支名使用 `feature/premerge-YYYYMMDDTHHMM[SS]Z--<topic>`。
- 协调流程从 `test-pre-merge-*` 批次开始并合并回所属批次。

5. 决策方法：
- 按语义兼容性评估，而非提交时间顺序。

6. 提升测试证据：
- `PRE_TEST` 作为开发前基线存在（验收意图）。
- 提升到 `develop` 由已执行的 `TEST` 结果门禁（包括集成验收），而非仅靠 `PRE_TEST`。

7. `test-pre-merge-*` 语义：
- `test-pre-merge-*` 只承担主线前验证，不承担在 `develop` 上先预测试的替代语义。
- 进入 `develop` 的正常 promote 对象是当前权威 `test-pre-merge-*` 批次，而不是绕回来源 `feature/*` 继续保留第二条正常路径。
- 当前批次完成后必须立即删除；若还要继续验证，只能从当前 `develop` 新建下一批次。
