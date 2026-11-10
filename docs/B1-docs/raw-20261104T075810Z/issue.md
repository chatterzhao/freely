---
schema_version: '1'
local_id: raw-20261104T075810Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4159'
    url: https://github.com/chatterzhao/freely/issues/4159
    synced_at: ''
  gitee:
    issue_id: IKSW8R
    url: https://gitee.com/zhaoquan/freely/issues/IKSW8R
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-04T07:58:10Z'
updated_at: '2026-11-04T07:58:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

# fix: config 无 schema，allowed_paths 类型错误导致豁免静默失效

workflow_kind: fix

## 根因
配置分为「bash 隐式变量」与「config.toml 显式键」两套，没有任何 schema 约束；类型错误不报错，只在消费端静默失效。已出现实证：`[skip_ibm_gate].allowed_paths` 实际存成字符串，gate 只认 list，豁免配置从未生效。

## 证据
- `.freely/config.toml:60`：`allowed_paths = "['templates/']"`（tomllib 实测为 `str`）。
- `docs/system/workspace/scripts/quality/governance-merge-gate:392-397`：只有 `isinstance(raw, list)` 分支处理，字符串直接跳过；`:397-398` 还有 `except Exception: pass`。
- `runtime/freely` 中带默认值的 `${VAR:-...}` 共 1,521 处、去重变量名 518 个；`.freely/config.toml` 仅 58 个键，绝大多数运行参数无文档、无校验。
- agent 角色分裂：`agents/agent-roles.toml`（技能）与 `.freely/agent-table.toml`（槽位/pool）各存一份真相。

## 影响
- 配置写错不报错，行为悄悄降级；豁免/开关类配置失效时无人察觉。
- 外部项目无法验证自己的配置是否被正确理解。
- 新增配置项没有唯一登记处，只能靠 grep 猜。

## 修复方案
1. 建 `contracts/config/schema.yaml`：列出每个键的类型、默认值、作用域、是否必填、消费者。
2. `freely doctor` 增加配置校验：类型不符、未知键、必填缺失都给出 `文件:行号` 与期望类型；`allowed_paths` 强制 list。
3. 一次性修正现有 `.freely/config.toml` 与 `templates/config.toml.example` 的 `allowed_paths` 写法。
4. 角色配置二选一：技能归 `agent-roles.toml`、槽位归 `agent-table.toml` 的边界写进 schema；或合并为单文件。

## 验收标准
- RED：把 `allowed_paths` 改成字符串后执行 `freely doctor`，必须报类型错误并指出行号；当前静默通过。
- RED：给 `config.toml` 加一个未知键，`freely doctor` 必须报告未知键；当前忽略。
- GREEN：`templates/config.toml.example` 中 `allowed_paths` 为 list，`freely init` 生成的新项目通过 doctor。
- GREEN：`contracts/config/schema.yaml` 覆盖 `.freely/config.toml` 全部 58 个键，doctor 能逐个校验。
