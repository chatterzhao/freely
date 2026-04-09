# Tasks: verification-contract-and-premerge-adequacy-governance

1. 更新 `doc-ibm-execution` / checklist / quality bar，强制 `pre-tests.md` 始终包含 `Unit`、`Integration`、`End-to-End`、`Real-Environment` 四章。
2. 为章节不适用场景冻结有限 `not_applicable_reason` 白名单，并要求额外一句短解释，避免自由发挥。
3. 更新 verification 真源，冻结 manager / worker handoff 必带的 machine-readable verification metadata。
4. 更新 `pre-tests.md` contract，补齐任务引用、测试用例设计、lane / environment / promotion requirement 等 adequacy 字段。
5. 设计 `test-pre-merge-* -> develop` fallback gate，只消费 owner issue 绑定的 `pre-tests.md`。
6. 让 gate 至少能区分：`pre_tests_missing`、`testcase_derivation_missing`、`execution_missing`、`verification_state_missing`。
7. 回写 milestone / candidate / owner IBM package，并在实现阶段补 focused regression 与 verification evidence。
