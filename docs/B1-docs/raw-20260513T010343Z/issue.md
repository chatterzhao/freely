---
local_id: raw-20260513T010343Z43Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '326'
    url: https://github.com/chatterzhao/freely/issues/326
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-13T01:03:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 根因

I-20260507T143545Z-A（timestamp-seconds-upgrade）曾对所有 `\d{4} → \d{4,6}` 做全局替换，但实际遗漏了多处。当前 YYYYMMDDTHHMMSSZ（秒精度）才是正确格式，YYYYMMDDTHHMMZ（分钟精度）仍是兼容旧格式。

## 问题清单

### A. 代码 regex 遗漏——功能性 bug（4 处）

`freely` 脚本中 4 处 `grep -oE '[0-9]{8}T[0-9]{6}Z'` 只匹配 6 位秒，分钟精度的 key 会静默不匹配：

| 行号 | grep 模式 | 应为 |
|------|-----------|------|
| L9667 | `[0-9]{6}` | `[0-9]{4,6}` |
| L12069 | 同上 | 同上 |
| L13584 | 同上 | 同上 |
| L13631 | 同上 | 同上 |

### B. 帮助/错误提示不一致（6 处）

wt-create 的 regex 已接受 `{4,6}`，但用户提示仍写分钟精度：

| 位置 | 当前文字 | 应改为 |
|------|---------|--------|
| L11 | `Raw issue key (YYYYMMDDTHHMMZ format)` | 提及秒格式或 `YYYYMMDDTHHMM[SS]Z` |
| L37, L40 | `20260506T1000Z`（举例） | 举例秒格式 |
| L189 | `Prefer YYYYMMDDTHHMMZ` | `YYYYMMDDTHHMM[SS]Z` |
| L191 | `Expected YYYYMMDDTHHMMZ` | 同上 |
| L188 | legacy check `[0-9]{4}$` | `[0-9]{4,6}$`（旧格式也应支持秒） |

### C. 文档写分钟精度（10+ 处）

| 文件 | 位置 | 当前 |
|------|------|------|
| `docs/system/workspace/ibm-framework.md` | L133-134, L138-139, L162 | `raw-YYYYMMDDTHHMMZ` |
| `docs/system/workspace/scripts/quality/governance-merge-gate` | L133, L811-813 | 同上 |
| `docs/CONSTITUTION.md` | L53 | `feature/premerge-YYYYMMDDTHHMMZ--<topic>` |
| `docs/system/workspace/skills/freely-fix-execution/SKILL.md` | L69 | 同上 |
| `docs/system/workspace/skills/freely-branch-management/references/semantic-regression-checklist.md` | L14, L17 | `YYYYMMDDTHHMMZ` |
| `docs/system/workspace/skills/freely-premerge-reconcile/SKILL.md` | L15, L17, L18, L20 | 同上 |

## 改动范围

1. `freely` L9667, L12069, L13584, L13631: `[0-9]{6}` → `[0-9]{4,6}`
2. `wt-create` L11, L37, L40, L188, L189, L191: 帮助/错误消息更新
3. 10+ 处文档：`YYYYMMDDTHHMMZ` → `YYYYMMDDTHHMM[SS]Z` 或明确标注秒精度

