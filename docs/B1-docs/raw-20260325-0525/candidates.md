# 候选：watchdog-slot-sweep-without-cooldown-governance

- id: `C-20260325-0525-A`
- title: Retire cooldown-driven recovery and make slot sweep canonical
- source_brainstorm: `docs/pre-brainstorms/20260325-0525--watchdog-slot-sweep-without-cooldown-governance/brainstorms.md`
- status: `absorbed`
- adoption_type: `supporting_evidence`
- milestone: `M-20260306-workspace-routing-foundation`
- decision_reason:
  - 本轮 pre-brainstorm 已冻结关键边界：真实恢复真相应转向 failure-driven full slot sweep，而不是继续把 cooldown 当主调度面。
  - 该边界仍由同一组 watchdog 真源、测试面与 live evidence 承担，不需要新开平行 issue。
  - 因此 candidate 生命周期在这里收口，但底层 issue 生命周期继续回到 `I-20260318-1630` 的 doc-loop / dev-loop / verification。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- why_now:
  - 当前 live replay 已证明仅把 cooldown 从 account 改成 slot 还不够，control-plane 仍会围绕账本和 earliest-reset 形成漂移
  - 真实 Codex 工作位会直接消费当前授权文件，错误切入无效 slot 会阻塞当前工作，因此恢复真相必须建立在实时 probe 上，而不是旧账本推断
  - `rate limit` 与 `deactivated_workspace` 这类失败现在都更像“当前 slot 不可继续”，应统一收进同一条 slot sweep recovery contract
- expected_outcome:
  - freeze whether cooldown is retired from the main recovery contract
  - define a canonical failure-driven full slot sweep path
  - route the contract rewrite back into `I-20260318-1630` instead of materializing a parallel issue
- likely_truth_sources:
  - `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/runtime/ai-cli`
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/progress/workspace-routing-foundation/p-global-ai-account-watchdog-and-manager-bootstrap.md`
- next_action:
  - 不再继续扩 pre-brainstorm；回到 `I-20260318-1630` 的 doc-loop，显式改写 issue / progress / tasks / capability 真源，把 cooldown 降级为 debug evidence 或排序提示，并把 `rate limit`、`deactivated_workspace`、auth failure、slot probe failure 统一路由到 full slot sweep
- revisit_trigger:
  - 仅当后续 live replay 证明这次 contract 改写超出 `I-20260318-1630` 的 owner / 真源 / 验收面，才重新考虑新开 issue
