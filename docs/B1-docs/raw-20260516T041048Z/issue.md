---
local_id: raw-20260516T041048Z48Z
kind: raw
- phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '356'
    url: https://github.com/chatterzhao/freely/issues/356
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T04:11:04Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260516T041048Z48Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T041048Z48Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T04:10:48Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T041048Z48Z`。实现前请用 `wt-create --raw-key 20260516T041048Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T04:10:48Z"
title: "governance-merge-gate GATE 1 时间戳不一致时应给出可操作的诊断提示"

## 背景

governance-merge-gate GATE 1 在做时间戳一致性检查时（branch key vs `docs/B1-docs/raw-*/issue.md` 的时间戳），当前报错信息只描述了"不一致"，但没有指导开发者/AI 如何诊断和修复。

当前报错示例：
```
GATE 1: timestamp mismatch — branch key 'raw-20260514T103532Z32Z' (20260514T1035)
vs issue raw-20260515T125610Z (20260515T1256) in docs/B1-docs/raw-20260515T125610Z/issue.md.
The raw/C/I lifecycle must share the same date-time key.
```

这个报错描述了问题但没有给出下一步动作。开发者/AI 看到后可能：
- 试图改文件名绕过（错误）
- 试图改门禁脚本绕过（更错）
- 不知道该怎么正确修复

## 需求

GATE 1 时间戳不一致时，报错信息应包含结构化的诊断路径：

1. **先检查格式**：issue 文件名和 frontmatter 的 `local_id` 是否符合 `raw-YYYYMMDDTHHMM[SS]Z` 格式
2. **格式合规但仍被拦截，考虑两个可能**：
   - 工位不是通过 `wt-create` 创建的，导致分支 key 与 issue key 不一致
   - 一个工位在处理多个 raw issue（违反"一个工位一个 issue"规范）
3. **确认为多个 issue 混入**：
   - 用 `wt-create --raw-key <错误issue的key>` 为该 issue 创建独立工位
   - 把属于该 issue 的实现（commit）迁移到新工位
   - 从当前工位移除不属于本工位的 issue 文件

改进后的报错示例格式：
```
GATE 1: timestamp mismatch — branch key 'raw-20260514T103532Z32Z' (20260514T1035)
vs issue raw-20260515T125610Z (20260515T1256) in docs/B1-docs/raw-20260515T125610Z/issue.md.

诊断步骤：
  1. 检查 issue 文件名和 frontmatter local_id 格式是否正确（raw-YYYYMMDDTHHMM[SS]Z）
  2. 格式正确但仍被拦截 → 可能存在以下问题：
     a. 工位不是通过 wt-create 创建（分支 key 来源不正确）
     b. 一个工位在处理多个 raw issue（违反 docs/LAWS.md 一个工位一个 issue）
  3. 如确认为多个 issue 混入：
     - 用 wt-create --raw-key <被混入的issue key> 创建独立工位
     - 将属于该 issue 的实现迁移到新工位
     - 从当前工位移除不属于本工位的 issue 文件
```

## 范围

只改 `docs/system/workspace/scripts/quality/governance-merge-gate` 中 GATE 1 时间戳不一致的报错文案，不改变检查逻辑。
