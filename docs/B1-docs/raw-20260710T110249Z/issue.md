---
local_id: raw-20260710T110249Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260710T110249Z-A
platform_ids:
  github:
    issue_id: '3871'
    url: https://github.com/chatterzhao/freely/issues/3871
    synced_at: ''
  gitee:
    issue_id: IK0950
    url: https://gitee.com/zhaoquan/freely/issues/IK0950
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T11:03:11Z'
updated_at: '2026-07-10T11:03:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

Manager AI cycle 持续被 rc=143 (SIGTERM) 杀死，即使 idle timeout fix 已生效。

## 初步发现

monitor-ai-acp.sh 的 bridge-dead 检测 (line 427) 调用  不带 base_tool 参数——返回不带后缀的默认 PID 文件路径。但自从 per-tool bridge (PR #3842/3849) 后，PID 文件是 、、 格式。默认 PID 文件不存在或已过期。

## 需要研究

1. bridge-dead 检测的完整链路：哪些条件触发 kill child_pid
2. _detect_acp_failure 的 4 层检测是否误匹配
3. per-tool bridge 后 PID 文件检查是否全面更新
4. cline/opencode idle-shutdown 是否错误触发了 Manager 的 kill
