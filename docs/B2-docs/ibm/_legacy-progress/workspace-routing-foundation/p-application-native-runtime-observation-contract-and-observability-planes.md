# Progress: application-native-runtime-observation-contract-and-observability-planes

- issue_id: `I-20260324-0415`
- title: Application-native runtime observation contract and observability planes
- phase_state: `completed`
- runtime_state: `closed_for_this_batch`
- summary: 最小 observability contract 的 dev/verification slice 已完成：`live-status` / `fleet-status` 承接 `current-state plane` / `fleet plane`，artifact plane 承接 canonical acceptance evidence，状态面只镜像最小 acceptance 摘要与 shared `deep ref groups`。当前 issue 已完成，后续若继续 richer runtime / UI observability productization，应新开 follow-on lifecycle，而不是重开本 issue。
- completed:
  - freeze application-native observation contract scope
  - freeze five observation planes and minimum identity block
  - freeze canonical acceptance evidence home in artifact plane
  - freeze mirrored summary rule for current-state / fleet / API
- freeze shared minimum deep-ref vocabulary across CLI/TUI/GUI/API
- write the minimum plane/deep-ref/acceptance-ref contract into active truth and runtime-facing references
- next:
  - merge this completed contract slice back to `develop`
  - keep richer runtime / UI productization out of this issue unless required by the minimum contract

## Verification

- `./bin/governance-check`
- `rg -n "current-state plane|fleet plane|artifact plane|acceptance evidence|acceptance_ref|deep ref|progress signal|stall signal" docs/system/workspace/three-loop-capability-lifecycle.md docs/system/workspace/skills/freely-multi-worktree-supervision/SKILL.md docs/system/workspace/skills/freely-watchdog-control-plane/SKILL.md docs/system/workspace/scripts/README.md docs/LAWS.md`
- `docs/epics/workspace-routing-foundation/application-native-runtime-observation-contract-and-observability-planes/code-reviews/20260324-application-native-runtime-observation-contract-and-observability-planes-verification.md`

## Completion Note

- `pre-tests.md` 的最小 contract checks 已全部满足。
- richer runtime / UI productization 与多 subagent 一等可视化保持为 follow-on scope，不阻塞本 issue `completed`。
