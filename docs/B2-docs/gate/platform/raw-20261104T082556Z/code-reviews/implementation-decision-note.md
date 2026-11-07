# Implementation Decision Note
- issue_id: I-20261104T082556Z-A
- decision: 文档定位收口到单一 `_issue_file_for`（B1 优先 + B2 兜底，缺失 rc1 / 歧义 rc2），5 个命令与 `cmd_promote` 统一使用；`platform_state` 只在字段已声明时写
- why_this: B1-only 路径假设让 B2 的 I-* 在任何命令下都找不到，promote 必然失败 → B1→B2 平台同步断开、只能手改 phase_state 绕过（状态分叉）。
- alternatives_considered: 只改 promote（update/comment 仍坏）；复制/软链文档到 B1（双真相源）；`find | head -1`（歧义随机取一个）。
- same_round_prerequisites: 为了让「promote + promote-finalize 全链路成功」这条验收**可验证**，本轮还修了两个被打同一个门禁暴露出来的前置缺陷：①`raw_reconciliation` 的评论归一化把本地内联评论头与平台评论正文当成同一种东西比较，且 `_body()` 没有剔除内联评论块 —— 导致「有系统评论的 raw」永远无法与平台副本一致；改为：`_body()` 剔除评论块、`_comments()` 用「块正文（去元数据）」与平台评论正文比较。②`gitee-issue.py get` 直接把 Gitee 的 `comments` 计数值当列表返回（永远是 0 条），`platform-adapter.fetch_issue` 因此永远读不到 Gitee 评论；改为在 `comments` 不是列表时补拉 `/issues/<num>/comments`。两者都有既有测试守护（`test-raw-reconciliation.py` 3 tests OK）。
- boundary_non_goals: 不改 close 的四段式与 0/3/1（#4184）；不改生命周期契约与 `_raw_effect`；不改 batch/scan dedup；不改任何平台写语义。
- residual_risk: ①B2 前缀兜底（`<id>-*.md`）只在精确名缺失时启用，若将来出现 `I-x-A` 与 `I-x-AB` 同存可能被判歧义并拒绝 —— 属预期的 fail-closed。②解析器每次调用做一次 `find`，在 800+ B2 文档下耗时约 30–60ms，`cmd_create/close` 每次仅调用一次，未做缓存（避免陈旧缓存引入更难查的 bug）。③`cmd_status` 等只读命令失败时仍 `exit 1`（与旧行为一致），未改为返回码细分。④歧义场景只能靠人工消歧，本轮未提供自动修复命令。
- verification: AT-001 develop 基线快照 RED `4 ok / 12 failed` → 工位 GREEN `16 ok / 0 failed`；7 个相关回归 worktree/baseline 退出码全 MATCH；真机用修好的 promote 完成本轮 absorb。
- self_bootstrap_findings: 本条即 R12 收口时自举发现（promote 对 B2 必然失败）。**同一轮内追加发现并修复一个连带缺陷**：`promote` / `promote_finalize` 写入的系统事件评论使用 `- key: value` 项目符号元数据且不在 `## Comments` 段落之下，而原读取器要求「`## Comments` 段落 + `{json}` 元数据行」，于是系统评论既判不出「未同步」也抽不出正文 —— 结果 finalize 的「拆解为以下任务」评论只留在本地，`pr-create-guarded` 的副本一致性检查报 `content_diverged` 直接挡下。修法：`_comment_blocks` / `_last_comment_body` 统一解析两种元数据形态，`_has_unsynced_comments` 改为比较最新评论时间戳与 `last_synced_comment_at`。真机修复过程：GitHub 评论推送成功，Gitee 因已关闭而拒绝评论（`当前issue已关闭评论功能`），用 `gitee-issue.py reopen → comment → close` 补齐，随后一致性检查通过。

## Implementation Decision Note
- decision: 单一文档解析器（B1 优先/B2 兜底/歧义拒绝）、5 命令 + promote 统一、platform_state 条件写
- why_this: B1-only 假设让 B2 I-* 永远找不到，promote 必然失败，B1→B2 同步断开
- alternatives_considered: 只改 promote；复制文档到 B1；find 取首个
- same_round_prerequisites: 为了让「promote + promote-finalize 全链路成功」这条验收**可验证**，本轮还修了两个被打同一个门禁暴露出来的前置缺陷：①`raw_reconciliation` 的评论归一化把本地内联评论头与平台评论正文当成同一种东西比较，且 `_body()` 没有剔除内联评论块 —— 导致「有系统评论的 raw」永远无法与平台副本一致；改为：`_body()` 剔除评论块、`_comments()` 用「块正文（去元数据）」与平台评论正文比较。②`gitee-issue.py get` 直接把 Gitee 的 `comments` 计数值当列表返回（永远是 0 条），`platform-adapter.fetch_issue` 因此永远读不到 Gitee 评论；改为在 `comments` 不是列表时补拉 `/issues/<num>/comments`。两者都有既有测试守护（`test-raw-reconciliation.py` 3 tests OK）。
- boundary_non_goals: close 四段式、生命周期契约、batch dedup、平台写语义均不动
- residual_risk: 前缀兜底可能判歧义（fail-closed）；每调用一次 find；只读命令仍 exit 1；歧义需人工消歧
