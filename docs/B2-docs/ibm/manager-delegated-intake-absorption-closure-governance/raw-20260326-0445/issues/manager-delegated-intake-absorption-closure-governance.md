# Issue: manager-delegated-intake-absorption-closure-governance

- issue_id: `I-20260326-0445`
- title: Manager-delegated intake absorption closure governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-delegated-intake-absorption-closure-governance`
- issue-name: `manager-delegated-intake-absorption-closure-governance`
- verification_artifact_dir: docs/B2-docs/ibm/manager-delegated-intake-absorption-closure-governance/raw-20260326-0445/code-reviews
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260326T181000Z/candidates.md#c-20260326-0445-a`
- source_brainstorm: `docs/B1-docs/raw-20260326T181000Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`
  - `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`

## Why

Freely 已经解决了 manager delegated continuation 的：

- intake durability
- classification / delegation
- prompt-level consumed evidence
- live-status pending-vs-consumed 可见性

但真实 dogfood 证明当前还缺最终 lifecycle closure：

- manager continuity 会把旧 interruption 一再写入 `absorbed_intake_ids`
- session-state / live-status 会把同一批 delegated continuation 记为 consumed
- 对应 `.freely/intake/<id>/meta.env` 却长期停在 `STATUS="delegated"`

这样会制造两个坏结果：

1. machine-readable backlog 会无限积灰，主管必须不断解释“这些其实已经 absorb 过”；
2. manager judgement absorbed 与 intake lifecycle absorbed 长期分离，导致治理和 runtime truth 漂移。

`I-20260322-0049` 已完成 scope 明确只覆盖 generated / consumed_into_prompt / pending_after_failure，不承接这层最终 closure，因此需要新的 lifecycle。

## Scope

1. 为 manager-owned delegated continuation 定义最终 absorbed closure contract。
2. 只在“本轮 delegated continuation 已进入当前 prompt，且本轮成功产出新的 manager continuity / followthrough artifact”时，将对应 intake lifecycle 收成 `absorbed`。
3. 失败轮、未产出 continuity 的轮次继续保持 `delegated`，保留 recovery / reentry 能力。
4. 把 absorbed 后的 `LINKED_ARTIFACT` / `ABSORPTION_TARGET` 指向真实 continuity / followthrough artifact，而不是继续停在 pending delegation。
5. 补 focused regression，确保：
   - 成功 continuity round 会关闭 intake lifecycle
   - active prompt visibility 仍正确
   - 失败或停机后不误关 lifecycle

## Non-Goals

1. 不重写 interruption dispatcher。
2. 不把所有 delegated intake 一刀切 absorbed。
3. 不同时扩展 worker-side delegated continuation lifecycle closure。
4. 不把 continuity 文本里的 `absorbed_intake_ids` 重新定义为唯一 machine-readable truth。

## Acceptance

1. 当 manager prompt 吸收 delegated continuation，且本轮成功产出新的 manager continuity 文件时，对应 intake `meta.env` 会被改写为 `STATUS="absorbed"`。
2. absorbed 后的 intake `LINKED_ARTIFACT` / `ABSORPTION_TARGET` 必须指向真实 continuity / manager followthrough artifact，不再停在 `pending://interruption-manager-delegation` 或 `handoff://continuation`。
3. 若本轮 manager 没有产出新的 continuity 文件，或当前轮失败退出，则对应 intake 必须继续保持 `STATUS="delegated"`。
4. `live-status` 的 pending delegated 视图不得因为本修复而丢失 active-prompt consumed / stopped-after-failure reentry 语义。
5. regression tests 至少覆盖：
   - delegated continuation 进入 manager prompt 后，成功写出 continuity 并关闭 intake lifecycle
   - active prompt visibility 仍显示 consumed 而非 pending
   - 无新 continuity 时 intake 不会误吸收

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-intake-absorption-closure`
- `docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `docs/progress/workspace-routing-foundation/p-manager-delegated-intake-absorption-closure-governance.md`
- `docs/B2-docs/ibm/manager-delegated-intake-absorption-closure-governance/code-reviews/20260326-manager-delegated-intake-absorption-closure-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-intake-absorption-closure`
- `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`

## Verification Summary

- The implementation is already present on canonical `develop` through same-family commit `93375c8` (`fix: close manager delegated intake lifecycle`).
- Focused regression still passes after replay:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-intake-absorption-closure`
  - `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status`
  - `./bin/governance-check`
- This closes only the manager-owned delegated intake lifecycle contract. It does not claim completion for unrelated worker-side delegated continuation or broader owner lifecycle families.
