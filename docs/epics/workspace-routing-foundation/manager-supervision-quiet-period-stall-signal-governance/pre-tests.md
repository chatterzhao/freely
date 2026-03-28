# Pre-Tests - manager-supervision-quiet-period-stall-signal-governance

1. 当 manager AI 存活、active worker 存活、delegated continuation 已进入当前 prompt，且 manager 只是 supervision-only quiet-period 时，不得直接触发 `runtime-stalled-ai-recovery`。
2. 当存在无关 active worker 时，不得因此把当前 manager quiet-period 错判为 lawful wait。
3. 当 worker 仍 active 但并不处于 delegated-busy 时，不得因此 suppress recovery。
4. 当 quiet-period 同时伴随更强 stall 证据，例如 stale launchable prompt、missing worker runtime、或 superseded intake 时，recovery 仍必须生效。
