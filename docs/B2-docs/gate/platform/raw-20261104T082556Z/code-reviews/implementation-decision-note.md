# Implementation Decision Note
- issue_id: I-20261104T082556Z-A
- decision: 文档定位收口到单一 `_issue_file_for`（B1 优先 + B2 兜底，缺失 rc1 / 歧义 rc2），5 个命令与 `cmd_promote` 统一使用；`platform_state` 只在字段已声明时写
- why_this: B1-only 路径假设让 B2 的 I-* 在任何命令下都找不到，promote 必然失败 → B1→B2 平台同步断开、只能手改 phase_state 绕过（状态分叉）。
- alternatives_considered: 只改 promote（update/comment 仍坏）；复制/软链文档到 B1（双真相源）；`find | head -1`（歧义随机取一个）。
- boundary_non_goals: 不改 close 的四段式与 0/3/1（#4184）；不改生命周期契约与 `_raw_effect`；不改 batch/scan dedup；不改任何平台写语义。
- residual_risk: ①B2 前缀兜底（`<id>-*.md`）只在精确名缺失时启用，若将来出现 `I-x-A` 与 `I-x-AB` 同存可能被判歧义并拒绝 —— 属预期的 fail-closed。②解析器每次调用做一次 `find`，在 800+ B2 文档下耗时约 30–60ms，`cmd_create/close` 每次仅调用一次，未做缓存（避免陈旧缓存引入更难查的 bug）。③`cmd_status` 等只读命令失败时仍 `exit 1`（与旧行为一致），未改为返回码细分。④歧义场景只能靠人工消歧，本轮未提供自动修复命令。
- verification: AT-001 develop 基线快照 RED `4 ok / 12 failed` → 工位 GREEN `16 ok / 0 failed`；7 个相关回归 worktree/baseline 退出码全 MATCH；真机用修好的 promote 完成本轮 absorb。
- self_bootstrap_findings: 本条即 R12 收口时自举发现（promote 对 B2 必然失败）；未发现其他未被 open issue 覆盖的新缺陷。

## Implementation Decision Note
- decision: 单一文档解析器（B1 优先/B2 兜底/歧义拒绝）、5 命令 + promote 统一、platform_state 条件写
- why_this: B1-only 假设让 B2 I-* 永远找不到，promote 必然失败，B1→B2 同步断开
- alternatives_considered: 只改 promote；复制文档到 B1；find 取首个
- boundary_non_goals: close 四段式、生命周期契约、batch dedup、平台写语义均不动
- residual_risk: 前缀兜底可能判歧义（fail-closed）；每调用一次 find；只读命令仍 exit 1；歧义需人工消歧
