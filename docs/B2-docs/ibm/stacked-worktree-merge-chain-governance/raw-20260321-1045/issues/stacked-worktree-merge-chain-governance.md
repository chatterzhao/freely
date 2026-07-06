# Issue: stacked-worktree-merge-chain-governance

- issue_id: `I-20260321-1045`
- title: Stacked worktree merge-chain governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `stacked-worktree-merge-chain-governance`
- issue-name: `stacked-worktree-merge-chain-governance`
- verification_artifact_dir: docs/B2-docs/ibm/stacked-worktree-merge-chain-governance/raw-20260321-1045/code-reviews
- source_candidate: `docs/B1-docs/raw-20260321T170600Z/candidates.md#c-20260321-1045-001`
- source_brainstorm: `docs/B1-docs/raw-20260321T170600Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/B2-docs/git-worktree/worktree-maintenance-governance/raw-20260320-1405issues/worktree-maintenance-governance.md`
- session_refs:
  - {tool: cc-use-codex-cli, session_id: "11111111-2222-4333-8444-555555555555", jsonl_path: "/Users/zhaoyu/.claude/projects/-private-tmp-freely-cc-codex-real-ed64yw-project/11111111-2222-4333-8444-555555555555.jsonl", role: "integration-smoke"}
  - {tool: codex-cli, session_id: "019d0f86-7c2e-7f50-999f-10cf4935e7ba", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/21/rollout-2026-03-21T01-27-02-019d0f86-7c2e-7f50-999f-10cf4935e7ba.jsonl", role: "integration-smoke"}

## Why

现有 `worktree-maintenance-governance` 已能处理单棵树 audit、平面 merge-prep 与 retirement handoff，但 dogfooding 证明还缺少一类高频现实场景：

- 当前 worktree 不是从 `develop` 直接派生，而是依赖未合并父分支
- child 分支完成并不代表可以直接并入 `develop`
- parent 自己的 cleanliness / docs / issue / review 也是 gate
- 基于最新 `develop` 的 merge-prep worktree 会暴露新的 additive governance conflict 或 integration bug

如果 skill 不显式表达这条链路，Freely 仍会反复靠人工经验判断“下一步该合谁、该在哪一层停下、问题归因到哪一层”。

## Scope

1. 扩展 `skill:worktree-maintenance-governance`
2. 新增 `stacked_merge_chain` 模式
3. 为该模式补专门 reference，明确：
   - child / parent / merge-prep / develop 四层 gate
   - parent-first merge rule
   - merge-prep worktree creation rule
   - integration-fix attribution
4. 更新 `lead-agent`、`manager-agent`、`start-lead-agent.sh`
5. 增加最小脚本回归，锁定 stacked merge-chain 提示

## Acceptance

- `worktree-maintenance-governance` 明确支持 `stacked_merge_chain`
- skill 能输出逐层 checklist，而不是只给一个 merge-ready 结论
- skill 明确要求：child 不得跳过 parent 直接合向 `develop`
- skill 明确要求：parent dirty / docs 未承接时，必须先收口 parent
- skill 明确要求：复杂链路必须显式创建 merge-prep worktree，而不是在 `develop` 主工位直接试合
- skill 能区分 additive governance conflict、real code conflict、merge-prep integration fix

## Completion

- `docs/system/workspace/skills/worktree-maintenance-governance/SKILL.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/stacked-merge-chain.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/merge-prep.md`
- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `docs/B2-docs/ibm/stacked-worktree-merge-chain-governance/code-reviews/20260326-stacked-merge-chain-canonical-replay-verification.md`

## Verification Summary

- canonical replay 继续证明：`worktree-maintenance-governance` 已支持 `stacked_merge_chain`，并保留 child -> parent -> merge-prep -> develop 的逐层 gate、parent-first merge rule 和 integration-fix attribution。
- 当前 issue 要求的是 skill/reference/prompt truth 收敛，不是 CLI 自动决策；后者若要继续推进，应从同一主题新开 candidate，而不是把当前 issue 继续留在 active queue。
- 当前批次据此把本 issue 从 `in_verification` 关闭为 `completed`。
