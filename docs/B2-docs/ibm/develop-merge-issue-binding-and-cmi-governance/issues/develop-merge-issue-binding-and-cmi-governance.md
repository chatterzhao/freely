# Issue: develop-merge-issue-binding-and-cmi-governance

- issue_id: `I-20260321-1835-A`
- title: Develop merge issue binding and C/M/I gate governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `develop-merge-issue-binding-and-cmi-governance`
- issue-name: `develop-merge-issue-binding-and-cmi-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260321/candidates.md#c-20260321-1835-a`
- source_brainstorm: `docs/B1-docs/raw-20260321/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/code-reviews`
- depends_on:
  - `docs/system/workspace/scripts/quality/governance-merge-gate`
  - `docs/system/workspace/hooks/pre-merge-commit.sh`
  - `docs/system/workspace/scripts/tests/test-governance-merge-gate`
  - `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

当前 develop merge gate 已经修掉了 hook 时序缺口，但还存在第二层漏洞：

- merge diff 里只要带一个 `status: absorbed` 的候选
- 且它的 `promoted_issue_path` 指向仓库里某个存在的 owner issue
- gate 就可能把它当成 develop merge 的充分治理证据

这不够。develop-bound implementation merge 必须先绑定到一个具体 issue，再验证这一条 issue 的 `C/M/I` 链是否完整、candidate 状态是否属于允许放行的少数状态。否则可以拿不相干的 owner issue 借道过门禁。

本轮又确认了第三层缺口：即便 merge diff 已经绑定到一个真实 owner issue，gate 仍可能放过两类不完整 execution merge：

- capability / implementation 变更由 `in_ibm` / `done_ibm` / `completed` issue 挂名
- capability / implementation 变更只带 bare issue doc，不带 same-line `progress` 或 `review`

结果是代码已经进 `develop`，但 lifecycle 还停在 pre-execution phase 或 bare issue，后续 closeout 只能人工补写。

## Scope

1. develop merge 若没有具体 issue / progress / review owner 进入 diff，直接阻断。
2. touched candidate 必须与同次 merge 中的 owner issue 处于同一条 `C/M/I` 线。
3. `promoted` / `absorbed` 不能只靠仓库里“存在某个 owner issue”放行；owner issue 或其 linked progress/review 必须进入同次 merge。
4. capability / implementation 变更只能由 execution-phase owner issue 挂名：
   - `in_dev`
   - `blocked_dev`
   - `in_verification`
5. capability / implementation 变更不能只带 bare issue：
   - `in_dev` / `blocked_dev` 必须携带 same-line `progress`
   - `in_verification` 必须携带 same-line `progress` 或 `review`
6. 用 focused regressions 锁住：
   - candidate-only merge
   - borrowed owner issue
   - absorbed candidate 试图借 unrelated issue 过门禁
   - capability change + `in_ibm` owner
   - capability change + `in_dev` owner but no progress
   - capability change + `in_verification` owner but no progress/review
7. 正向放行矩阵也必须锁住：
   - same-line direct issue touch
   - promoted candidate 携带自己的 owner issue/progress
   - absorbed candidate 携带 canonical owner issue/progress
   - cross-line progress owner 仍被阻断
   - capability change + `in_dev` owner + same-line progress
   - capability change + `in_verification` owner + same-line review

## Acceptance

- develop-bound merge 若没有具体 issue/progress/review owner 进入 diff，会被 `governance-merge-gate` 拦截
- develop-bound merge 若 touched candidate 与 touched owner issue 不在同一条 `C/M/I` 线上，会被拦截
- `promoted` candidate 若 owner issue 未随同 merge diff 进入，不能放行
- `absorbed` candidate 若 absorbing owner 未随同 merge diff 进入，不能放行
- focused regressions 明确覆盖 borrowed owner issue 场景
- capability / implementation merge 若 owner issue 仍处于 `in_ibm` / `done_ibm` / `completed`，会被拦截
- capability / implementation merge 若 `in_dev` / `blocked_dev` 只带 bare issue 而无 same-line `progress`，会被拦截
- capability / implementation merge 若 `in_verification` 只带 bare issue 而无 same-line `progress` / `review`，会被拦截
- same-line direct issue touch 会被放行
- `promoted` candidate 携带同线 owner issue/progress 会被放行
- `absorbed` candidate 携带 canonical owner issue/progress 会被放行
- `promoted` candidate 若尝试借不同 lifecycle 线的 progress owner，会被拦截
- capability / implementation merge 若 `in_dev` owner 携带 same-line `progress`，会被放行
- capability / implementation merge 若 `in_verification` owner 携带 same-line `review`，会被放行
- `pre-merge-commit` 真实 `git merge` 路径继续命中同一 gate

## Ready For Dev

当前边界已经稳定：

1. 本 issue 不是 reopen `three-loops-sibling-relationship-and-terminal-governance`，而是 `C-20260321-1835-A` 的独立 gate follow-on。
2. 第一阶段先把“issue binding + same-line C/M/I”收紧到 `governance-merge-gate`，不顺手重写整个 milestone / issue lifecycle 法则。
3. 本 issue 自己必须以独立 owner issue 进入 merge，不能再借 absorbed supporting evidence 自证合法。

## Implementation References

- `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/brainstorms/b-develop-merge-issue-binding-and-cmi-governance.md`
- `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/prd.md`
- `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/pre-tests.md`
- `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/tasks.md`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/hooks/pre-merge-commit.sh`

## Completion

- `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
- `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/brainstorms/b-develop-merge-issue-binding-and-cmi-governance.md`
- `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/prd.md`
- `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/pre-tests.md`
- `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-develop-merge-issue-binding-and-cmi-governance.md`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `docs/system/workspace/scripts/tests/test-pre-push-hook`

## Verification

- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/test-pre-merge-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-pre-push-hook`
- `./bin/governance-merge-gate --staged`

## Next

- `2026-03-30 16:41 PDT` the strengthened gate landed on `develop` as commit `5e3ec97`.
- Follow-on runtime closeout replay then proved the new boundary in real use: initial merge attempts were blocked for completed-owner and absorbed-candidate misuse, and the corrected same-line execution-owner merge passed as `544e1dd`.
- Canonical verification truth is now `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/code-reviews/20260330-develop-merge-cmi-gate-verification.md`.
- Future regressions that bypass owner issue binding, same-line `C/M/I`, execution-phase ownership, or same-line progress/review must reopen as new lifecycle work instead of mutating this completed owner.
