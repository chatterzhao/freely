# Tasks: pre-tests-evidence-binding-and-completion-gate-governance

1. 将 `C-20260327-0651-A` 物化为 issue-bound IBM artifacts，并给 issue 增加 `pre_tests_path` / `verification_artifact_dir`。
2. 定义 `pre-tests.md` 的 machine-readable acceptance item 最小字段。
3. 实现 `docs/system/workspace/scripts/quality/pretests-gate` 与 `bin/pretests-gate`。
4. 将 `pre-commit` 接到同一 gate，仅在 staged issue 准备进入 `completed` 时触发。
5. 补 focused regressions，覆盖 fail/pass 路径与非目标提交不误伤。
6. 回写 `doc-ibm-execution` references、milestone 与 progress。
