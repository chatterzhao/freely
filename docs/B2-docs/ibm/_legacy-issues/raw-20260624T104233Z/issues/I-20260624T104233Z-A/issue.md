- issue_id: I-20260624T104233Z-A
- kind: fix
- phase_state: done_b2_ibm
- milestone: M-20260624T104233Z-A
- source_candidate: docs/B1-docs/raw-20260624T104229Z33Z/candidates.md#C-20260624T104233Z-A
- verification_artifact_dir: docs/B2-docs/agents-daemon-to-pre-tests/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260624T104233Z-A/issue.md
- title: AGENTS.md daemon test refs → pre-tests.md

# I-20260624T104233Z-A: AGENTS.md daemon test refs → pre-tests.md

- source_candidate: docs/B1-docs/raw-20260624T104229Z33Z/candidates.md#C-20260624T104233Z-A
- verification_artifact_dir: docs/B2-docs/agents-daemon-to-pre-tests/code-reviews

## 实现
- AGENTS.md 中 hardcoded numbered steps（pre-init-runtime、freely-package、start daemon、verify Manager cycle、merge/fix）替换为 pre-tests.md 委托
- Freely 自举上下文保留，标注为 "daemon 型项目参考"
- `./bin/test-pre-merge-selfhost` 引用保留
- 全项目搜索确认：三个 skill 文件（freely-fix-execution、freely-test-execution、freely-feat-execution）已指向 pre-tests.md，无残留 daemon-as-test 模式
