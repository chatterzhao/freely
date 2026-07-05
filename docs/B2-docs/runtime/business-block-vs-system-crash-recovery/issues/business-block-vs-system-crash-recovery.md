# Issue: business-block-vs-system-crash-recovery

- issue_id: `I-20260308-1931`
- title: 业务阻塞状态与系统崩溃恢复定位治理
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `business-block-vs-system-crash-recovery`
- issue-name: `business-block-vs-system-crash-recovery`
- source_candidate: `docs/B1-docs/raw-20260308-1930/candidates.md#c-20260308-1931`
- source_brainstorm: `docs/B1-docs/raw-20260308-1930/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/stage-prefixed-progress-identifier/issues/stage-prefixed-progress-identifier.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]

## Why

Freely 必须区分“AI 识别出的业务阻塞”和“系统监控发现的运行时崩溃”。如果把二者混成一个 `blocked_*` 状态，auto-loop 会在恢复时伪造不存在的交接，并且无法稳定找到正确的 issue、session、worktree 和 resume 路径。

## Scope

1. 为 `blocked_*` 建立业务阻塞硬定义。
2. 明确 PID 消失、CLI 崩溃、会话断裂时不直接改 `phase_state`。
3. 固定恢复定位顺序与降级扫描路径。
4. 统一最小恢复字段与 `resume_hint` 语义。
5. 更新相关治理文档与 skills，使其按该逻辑处理系统崩溃。

## Acceptance

- `blocked_*` 只用于 AI 已识别并显式留痕的业务阻塞。
- 系统崩溃类事件先进入恢复定位，不直接改主状态。
- 恢复定位顺序和最小恢复字段在治理文档中统一可追溯。
- 核心恢复相关 skills 使用同一恢复定位顺序。

## Completion

- `docs/LAWS.md` 已把 `blocked_*` 硬定义为业务阻塞，并禁止把 PID 消失、CLI 崩溃、会话断裂等系统事件直接写成 `blocked_*`。
- `docs/system/workspace/skills/context-source-skill/SKILL.md` 与 `docs/system/workspace/skills/recovery-subagent-governance/SKILL.md` 已统一恢复定位顺序：`recovery -> progress -> issue -> milestone -> active worktree/uncommitted changes`。
- `runtime_state`、`session_refs`、`resume_hint` 的恢复字段要求已写入治理口径，满足 Freely 自举阶段“文档即实现”的交付标准。
- 本 issue 的正式实现已落到治理与 skill 资产；后续若补 runtime 检查脚本，应作为新 issue 承接，不回退当前边界定义。
