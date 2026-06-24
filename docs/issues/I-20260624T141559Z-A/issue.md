- issue_id: I-20260624T141559Z-A
- kind: fix
- phase_state: done_dev
- milestone: M-20260624T141559Z-A
- source_candidate: docs/pre-brainstorms/20260624T141559Z--feedback-issue-sync/candidates.md#C-20260624T141559Z-A
- source_raw: raw-20260624T141559Z
- verification_artifact_dir: docs/epics/feedback-issue-sync/code-reviews
- canonical_issue_path: docs/issues/I-20260624T141559Z-A/issue.md
- title: cmd_feedback 改为 issue-sync 薄封装

# I-20260624T141559Z-A: cmd_feedback 对齐 issue-sync 多平台架构

- source_candidate: `docs/pre-brainstorms/20260624T141559Z--feedback-issue-sync/candidates.md#C-20260624T141559Z-A`
- source_raw: `raw-20260624T141559Z`
- verification_artifact_dir: `docs/epics/feedback-issue-sync/code-reviews`
- pre_tests_path: `docs/epics/feedback-issue-sync/pre-tests.md`

## 实现

`cmd_feedback` 改为 `issue-sync create` 薄封装：
1. 去掉 `--repo` 参数，repo 由 `issue-sync` 从 git remote 自动检测
2. 生成 `docs/issues/raw-{key}/issue.md` 本地文件
3. 调用 `issue-sync create` 推送到所有配置的平台
4. 删除 `_resolve_gh_repo()` helper
5. 修复 crash reporter 中的 `--repo` 调用

改动仅 `docs/system/workspace/scripts/runtime/freely` 一个文件。
