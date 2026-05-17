---
local_id: I-20260401-1703-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '83'
    url: https://github.com/chatterzhao/freely/issues/83
    synced_at: '2026-04-27T11:22:08Z'
  gitee:
    issue_id: IJFO7O
    url: https://gitee.com/zhaoquan/freely/issues/IJFO7O
    synced_at: '2026-04-27T13:15:42Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/runtime-adapter-axis-and-per-tool-adapter-selection/issues/runtime-adapter-axis-and-per-tool-adapter-selection.md
last_synced_comment_at:
  github: '2026-04-27T11:22:08Z'
hash: ''
created_at: '2026-04-27T11:22:08Z'
updated_at: '2026-05-17T12:21:37Z'
platform_state: closed
---

ACP boundary 已经收口，但 runtime 现在还没有 first-class `adapter axis`。

当前真实形态仍然是：

- config 主要以 `AI_TOOL` 为中心
- `tool-launchers.sh` 主要以 `tool -> launcher case` 分派
- `freely` 自己持有 continuity / status / launch metadata / session writeback

如果不先把 adapter selection 从 tool selection 中抽出来，后续无论要不要接 ACP，都会把 communication plane、tool-specific launch glue、continuity truth 一起拖进同一次改造。

因此这条 owner 的职责不是接 ACP，而是先把 runtime 切出一个安全的 adapter boundary。

canonical: docs/epics/workspace-routing-foundation/runtime-adapter-axis-and-per-tool-adapter-selection/issues/runtime-adapter-axis-and-per-tool-adapter-selection.md
