---
b1_id: B1-20260708T211928Z
phase_state: completed
source_raw: raw-20260708T211928Z
---
# B1: scan I-* classification + frontmatter parse + station precision

## Problem
1. parse_frontmatter: I-* issue 的 YAML+bullet 混合格式未正确处理，phase_state 读为空
2. _detect_station: 未区分 raw vs linked (I-*)，所有 2a_non_terminal 判为 raw_created
3. I-* issue 需要自己的 station (i_non_terminal / i_no_phase)

## Decision
1. parse_frontmatter: bullet 行始终做补充解析(不覆盖已有 YAML 字段)
2. _detect_station: is_linked 判断分流 → raw_* vs i_* 站
3. 新增 STATION_ACTIONS: i_non_terminal, i_no_phase, raw_not_started

## Result
33 raw_not_started + 15 i_non_terminal + 1 agent_dead + 1 sync_batch
