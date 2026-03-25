# Progress: application-native-runtime-observation-contract-and-observability-planes

- issue: `I-20260324-0415`
- title: Application-native runtime observation contract and observability planes
- phase_state: `done_ibm`
- runtime_state: `ready_for_dev_handoff`
- summary: 已把 observability 方向从 pre-brainstorm materialize 成正式 IBM。当前 shared contract 已冻结：artifact plane 持有 canonical acceptance evidence，current-state / fleet / API 只镜像最小摘要与 `acceptance_ref`，CLI/TUI/GUI/API 共享同一组最小 `deep ref groups`；下一步进入 dev，把最小 machine-readable contract 写进 active truth 与 runtime-facing references。
- completed:
  - freeze application-native observation contract scope
  - freeze five observation planes and minimum identity block
  - freeze canonical acceptance evidence home in artifact plane
  - freeze mirrored summary rule for current-state / fleet / API
  - freeze shared minimum deep-ref vocabulary across CLI/TUI/GUI/API
- next:
  - enter dev and write the shared contract into active truth / runtime-facing references
  - keep richer runtime / UI productization out of this issue unless required by the minimum contract
