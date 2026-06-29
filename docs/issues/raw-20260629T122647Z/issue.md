---
local_id: raw-20260629T122647Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3623'
    url: https://github.com/chatterzhao/freely/issues/3623
    synced_at: ''
  gitee:
    issue_id: IJXO03
    url: https://gitee.com/zhaoquan/freely/issues/IJXO03
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T12:27:08Z'
updated_at: '2026-06-29T12:27:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景

freely feedback 当前只有创建功能。但 workflow skill 阶段 0 中有编辑 raw issue 的需求（描述不准确时修改）。platform-adapter.py 已有 update_issue() 函数（L346-370），但未暴露为 CLI 子命令。

## 现状

### platform-adapter.py update_issue (L346-370)
- 参数: local_id, platform_issue_id, title=, body=
- GitHub: gh issue edit --repo X Y --title ... --body ...
- Gitee: gitee-issue.py update X --title ... --body ...
- 支持同时更新 title 和 body

### freely feedback 现状
- --title (必填)
- --body (必填)
- --kind (必填)
- --severity (可选)

## 需要实现

### freely feedback edit 子命令

用法:
  freely feedback edit --raw-key <key> --title ... --body ...

参数:
  --raw-key  必填，raw issue 的 key（如 20260629T122254Z）
  --title    可选，新标题
  --body     可选，新正文
  --title 和 --body 至少提供一个

实现逻辑:
1. 读取 docs/issues/raw-{key}/issue.md 的 platform_ids
2. 调用 platform-adapter.py update_issue(local_id, platform_id, title, body)
3. 更新本地 issue.md 的标题和正文
4. 输出更新结果

### 命令规范化要求
- feedback 子命令格式统一: freely feedback create | edit
- 现有 freely feedback (默认 create) 向后兼容
- --help 输出完整

### 关联修复
- freely feedback 输出中的 --skill 引用需要改为 --kind (lines 23607-23608)
- workflow skill 阶段 0 已使用 freely feedback edit，需要实现

## 验收
- freely feedback edit --raw-key <key> --title ... 可用
- freely feedback edit --raw-key <key> --body ... 可用
- 同时更新本地 issue.md 和平台 issue
- freely feedback --help 显示 edit 子命令
