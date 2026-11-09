# Implementation Decision Note
- issue_id: I-20261103T132636Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132636Z/issues/I-20261103T132636Z-A.md
- decision: 外部值一律走 `sys.argv`（`python3 - <<'PY'` 静态脚本体）；`sed -i` 统一 `-i.bak` 且同命令删备份
- why_this: 分支名是外部输入，`git check-ref-format` 允许 `'`/`;`/`$`/反引号；插值进 `python3 -c` 等于执行审查对象的代码。`sed -i ''` 是 BSD-only，GNU 下把 `''` 当文件名并让 `set -e` 在**评审已记录后**中止。
- alternatives_considered: ①`printf %q` 后仍走 `python3 -c`——转义规则与 python 字符串字面量不是同一套；②一次性改完 195 处 `python3 -c`——需逐处判断是否真有外部值，应先加 lint 再收敛；③`sed -i.bak` 但延迟清理——中间失败/并发会残留；④用 python 替代 sed——改动面更大。
- boundary_non_goals: 不改 sed 的替换表达式与目标；不改 python 片段逻辑；不动状态文件 `source`、TSV 通道、其余 `python3 -c`（#4247）。
- residual_risk: ①仍有多处 `python3 -c` 把变量插值进**双引号**脚本体，虽然需要外部值直接可控才可利用，但边界尚未机械约束（#4247 的 lint）；②`sed -i.bak` 在文件位于只读目录时会失败（与旧行为一致）；③argv 形式下 `sys.argv[2]` 若为空需调用方保证，本轮两处调用方都有前置校验。
- verification: AT-001 基线 RED `4 ok / 3 failed`（PoC 输出 `fix/x\nPWNED`）→ 工位 GREEN `7 ok / 0 failed`（argv 输出 `GOT=fix/x');print('PWNED');#`）；`bash -n` 通过；`bin/test-all --ci` 与 4 个相关测试全绿。
- self_bootstrap_findings: ①issue 报的 3 处高危入口实际只剩 2 处（行号漂移），但 `pr-review-guarded` 的第二处在 Step 3.5，issue 未点出；②基线 `wt-close:1251` 已用 `sed -i.bak` 却从不清理——说明项目里混用两种语法，且「清备份」这个约束此前无人守；③PoC 若不真的执行，测试就只是「grep 一下」，因此 AT 里把「旧形式确实执行」也作为断言。

## Implementation Decision Note
- decision: argv 传外部值；`sed -i.bak` + 同命令清理
- why_this: 分支名可注入 → RCE；BSD sed 在 GNU 下中止流程
- alternatives_considered: printf %q / 一次改完 195 处 / 延迟清理 / python 替代 sed
- boundary_non_goals: sed 表达式、python 逻辑、状态文件、TSV、其余 python -c 均不动
- residual_risk: 双引号内插值仍在、只读目录、argv 空值依赖调用方
