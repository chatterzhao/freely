# Pre-Tests

1. 当 protected branch ancestry 中出现普通 merge 缺 canonical trailer 且没有 matching backfill entry 时，`./bin/governance-check` 必须失败。
2. 当普通 merge 缺 trailer 但有 matching backfill entry 时，`./bin/governance-check` 必须通过。
3. 当 merge commit 已经带 canonical trailer，却仍声明普通 merge gap backfill 时，`./bin/governance-check` 必须失败。
4. break-glass merge 仍由既有 break-glass ledger 审计，不得被普通 merge gap ledger 误吸收。

## Post-merge Acceptance

1. `908a6ad` 有 canonical backfill ledger entry。
2. `governance-check` 继续覆盖普通 merge 与 break-glass merge 两条 receipt 审计路径。
3. 新 ledger 不得被解释成未来缺 trailer merge 的合法常规入口。
