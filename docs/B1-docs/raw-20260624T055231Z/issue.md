---
local_id: raw-20260624T055231Z31Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T055231Z-A
platform_ids:
  github:
    issue_id: '3403'
    url: https://github.com/chatterzhao/freely/issues/3403
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T05:52:51Z'
updated_at: '2026-06-24T05:52:51Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 现象
#3399 (JSON5→TOML 重构) 合并后 deploy-skills 仍只检测到 claude，未检测到 codex/opencode。根因是重构不彻底，遗留了 JSON5 回退路径。

## 问题
1. bin/deploy-skills 仍通过 inline Python 读 JSON5（而非 TOML + query tool）
2. freely TOOL_REGISTRY 仍硬编码 JSON5
3. tool-registry.json5 文件未删除，各脚本保留 JSON5 回退——违背'彻底重构为 TOML'的设计意图

## 修复
1. 删除 tool-registry.json5
2. 三个消费脚本去掉 JSON5 回退，只读 TOML
3. deploy-skills 使用 tool-registry-query.py 读 TOML（而非 inline Python + comment stripping）
