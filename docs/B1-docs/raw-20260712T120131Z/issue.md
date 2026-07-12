---
local_id: raw-20260712T120131Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3889'
    url: https://github.com/chatterzhao/freely/issues/3889
    synced_at: ''
  gitee:
    issue_id: IK0GG3
    url: https://gitee.com/zhaoquan/freely/issues/IK0GG3
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-12T12:01:53Z'
updated_at: '2026-07-12T12:01:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
tool-registry.toml 是系统级工具接入定义（binary路径、bridge协议、slot发现规则），不是运行时脚本。
当前路径 docs/system/workspace/scripts/runtime/ 混在 daemon/monitor/bridge 等运行时代码里，位置不对。

## 修复
- tool-registry.toml: docs/system/workspace/scripts/runtime/ → docs/system/workspace/tools/
- 更新所有引用路径:
  - tool-launchers.sh: TOOL_REGISTRY 变量
  - start-lead-agent.sh: _runtime_dir/tool-registry.toml
  - monitor-ai-acp.sh: 注释中的路径引用

## 不移动
- tool-registry-query.py 保留在 scripts/runtime/（它是运行时代码，只是读取 tool-registry.toml 的数据）

## 验收
- 所有引用路径指向新位置
- freely daemon 正常启动
