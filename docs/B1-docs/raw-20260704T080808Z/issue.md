---
local_id: raw-20260704T080808Z08Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '3727'
    url: https://github.com/chatterzhao/freely/issues/3727
    synced_at: ''
  gitee:
    issue_id: IJYS3F
    url: https://gitee.com/zhaoquan/freely/issues/IJYS3F
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-04T08:08:29Z'
updated_at: '2026-07-04T08:47:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n
## 问题

当前一个项目只有一个 ACP bridge，所有 agent 共享 manager 的 tool/slot。agent-table.toml 中 worker/reviewer 即使配置了不同的 slot 也无效。

需要支持:
1. 同 base_tool 不同 slot: manager=opencode-apikey-ds-flash, worker=opencode-apikey-openai-gpt
2. 不同 base_tool: manager=opencode, worker=claude

## 架构方向

将 ACP bridge 与项目解绑 → 与 base_tool 绑定:
- daemon 启动时，扫描 agent-table 中所有不同的 base_tool
- 每个 base_tool 起一个独立的 ACP bridge
- agent 创建 session 时，根据其 slot 的 base_tool 连到对应的 bridge

## 与 raw-20260704T064539Z39Z 的协调

两个 issue 需协同设计:
- raw-20260704T064539Z39Z (本期): 统一 session 管理方法 acp_session_connect()
- 本 issue (下期): 多 bridge 并行

acp_session_connect() 需要知道: 当前 agent 的 slot → base_tool → 哪个 bridge socket。本期设计时预留 bridge 选择参数。

## 设计问题

1. 多 bridge 的启动时机和生命周期管理
2. bridge socket 的命名/寻址（按 base_tool 区分）
3. slot → base_tool → bridge 的路由
4. 同 tool 不同 slot 的 fork: 能否跨 slot fork? 同一个 opencode bridge，不同 slot 的 session 之间 fork?
absorbed_into: I-20260704T080808Z-A
