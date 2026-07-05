---
candidate_id: C-20260630T124528Z-A
status: promoted
source_raw: raw-20260630T124528Z
created_at: 2026-06-30
milestone: M-20260630T124528Z-A
---

## C-20260630T124528Z-A: legacy issue

- candidate_format_version: v2
- title: freely init 统一 ACP 工具发现/下载/配置，tool-registry 新增 download_url + install_method
- status: promoted
- decision_reason: Option A — init 时统一处理所有工具的 ACP binary 发现和下载，写入 config.toml 持久化。循环 registry 驱动，不硬编码工具名。同时修复 _acp_bridge_health_check Shell 注入。
- next_action: B2_IBM → 物化 I-* issue + pre-tests + tasks + code-reviews
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - tool-registry 四个工具都有 install_method + download_url
  - ensure-codex-acp 通用化为 ensure-acp-binary，接受 --tool 参数
  - cmd_init() 新增 ACP 工具准备步骤，循环 registry 搜索/下载/写入 config.toml
  - 所有工具的下载都需要用户确认（y/N 交互）
  - 下载源只允许来自 registry 配置的 download_url
  - config.toml 新增 FREELY_ACP_<TOOL>_BIN 字段
  - _ensure_acp_bridge_running 优先从 config.toml 读 binary 路径
  - _acp_bridge_health_check Shell 注入修复
- promotion_gate: 四个工具的 ACP binary 能通过 freely init 发现或下载，config.toml 正确记录，runtime 能读到
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-code
  - mode: inline
  - summary: 全面审查 freely init ACP 流程、tool-registry 字段设计、ensure-codex-acp 通用化方案、config.toml schema 扩展
  - verdict: pass
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260630T124528Z-A/issue.md
- milestone: M-20260630T124528Z-A
- session_refs: []
