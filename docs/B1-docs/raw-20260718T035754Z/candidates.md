---
candidate_id: C-20260718T035754Z-A
status: promoted
source_raw: raw-20260718T035754Z
created_at: 2026-07-18
milestone: M-20260718T035754Z-A
---

## C-20260718T035754Z-A: bridge 启动时 ACP binary 自愈回写 config.toml

- candidate_format_version: v2
- title: bridge 启动时 ACP binary 自愈回写
- status: promoted
- decision_reason: PATH fallback 成功后 upsert_config_key 回写，1 次daemon start 即自愈
- acceptance_criteria:
  - 首次 daemon start（config.toml 为空时）后 FREELY_ACP_CLAUDE_BIN 自动填写正确路径
  - 已有正确路径时 bridge 仍正常启动（幂等）
  - bash -n 语法通过
- promotion_gate: RED(GREEN 实证前的空 config)→GREEN(实证后写入真实路径)
- promoted_issue_id: I-20260718T035754Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T035754Z/issues/I-20260718T035754Z-A.md
- milestone: M-20260718T035754Z-A
