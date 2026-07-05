---
local_id: raw-20260704T164337Z37Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3730'
    url: https://github.com/chatterzhao/freely/issues/3730
    synced_at: ''
  gitee:
    issue_id: IJYTFJ
    url: https://gitee.com/zhaoquan/freely/issues/IJYTFJ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-04T16:43:58Z'
updated_at: '2026-07-04T16:43:58Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n
## 背景

PR #3728+#3729 重构后，有遗留清理工作：

## 1. 彻底删除 6 个 DEPRECATED 函数 (watchdog_sse.py)

0 外部调用者，全部已被 acp_session_connect 替代:
- _acp_session_new()
- _acp_session_fork()
- _acp_session_resume()
- _acp_session_prompt()
- _should_use_fork()
- _create_reviewer_session()

## 2. acp-bridge.py 的 _pid_file/_socket_path 调用仍用旧签名

line 119, 583, 738, 769, 771, 780, 795, 796 共 8 处调用没传 base_tool 参数。
需要传入 base_tool（从 --base-tool CLI 参数获取），否则生成旧格式 socket/pid。

## 3. freely shell 中 agent_assign 裸调用迁移

8 处直接调 agent_assign 应迁移到 acp_session_register:
- line 5994: worker dual-write
- line 18774, 18808, 18839, 18901: _ensure_reviewer_agent + _acp_session_new/fork

## 4. _acp_bridge_health_check 未更新签名
absorbed_into: I-20260704T164337Z-A
