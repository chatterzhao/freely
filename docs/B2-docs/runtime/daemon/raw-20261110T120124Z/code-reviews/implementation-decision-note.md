# Implementation Decision Note
- issue_id: I-20261110T120124Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261110T120124Z/issues/I-20261110T120124Z-A.md
- decision: 一次闭合 #4157 剩余 6 项：watchdog 诊断化 + pid、事件 severity/trace_id、cycle/crash 按数量保留、打包排除缓存/死备份、Gitee token header + Codex key env、DB user_version + 迁移失败即抛
- why_this: 六项的共同模式是「失败或资源无界却不可见」。watchdog 会诈死；事件日志没有可过滤/可关联字段；cycle/crash 每次新文件永不清理；安装包把 `__pycache__` 与 `*.bak.py` 装出去；token 出现在 URL、key 出现在 `ps` 可见的 argv；DB 迁移错误被 `except: pass` 吞掉。这些都是运维面最贵的静默债。
- alternatives_considered: ①把 watchdog 做成受管守护——与 `sse-watchdog` / `ensure-manager` 职责重叠，且它本是人工诊断工具；②给 120 个调用点加 severity 参数——易漏且改动面大，改为函数内映射；③复用 `_rotate_log` 处理 cycle/crash——它是单文件大小轮转，语义不匹配；④改 package allowlist 排除——目录级 allowlist 无法表达文件级排除；⑤token 放 POST body——GET 请求无法用；⑥删掉 `--key`——破坏既有登录流程；⑦只加 user_version 不抛错——迁移仍静默。
- boundary_non_goals: 不改 `append_runtime_event` 签名、不改 `--key` CLI 语义、不改 #4158 的 output 守卫、不改 lifecycle-trace 的 seq 语义、不改 `_rotate_log`、不改 `ai-cli` 交互登录与槽位逻辑、不改 R23.5 派发契约。
- residual_risk: ①`--key` 仍会把 key 写进 shell history（用户显式输入路径，本轮未改；建议用交互输入）；②watchdog 仍是人工诊断工具，不是受管守护，进程死了不会自动拉起；③Gitee header 认证已用真实只读 `get` 验证，但若将来 API 只接受 query 需回退；④`user_version` 只到 1，后续 schema 变更需同步 bump；⑤日志保留按 mtime 排序，系统时间跳变时排序可能异常；⑥`crash-*.log.stdout` 不参与裁剪（与主 crash 日志同生命周期，数量上限约为 2N）。
- verification: AT-001 基线 RED `0 ok / 11 failed` → 工位 GREEN `11 ok / 0 failed`；真实 `gitee-issue.py get IKUEK0` header 认证返回 JSON；12 项回归 + `test-all --ci` `9 ok / 0 failed`；local 仅既有失败；三个 ACP/平台既有失败已用基线对比确认。
- self_bootstrap_findings: ①package 的 `refuse_dangerous_output` 用字符串前缀比较，macOS `/var` 与 `/private/var` 会让夹具误判，AT 必须 `resolve()`；②`refuse_dangerous_output` 先 `cd dirname`，输出父目录不存在时会拼出 `/2026...`，夹具要先建父目录；③ai-cli 里 `printf ... "$api_key"` 是函数返回值而非 argv，静态断言必须精确到 python 调用形态，否则会把安全代码误判成漏洞；④关闭 `except: pass` 时要区分「duplicate column 是预期」与「真失败」，否则迁移会在正常旧库上炸。

## Implementation Decision Note
- decision: 六项一次闭合，watchdog 诊断化、事件字段函数内生成、日志按数量保留、打包排除、凭据走 header/env、DB 版本化
- why_this: 失败与资源无界都不可见
- alternatives_considered: 受管守护 / 逐调用点加参数 / 复用 _rotate_log / 改 allowlist / token 进 body / 删 --key / 只加版本
- boundary_non_goals: 签名、CLI 语义、output 守卫、trace seq、交互登录均不动
- residual_risk: --key history、非守护、Gitee header 兼容、版本号维护、mtime 排序、stdout 副本
