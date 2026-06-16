- candidate_id: C-20260616T044030Z-A
- title: Complete config.toml migration — clean break, TOML-only, zero config.env
- status: promoted
- milestone: M-20260616T044030Z-A
- promoted_issue_path: docs/issues/I-20260616T044030Z-A/issue.md
- decision_reason: 彻底 TOML-only 方案 — 单一配置路径、零兼容负担、用户必须手工阅读注释配置
- next_action: Materialize I-* issue in B2_IBM
---

# Candidate: config.toml Complete Migration — Clean Break

## Problem
Phase 1+2 code merged with config.env fallback, creating two config reading paths.
Auto-generated config.toml means users never read comments and don't understand their configuration.

## Solution
**彻底 TOML-only，零 config.env:**
- config.toml 是唯一配置格式，无 config.env 读取/迁移/回退
- `freely init` 只释放 config.toml.example，不自动生成
- 启动时 config.toml 缺失 → 阻塞并提示 cp example + 手工编辑
- 所有脚本 TOML-only

## Acceptance Criteria
- [x] freely init 释放 config.toml.example 到 .freely/，不生成 config.toml
- [x] load_config: config.toml 不存在时阻塞 + 清晰提示
- [x] 零 config.env 代码路径
- [x] config.toml.example: 56 字段全量中文注释，合理默认值
- [x] 修复: dict_to_toml/_shell_quote/cmd_print 等质量缺陷
- [x] 文档 config.env→config.toml

## Revisit trigger
If any config.env read/migration/fallback code is discovered in runtime paths.
