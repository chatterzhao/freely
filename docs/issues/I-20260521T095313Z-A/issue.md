- issue_id: I-20260521T095313Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260521T095313Z-A
- source_candidate: docs/pre-brainstorms/20260521T095313Z--type-based-alias-resolution/candidates.md#C-20260521T095313Z-A
- verification_artifact_dir: docs/epics/type-based-alias-resolution/code-reviews
- canonical_issue_path: docs/issues/I-20260521T095313Z-A/issue.md
- title: use type instead of alias for AI_TOOL alias resolution
- summary: |
    Replace shell-dependent `alias` command with `type` for unified
    alias/function/binary resolution in _resolve_tool_family and
    _apply_tool_alias_settings. Fix Python f-string bug that prevented
    CLAUDE_CODE_SETTINGS_FILE export. Fix deploy-skills cc* mapping
    (usage text and supported tools error message).
