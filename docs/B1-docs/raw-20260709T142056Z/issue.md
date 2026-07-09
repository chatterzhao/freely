---
local_id: raw-20260709T142056Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3843'
    url: https://github.com/chatterzhao/freely/issues/3843
    synced_at: ''
  gitee:
    issue_id: IK00M5
    url: https://gitee.com/zhaoquan/freely/issues/IK00M5
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-09T14:21:30Z'
updated_at: '2026-07-09T14:21:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

`check_doc_gate_or_fail` 要求 7 个文件存在才能启动 daemon，但其中 3 个不是 agent 注入治理文档：

| 文件 | 问题 |
|------|------|
| `docs/B1-docs/README.md` | 路径错误。CONSTITUTION §151 说的是项目根 README.md，不是 B1-docs 下的。全项目零消费者。 |
| `docs/B1-docs/INDEX.md` | 死代码残留。唯一消费者 `pre_brainstorm_patrol_seed_snapshot_for_project` 零调用者。`pre-brainstorms/` 空目录。架构已迁移到 `task-lifecycle-scan.py`。 |
| `docs/B1-docs/CONVERGENCE.md` | 过时临时落点。CONSTITUTION §79 的兜底路径，实际从未被写入。cleanup/恢复已有 wt-close + milestones 覆盖。 |

## 根因

doc gate 混淆了 governance tier（agent 注入）和 process documentation tier（项目内部文档）。

Agent 注入链路是: `CLAUDE.md → AGENTS.md → CONSTITUTION/LAWS/PROJECT_INTENT`。AGENTS.md §权威来源 明确声明了这 4 个核心治理文档。doc gate 应该只检查这 4 个文件。

后 3 个文件是项目内部过程文档，不影响 agent 正确运行。把它们放在阻塞启动的 gate 里，导致 daemon 首次重启就永远卡住——因为 `freely init` 从不创建它们。

## 修复

1. `check_doc_gate_or_fail` 精简为只检查 4 个 agent 注入文件
2. 移除 `pre_brainstorm_patrol_seed_snapshot_for_project` 死代码
3. CONSTITUTION §79 更新：CONVERGENCE 落点已过时

## 验收
- daemon 启动不再被 doc gate 阻塞
- 4 个核心治理文档仍然被检查
