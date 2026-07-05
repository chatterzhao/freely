# Pre-tests: sensitive-local-artifact-ignore-governance

## Acceptance Structure

### Pre-merge acceptance

- acceptance target: `sensitive local artifact ignore contract`
- testing layer: `focused regression`
- target environment: `feature worktree`
- required evidence: `git check-ignore --no-index` regression plus governance check
- blocker taxonomy:
  - `definition_missing`
  - `conflict_found`
  - `commands_only`
  - `execution_pending_or_failed`

1. 根目录 `auth.json` 与 issue 定义的敏感本地文件默认被忽略。
2. 常见私钥/证书扩展名被忽略，但正常 repo 路径不受影响。
3. 修复保持窄面，不扩成凭证存储重构。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `root auth.json and the issue-defined local sensitive artifact names are ignored by default`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-sensitive-local-artifact-ignore-governance`

### PT-2
- id: `PT-2`
- requirement: `common private-key and certificate extensions are ignored without hiding normal repository paths`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-sensitive-local-artifact-ignore-governance`

### PT-3
- id: `PT-3`
- requirement: `governance validation passes after the narrow ignore contract is applied`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/sensitive-local-artifact-ignore-governance/code-reviews/20260330-sensitive-local-artifact-ignore-verification.md`
