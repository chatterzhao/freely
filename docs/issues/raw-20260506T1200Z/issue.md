---
local_id: raw-20260506T1200Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github: "239"
primary_platform: github
created_at: 2026-05-06T12:00:00Z
author: zhaoquan
channel: github
session_refs: []
---

## 问题
doc-pre-brainstorm-execution / doc-ibm-execution 命名未体现 B1_IBM/B2_IBM。
I→B→M 骨架未被下层 skill 强制消费。

## 修复
1. 改名 doc-B1_IBM-execution / doc-B2_IBM-execution，全局替换
2. 两个 SKILL.md 加入 I→B→M 骨架
3. ibm-framework.md 术语统一
