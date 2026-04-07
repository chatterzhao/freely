# PRD: codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance

## Problem

Freely 当前对 Codex API-key live auth 的 launch-time probe 会在明显的 reconnect / connection-failure evidence 已出现后继续等待 timeout，导致 status/switch/bootstrap surfaces 卡住且误报。

## Product Requirement

Freely must treat partial-output reconnect evidence as a bounded, network-local fast-fail signal:

1. detect it early
2. stop the probe promptly
3. preserve an artifact
4. surface `network_failure`
5. align runtime network classification with the same evidence family

## User-Facing Outcome

- `freely ai status` 不再把此类 incident 伪装成 generic timeout
- `freely ai switch codex` 在 unsaved live auth 场景下可返回 `current_auth_unusable + probe_status=network_failure`
- manager bootstrap 不会长期持有 probe lock 等待一个已知失败的 probe

## Boundaries

- Keep probe launch semantics intact.
- Keep slot rotation semantics intact.
- Do not claim auth/account invalidity from reconnect evidence alone.
