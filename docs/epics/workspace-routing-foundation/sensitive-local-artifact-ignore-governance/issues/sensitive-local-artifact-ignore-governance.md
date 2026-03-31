# Issue: sensitive-local-artifact-ignore-governance

- issue_id: `I-20260329-2155-A`
- title: Sensitive local artifact ignore governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `sensitive-local-artifact-ignore-governance`
- issue-name: `sensitive-local-artifact-ignore-governance`
- priority: P2
- source_candidate: `docs/pre-brainstorms/20260329-2155--sensitive-local-artifact-ignore-governance/candidates.md#c-20260329-2155-a`
- source_brainstorm: `docs/pre-brainstorms/20260329-2155--sensitive-local-artifact-ignore-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`develop` 根目录现场出现过一个真实的 `auth.json`，而仓库没有任何规则会默认忽略它。这意味着 Freely 当前对本地敏感副产物的治理只覆盖 `.env*`，没有覆盖账号凭证、私钥、证书等常见高风险文件。

这条线的目标不是重做凭证存储，而是把“误落到仓库里的敏感本地文件不应进入 Git”冻结成一个最小、可测试的 contract。

## Scope

1. 为常见误落的本地敏感文件名和私钥/证书扩展名添加最小 `.gitignore` 保护。
2. 只引入保守、可解释的规则，不扩大成无边界黑名单。
3. 增加 focused regression，验证这些路径被 `git check-ignore --no-index` 命中。
4. 确认 `develop` 中的 stray `auth.json` 已被移除。

## Non-Goals

1. 不重做账号凭证存储架构。
2. 不追查历史所有外部工具为什么会写出 `./auth.json`。
3. 不把任何可能含敏感内容的文件类型都加入忽略。
4. 不改动真实登录、slot 删除、runtime 恢复等账号行为。

## Acceptance

1. 根目录 `auth.json` 默认被忽略。
2. issue 定义的常见本地凭证文件名默认被忽略。
3. issue 定义的常见私钥/证书扩展名默认被忽略。
4. focused regression 覆盖 `git check-ignore --no-index` contract。
5. `develop` 不再保留本次 stray sensitive file。
6. 规则保持足够窄，后续若需要证书/密钥夹具，仍可通过显式 unignore 恢复。

## Verification

- `bash docs/system/workspace/scripts/tests/test-sensitive-local-artifact-ignore-governance`
- `./bin/governance-check`
- `git status --short` in `develop` shows no stray `auth.json`

## Implementation References

- `.gitignore`
- `docs/system/workspace/scripts/tests/test-sensitive-local-artifact-ignore-governance`
- `docs/pre-brainstorms/20260329-2155--sensitive-local-artifact-ignore-governance/brainstorms.md`
- `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/tasks.md`

## Next

- `2026-03-30 17:34 PDT` the minimal ignore contract is already absorbed by `develop` commit `208c591`, with completion evidence recorded in `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/code-reviews/20260330-sensitive-local-artifact-ignore-verification.md`.
- Any broader sensitive-artifact family should open a new lifecycle instead of reopening this completed owner.
