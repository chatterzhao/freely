# Issue: develop-merge-issue-binding-and-cmi-governance

- issue_id: `I-20260321-1835-A`
- title: Develop merge issue binding and C/M/I gate governance
- phase_state: `in_dev`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `develop-merge-issue-binding-and-cmi-governance`
- issue-name: `develop-merge-issue-binding-and-cmi-governance`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260321-1835--lifecycle-complete-before-merge-governance/candidates.md#c-20260321-1835-a`
- source_brainstorm: `docs/pre-brainstorms/20260321-1835--lifecycle-complete-before-merge-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/code-reviews`
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

## Scope

1. develop merge 若没有具体 issue / progress / review owner 进入 diff，直接阻断。
2. touched candidate 必须与同次 merge 中的 owner issue 处于同一条 `C/M/I` 线。
3. `promoted` / `absorbed` 不能只靠仓库里“存在某个 owner issue”放行；owner issue 或其 linked progress/review 必须进入同次 merge。
4. 用 focused regressions 锁住：
   - candidate-only merge
   - borrowed owner issue
   - absorbed candidate 试图借 unrelated issue 过门禁

## Acceptance

- develop-bound merge 若没有具体 issue/progress/review owner 进入 diff，会被 `governance-merge-gate` 拦截
- develop-bound merge 若 touched candidate 与 touched owner issue 不在同一条 `C/M/I` 线上，会被拦截
- `promoted` candidate 若 owner issue 未随同 merge diff 进入，不能放行
- `absorbed` candidate 若 absorbing owner 未随同 merge diff 进入，不能放行
- focused regressions 明确覆盖 borrowed owner issue 场景
- `pre-merge-commit` 真实 `git merge` 路径继续命中同一 gate

## Ready For Dev

当前边界已经稳定：

1. 本 issue 不是 reopen `three-loops-sibling-relationship-and-terminal-governance`，而是 `C-20260321-1835-A` 的独立 gate follow-on。
2. 第一阶段先把“issue binding + same-line C/M/I”收紧到 `governance-merge-gate`，不顺手重写整个 milestone / issue lifecycle 法则。
3. 本 issue 自己必须以独立 owner issue 进入 merge，不能再借 absorbed supporting evidence 自证合法。

## Implementation References

- `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/brainstorms/b-develop-merge-issue-binding-and-cmi-governance.md`
- `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/prd.md`
- `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/tasks.md`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/hooks/pre-merge-commit.sh`

## Completion

- `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
- `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/brainstorms/b-develop-merge-issue-binding-and-cmi-governance.md`
- `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/prd.md`
- `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-develop-merge-issue-binding-and-cmi-governance.md`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`

## Verification

- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/test-pre-merge-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-pre-push-hook`
- `./bin/governance-merge-gate --staged`

## Next

- next_action: `implement and verify same-line issue binding enforcement`
- revisit_trigger: 若后续仍发现无 issue owner、borrowed owner、或 absorbed candidate 借 unrelated issue 过 develop gate，则继续沿本 issue 追加 regression
