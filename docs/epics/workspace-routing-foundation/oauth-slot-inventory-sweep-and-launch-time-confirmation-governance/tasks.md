# Tasks

1. 将 `C-20260327-1115-A` materialize 为新的 milestone-owned follow-on issue，而不是回写已完成的 `I-20260318-1630`。
2. 在 `availability-watchdog.sh` 中增加统一的 OAuth inventory sweep 入口与结果分类。
3. 增加 availability cache 写回逻辑，并让 watchdog / `ai status` / `switch auto` 共享同一份 truth surface。
4. 把 `codex-slot-cooldowns.tsv` 改成由 full sweep overwrite 的 slot ledger，而不是增量残留。
5. 保留 launch-time auth copy / 最小真实 probe，但降级为最终确认层。
6. 补 focused regressions，直接锁住“不改活跃 auth”“先 sweep 再 switch”“cooldown overwrite”三条 contract。
7. 完成 canonical progress / verification / milestone writeback。
