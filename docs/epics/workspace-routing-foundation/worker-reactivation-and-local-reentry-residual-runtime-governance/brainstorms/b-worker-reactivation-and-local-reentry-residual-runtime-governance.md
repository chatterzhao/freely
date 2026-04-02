# Brainstorm: worker-reactivation-and-local-reentry-residual-runtime-governance

## Goal

把 worker reactivation 与 worker-side local continuation reentry 的 residual gap 从当前 security lane 中剥离出来，冻结为单一 workspace-routing owner。

## Boundaries

- 上游已完成 owner 仍成立：
  - chat-triggered worker runtime reactivation
  - worker active reentry for manager-delegated continuation
  - manager attach reuse missing-AI repair
- 本条只吸收“它们的剩余 worker-side runtime boundary”。
- 不回收 Freely 默认自治 posture / activation consent / tool policy materialization。

## Current Reproduced Truth

1. worker chat/tui reactivation residual
   - 原始 residual 是 stopped worker + delegated continuation 仍可能走到 attach reuse
   - runtime 可写出 optimistic `already_running_attach`
   - 但未形成 durable `ai.pid`
2. worker local continuation reentry residual
   - 原始 residual 是 active-worker predicate 不够清晰
   - 现存测试、旧 verification 与 runtime truth 之间还有缝

## Closed Truth

1. worker attach-reuse 只在 AI pid 已确认 running 且归属当前项目时才允许成立。
2. worker `operator_stop` 后若只剩 supervisor 而无 durable AI child，runtime 会 repair/restart，不再写 optimistic success。
3. worker local continuation reentry 已按 frozen active-worker predicate 对齐 runtime 与 fixture。

## Materialization Direction

1. 两个残差都由同一最小 owner 承接并收口。
2. local reentry 最终证明需要 runtime repair 与 fixture contract tightening，而不只是 stale fixture cleanup。
3. 旁路 repro 若继续存在，应单独建 follow-up，不再阻塞本 owner closure。
