---
b1_id: B1-20260718T035754Z
phase_state: completed
source_raw: raw-20260718T035754Z
produced_candidate: C-20260718T035754Z-A
created_at: 2026-07-18
---

# B1_IBM: ACP binary path 自愈回写

## Problem
config.toml 四个 FREELY_ACP_*_BIN 全为空。`_init_acp_tool_setup()` 存在但 init 未跑/跑了也因 tool_adapter=direct 跳过。Bridge 每次通过 PATH fallback 发现 binary，发现后不回写。

## Decision: Option A — bridge 启动时自愈回写
在 `_ensure_acp_bridge_running()` 的 PATH fallback 成功后追加 `upsert_config_key`。
- 不改 resolution 链
- 不改 init 流程
- 首次 daemon start 即可修复
- 幂等：已填正确路径则跳过 write

## Candidate
- candidate_id: C-20260718T035754Z-A
- status: promoted
- milestone: M-20260718T035754Z-A
