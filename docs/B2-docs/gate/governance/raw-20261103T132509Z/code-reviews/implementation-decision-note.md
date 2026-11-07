# Implementation Decision Note
- issue_id: I-20261103T132509Z-A
- decision: 接线孤儿 commit-msg.sh（方案 1），并用受控 handshake 让自填 trailer 也被拒；trailer 校验收窄到 develop/main 以免自锁 test 工位
- why_this: 130 行实现无人执行、README 宣称三层实际缺第一层，手工 merge 后自填 trailer 即可伪造合规，属「看起来有、实际不跑」的假安全感。依赖 R8 已完成的 fail-closed shim 模板。
- alternatives_considered: 删除实现并把 README 降级为仅事后审计（削弱治理）；保留 test-pre-merge-* 的 receipt 要求（自锁每轮 sync merge）；只校验 trailer 文本（挡不住自填）；改 pr-merge-guarded 写入值（675+ 历史 merge 已用 pr-merge-guarded，制造新不一致）；夹带修 governance-check（越界到 R9.5）。
- boundary_non_goals: 不改 `post-checkout` / `governance-check` / `pr-merge-guarded` 一个字节；不批量改写历史 merge；不删除任何既有检查；不夹带 #4211 / #4151 / R11。
- residual_risk: ①第三层 `governance-check` 仍只认旧 receipt 值且被 `set -e` 提前退出 → 已立项 #4211（goal R9.5），本 PR 不修。②`.githooks/bin/git` 未接 PATH（R8 残余风险）。③5 个预存红测试归 #4151 / R1。
- verification: AT-001 基线 RED 9 失败 / 5 既有能力 PASS → GREEN 14/14；隔离仓库 6 场景（缺 trailer 拒绝并打印原因、自填 trailer 被 handshake 拒、合法 guarded merge 通过、test 沙箱 merge 通过、普通 commit 通过、通用规范生效）；真实历史 25 条 commit 0 违规；13 个回归以未修改 develop HEAD 基线对比 0 新增失败；check-epics-map 对齐。
- self_bootstrap_findings: 评审发现 `governance-check:369` 的 merge_path allowlist 与 `pr-merge-guarded` 写入值不一致且审计层因 `set -e` 提前退出从未运行；逐条证伪 #4147（本轮）/ #4151（测试执行链）均不覆盖 → 用 `freely feedback` 创建 `raw-20261107T090847Z` / #4211 / IKTNCE（P1），排入 goal R9.5，本 PR 不夹带。
