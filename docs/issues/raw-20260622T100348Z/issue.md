---
local_id: raw-20260622T100348Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3347'
    url: https://github.com/chatterzhao/freely/issues/3347
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T10:04:05Z'
updated_at: '2026-06-22T10:04:05Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

当前所有命令的 `--help` 输出都没有说明 `--reason` 参数的存在和使用方式。用户（包括 AI）只能通过触发 GATE 才能了解到 `--reason` 的格式和要求，增加了不必要的摩擦。

## 需要改进的命令

| 命令 | bypass flag | --help 需补充的内容 |
|------|------------|-------------------|
| `freely init` | `--force` | 何时需要 --reason、格式、有效理由类型 |
| `freely start` | `--force` | 何时需要 --reason、格式、有效理由类型 |
| `freely daemon start` | `--force` | 何时需要 --reason、格式、有效理由类型 |
| `freely task-mode set` | `--force` | 何时需要 --reason、格式、有效理由类型 |
| `wt-close` | `--force`/`--discard-unmerged`/`--skip-platform` | 每个 flag 何时需要、有效理由类型 |
| `pr-review-guarded` | `--verdict pass` (覆盖失败维度) | 何时需要 --reason、格式、有效理由类型 |

## 统一格式

所有 `--reason` 参数必须遵循格式:
```
--reason "违规绕过门禁中，理由充分，是：<业务理由>"
```

## 有效业务理由类型（非技术症状）

业务理由必须是真正的业务原因，不能是技术症状:
- ✅ "该功能确定放弃，不再继续实现此 raw issue"
- ✅ "该方案已被否决，未合并提交确认丢弃"
- ✅ "配置文件损坏无法修复，需重建初始化"
- ✅ "运行时状态损坏导致无法正常启动，需强制重建"
- ✅ "当前 AI 进程陷入死循环无法响应，需强制终止后切换模式"
- ✅ "IBM Completeness 维度不适用于本次纯文档修改"
- ❌ "phase_state 未 completed"（技术症状）
- ❌ "连接超时"（技术症状）
- ❌ "编译失败"（技术症状）

## 涉及文件

主要改动在 `docs/system/workspace/scripts/runtime/freely` 中各命令的 usage/help 函数，以及 `wt-close` 和 `pr-review-guarded` 的 help 输出。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
