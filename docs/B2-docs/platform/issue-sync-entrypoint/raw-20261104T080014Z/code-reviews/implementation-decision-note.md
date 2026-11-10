# Implementation Decision Note
- issue_id: I-20261104T080014Z-A
- issue_path: docs/B2-docs/platform/issue-sync-entrypoint/raw-20261104T080014Z/issues/I-20261104T080014Z-A.md
- decision: adapter 增单平台 `issue-write-one`，issue-sync 四类 GitHub 写改调它；拆 1300 行与 feedback 逐字对齐留 follow-up
- why_this: issue-sync 直连 `gh issue create/comment/close/edit`，而 adapter 已拥有 handler、标签自动创建、错误归一与 0/3/1 partial 语义。两套并存导致同一操作在不同入口的标签/body/错误行为不同。
- alternatives_considered: ①把 `cmd_create` 整体改为一次 `create-issue` 双平台调用——会重写 platform_ids 回写与 partial 处理，风险大；②issue-sync 用 importlib 调 adapter Python API——文件名带连字符、参数传递脆；③删掉 `_gh_*` 全走 `create-issue`——同上；④本轮顺带拆 1300 行——独立重构，混入会让 RED 失焦；⑤给 adapter 加 delete——运维专用，登记例外。
- boundary_non_goals: 未改 cmd_create 双平台编排、platform_ids 回写、feedback body、adapter 既有 CLI 契约与退出码、`issue-sync-bootstrap` 的 delete。
- residual_risk: ①`_gh_close` 不再传 GitHub `--reason`（adapter 跨平台契约无该字段），close 状态一致但原因丢失；②adapter 输出 JSON，url 提取依赖 `"` 边界，若未来输出格式变化需同步；③`FREELY_PLATFORM_REPO` 是新增隐式契约，外部调用方若设置同名变量会覆盖检测；④`issue-sync` 仍在 1300 行量级，拆分前子命令不可独立单测；⑤`test-issue-sync-replica-guard.py` 仍有 4 项既有失败（基线 6 项）。
- verification: AT-001 基线 RED `0/4` → 工位 GREEN `4/0`；promote-b2 23/0、close-terminal-first 27/0、platform-adapter 三组全绿、`test-all --ci` 10/0。
- self_bootstrap_findings: ①adapter 输出是 JSON 而非裸 url，`grep -o '[^ ]*'` 会把 `"}}` 吞进 issue id，必须用 `[^"]*`；②夹具里的 issue-sync 没有 git remote，新增 `FREELY_PLATFORM_REPO` 覆盖是让「收口」与「可测」共存的最小改动；③既有测试的 adapter stub 必须同步新子命令，否则会把「夹具缺契约」误报成产品回归。

## Implementation Decision Note
- decision: 单平台 adapter 命令 + issue-sync 编排
- why_this: 写实现两份、标签/错误语义分叉
- alternatives_considered: 双平台一次调用 / importlib / 全删 _gh_* / 顺带拆文件 / 加 delete
- boundary_non_goals: 编排、回写、feedback、既有契约、bootstrap delete
- residual_risk: close reason 丢失、JSON 提取、repo env 契约、未拆分、既有失败
