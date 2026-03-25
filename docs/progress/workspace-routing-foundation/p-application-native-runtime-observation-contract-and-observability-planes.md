# Progress: application-native-runtime-observation-contract-and-observability-planes

- issue: `I-20260324-0415`
- title: Application-native runtime observation contract and observability planes
- phase_state: `done_ibm`
- runtime_state: `active_dev`
- summary: 已从 IBM 进入 dev，第一刀先把 day-1 observability contract 写进 active truth 与 runtime-facing references：`live-status` / `fleet-status` 承接 `current-state plane` / `fleet plane`，artifact plane 承接 canonical acceptance evidence，状态面只镜像最小 acceptance 摘要与 shared `deep ref groups`。
- completed:
  - freeze application-native observation contract scope
  - freeze five observation planes and minimum identity block
  - freeze canonical acceptance evidence home in artifact plane
  - freeze mirrored summary rule for current-state / fleet / API
- freeze shared minimum deep-ref vocabulary across CLI/TUI/GUI/API
- write the minimum plane/deep-ref/acceptance-ref contract into active truth and runtime-facing references
- next:
  - review whether any remaining active truth still treats completion/delete judgement as status-surface-owned instead of artifact-plane-owned
  - keep richer runtime / UI productization out of this issue unless required by the minimum contract
