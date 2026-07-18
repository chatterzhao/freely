---
local_id: raw-20260718T004314Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260718T004314Z-A
platform_ids:
  github:
    issue_id: '3987'
    url: https://github.com/chatterzhao/freely/issues/3987
    synced_at: ''
  gitee:
    issue_id: IK1VHQ
    url: https://gitee.com/zhaoquan/freely/issues/IK1VHQ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-18T00:43:38Z'
updated_at: '2026-07-18T00:43:38Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
docs/system/workspace/scripts/runtime/freely L2120 存在孤儿行 `_agent_env="$source_project/.freely/agent-id.env"`（commit aea0c5749 2026-06-27 坏编辑残留，缩进异常，赋值结果无人消费）。`source_project` 仅在 sync-tooling 函数族中定义；在 manager_worker_launch_state_reconcile_prompt_liveness 作用域未定义 → set -u 下 unbound variable 为 shell 级致命错误，绕过一切 `|| true` / `>/dev/null 2>&1` 防护直接杀死进程。

## 影响
daemon start / daemon status 只要 manager-worker-launch-state.env 存在且 continuity 条件满足即走到 L2120 → 整个 runtime 脚本静默退出 rc=1，无任何输出。实测 2026-07-18 00:27 起 runtime 无法重启（launch-state 含 round-078 残留 prompts 时路径必达）。正确的 _agent_env 逻辑在 manager_reconcile_agent_id_env() 内有默认参数，孤儿行纯多余。

## 修复方案
删除 L2120 孤儿行。RED=sourced probe 复现 'line 2120: source_project: unbound variable' + daemon start 静默 rc=1；GREEN=refresh 函数正常返回 + daemon start 通过该点。
