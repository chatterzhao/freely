# Tasks

1. 把 `I-20260405-1615-A` 冻结的 promote model 映射到治理真源，不再保留 `feature/* -> develop` 的旧默认路径。
2. 同轮更新直接耦合的 gate enforcement 和 regression tests，避免文档与脚本分叉。
3. 保持 `test-pre-merge-*` family 作为 single-feature 与 explicit multi-bundle 的共享前缀，不新增第二个 `test-pre-*` 前缀。
4. 保留 `hotfix/* -> develop` 的合法路径。
5. 不扩大到 lifecycle automation、manifest generation、batch-create UX。
6. 完成 candidate / milestone / issue 写回，使后续 execution authority 以本 owner 为准。
