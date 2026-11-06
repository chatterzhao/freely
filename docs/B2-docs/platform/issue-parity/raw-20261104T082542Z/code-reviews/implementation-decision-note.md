# Implementation Decision Note
- issue_id: I-20261104T082542Z-A
- decision: 复用 Q2 标题契约新增 `local_heading_title()`，让 pull_raw_issue 落盘写入一个前缀无关 H1；另提供默认 dry-run 的安全回填命令，不批量改写历史语料
- why_this: 每轮新 raw issue 的首次 PR 都因本地 _local_record 取不到 H1、平台 title 去前缀后非空而判 content_diverged，Q1/Q2/R1 三轮均靠人工现场补 H1。用户要求「不要修改了退化」，因此不改 Q2 既有函数，只新增纯函数并让两侧前缀剥离共用同一契约。
- alternatives_considered: 在 wt-create / issue-sync 里现场补 H1（非真源修复）；修改 Q2 的 `_STALE_PREFIX` 正则以支持任意 key（改变既有函数行为，越界）；本 PR 批量回填 700 份历史文件（410 已 absorbed、18 多 H1、标题来源不足，风险不可控）；直接用 `_STALE_PREFIX` 剥前缀（4 个历史非标准 key 会产生重复前缀，已实证）。
- boundary_non_goals: 不改 `canonical_raw_title` / `is_canonical_raw_title` / `platform_title`；不改 created_at 兼容分支、本地身份解析、`_resolve_raw_identity` 兜底、`issue-sync._platform_title` 与 `feedback edit`；不改写 700 份历史 raw；不统一历史 raw key 格式。
- residual_risk: ①4 个历史非标准 raw key 暴露了 `canonical_raw_title()` 的边界（非时间戳 key 可能产生重复前缀），本 PR 只保证新 helper 正确，未改 Q2 函数；若后续 `issue-sync` 更新这些历史 issue 的平台标题仍可能触发，与 #4154「契约常量与 raw key 多副本收口」同簇，未重复建 issue。②回填命令的平台查询依赖网络且 Gitee 对非仓库成员 assignee 有 403（本轮实测），但回填只读 issue 标题，不 claim assignee，不受影响。③700 份历史 raw 仍缺 H1，未来若批量回填需独立评估。
- verification: AT-001 RED → GREEN（18 项检查）；真实双平台副本物化后本地/平台 fingerprint 9140d678763e4dd9 一致、title/body 双 MATCH；805 份真实 issue.md 的 Q2 四个既有函数新旧对比 0 差异；7 个相关回归测试全 PASS；check-epics-map 对齐。
- self_bootstrap_findings: 4 个历史非标准 raw key 与 `canonical_raw_title` 重复前缀边界（见 residual_risk）；3 个 `test-merge-guarded*` 恒 ENOENT 等预存红测试已被 #4151 覆盖（R1 已记录）。两者均未被新建 raw issue，理由已写入 B1 brainstorms §Related findings。
