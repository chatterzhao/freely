# Tasks: codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance

1. Teach `availability-watchdog.sh` to detect reconnect / connection-failure partial output and return `network_failure` immediately.
2. Ensure the fast-fail path terminates the probe process tree and writes the artifact before releasing the probe lock.
3. Update `ai-cli` surfaces so current-live auth flows preserve `probe_status=network_failure`.
4. Update `freely` runtime log classification so reconnect text lands in execution-network taxonomy.
5. Narrow runtime signal classification so auth/network/rate-limit detection consumes runtime `ERROR/WARN` evidence instead of arbitrary document/prompt text.
6. Replay the focused reconnect/status/runtime regression suite.
7. Re-check whether any residual diff from `feature/fix-codex-apikey-availability-lock` is still required; retire that tree if not.
