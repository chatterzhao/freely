---
local_id: I-20260329-2155-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260329-2155/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '69'
    url: https://github.com/chatterzhao/freely/issues/69
    synced_at: '2026-04-27T11:21:19Z'
  gitee:
    issue_id: IJFO77
    url: https://gitee.com/zhaoquan/freely/issues/IJFO77
    synced_at: '2026-04-27T13:15:17Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/sensitive-local-artifact-ignore-governance/issues/sensitive-local-artifact-ignore-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:19Z'
hash: ''
created_at: '2026-04-27T11:21:19Z'
updated_at: '2026-05-17T12:21:05Z'
platform_state: closed
---

`develop` 根目录现场出现过一个真实的 `auth.json`，而仓库没有任何规则会默认忽略它。这意味着 Freely 当前对本地敏感副产物的治理只覆盖 `.env*`，没有覆盖账号凭证、私钥、证书等常见高风险文件。

这条线的目标不是重做凭证存储，而是把“误落到仓库里的敏感本地文件不应进入 Git”冻结成一个最小、可测试的 contract。

canonical: docs/B2-docs/ibm/sensitive-local-artifact-ignore-governance/issues/sensitive-local-artifact-ignore-governance.md
