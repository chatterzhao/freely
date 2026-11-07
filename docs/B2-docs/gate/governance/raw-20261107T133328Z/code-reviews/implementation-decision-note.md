# Implementation Decision Note
- issue_id: I-20261107T133328Z-A
- decision: `wt-close` 删除自算的评论/resolution 计数，改为调用 `quality/comment-resolution-scan.py`，只对本 issue 的命中行阻塞；报错文案直接透出 scan 输出
- why_this: 同一规则两份实现已实际漂移（scan 在 R13 已忽略 `- source: system`，wt-close 仍把系统事件评论当人类评论），导致任何经过 promote 的 raw 都无法收口，只能 `--force` —— 而 `--force` 会永久丢弃实现，是禁止项。
- alternatives_considered: ①在 wt-close 里再写一份「忽略 `- source: system`」（仍是两份实现）；②让 `promote_finalize` 顺手写 `#### resolution-`（伪造人类决议，且会给本地加块破坏副本一致性）；③`--force` 绕过（禁止）。
- boundary_non_goals: wt-close 的其他 Phase（replica 一致性、phase_state、平台关闭、worktree/分支清理、任务回收）未改；`comment-resolution-scan.py` 的判定语义未改。
- residual_risk: ①scan 现在对整个 `docs/B1-docs` 跑一次（0.2s 量级），wt-close 只取本 issue 的行 —— 若语料涨到上万条需要再看耗时；②历史语料里若有「人类评论用 `- source: system` 标注」的误标，会被判为系统评论而漏检（当前语料已核对：系统评论只由 promote/promote_finalize/dropped 产生）；③wt-close 仍是 shell 脚本内联检查，长期应收口到 runtime 子命令（记入 revisit）。
- verification: AT-001 develop 基线快照 RED `7 ok / 3 failed` → 工位 GREEN `10 ok / 0 failed`；相关回归基线对比退出码一致；真机：修复后 `wt-close` 成功收口 R13（此前 rc=1 阻塞）。
- self_bootstrap_findings: 本条即 R13 收口时自举发现；未发现其他未被 open issue 覆盖的新缺陷。
