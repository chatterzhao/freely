---
raw_id: raw-20261110T120124Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 前置评审（逐项在目标文件上核对，不照抄 #4157 旧行号）

| 分项 | 真源 | 结论 |
|---|---|---|
| 1 watchdog | `bin/freely-watchdog`（全文 60 行） | `tail -f` 缺文件 + pipefail → 立即死；`PRE_CHECK_MAP` 的 `return 1` 在 `while` 子壳 + `set -e` → 首次违规即死；`local wt="$ROOT_DIR/../freely-worktrees"` 是第四套根推导；无 pid。**成立** |
| 2 severity/trace_id | `runtime/freely:1565 append_runtime_event` | 只有 `ts event k=v`，无 severity/trace_id。**成立** |
| 3 日志轮转 | `_rotate_log:9040`；`cycle_log:23380`；`crash_log:24001` | `_rotate_log` 只裁单个文件，cycle-*/crash-* 是每次新文件，从未清理。**成立** |
| 4 打包卫生 | `bin/freely-package` 目录分支 | `cp -R` 后无排除；`count` 还按源目录统计。**成立** |
| 5 凭据 | `gitee-issue.py:125` 把 token 塞进 query；`ai-cli:928` 用 `python3 - ... "$api_key"` 传 argv | 两处都成立；`--key` 进 shell history 是用户显式输入路径，本轮保留兼容，只用 env 传递落盘，**不改变 CLI 参数语义**（文档标注） |
| 6 DB | `freely_db_manager.py` 迁移两处 `except Exception: pass`（14 列循环 + `review_stage`） | 无 `user_version`，迁移失败静默。**成立** |

`--output /` `~` 守卫**已由 #4158 落地**（`refuse_dangerous_output`），不在本轮重复。

## 方案方向

### 分项 1：诊断工具而不是伪守护（选中）
- 建日志文件、`tail -F`、`PRE_CHECK_MAP ... || continue`、pid + 二次启动 no-op、退出清理 pid。
- 不加 systemd 式守护：该脚本本来就是人工诊断工具，加守护会与 `sse-watchdog` / `ensure-manager` 的职责重叠（那两条链路已有单实例）。
- 否决：把 `return 1` 改成 `return 0`（丢失失败语义）；只改 `tail -f` 为 `tail -F`（首次违规仍会死）。

### 分项 2：函数内生成，不改 120 个调用点（选中）
- `severity` 由事件名映射（error / warn / info），`trace_id` 取 `FREELY_TRACE_ID` 或 `FREELY_RUN_ID` + 日期。
- 否决：给每个调用点加参数（120 处、易漏）；只加 trace_id 不加 severity（无法过滤）。

### 分项 3：按数量裁剪（选中）
- 新增 `_prune_logs_by_count`，cycle 保留 50、crash 保留 20，可用环境变量覆盖。
- 否决：复用 `_rotate_log`（它是单文件大小轮转，语义不匹配）。

### 分项 4：复制后排除（选中）
- `cp -R` 后删 `__pycache__` 目录与 `*.bak.py`，`count` 改为统计产物。
- 否决：改 allowlist（目录级 allowlist 无法表达文件级排除）。

### 分项 5：token 走 header、key 走 env（选中）
- `gitee-issue.py` 用 `Authorization: Bearer <token>`；已用真实只读 `get IKUEK0` 验证通过。
- `ai-cli` 的 codex bundle 写入改为 `FREELY_CODEX_API_KEY` 环境变量 + Python 从 `os.environ` 读取，不再出现在 `ps` 的 argv。
- 否决：把 token 放 POST body（GET 请求无法用）；删掉 `--key`（破坏既有登录流程）。

### 分项 6：`PRAGMA user_version` + 迁移失败即抛（选中）
- `SCHEMA_VERSION = 1`；打开库时若 `user_version > 1` 直接报错（拒绝旧版本改新库）；迁移失败 `raise RuntimeError`，`review_stage` 的 duplicate-column 是唯一允许的例外。
- 否决：只加 user_version 不抛错（迁移仍静默）；只抛错不加版本（无法发现降级）。

## fidelity 基线

- RED 必须证明：watchdog 缺日志即退、无 pid；事件无 severity/trace_id；无裁剪函数；打包产物含 `__pycache__`/`*.bak.py`；token 在 query；key 在 argv；DB 无 user_version 且迁移吞错。
- GREEN 必须证明 7 项静态 + 4 项行为（事件字段、保留数、打包产物、watchdog 存活）全绿。

## 价值判定

六项共同构成「出问题后无人知道」的运维底座：watchdog 诈死、日志无法过滤/关联、磁盘无限增长、安装包带缓存与死代码、同机可见密钥、迁移失败静默。均已在 develop `83ba84a74` 上实测成立。
