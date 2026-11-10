# Pre-Tests: 运维底座六项收口
- issue_id: I-20261110T120124Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: watchdog 缺日志仍存活并持有 pid；`append_runtime_event` 输出 severity/trace_id；cycle/crash 日志保留上限；打包产物无 `__pycache__`/`*.bak.py`；Gitee token 走 Authorization header；Codex key 走 env 不进 argv；DB 记录 `user_version` 且迁移失败即抛
- acceptance_target: 六类「失败/资源无界却不可见」在真实执行路径上可观测、有界
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: `git archive develop` 隔离基线 / 工位真源；行为测试用临时项目 + `source runtime/freely`、60 个临时日志文件、临时 fake-root 打包、临时 pid/log 启动 watchdog；真实 Gitee 只读 `get` 一次验证 header。不写真实安装态、不碰真实 `.freely`、不改系统 PATH、不杀本机进程
- required_evidence: 7 静态 + 4 行为 = 11 项全 GREEN；基线 RED `0 ok / 11 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-obs-ops-backlog.py
- test_command: python3 docs/system/workspace/scripts/tests/test-obs-ops-backlog.py
- expected_output: SUMMARY: 11 ok, 0 failed
- expected_RED_output: SUMMARY: 0 ok / 11 failed
- actual_RED_output: develop `83ba84a74` 基线 + 最终版 AT-001 → `SUMMARY: 0 ok, 11 failed`（AT-001-RED.log）；含 watchdog 缺日志即退、事件无 severity、无裁剪函数、打包带 `__pycache__`、token 在 query、key 在 argv、DB 无 user_version。
- actual_output: 工位同一断言 → `SUMMARY: 11 ok, 0 failed`（AT-001-GREEN.log）；另用真实 `gitee-issue.py get IKUEK0` 走 header 认证返回 JSON。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261110T120124Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 静态组逐项断言接线（watchdog 的 `tail -F`/建日志/pid/`|| continue`；事件函数切片内 severity+trace_id；裁剪函数与 cycle/crash 调用；package 排除；gitee header 且无 `query["access_token"]`；ai-cli env 且 python argv 无 key；DB `PRAGMA user_version` 且迁移段无 `except: pass`）。行为组：①临时项目 source 后写事件，断言输出可被 awk 解析出 `severity=`/`trace_id=`；②60 个 cycle 日志裁剪到 50；③fake-root 打包后产物无缓存/死备份；④缺日志启动 watchdog 1.2s 后仍存活且 pid 文件非空。
- red_how: `git archive develop | tar -x -C /tmp/r26-base`，只注入最终版 AT-001，`--source-dir` 运行。
- implementation_findings: ①AT 的 `--output` 必须用 resolve 后的临时路径（macOS `/var` → `/private/var`），否则 package 的字符串前缀守卫会误判；②package 的输出父目录必须先 `mkdir`，否则 `refuse_dangerous_output` 的 `cd dirname` 失败会拼出 `/2026...`；③ai-cli 的 `printf ... "$provider_name" "$base_url" "$api_key"` 是函数返回值（stdout），不是 argv，断言必须精确到 python 调用的 argv 形态，否则误报。

## End-to-End
- acceptance_target: 真实 runtime/package/gitee 路径
- testing_layer: end-to-end
- target_environment: 临时项目 + fake-root + 本地 stub/真实只读 API
- required_evidence: AT-001（4 项行为）+ `bin/test-all --ci`
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-obs-ops-backlog.py
2. bin/test-all --ci

## Unit
- acceptance_target: 六项接线与负向断言
- testing_layer: unit
- target_environment: fix/raw-20261110T120124Z-obs-ops-backlog
- required_evidence: AT-001（7 项静态）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-obs-ops-backlog.py

## Integration
- acceptance_target: DB / 派发 / 契约 / CLI / 平台 / 打包不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 12 项回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-db-single-writer.py
2. python3 docs/system/workspace/scripts/tests/test-dispatch-cas-sse-singleton.py
3. python3 docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py
4. python3 docs/system/workspace/scripts/tests/test-contract-single-source.py
5. python3 docs/system/workspace/scripts/tests/test-fail-semantics-preflight.py
6. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
7. python3 docs/system/workspace/scripts/tests/test-install-state.py
8. python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
9. bash docs/system/workspace/scripts/tests/test-availability-watchdog-path-resolution
10. bash docs/system/workspace/scripts/tests/test-cli-help-contracts
11. python3 docs/system/workspace/scripts/runtime/gitee-issue.py get IKUEK0（真实只读）
12. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 夹具在临时目录构建，不写真实安装态；watchdog 用临时 pid/log 启动并 terminate；真实网络只做一次 Gitee 只读 `get`（验证 header），不创建/修改平台数据。
- real_environment_reason: AT-001 RED `0/11` → GREEN `11/0`；DB/派发/契约/CLI/安装态/平台探针/并发回归全绿；`test-all --ci` `9 ok / 0 failed`；local 唯一失败是既有 `test-github-label-autocreate.py`。三个平台/ACP 相关既有失败（`test-gitee-issue`、`test-ai-cli-codex-apikey-slot-bundle-switch`、`test-ai-cli-login-codex-apikey-direct-args`）在 develop 基线同样失败，已用基线快照对比确认。
