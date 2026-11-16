# Tasks — raw-20261116T050414Z

- [x] T1: 新增 `docs/system/workspace/scripts/runtime/raw_title_normalize.py`：`normalize_open_raw_titles()`（title+body 定 key、canonical_raw_title 算 expected、仅 adapter 写标题、from→to 日志、幂等、dry-run、失败非零）
- [x] T2: `runtime/freely.cmd_task_source_scan()` 在分析器前调用规范化 preflight；刷新 `bin/freely` 投影锁
- [x] T3: `raw-reconciliation-gate` / `reconcile()` 新增 `non_canonical_title` 结构化诊断；`freely_wt_assert_raw_reconciled_readonly()` 打印精简摘要
- [x] T4: `pr-create-guarded` Step 0b 增加 preflight：仅 `non_canonical_title` 时规范化并重跑门禁
- [x] T5: 新增 AT `test-raw-title-normalize.py`，develop 基线 RED → 修复后 GREEN，纳入 CORE/CI_CORE
- [x] T6: test-pre-merge 工位 FF 同步 → `test-gate run --command "bin/test-all --ci"` → GREEN
后续受门禁保护的收口切片（按 pipeline 顺序执行，状态回写 goal 恢复点）：

1. `pr-create-guarded` → `pr-review-guarded` → `pr-merge-guarded`
2. `wt-close` → 更新 goal 恢复点 / memory

> 进度：B1/B2 完成，待 RED 阶段确认基线红后进入 dev 实现。
