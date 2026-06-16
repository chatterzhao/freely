---
local_id: raw-20260506T0230Z
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
kind: raw
source_family: chat_inbox
created: 2026-05-06 02:30:00+00:00
platform_ids:
  github:
    issue_id: '281'
    url: https://github.com/chatterzhao/freely/issues/281
    synced_at: '2026-05-10T09:29:55Z'
updated_at: 2026-05-17T04:47:25Z
primary_platform: github
created_at: '2026-05-10T09:29:55Z'
platform_state: closed
---

# raw-20260506T0230Z: governance-merge-gate 应识别 raw issue 作为生命周期入口

## 现象

merge 到 develop 时，governance-merge-gate 报错：

> This develop-bound merge has no candidate-driven lifecycle evidence

但 diff 中已有 3 个 raw issue（raw-20260506T0100Z, raw-20260506T0130Z, raw-20260506T0200Z）。

## 根因

gate 只检查 C/M/I 三段（candidate → milestone → issue），没认 raw 阶段。

完整生命周期是 raw → C → M → I。raw issue 是最上游入口，它的存在本身就是生命周期证据。

## 修复

governance-merge-gate 应接受 raw issue 作为合法生命周期起点：

- diff 中有 raw-* issue → 生命周期证据成立
- raw issue 有 phase_state ∈ {proposed, absorbed, dropped} → 合法
- raw issue 可以通过 candidate 或直接 promote 到 I-*
