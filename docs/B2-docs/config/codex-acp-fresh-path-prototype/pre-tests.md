# Pre-tests: codex-acp-fresh-path-prototype

## Acceptance Structure

### Pre-merge focused regression / smoke

1. `metadata-surface`
   - `codex` 当前 supported adapters 明确为 `direct,acp`
   - status surface 能显示 `tool_supported_adapters: direct,acp`
   - `codex` 的 per-adapter launch-kind restrictions 有 focused coverage
2. `launcher-surface`
   - `monitor-ai-cli.sh` / `tool-launchers.sh` 在 `tool=codex` 且 `adapter=acp` 时进入真实 ACP launcher path
   - focused coverage now includes a fake ACP agent end-to-end turn, not just unsupported placeholder assertions
   - `tool=codex` 且 `adapter=direct` 继续走现有 direct path
3. `resume-safety`
   - `codex + adapter=acp + resume` 不会 silently degrade
   - runtime 对该组合给出显式 blocked / unsupported / reroute signal

### Post-merge integration acceptance

1. `freely init --ai codex:gpt-5.4:auto --tool-adapter acp` 与 `freely set-tool --tool codex --tool-adapter acp` 能把项目切到真实 ACP launch path。
2. `codex + adapter=direct` 的 existing direct fresh / resume regressions 继续通过。
3. ACP path 不新增第二套 continuity / recovery / status truth。

### Post-merge application-native real-environment acceptance

1. 在真实 project workcell 中，`codex + adapter=acp` 至少能完成一个最小 fresh task。
2. 若对同一 project 显式请求 `launch_kind=resume` 且 adapter 为 `acp`，runtime 必须显式说明当前限制，而不是伪造 direct-equivalent resume。
3. 若第一次 ACP launch 依赖自动拉取 `codex-acp` release binary，则需要把 binary acquisition 成功也视为 viability evidence 的一部分。

### Non-Goals

1. 本轮不要求所有工具都进入 ACP。
2. 本轮不要求 `codex + adapter=acp` 已实现 resume parity。
3. 本轮不要求 ACP path 成为 `codex` 默认 adapter。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `codex metadata and launcher dispatch expose a real ACP path instead of a placeholder`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-acp-fresh`

### PT-2
- id: `PT-2`
- requirement: `codex ACP prototype keeps direct-path configuration and adapter policy surfaces canonical`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-tool-adapter-policy-resolution`

### PT-3
- id: `PT-3`
- requirement: `real-environment codex ACP fresh-path viability evidence is captured before closeout`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/B2-docs/config/codex-acp-fresh-path-prototype/code-reviews/20260401-codex-acp-fresh-path-prototype-verification.md`
