# Implementation Decision Note
- issue_id: I-20261105T062506Z-A
- decision: seed manifest 声明 bootstrap（copy/required=false），打包前置只读一致性检查保证 gitignored allowlist 条目都有 seed 声明
- why_this: 打包白名单与 seed 清单各自维护，导致任何新工位里的打包都因缺 gitignored 文件而失败，且失败原因与被测代码无关。用户要求「优秀的 freely」，这类清单漂移必须由机器约束而不是靠人记住。
- alternatives_considered: 把 bootstrap 改成 tracked（越界）；检查放在打包后（太晚）；seed 设 required=true（干净 clone 上 wt-create 整体失败，退化）；批量改写历史工位（高风险无收益）；把检查做成改写清单的动作（违反只读边界）。
- boundary_non_goals: 不改 `worktree_seed.py` / `wt-create` / `_init_test_worktree_state()` / allowlist 内容；不改输出路径守卫与 allowlist 复制循环；不改顶层 `return 1`（#4201）、R3 四态、R4 反查、Q2 标题契约。
- residual_risk: ①顶层 `return 1` 仍待 #4201 修。①b 干净 clone 上 seeder 仍会因既有的 `.freely/agent-table.toml required=true` 失败；本 PR 不改变该既有约束，评审判定证据不足以另立新 issue。②checker 在 checker 脚本缺失的旧安装态会跳过（兼容性折中），主仓库打包仍由 allowlist 校验 fail-closed。③`git check-ignore` 依赖 git 元数据，非 git 目录下判定为「非 ignored」，但打包命令本就在 git 工作树中执行。
- verification: AT-001 RED 11 项失败 → GREEN 13 项全通过；真实项目 parity 检查 `1 ignored / 0 undeclared`；最小 seed 项目真实打包成功；新增未 seed 条目被点名拦下；7 个相关回归基线对比 0 新增失败；R5 工位残留用封装 seeder 补齐后输出守卫 PASS；check-epics-map 对齐。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；相邻现象已被 #4201 / #4151 / #4146 / #4157 覆盖，未重复立项。
