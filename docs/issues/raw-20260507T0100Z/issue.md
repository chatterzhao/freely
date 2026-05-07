---
local_id: raw-20260507T0100Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github: "237"
primary_platform: github
created_at: 2026-05-07T01:00:00Z
author: zhaoquan
channel: github
session_refs: []
---

## 问题
fix-execution SKILL.md 分支规范表中普通 fix 的分支前缀是 feature/ 不是 fix/。

## 修复
7 处 feature/ → fix/，使用 raw-{raw-key}-{slug} 格式。
