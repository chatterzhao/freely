---
local_id: raw-20260506T0230Z
phase_state: proposed
kind: raw
source_family: chat_inbox
created: 2026-05-06T02:30:00Z
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
