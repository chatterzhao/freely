---
raw_id: raw-20261109T074900Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 覆盖域（issue 3 条修复面）

| # | 面 | develop `d82ba3e46` 实测 | 本轮 |
|---|---|---|---|
| 1 | 派发非幂等（两条派发器、无 CAS） | `--state working` / `launching` / `launch_sse_watchdog` / `_start_watchdog_sse_py` 在 `freely` **零命中**；R23.5 刚改过派发管线，状态机可能已迁移 | ➡ 拆 **#4254 / IKUA5K** |
| 2 | SSE 三重实例 + watch-in-watch | 同上，issue 正文行号全部漂移 | ➡ 拆 **#4254 / IKUA5K** |
| 3 | `pkill -f` 未转义项目路径 | **5 处**；其中 `:9007` / `:22349` 直接把 `${project}` 拼进正则 | ✅ 修 |

## 真源普查（不照 issue 旧行号改代码）

- `grep -n "pkill -f" freely` → :9007 / :14886 / :22349 / :22394 / :22432。
- 只有 :9007 与 :22349 含 `--project.*${project}`；另 3 处是固定 pattern 数组（`$p` / `$_p`），不含项目路径，不在本轮范围。
- `launch_sse_watchdog` / `_start_watchdog_sse_py` / `--state working` / `launching` 在最新 develop **均零命中** —— issue 正文的 `:8913` / `:22238` 等行号已失效，且 R23.5 改动了 `consume_delegate_workers` 的派发管线。因此面 1/2 不能按旧描述实现，必须先重新定位真源，独立成轮。

## scope 收敛（沿用 R22 / R23.5 先例）

本轮只做面 3，理由：
- 单点、后果直接（停止项目 A 可能误杀项目 B 的 A2A server）、可静态 + 真实 `pgrep -f` 反向 PoC 验证。
- 面 1/2 是状态机与守护进程链路改动，需要独立真源普查、并发夹具与端到端验证；混进本 PR 无法证明「行为不变」。
- 按用户「期间发现问题自举用 feedback 建 raw issue」的要求，已用 `./bin/freely feedback` 拆出 `raw-20261110T064015Z` / #4254 / IKUA5K（P1），正文明确写「必须先重新做真源普查，不要照旧行号改」。

## 方案方向

- 新增单一 `freely_escape_regex()` helper，用 `python3 - "$1" <<'PY'` + `re.escape(sys.argv[1])`：与 R22 建立的 argv 安全形式一致，避免手写不完整的元字符表，也不引入新的 `python3 -c` 插值（R23.5 刚加的 boundary lint 会盯着这种形态）。
- 两处 pkill 各调用一次 helper，把结果放进 `local _project_re`，正则其余部分逐字不动。
- 不改用 `pgrep` + 显式排除：那会改变「按命令行模式清理残留进程」的既有语义，且要处理 PID 自排除，改动面更大。

## fidelity 基线

- 对照组在 RED 必须 PASS：未转义路径确实会匹配同前缀的另一个项目、固定 pattern pkill 站点仍在、真实 `pgrep -f` 用未转义 pattern 命中 ≥2 个进程、转义后只命中 1 个、`bash -n` 通过。
- PoC 要用**真实进程**：起两个带标记的 python 子进程，命令行分别含 `proj.v1` 与 `projXv1`，用 `pgrep -f` 实测命中数；测试结束 `terminate()` 清理，不调用 `pkill`。
- 断言必须覆盖「转义后仍匹配自己的项目」（不能因转义变成永不命中）。

## 价值判定

- 不过时：两处未转义 pkill 实测仍在；项目路径含 `.` / `+` 很常见。
- 不重叠：#4156/R22 修的是 `pr-review-guarded` 分支名插值；R23.5 修的是 TSV 派发；#4155/R19 修的是启动锁与 DB 单实例。
- P1：误杀其它项目的 A2A server 会让对方 daemon 控制面失效。

## 被否决

- **手写 sed/bash 转义表**：元字符集合容易漏（尤其 `(` `[` `$` `*`），且会与 R23.5 的 lint 形态冲突。
- **改用 `pgrep -f` + PID 白名单**：改变既有清理语义，需处理自排除，改动面更大。
- **把 5 处 pkill 全改**：另 3 处是固定 pattern，不含外部路径，改了属于无收益的行为变更。
- **本轮顺带做派发 CAS / SSE 收敛**：真源未定位、需并发夹具，独立成轮（#4254）。

## Related findings

- `freely` 里 `re.escape` 此前只在 python heredoc 内部用过（:21378），没有 shell 侧 helper；本轮补上后，后续所有「外部路径进正则」的站点都有单一真源。
- PoC 最初用 `+` 作元字符，结果 `+` 作为量词导致连自身进程都不匹配，方向写反；改为 `.` 后未转义 pattern 才会误命中同前缀 sibling，这才是真实风险形态。
