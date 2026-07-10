---
kind: raw
local_id: raw-20260517T073433Z33Z
priority: P2
source: chat-inbox
created_at: '2026-05-17T07:34:34Z'
title: 时间戳生成处缺少 Z 时区标识，应统一使用 UTC+Z 格式
phase_state: absorbed
platform_ids:
  github:
    issue_id: '448'
    url: https://github.com/chatterzhao/freely/issues/448
    synced_at: '2026-05-17T07:34:43Z'
updated_at: '2026-06-17T00:26:31Z'
primary_platform: github
platform_state: closed---

## 问题

多个时间戳生成点使用本地时间，缺少 `Z` 时区标识。

| 位置 | 当前格式 | 问题 |
|------|---------|------|
| `freely` 行 5330: `ts=$(date '+%Y%m%d-%H%M%S')` | `20260517-002149` | 本地时间，无 Z |
| `freely` 行 70: `current_timestamp_local_for_display()` | 本地显示 | 显示用，可保留 |
| `freely-package` nightly | `YYYYMMDD-nightly` | 无时分，无 Z |
| `freely-package` stable | `YYYY.MM.DD-stable` | 无时分，无 Z |

行 5330 生成 prompt 文件名（`prompt-$ts.txt`）和 cycle log 名（`cycle-$ts.log`），影响所有 AI 会话日志的命名。

## 修复

统一使用 UTC + `Z` 后缀格式：`YYYYMMDDTHHMMSSZ`

```bash
# 行 5330 改为:
ts="$(date -u +'%Y%m%dT%H%M%SZ')"
```

`freely-package` 版本格式在 #447 中已覆盖，此处补充 Z 要求。

## 范围

- `docs/system/workspace/scripts/runtime/freely`：行 5330 及相关时间戳生成
- `bin/freely-package`：版本号格式（关联 #447）
