# Pre-tests: three-loops-sibling-relationship-and-terminal-governance

## Pre-merge acceptance

1. `CONSTITUTION.md` 不再把 `doc-loop` / `dev-loop` 表述成包含式“层”，而是明确 `auto-loop` outer、`doc-loop` / `dev-loop` sibling。
2. `PROJECT_INTENT.md` 的方法论、图和路由表彼此一致：
   - “三个 loop”而非“三层”
   - verification / cleanup / recovery 不是新增 loop
   - `auto-loop` 负责完成判定、验证裁决、cleanup / retirement 路由
   - `doc-loop` / `dev-loop` 负责产出 evidence，不负责最终宣布 terminal completion
3. `three-loop-capability-lifecycle.md` 清楚区分：
   - loop
   - route_kind
   - phase / lifecycle state
   - terminal retirement
4. `manager-agent.md` 与 `auto-loop-orchestrator/SKILL.md` 的 manager wording 不再暗示 `doc-loop` / `dev-loop` 的层级包含。
5. watchdog / manager active truth 对“死循环”职责一致：
   - 短窗口反复启动 AI 工具进程、异常重启风暴、或进程总数异常增长属于 watchdog signal
   - watchdog 负责暴露 signal，不负责独自宣布 dead-loop 业务结论
   - 主管在 `auto-loop` 中基于该 signal 裁决是正常 recovery、prompt/continuity 漂移，还是 dead-loop / thrash
6. milestone / candidate promoted traceability 已回写，当前 lifecycle 不再停留在纯 pre-brainstorm。
7. 脚本提示词真源与高层 active truth 一致：
   - `compose-context-source-prompt.sh` 不再把 `auto-loop` 写成“第二层”
   - `scripts/README.md` 不再暗示脚本入口仍沿用旧层级包含语义
8. 其余 runtime-facing active truth / prompt contract 与高层语义一致：
   - `worker-agent` / `lead-agent` / `context-source-skill` / `dev-loop-execution` / `doc-pre-brainstorm-execution` / `watchdog-control-plane`
   - `start-lead-agent.sh`
   - 不残留“局部 loop 自宣 terminal completion / cleanup / retire”的语义

## Verification

1. `./bin/governance-check`
2. `rg -n "三层循环|三层 loop|三层职责边界|第二层 auto-loop" docs/CONSTITUTION.md docs/PROJECT_INTENT.md docs/system/workspace/three-loop-capability-lifecycle.md docs/system/workspace/agents/manager-agent.md docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md docs/system/workspace/scripts/compose-context-source-prompt.sh docs/system/workspace/scripts/README.md docs/LAWS.md`
3. manual read-through of the active truth set to confirm no file still implies:
   - `doc-loop` contains `dev-loop`
   - verification / cleanup is a fourth loop
   - local loop exit equals outer terminal completion
   - worker can declare `completed / cleanup / retire` without `auto-loop` judgement
   - watchdog alone can keep blindly relaunching forever after short-window restart churn without manager judgement
4. manual audit of runtime-facing contract files to confirm prompt/script entrypoints and role docs do not drift from the sibling-loop model

## Non-goals

1. 不要求改写历史 issue/progress/review 证据。
2. 不要求在本 issue 中实现新的 CLI/TUI/GUI observability plane。
