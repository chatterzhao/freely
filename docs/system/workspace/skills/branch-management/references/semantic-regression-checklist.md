# 语义回归检查清单

在合并到 `pre-develop` 后、提升前运行：

1. 分支治理意图：
- `feature/*` 必须从 `pre-develop` 创建。
- `main/develop/pre-develop` 必须保持 add/commit 禁止。

2. Worktree 治理意图：
- Worktree 根目录必须是同级 `{project-name}-worktrees`。
- 在项目根目录内创建 worktree 必须保持禁止。

3. Pre-brainstorms 命名意图：
- 新记录 ID 使用 `YYYYMMDD-HHMM--<topic>`。

4. Premerge 策略意图：
- 临时协调分支名使用 `feature/premerge-YYYYMMDD-HHMM--<topic>`。
- 协调流程从 `pre-develop` 开始并合并回 `pre-develop`。

5. 决策方法：
- 按语义兼容性评估，而非提交时间顺序。

6. 提升测试证据：
- `PRE_TEST` 作为开发前基线存在（验收意图）。
- 提升到 `develop` 由已执行的 `TEST` 结果门禁（包括集成验收），而非仅靠 `PRE_TEST`。
