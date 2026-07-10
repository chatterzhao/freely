---
local_id: raw-20260624T004510Z10Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T004510Z-A
platform_ids:
  github:
    issue_id: '3397'
    url: https://github.com/chatterzhao/freely/issues/3397
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T00:45:28Z'
updated_at: '2026-06-24T01:00:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 现象

`daemon start` 时 `deploy-skills` 总是退出码 1，日志显示：
```
WARNING: unsupported tools: opencode-apikey-ds-flash-auto
```

## 根因

`bin/deploy-skills` 的 tool 匹配 case 语句第 103 行：

```bash
case "$tool" in
    claude*)    ... ;;     # 前缀匹配 ✅
    codex*)     ... ;;     # 前缀匹配 ✅
    oc-*|opencode) ... ;;  # opencode 是精确匹配 ❌ 没有 *
    cc*)        ... ;;     # 前缀匹配 ✅
```

`opencode` 缺少 `*` 通配符。`AI_TOOL=opencode-apikey-ds-flash-auto` 匹配不上，掉到 default → unsupported → exit 1。

所有其他工具都用 `*` 前缀匹配，唯独 `opencode` 是精确匹配——明显的 copy-paste bug。

## 要做的事

`bin/deploy-skills` 第 103 行：`opencode)` → `opencode*)`

## 为什么 exit 1 是非致命的但仍需修

虽然 daemon start 日志写了 "non-fatal"，但：
- 每次启动都报错，污染日志
- skill 没有部署到任何目录——Manager/Worker 可能找不到 skill
- exit 1 在 `set -e` 环境下会中断脚本

## 参考
- `bin/deploy-skills` 第 97-108 行
- AI_TOOL 配置：`.freely/config.toml`
