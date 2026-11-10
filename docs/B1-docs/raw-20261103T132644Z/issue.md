---
schema_version: '1'
local_id: raw-20261103T132644Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132644Z-A
platform_ids:
  github:
    issue_id: '4157'
    url: https://github.com/chatterzhao/freely/issues/4157
    synced_at: ''
  gitee:
    issue_id: IKSPQF
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQF
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132644Z/issues/I-20261103T132644Z-A.md
last_synced_comment_at:
  github: '2026-11-10T11:49:16Z'
  gitee: '2026-11-10T11:49:16Z'
hash: ''
created_at: '2026-11-03T13:26:44Z'
updated_at: '2026-11-10T11:57:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261103T132644Z-A
source_candidate: ''
completed_at: '2026-11-10T11:49:16Z'
closeout_note: ''
---

# fix: 补失败语义与可观测性缺口

workflow_kind: fix

## 根因
失败被表达成「正常结束」或「降级告警」，且跨进程无关联 id；运维面若干「无界 / 无守卫」项叠加（日志、凭据、打包路径、环境前置）。

## 证据
- `freely:23828-23833`：工具不可用且无恢复路径时 `log_warn ... will now stop` 后 `exit 0` → 外层（systemd / tmux）视为正常退出，不触发重启策略。
- `bin/freely-watchdog` 自身失效无人发现：`tail -f` 目标不存在 → `pipefail` 让脚本静默非零退出；`PRE_CHECK_MAP` `return 1` 在 `set -e` 下结束 `while` 子壳 → 第一次违规后 watchdog 死亡；`:10` 是第四套 worktree 根推导；无 pid、无守护。
- `bin/freely-cycle:46,109,114` 全部 `2>/dev/null`，`:52 except: rows=[]` → a2a 查询坏掉时输出 `{"worker_state":"unknown","suggested_action":"continue"}`，manager 无法区分「没 worker」与「查询坏了」，导致空转。
- 可观测性：`append_runtime_event:1436-1452` 格式 `ts event=name k=v`，无 severity、无 trace / span id，120 个调用点只有 32 处带 `raw_key=`；`%q` 转义让日志难被机器解析。正面：`lifecycle-trace.log` + `.seq` 有序、崩溃有 `crash-*.log`、`workcell-state.env` 保留 `LAST_EXIT_REASON`。
- 日志无界：有轮转的只有 5 个固定名日志（`freely:22806-22810` → `_rotate_log:8753-8766`）；`cycle-$ts.log`、`cycle-worker-$ts.log:13311`、`crash-*.log:23685` 无轮转（实测 `.freely/logs` 71 文件 / 4.1MB）。
- 凭据暴露面：`ai-cli:927` 把 `api_key` 放 **argv**（同机 `ps -ef` 可见）；`ai-cli:2392` 支持 `--key` 进 shell history；`gitee-issue.py:120-127` 把 `access_token` 放 URL query。正面：落盘权限正确（`ai-cli:1002 chmod 600`、`:1053 chmod 700`）。
- 打包无守卫：`bin/freely-package:68,110,134` `rm -rf "$OUTPUT"` 直接用 `--output` 原值（无空 / `/` / `$HOME` 校验）→ `--output ~` 清空家目录；`:107-141` 按 allowlist `cp -R` 会把 `__pycache__/` 与死代码 `task-lifecycle-scan.bak.py`（2,007 行）一起装出去。
- 环境前置缺失：13 个文件 `import tomllib`（3.11+），全仓无 python 版本检查 → 3.8 / 3.9 上首跑 `ModuleNotFoundError`，报错点离真实原因很远；DB 无 `schema_version` / `PRAGMA user_version`，迁移包在 `except: pass`（`freely_db_manager.py:276-297`）。

## 影响
失效被记成正常，重启策略不触发；排障只能靠人拼文件、跨进程无法关联；一次 `--output` 误用可能清空家目录；新机器首跑报错点远离真实原因。单项都不算 P0，但共同构成「出问题后无人知道」的运维底座。

## 修复方案（分项，可各自独立合并）
1. `freely:23833` 的 `exit 0` 改 `exit 1`，或写显式 `degraded` 状态供外层识别。
2. `bin/freely-watchdog` 加 pid + 简单守护，或明确降级为「人工诊断工具」（改文档、不加守护）；`PRE_CHECK_MAP` 的 `return 1` 改为 `continue` + 计数。
3. `append_runtime_event` 增加 `severity` 与 `trace_id`，并把 `raw_key=` 补到剩余 88 个调用点。
4. `cycle-*.log` / `crash-*.log` 接入 `_rotate_log`。
5. `bin/freely-package:68` 的 `--output` 加 `/`、`$HOME`、`..` 守卫（空值已由 `:57-59` 兜底为默认目录，不构成风险）；该路径安全问题已拆至 #4158。本 issue 只保留「打包排除 `__pycache__/` 与 `*.bak.py`」。
6. 加 python 版本前置检查（`freely doctor` 与 daemon 启动各一处）；DB 加 `PRAGMA user_version` 且迁移失败不吞。
7. 凭据从 argv 改 stdin / env；`gitee-issue.py:120-127` 的 token 从 query 改 `Authorization` 头。
8. 修 `.env.example`（指向 `config.toml` + `toml2env`）；`skills/README.md` 补齐 7 个执行面 skill 的角色归属。

## 验收标准
- RED：`grep -n "will now stop" freely` 对应分支返回 1（当前 0），有测试断言退出码。
- RED：`bin/freely-package --output /` 与 `--output ~` 均被拒绝并报错；当前会执行 `rm -rf /` / `rm -rf $HOME`。`--output ""` 不属于风险路径（`:57-59` 已兜底），该安全项已拆至 #4158。
- RED：stub 掉 `tomllib`（或 3.9 环境）启动 daemon，断言在启动早期给出「需要 Python >= 3.11」的明确错误，而不是 `ModuleNotFoundError` 堆栈。
- GREEN：`append_runtime_event` 输出含 `severity=` 与 `trace_id=`，可用 `awk` 稳定解析。
- GREEN：`.freely/logs` 下 `cycle-*` / `crash-*` 有轮转上限（配置项或固定保留数）。

### comment-20261110T114916Z
- source: system
- event: promote_finalized
- children: ["I-20261103T132644Z-A"]

拆解为以下任务:
1. [I-20261103T132644Z-A](will-be-updated)
