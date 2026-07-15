---
b1_id: B1-20260715T142813Z
phase_state: completed
source_raw: raw-20260715T142813Z
created_at: 2026-07-15
---

# B1: _init_agent_table_slot_pin 废弃 agent-id.env

## Input
raw-20260715T142813Z: Worker/Reviewer daemon 因 agent-id.env 不存在而永远拿到 manager slot

## Problem

### 当前实现
_init_agent_table_slot_pin (line 4800) 读 agent-id.env 文件确定 agent role。
该文件已废弃（agent-table 替代），不存在时 fallback manager_01。
所有 Worker 和 Reviewer daemon 都拿到 claude-apikey-ds-flash-auto slot。

### 已有正确实现
_resolve_current_agent_id() (line 341) 优先读 agent_working SQLite 表，
agent-id.env 仅作 fallback。需复用。

### 影响
- Worker daemon 用 manager slot (claude) 而非 worker slot (opencode)
- Reviewer daemon 用 manager slot 而非 reviewer slot (cline)  
- 跨 base tool 委派永远失败

## Decision
_init_agent_table_slot_pin 改用 _resolve_current_agent_id 读 agent_working 表。
保留 agent-id.env 作为 fallback 兼容旧配置。3 行代码改动。

## Candidate
C-20260715T142813Z-A promoted M-20260715T142813Z-A
