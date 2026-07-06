# Pre-tests

## Pre-merge acceptance

1. 对于 manager 工位上的 local delegated continuation：
   - 当 runtime 把它写入当前 prompt
   - 且同一轮成功产出新的 `manager-continuity-*.md`
   - 对应 `.freely/intake/<id>/meta.env` 必须从 `STATUS="delegated"` 收成 `STATUS="absorbed"`。
2. absorbed 后的 intake 必须把 `LINKED_ARTIFACT` / `ABSORPTION_TARGET` 指向真实 continuity / followthrough artifact，而不是继续保留 `pending://...` / `handoff://continuation`。
3. 如果 delegated continuation 虽然进入 prompt，但本轮没有新 continuity 文件，或轮次失败退出，则 intake 必须保持 `STATUS="delegated"`。
4. active prompt visibility contract 不能回退：
   - AI 活跃时，同一 intake 显示为 consumed，不再显示为 pending
   - 停机且未完成 absorbed closure 时，它仍能重新回到 pending
5. 本轮测试必须直接断言 intake `meta.env` 的状态变化，而不是只看 continuity 文本里的 `absorbed_intake_ids`。

## Post-merge acceptance

1. 在 canonical `develop` 上通过 `freely chat` 写入 same-family continuation 后，如果 manager 成功写出新的 continuity，历史 delegated intake 不应无限残留为 `STATUS="delegated"`。
2. `live-status` 不得同时再出现“pending ids 与 last consumed ids 完全同一批”的漂移，除非当前没有成功 continuity 输出而只是 recovery 中间态。
3. 该修复不能被误用为完成判据：
   - `I-20260318-1630`、`C-20260323-2045-A` 仍按 issue completion chain + worktree retirement chain 判断完成
   - intake absorbed 只代表 interruption lifecycle 收口，不代表对应 issue 已完成
