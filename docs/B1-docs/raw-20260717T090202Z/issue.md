---
local_id: raw-20260717T090202Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T090202Z-A
platform_ids:
  gitee:
    issue_id: IK1RR5
    url: https://gitee.com/zhaoquan/freely/issues/IK1RR5
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T17:02:28+08:00'
updated_at: '2026-07-17T17:02:28+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 回归（raw-20260717T004620Z lane 的 C4-fix-2 引入,自查发现）
PROCESS_CHURN_PEAK 10→3 的修改判断失误:update_restart_storm_window 在每次 AI cycle 完成时记录当前活进程数(supervisor+dispatcher+ai 健康态恒=3) → peak=3 即达阈值 → 每个 cycle 后触发 restart_storm_pause 30s。生产实抓:2026-07-17T08:59:43Z 起每轮 `reason=process_churn_peak_threshold count=1 peak=3 observe_delay=30`,manager patrol 被节流 ~30s/cycle。

## 根因
peak 口径=窗口内记录到的活进程数峰值,与"churn"无关;健康态即满值。当时 AC(C4b"阈值落在可达域")对该口径的语义理解错误——可达≠应达。

## 修复方向
PEAK 条件语义修正:仅对 supervisor 死亡记录(record_supervisor_death_for_storm_window 写入的行)计峰,或该条件恢复为禁用值(10,不可达)并在 SKILL 注明 count 阈值为主判据。附带更新 raw-20260717T004620Z 的 AT-006 断言语义与 capability-lifecycle 阈值文档。

## 影响面
生产 manager 每 cycle 多等 30s;无数据损坏。
