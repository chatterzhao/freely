# Implementation Decision Note
- issue_id: I-20260708T183102Z-A
- decision: 修 6 处：pr-merge-guarded 读写路径对齐 + raw_key 定位；wt-close 跳过已有 platform_state: closed + 去掉 updated_at + 修正 I-* 路径 + 遇 diff 引导正规化而非 force。
- why_this: pr-merge-guarded 的读写路径不一致导致 issue-sync 静默失败（#1）。worktree 解析用分支名子串匹配不如 raw_key 精确（#2）。wt-close 的冗余 issue-sync（#3）和 force 引导（#4）导致正常流程阻塞和用户误操作。updated_at 时间戳（#5）和 develop 路径写入（#6）是同一类 bug。
- alternatives_considered: (1) 只修路径不改 wt-close → wt-close 仍会冗余执行；(2) 完全移除 wt-close issue-sync → force-close 场景需要它；(3) 保持现状 → 每个 PR 都会被 diff 阻塞。选择：保留 wt-close issue-sync 但加 condition guard。
- boundary_non_goals: 不改 pr-create-guarded 的 issue-sync 流程；不改 scan 的分类逻辑；不改 worktree-common.sh 的 dev↔test 一致性检查。
- residual_risk: pr-merge-guarded 的 yaml 解析依赖 PyYAML——如果模块不可用，phase_status 为空会 fallback 到 raw/"" case，仍会执行 issue-sync close（行为不变，不算回退）。
