# IBM Brainstorm: three-loops-sibling-relationship-and-terminal-governance

## Problem Slice

这条 issue 只收 active truth 与 runtime-facing contract，不做全仓历史 evidence 替换：

- 把“`三层`”纠偏成“`三个 loop`”
- 把 `auto-loop` / `doc-loop` / `dev-loop` 的关系钉成 `outer + sibling + sibling`
- 把 verification / cleanup / recovery 固定到 route / phase / governance path
- 把 terminal closure 重新锚到 outer governance，而不是任一局部 loop exit
- 把脚本、agent、skill、提示词入口这些长期被 runtime/AI 消费的真源同步到同一语义

## Active Truth Set

1. `docs/CONSTITUTION.md`
2. `docs/PROJECT_INTENT.md`
3. `docs/system/workspace/three-loop-capability-lifecycle.md`
4. `docs/system/workspace/agents/manager-agent.md`
5. `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
6. `docs/system/workspace/agents/worker-agent.md`
7. `docs/system/workspace/agents/lead-agent.md`
8. `docs/system/workspace/skills/context-source-skill/SKILL.md`
9. `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
10. `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
11. `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
12. `docs/system/workspace/scripts/start-lead-agent.sh`
13. `docs/system/workspace/scripts/compose-context-source-prompt.sh`
14. `docs/system/workspace/scripts/README.md`
15. `docs/LAWS.md`（仅补 appendix wording，不改 phase/acceptance semantics）

## Boundary

- 不回写历史 issue / progress / review 的历史表述
- 不试图在本 issue 中完成 observability 产品面
- 不在本 issue 中发明第四个 loop
- 不在本 issue 中偷带 runtime/watchdog 算法实现；这里只收 contract 与入口真源

## Dev Shape

1. 先统一 high-level wording 与图示
2. 再统一 route / lifecycle / terminal 解释
3. 再扫 agent / skill / script / prompt 入口，打掉旧 contract 漏网
4. 最后补 milestone / candidate promoted traceability 与 pre-tests 覆盖
