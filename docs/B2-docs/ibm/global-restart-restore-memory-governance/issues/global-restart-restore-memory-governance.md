# Issue: global-restart-restore-memory-governance

- issue_id: `I-20260327-2006-A-global-restart`
- title: Global restart restore memory governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `global-restart-restore-memory-governance`
- issue-name: `global-restart-restore-memory-governance`
- source_candidate: `docs/B1-docs/raw-20260327T200600Z/candidates.md#c-20260327-2006-a`
- source_brainstorm: `docs/B1-docs/raw-20260327T200600Z/brainstorms.md`
- pre_tests_path: `docs/B2-docs/ibm/global-restart-restore-memory-governance/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/ibm/global-restart-restore-memory-governance/code-reviews/`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/B2-docs/ibm/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
  - {tool: codex, session_id: "019d377f-37b7-7cf2-8b76-d6a4a36a4a7f", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-49-37-019d377f-37b7-7cf2-8b76-d6a4a36a4a7f.jsonl", role: "downstream-issue-continuity-refresh"}
  - {tool: codex, session_id: "019d3d46-4e39-7020-afdc-cd2f6822ae30", jsonl_path: "unavailable://live-status-deep-ref-only", role: "downstream-first-hop-recheck"}

## Why

一旦 future global `restart` 成为显式 all-project control-plane action，Freely 不能只做 blind kill + blind relaunch。它必须记住 restart 前哪些 projects 处于 running，保留恢复所需的 durable evidence，并显式排除 operator 已停下的 projects。

## Scope

1. 定义 explicit global restart surface 与 all-project blast radius。
2. 冻结 `$FREELY_HOME/control-plane/restart/{latest.json,history/<timestamp>.json}` manifest namespace 与 keep-latest-and-last-20 retention。
3. 定义 previously-running project set、operator-stopped exclusion 与 fleet restore policy。
4. 冻结 mandatory restore anchors 与 auxiliary evidence 的层级关系。
5. 保证本 issue 不重新定义 project command semantics，而是消费 `I-20260327-2006-A` 已冻结的 taxonomy。

## Non-Goals

1. 不重新定义 project `start` / `stop` / `restart` / `start --force` / `restore-work` 的单项目语义。
2. 不把 global restart 降级成 project force 的别名。
3. 不在本轮直接实现 runtime patch 或 verification closeout。
4. 不把 `I-20260318-1630` 重新打开为 global restart owner。

## Acceptance

- global restart surface 与 project command family 明确分层。
- restore manifest 的 durable home、retention 与 required fields 稳定到足以驱动实现。
- previously-running project set 只恢复 restart 前本来就是 running/desired-running 的 projects。
- operator-stopped projects 不会被误恢复。
- mandatory restore anchors 与 auxiliary evidence 的边界稳定，不再把 transient run-state 误判为 required restore truth。

## Next

- `2026-03-30 17:34 PDT` owner implementation and verification are already absorbed by `develop` commits `8441b92` and merge `2467cc7`. Completion evidence is anchored by `docs/B2-docs/ibm/global-restart-restore-memory-governance/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`.
- Any broader global reset surface must open a new lifecycle rather than rewriting this completed owner.
