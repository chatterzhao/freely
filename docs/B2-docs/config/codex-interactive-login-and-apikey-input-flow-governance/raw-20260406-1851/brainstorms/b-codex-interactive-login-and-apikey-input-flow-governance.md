# IBM Brainstorm: codex-interactive-login-and-apikey-input-flow-governance

## Frozen Boundary

- Treat interactive `freely ai login codex` mode selection and `freely ai login codex apikey` input collection as a bounded Codex-first UX owner.
- Preserve direct-arg parity with `--name/--url/--key` without widening the owner into generic provider registries or multi-tool UX.
- Keep this owner separate from current-live bootstrap, watchdog/bootstrap identity semantics, and standalone backend extraction.

## Implementation Notes

- Source implementation lives in `feature/codex-apikey-login-interactive`.
- Expected implementation surface is bounded to `docs/system/workspace/scripts/runtime/ai-cli` and the four issue-bound login regressions.
- Successful API-key login may materialize the live bundle and immediately save a slot, but that contract remains Codex-only inside this owner.
