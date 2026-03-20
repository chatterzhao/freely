# Issue: human-chat-intake-and-manager-delegation

- issue_id: `I-20260319-1715`
- title: CLI-first human chat intake and manager delegation loop
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `human-chat-intake-and-manager-delegation`
- issue-name: `human-chat-intake-and-manager-delegation`
- source_candidate: `docs/pre-brainstorms/20260319-1715--human-chat-intake-and-manager-delegation/candidates.md#c-20260319-1715-a`
- source_brainstorm: `docs/pre-brainstorms/20260319-1715--human-chat-intake-and-manager-delegation/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经把 human chat 定义为 discovery / continuation / control 的正式输入来源之一，也已经有 durable intake、manager notice/claim、specialized handling skill 与回写测试；剩下缺口是把这条能力线正式 materialize 成 issue-bound 产物，避免只停留在 pre-brainstorm candidate。

## Scope

1. 提供 CLI-first human chat intake 入口。
2. 记录 durable intake artifact，并让 manager 可扫描、可 claim、可分类。
3. 委派 `skill:human-interruption-handling` 生成 resolution artifact 与 absorption 建议。
4. 把 discovery 输入继续吸收回 `doc-pre-brainstorm-execution`。
5. 让 completion signal 能回写到 intake / milestone / issue 记录。

## Acceptance

- `./bin/freely intake chat --project <abs_path> --message <text>` 可写入 durable intake。
- `./bin/freely intake status --project <abs_path>` 可展示 active intake。
- manager prompt 会暴露 human chat intake queue。
- `skill:human-interruption-handling` 能产出 resolution artifact。
- `test-freely-human-chat-intake` 覆盖 record / claim / resolve / status 回写。
- pre-brainstorm candidate 已绑定到正式 issue 和 milestone。

## Verification

- 已执行：
  - `bash docs/system/workspace/scripts/tests/test-freely-human-chat-intake`
- 已落盘实现：
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-human-chat-intake`
  - `docs/system/workspace/skills/human-interruption-handling/SKILL.md`
  - `docs/system/workspace/agents/manager-agent.md`

## Next

- 保持 `in_verification`，等待 review 与 promote / cleanup 判断。
