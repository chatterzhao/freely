---
local_id: raw-20260717T041435Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T041435Z-A
platform_ids:
  github:
    issue_id: '3955'
    url: https://github.com/chatterzhao/freely/issues/3955
    synced_at: ''
  gitee:
    issue_id: IK1NSZ
    url: https://gitee.com/zhaoquan/freely/issues/IK1NSZ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T04:14:58Z'
updated_at: '2026-07-17T04:14:58Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题
同一字段两个门禁要求互斥格式：
- pretests-gate（docs/system/workspace/scripts/quality/pretests-gate ~L164-170 extract）：`^- field:` bullet 且只剥反引号——带单引号的值不匹配 VERIFICATION_DIR_RE（^docs/B2-docs/...）→ 报"不符合规范路径格式"
- pr-review-guarded（bin/pr-review-guarded ~L211）：sed "s/.*: *'\([^']*\)'/\1/" 只认单引号包裹——无引号值解析出整行 → 报"path does not match canonical format"

## 实证
2026-07-17 lane fix/raw-20260717T004620Z（无引号）被 pr-review-guarded 拦；lane fix/raw-20260717T004721Z（有引号）被 pretests-gate 拦。当前工作 lane 均用"双行"临时解法（无 dash 引号行喂 review + bullet 无引号行喂 gate），I-20260717T004721Z-A 是范例。

## 修复方向
两个解析器统一为"引号可选"：pretests-gate extract 剥 `'\"` 与反引号；pr-review-guarded sed 兼容无引号（如先剥引号再取值）。补一条双格式回归测试。

## 附带
runtime_pid_file_for_role 的 acp_bridge 分支返回未加引号的 glob（runtime/freely ~L1803），多 bridge 时展开成多行路径使 cat/rm 静默失败——同属治理工具解析 robustness，可同 lane 修复或 B1 判拆。
