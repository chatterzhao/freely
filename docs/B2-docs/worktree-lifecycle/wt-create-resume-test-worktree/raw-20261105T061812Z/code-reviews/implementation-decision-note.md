# Implementation Decision Note
- issue_id: I-20261105T061812Z-A
- decision: pre-flight 以「git 实际登记的工位目录 + test-gate.env 初始化标记」判定完成态，恢复路径按缺失项分别补建
- why_this: 分支存在不等于工位可用；旧判定只看分支，会把「工位目录被删」与「Step 2 半初始化」都误判为完成并 no-op exit 0，后续 B1/B2/测试全部落空。用户要求「优秀的 freely」，工具链的中断恢复必须可自愈。
- alternatives_considered: 用 `freely_wt_resolve_target_path()` 推算目录（错：那是新建目标语义，目录已存在会加 hash 后缀，正是 R4 根因）；新增独立 marker 文件（引入双真源）；整条重建工位（破坏正常恢复路径语义）；顺手修 R4 与 #4201（越界，破坏单 issue 边界）。
- boundary_non_goals: 不改 `worktree-common.sh` / `freely_wt_resolve_target_path`；不改 `_update_scan_state` 与恢复摘要的路径解析（R4/#4191 独立）；不改顶层 `return 1` 三处（#4201 独立）；不改 `_init_test_worktree_state()` 的初始化契约。
- residual_risk: ①恢复摘要仍可能打印带 hash 后缀的 dev 路径（R4 待修，本轮明确未触碰）。②顶层 `return 1` 失败语义仍依赖 set -e 隐式兜底（#4201 待修）。③2 个预存红测试归 #4151。
- verification: AT-001 RED 6 项失败 → GREEN 13 项全通过；CASE A/B/C/D 四种残留态在隔离 git 仓库真实执行；4 个既有 wt-create 回归基线对比 0 新增失败；check-epics-map 对齐；R2 物化 H1 自举验证通过。
- self_bootstrap_findings: 顶层 `return 1` 缺陷 → 证伪 #4153（方向相反）与 #4157（不同文件）后用 `./bin/freely feedback` 创建 `raw-20261106T084804Z` / #4201 / IKTHI3，排入 goal R6.5；2 个预存红测试归 #4151，未重复建 issue。
