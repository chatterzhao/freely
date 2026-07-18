# PRD: L2120 孤儿行删除
- issue_id: I-20260718T004314Z-A

## Goal
runtime daemon start/status 不再因 L2120 孤儿行 unbound variable 静默死亡。

## 实现方案
删除 `docs/system/workspace/scripts/runtime/freely` L2120：`_agent_env="$source_project/.freely/agent-id.env"`（aea0c5749 残留，无消费者）。

## Dev-Loop Handoff
RED: harness 以 HEAD 版脚本 sourced 调 refresh → stderr 现 unbound + probe 死。GREEN: 工位版正常返回 + bash -n + daemon start 推进过 reconcile 点。
