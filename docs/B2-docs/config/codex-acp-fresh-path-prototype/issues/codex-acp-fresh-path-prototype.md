# Issue: codex-acp-fresh-path-prototype

- issue_id: `I-20260401-1545-A-01`
- title: Codex ACP fresh-path prototype
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-acp-fresh-path-prototype`
- issue-name: `codex-acp-fresh-path-prototype`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260401/candidates.md#c-20260401-1545-a`
- source_brainstorm: `docs/B1-docs/raw-20260401/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/codex-acp-fresh-path-prototype/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/config/codex-acp-fresh-path-prototype/code-reviews`
- depends_on:
  - `docs/B2-docs/acp/acp-optional-adapter-boundary-governance/issues/acp-optional-adapter-boundary-governance.md`
  - `docs/B2-docs/runtime/runtime-adapter-axis-and-per-tool-adapter-selection/issues/runtime-adapter-axis-and-per-tool-adapter-selection.md`
  - `docs/B2-docs/config/codex-verified-resume-evidence-governance/issues/codex-verified-resume-evidence-governance.md`
  - `docs/B2-docs/ibm/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
  - {tool: shell, session_id: "51019", jsonl_path: "unavailable://pty-download-session", role: "binary-acquisition-exec"}
  - {tool: codex, session_id: "019d4c11-0bc0-7492-a63f-e9bbc1962d5b", jsonl_path: "unavailable://codex-acp-binary-session", role: "real-acp-fresh-sample"}

## Why

ACP 边界已经冻结，runtime `adapter axis` 也已经 materialize 到 config / dispatch / status truth。下一步如果继续停在抽象层，只会重复“ACP 可不可以”而不产生真实判断。

第一刀 prototype 应优先选 `codex`，原因是：

1. `codex` 是当前宪法已承诺工具面，且 direct path 是 Freely 最成熟的 canonical implementation。
2. `codex` 没有 `cc-use-codex-cli` 的 nested capability 复杂度。
3. ACP 官方 agents / registry 当前已有 Codex CLI adapter 现实，因此它不是纯 speculative target。
4. Freely 对 `codex` 的 strongest contract 是 explicit resume evidence；因此第一刀 prototype 必须收窄为 fresh path，而不是一开始就假定 ACP 能无损替代 current direct resume semantics。

## Scope

1. 为 `codex` 增加第一条真实 `adapter=acp` path。
2. 第一刀只覆盖：
   - `fresh`
   - `fresh_with_handoff`
3. 保持 `codex + adapter=direct` 继续承担 strongest explicit resume contract。
4. 在 ACP path 下继续写回同一套 Freely truth：
   - config
   - status
   - launch metadata
   - continuity / evidence surfaces
5. 若 ACP path 当前不具备 explicit resume parity，则：
   - `resume` 不得假装等价
   - runtime 必须显式 blocked / reroute / stay-direct
6. 给 `codex` 冻结第一版 per-tool ACP support contract：
   - supported adapters
   - launch kinds allowed by each adapter
   - continuity caveats

## Non-Goals

1. 不在本 issue 中让所有工具都支持 ACP。
2. 不在本 issue 中把 ACP path 升格成 `codex` 的默认路径。
3. 不在本 issue 中实现 `codex + adapter=acp` 的 resume parity，除非真实验证显示它已经等价且证据完整。
4. 不重写 Freely 的 continuity / recovery / governance surfaces。
5. 不把外部 ACP adapter 的能力空洞包装成“已经等价于 direct”。

## Acceptance

1. `codex` 的 runtime metadata 明确支持：
   - `adapter=direct`
   - `adapter=acp`
2. `freely init` / `freely set-tool` / `status` 对 `codex` 的 ACP path 继续走现有 adapter truth surfaces，不新增平行配置面。
3. `monitor-ai-cli.sh` / `tool-launchers.sh` 能在 `tool=codex` 且 `adapter=acp` 时进入一条真实 launcher path，而不是仅停留在 unsupported placeholder。
4. 在真实环境里，`codex + adapter=acp` 至少能完成一个最小 fresh task。
5. `codex + adapter=direct` 的 existing fresh/resume path 不出现回归。
6. 若 `codex + adapter=acp` 当前不支持 explicit resume target，则：
   - `resume` 不得 silently degrade
   - tests/documentation 明确该限制
7. issue / PRD / pre-tests / tasks / brainstorm 对“fresh-path first, direct retains resume strongest contract”口径一致。

## Ready For Dev

建议按四个 slice 推进：

1. metadata slice
   - 为 `codex` 显式声明 `supported_adapters=direct,acp`
   - 冻结 `direct` 与 `acp` 各自允许的 launch kinds
2. launcher slice
   - 在 `tool-launchers.sh` / `monitor-ai-cli.sh` 增加 `codex + acp` path
3. continuity slice
   - 保持 existing evidence surfaces
   - 对 ACP path 的 fresh launch 写回最小 canonical metadata
4. validation slice
   - focused regressions
   - one real-environment fresh task via `codex + adapter=acp`

## Implementation References

- `docs/B2-docs/acp/acp-optional-adapter-boundary-governance/issues/acp-optional-adapter-boundary-governance.md`
- `docs/B2-docs/runtime/runtime-adapter-axis-and-per-tool-adapter-selection/issues/runtime-adapter-axis-and-per-tool-adapter-selection.md`
- `docs/B2-docs/config/codex-acp-fresh-path-prototype/brainstorms/b-codex-acp-fresh-path-prototype.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/monitor-ai-cli.sh`

## Verification

- `./bin/governance-check`
- focused tests for `codex` adapter metadata, launch dispatch, and unsupported resume semantics
- one real-environment `codex + adapter=acp` fresh-path sample
- regression coverage that `codex + adapter=direct` still owns strongest resume path

## Next

- `2026-04-01 21:26 PDT` completion: `develop` merge `a0f9a48` absorbed the first real `codex + adapter=acp` prototype, and canonical develop rechecks kept the fresh-path bridge green.
- This owner closes as a fresh-path prototype only: direct path still owns the strongest explicit `resume` contract, and ACP parity beyond `fresh` / `fresh_with_handoff` must reopen as new lifecycle work.
- Re-open only if canonical develop evidence shows the Codex ACP bridge regressing, or if a later owner is ready to prove explicit resume parity rather than assuming it.
