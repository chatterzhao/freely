# Implementation Decision Note
- issue_id: I-20261109T074900Z-A
- issue_path: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20261109T074900Z/issues/I-20261109T074900Z-A.md
- decision: 单一 `freely_escape_regex()`（Python re.escape + argv）供两处项目路径 pkill 使用；派发 CAS / SSE 收敛拆 #4254
- why_this: 项目路径含 `. + ( [` 等元字符时，直接拼进 `pkill -f` 正则会变成通配符，停止项目 A 可能误杀项目 B 的 A2A server；Python `re.escape` 覆盖完整元字符集合，argv 形式与 R22 已修的注入面一致，也不会被 R23.5 的 boundary lint 标记。
- alternatives_considered: ①手写 sed/bash 转义表（元字符易漏且与 lint 冲突）；②`pgrep -f` + PID 白名单（改变清理语义、需自排除）；③5 处 pkill 全改（另 3 处无外部路径，无收益）；④本轮做派发 CAS / SSE（真源未定位，需独立并发夹具）。
- boundary_non_goals: 3 处固定 pattern pkill 逐字不动；`|| true` / `2>/dev/null` / 正则其它字面量不动；不改启动锁与 DB 单实例。
- residual_risk: ①helper 每次调用起一个 python 进程，仅用于 stop 清理路径，频率极低；②`_project_re` 依赖 `project` 变量在调用点已解析为绝对路径（两处调用点均满足）；③面 1/2 真源需在 #4254 重新普查，不能照 issue 旧行号改。
- verification: AT-001 基线 RED `5 ok / 7 failed` → GREEN `12 ok / 0 failed`；真实 `pgrep -f` 反向 PoC；`bash -n`、`check-epics-map`、`bin/test-all --ci`、5 个相关回归基线对比 0 新增失败。
- self_bootstrap_findings: ①issue 正文的 `launch_sse_watchdog` / `_start_watchdog_sse_py` / `--state working` 在最新 develop **零命中**，R23.5 改过派发管线后旧行号全部失效，必须重新普查；②`pkill -f` 共 5 处，只有 2 处含 `${project}`，静态断言要精确到「含 --project」的站点，一刀切会误伤固定 pattern；③PoC 最初用 `+` 当元字符，因 `+` 是量词导致连自身都不匹配、对照组方向写反，改用 `.` 才呈现真实误杀形态；④`re.escape` 此前只在 python heredoc 内用过，shell 侧无 helper，本轮补齐单一真源。
