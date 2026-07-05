---
b1_id: B1-20260626T173930Z
source_raw: raw-20260626T173930Z
produced_candidate: C-20260626T173930Z-A
---
# B1_IBM: 统一 slot 组装 + slot recovery 基于 agent-table
## Problem
两个函数做同一件事（test vs work），且 slot recovery 不测试 slot 可用性。
## Decision
合并为 ai_cli_tool_with_auth_assemble(type, slot)。slot recovery 用 _test_slot 测试。
## Candidate
candidate_id: C-20260626T173930Z-A; status: promoted; milestone: M-20260626T173930Z-A
