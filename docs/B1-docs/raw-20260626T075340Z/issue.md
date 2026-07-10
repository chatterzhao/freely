---
local_id: raw-20260626T075340Z40Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3543'
    url: https://github.com/chatterzhao/freely/issues/3543
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T07:54:00Z'
updated_at: '2026-06-26T08:08:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260626T075340Z-A
source_candidate: docs/B1-docs/raw-20260626T075340Z40Z/candidates.md#C-20260626T075340Z-A
platform_state: closed
---

## 问题

`tool-registry.toml` 中 `[cline.slot]` 和 `[cline.session]` 多个字段与实际 cline 行为不符，导致 bridge 无法正确解析 slot 配置和 session。

## 根因分析

cline 使用 `--config <dir>` 指定配置目录（非环境变量），目录结构为：
```
<config>/
  data/
    settings/
      providers.json   # API key + model 配置
    sessions/           # session 数据落在此处（与 codex 一样在 slot 目录内）
```

`.zshrc` alias 已验证：
```
alias cline-account-ds-flash-free-auto='cline --config /Users/zhaoyu/.ai-auth/cline-account-ds-flash-free-auto'
```

实际 session ID 格式：`1782208464405_m02bu`（13位时间戳_5字符nanoid，无 `_cli` 后缀）。

## 需要修改

### [cline.slot]
| 字段 | 当前值 | 正确值 | 原因 |
|------|--------|--------|------|
| discovery | alias_env_var | **alias_cli_arg** | alias 用 `--config` flag |
| alias_key | CLINE_CONFIG_FILE | **--config** | 同上 |
| config_file | providers.json | **data/settings/providers.json** | 相对 `--config` 目录的路径 |
| is_dir | false | **true** | `--config` 接收目录 |
| bridge_config_env | CLINE_CONFIG_FILE | **CLINE_CONFIG_DIR** | 待验证 cline 是否读取该 env var；如不读取需改 bridge 动态注入 `--config` flag |

### [cline.session]
| 字段 | 当前值 | 正确值 | 原因 |
|------|--------|--------|------|
| id_format | timestamp_nanoid_cli | **timestamp_nanoid** | 实际 session ID 无 `_cli` 后缀 |
| extract_regex | `\d{13}_[A-Za-z0-9]{5,10}_cli` | **`\d{13}_[A-Za-z0-9]{5,10}`** | 同上 |
| directory_template | ${HOME}/.cline/data/sessions | 需考虑 slot 目录 | cline session 落在 `--config` 目录的 `data/sessions/` 下 |

## 待验证

- `CLINE_CONFIG_DIR` 环境变量是否被 cline 读取，用于替代 `--config` CLI flag
- 如果不支持，需在 bridge/`_ensure_acp_bridge_running` 中支持动态注入 `--config <slot_path>` 到 acp.args
