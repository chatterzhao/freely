# Implementation Decision Note
- issue_id: I-20261105T062203Z-A
- decision: 恢复模式复用 R3 的 `_wt_registered_dir()` 反查真实 dev 工位路径，恢复摘要与 scan_state_worktree 均使用该结果；反查失败硬报错
- why_this: `freely_wt_resolve_target_path()` 是「为即将新建的工位算目标路径」，目录已存在时追加 hash 后缀；恢复模式下 dev 工位本就存在，必然产出不存在的路径并污染 scan state，导致自动化按提示进入工位失败。用户要求「优秀的 freely」，运行时状态字段必须指向真实工位。
- alternatives_considered: 修改 `freely_wt_resolve_target_path()` 让目录存在时直接返回（会破坏 3 个正常新建调用点的冲突避让）；全局替换所有调用点（越界）；反查失败回退到推算路径（以另一种形式保留缺陷）；顺手修 #4201 顶层 return（越界，破坏单 issue 边界）。
- boundary_non_goals: 不改 `worktree-common.sh` / 正常创建 / test 工位新建 / legacy 补建的 resolve_target_path；不改顶层 `return 1`（#4201 独立）；不改 `_init_test_worktree_state()` 初始化契约；不改 R3 四态判定、no-op 与不一致拒绝。
- residual_risk: ①顶层 `return 1` 失败语义仍依赖 set -e（#4201 待修）。②`_wt_registered_dir()` 依赖 `git worktree list --porcelain` 文本解析，路径含空格时需改 `-z`（当前项目路径不含空格）。③2 个预存红测试归 #4151。
- verification: AT-001 RED 3 项失败（`-300efa56` 后缀污染）→ GREEN 8 项全通过；7 个相关回归测试（R1/R2/R3/Q1/Q2 + 命令生命周期）全 PASS；check-epics-map 对齐；R2 物化 H1 自举验证通过。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；已覆盖的 #4201 顶层 return、#4151 预存红测试、#4192 seed 声明均不重复立项。
