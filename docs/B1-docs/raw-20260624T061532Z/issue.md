---
local_id: raw-20260624T061532Z32Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T061532Z-A
platform_ids:
  github:
    issue_id: '3405'
    url: https://github.com/chatterzhao/freely/issues/3405
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T06:15:50Z'
updated_at: '2026-06-24T06:15:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 现象
#3403 删除 tool-registry.json5 后，tool-registry-query.py 仍保留 `_strip_json5()`、`_load_json5()`、`_load_registry()` 等 JSON5 兼容代码。

## 要清理
1. 删除 `_strip_json5()` 函数（~45行 comment stripping 逻辑）
2. 删除 `_load_json5()` 函数
3. 简化 `_load_registry()` → 直接调用 `_load_toml()`
4. 更新 docstring 去掉 '(or .json5)' 引用
5. 删除 `import re`（不再需要正则 strip comments）
