# Implementation Decision Note
- issue_id: I-20261104T080200Z-A
- issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261104T080200Z/issues/I-20261104T080200Z-A.md
- decision: 迁移 `bin/pr-review-guarded`（806→4 行投影）到 `scripts/worktree/`；新增注册表 `bin-projections.yaml` + 门禁 `bin/check-bin-projection`（未登记 / 过期 / 已降到阈值内三种拒绝）+ 全量清单 `bin-inventory.md`；剩余 35 条另立 `raw-20261111T125724Z`。
- why_this: 真源边界失效是真问题，但「超阈值就迁」会把自包含工具迁成影子实现；注册表 + 过期即失败既覆盖全部 99 个入口，又给剩余债务一个可收敛的路径。
- alternatives_considered: ①一次迁 38 个——多数是自包含工具或 dispatcher，硬迁产生影子实现；②只迁一个不建门禁——下次又会漂移，验收 2/3 也落空；③用 `check-file-size` 管——它对 `bin/` 按 500/750/1000 阈值分级，抓不住「投影层」这个语义。
- boundary_non_goals: 不迁 dispatcher；不迁自包含 `check-*` / `test-all`；不改 `bin/freely` 分派；不改任何命令行为。
- residual_risk: ①35 条 impl 仍是债务，需要 #4302 推进；②阈值 40 是经验值；③门禁不校验 reason 措辞。

## 为什么要有「过期即失败」这条

只有「未登记就失败」的话，注册表会变成永久豁免清单：迁完不删条目，门禁永远绿。
加「登记了但已降到阈值内 → 失败」之后，迁移完成的下一步必然是把条目删掉，
注册表只会收缩，不会膨胀。
