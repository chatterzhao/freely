# Candidates: ai-autonomy-checkpoint-commit-governance

- candidate_id: `c-20260318-0715-a`
- title: `commit-first after checkpoint-ready` 自治治理
- status: `needs_research`
- summary: 将“达到 checkpoint 边界后，AI 下一轮优先 continuity + commit”收敛为 Freely 的正式自治治理能力
- decision_reason: 当前问题来自 `I-20260318-0930` verification 暴露出的边界外治理缺口，方向已明确，但尚未收敛到可直接进入 IBM 的稳定 issue 边界。
- promoted_issue_path: `pending://issue-materialization`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

## Proposed directions

1. 增加 `commit-first after checkpoint-ready` 规则，并把它写入 `LAWS`。
2. 在 `runtime/freely` 中把“达到 checkpoint 边界且最小验证通过”升级为下一轮默认动作。
3. 让主管位在项目级工位视图中明确看到 worker 的 checkpoint/commit readiness，并优先安排收口。
4. 为 worker 增加可复用的自治提交 skill 或 runtime hook，避免每次只靠人工介入。

## Acceptance hint

- `checkpoint-ready` 必须成为结构化 control-plane 结论，而不是 prompt 里的自然语言提醒。
- `freely` / `checkpoint-guard` / supervisor 排班三者的职责边界必须可解释且不重叠。
- 首跳在看到 `checkpoint-ready + minimal verification passed` 时，默认动作应优先 continuity + commit/cleanup，而不是继续扩写实现。
- 多 worktree 监督视图必须能暴露哪个 worker 该先收口，且不伪造 issue/phase。

## Current route judgment

- source_class: `milestone + continuation-triggered discovery`
- route_kind: `pre_brainstorm`
- target_skill: `doc-pre-brainstorm-execution`
- why_now: 当前边界已经足以形成高优先级 candidate，但还不足以稳定到 issue-bound IBM；继续 pre-brainstorm 的收益高于回到当前 verification 内扩 scope。
