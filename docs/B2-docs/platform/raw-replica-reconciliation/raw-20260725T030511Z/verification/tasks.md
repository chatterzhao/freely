# Tasks: I-20260725T030511Z-A

1. 定义并测试 raw 副本 projection 与 reconciliation receipt。
2. 统一 adapter 的 raw search/discovery 结果契约，修复空结果与大小写边界。
3. 将 scan 读取失败显式表示为 degraded。
4. 将 `wt-create`、PR 和 close 入口接入同一只读 gate。
5. 在 test-pre-merge 运行真实平台无写验证与回归测试。
