# Implementation Decision Note
- issue_id: I-20261107T090847Z-A
- decision: governance-check 的 merge_path allowlist 兼容两代合法值，并修复 set -e 提前退出使 receipt 审计与汇总总能执行；不删除或削弱任何既有检查
- why_this: README 宣称的第三层 post-merge audit 对 675+ 个合法 `pr-merge-guarded` merge 误报、又因控制流提前退出实际不运行，形成「既有假阳性又不生效」双重失真，R9 补上第一层后第三层必须补齐。
- alternatives_considered: 只认新值（历史 1312 次旧值不兼容）；改 `pr-merge-guarded` 写入值（制造第三代不一致）；删检查或整体 `|| true` 掉检查链（削弱治理）；把 audit 包 subprocess 吞错误（掩盖）。
- boundary_non_goals: 不改 `pr-merge-guarded` / `commit-msg.sh` / `post-checkout` / backfills 与 break-glass ledger；不批量改写历史 merge；不夹带 #4147 / #4151 / R11。
- residual_risk: ①完整 governance-check 在真实仓库仍有大量预存 `[FAIL]`（治理文档缺口，#4151 家族），本 PR 只保证它们被完整报告且审计跑完，不逐条修复。②`.githooks/bin/git` 未接 PATH（R8 残余）。③2 个预存红测试归 #4151。
- verification: AT-001 基线 RED 3 失败 / 5 既有能力 PASS → GREEN 全通过；真实 develop HEAD 上修复后 audit `PROBE_ERRORS=0`（基线误报 unknown）；完整脚本输出 `Governance check failed with N error(s)` 汇总行（基线静默退出、0 行输出）；9 个回归以未修改 develop HEAD 基线对比 0 新增失败；check-epics-map 对齐。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；本 issue 自身是 R9 评审期间按自举规则创建并排入 goal R9.5 的闭环，未重复立项。
