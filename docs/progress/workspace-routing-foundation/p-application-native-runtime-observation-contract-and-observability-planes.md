# Progress: application-native-runtime-observation-contract-and-observability-planes

- issue: `I-20260324-0415`
- title: Application-native runtime observation contract and observability planes
- phase_state: `in_verification`
- runtime_state: `closed_for_this_batch`
- summary: 最小 observability contract 的 dev slice 已落到 active truth 与 runtime-facing references：`live-status` / `fleet-status` 承接 `current-state plane` / `fleet plane`，artifact plane 承接 canonical acceptance evidence，状态面只镜像最小 acceptance 摘要与 shared `deep ref groups`。当前进入 verification closeout，等待 manager review / merge judgement。
- completed:
  - freeze application-native observation contract scope
  - freeze five observation planes and minimum identity block
  - freeze canonical acceptance evidence home in artifact plane
  - freeze mirrored summary rule for current-state / fleet / API
- freeze shared minimum deep-ref vocabulary across CLI/TUI/GUI/API
- write the minimum plane/deep-ref/acceptance-ref contract into active truth and runtime-facing references
- next:
  - manager review whether this minimum contract slice is ready to merge
  - keep richer runtime / UI productization out of this issue unless required by the minimum contract

## Verification

- `./bin/governance-check`
- `rg -n "current-state plane|fleet plane|artifact plane|acceptance evidence|acceptance_ref|deep ref|progress signal|stall signal" docs/system/workspace/three-loop-capability-lifecycle.md docs/system/workspace/skills/multi-worktree-supervision/SKILL.md docs/system/workspace/skills/watchdog-control-plane/SKILL.md docs/system/workspace/scripts/README.md docs/LAWS.md`
- `docs/epics/workspace-routing-foundation/application-native-runtime-observation-contract-and-observability-planes/code-reviews/20260324-application-native-runtime-observation-contract-and-observability-planes-verification.md`
