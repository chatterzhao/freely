# Tasks: 关闭路径先校验后执行，部分成功独立退出码
- issue_id: I-20261104T082603Z-A
- pre_tests_path: docs/B2-docs/gate/platform/raw-20261104T082603Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复核 5 处证据点（adapter 先于 transition、终态约束、严格路径压码、非严格路径无条件写 closed、adapter 两态退出码）。
- [x] T2: 写 AT-001（静态 + stub adapter 行为 + issue-sync 端到端），基线快照确认 RED。
- [x] T3: `raw_lifecycle_effects.py` 四段式改造 + 终态错误信息带 current phase。
- [x] T4: `platform-adapter.py` `_close_exit_code()` 与 `close-multi`/`close-raw` 0/3/1。
- [x] T5: `bin/issue-sync` 严格路径上抛 3/1、非严格路径逐平台记账。
- [x] T6: 跑 GREEN、5 个相关回归基线对比、真实仓库只读核验。
- [x] T7: 补齐 B2 验证文档与 milestone，按封装命令收口。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7 | AT-001 |
