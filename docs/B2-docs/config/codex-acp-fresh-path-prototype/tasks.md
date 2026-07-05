# Tasks: codex-acp-fresh-path-prototype

1. 为 `codex` 冻结第一版 per-tool adapter support matrix：`direct,acp`。
2. 为 `codex` 冻结 per-adapter launch-kind contract，明确 `acp` 首轮只支持 `fresh` / `fresh_with_handoff`。
3. 在 `tool-launchers.sh` 与 `monitor-ai-cli.sh` 中增加 `codex + adapter=acp` 的真实 launch path。
4. 保持 `codex + adapter=direct` 继续拥有 strongest explicit resume contract。
5. 对 `codex + adapter=acp + resume` 增加显式 blocked / unsupported / reroute contract，不允许 silent degrade。
6. 增加 focused tests，覆盖 metadata、status、launcher dispatch、resume-safety。
7. 跑一个真实环境 `codex + adapter=acp` fresh-path 样本，作为 prototype viability evidence。
8. 保证 `codex-acp` binary acquisition 有稳定 contract：允许用 cache / pinned release / `FREELY_CODEX_ACP_BIN` override，而不是把 `npx` optional dependency 缺失当成运行时真相。
