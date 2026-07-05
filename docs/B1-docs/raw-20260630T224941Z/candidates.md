---
candidate_id: C-20260630T224941Z-A
status: promoted
source_raw: raw-20260630T224941Z
created_at: 2026-06-30
milestone: M-20260630T224941Z-A
---

## C-20260630T224941Z-A: config.toml.example 全面修订 + init 创建逻辑 + merge lock 死锁诊断

- candidate_format_version: v2
- title: config.toml.example 修订、init 创建 config.toml、merge lock 诊断
- status: promoted
- decision_reason: 三条改动共享同一动机——改善首次使用体验和运维可靠性。可分 candidate 但建议单 PR 推进（改动面可控）
- next_action: B2_IBM → 先改 example（纯文档），再改 init 逻辑和 merge lock
- revisit_trigger: N/A
- acceptance_criteria:
  - config.toml.example 每字段注释含：用途、合法值、空值影响、init 行为、谁填
  - 新增第十六节 FREELY_ACP_*_BIN（4 个字段，空值，由 init 自动填入）
  - AI_TOOL 合法值列表补 `cline`
  - init 无 config.toml 时自动从 example 复制 + 填入 PROJECT_ROOT/INTENT_FILE/CONSTITUTION_FILE/FREELY_HOME
  - init 有 config.toml 时只补缺失 ACP 字段
  - --reset 备份(时间戳) + 从 example 覆盖
  - --auto --reset: 自动确认；无 --auto: y/N 并 30s 超时
  - merge lock 写 PID + 死锁检测 + 清晰提示
- promotion_gate: 所有字段注释准确，init 三个场景通过测试，merge lock 死锁检测可验证
- open_questions: []
- promoted_issue_path: docs/B2-docs/config/config-toml/raw-20260630T224941Z/issues/I-20260630T224941Z-A.md
- milestone: M-20260630T224941Z-A
- session_refs: []
