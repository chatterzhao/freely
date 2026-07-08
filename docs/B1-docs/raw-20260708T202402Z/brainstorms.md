---
b1_id: B1-20260708T202402Z
phase_state: completed
source_raw: raw-20260708T202402Z
---
# B1: Scan Station Chain + Two-Level Delegation + Batch Dedup

## Problem
lifecycle-v3丢失了旧scan的4个核心设计:
1. 两级 [manager]/[worker] 委派模板
2. Station生命周期链
3. add_platform_sync_batch跨scan去重
4. 精确命令参数

## Decision
从旧scan恢复STATION_ACTIONS(14站)+_detect_station()+_build_sync_batch(指纹去重)
保留新scan的argparse、platform-adapter、A2A集成

## Result
275 items → 55 items (1 sync batch + 53 raw_created + 1 agent_dead)
