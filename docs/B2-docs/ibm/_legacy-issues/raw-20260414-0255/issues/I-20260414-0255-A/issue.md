---
local_id: I-20260414-0255-A
kind: linked
phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260414-0255/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '149'
    url: https://github.com/chatterzhao/freely/issues/149
    synced_at: '2026-04-27T11:27:41Z'
  gitee:
    issue_id: IJFOA1
    url: https://gitee.com/zhaoquan/freely/issues/IJFOA1
    synced_at: '2026-04-27T13:17:22Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:27:41Z'
hash: ''
created_at: '2026-04-27T11:27:41Z'
updated_at: '2026-05-17T12:24:31Z'
platform_state: closed
---

真实 `freely start` 重放已经把这条 lane 的问题收敛到一个更窄、更准确的根因：

1. `codex` 运行期 after-failure same-tool recovery 仍复用了 cached-ready 选择器。
2. 该选择器会先看 availability cache，于是像 `worahe1012`、`a1018-1` 这样的 saved slot 可能在真正执行前就被跳过。
3. 一旦 inner loop 先跳号，现场就会伪装成 “failure type 判断错了” 或 “应该分 limit/network/auth 多种切法”，但那不是根因。
4. 正确合同只有一条：任何触发切号的失败都走统一切号方法；在同工具内部，先切到当前后的下一个 saved slot 并真正执行，直到 same-tool 耗尽后再交给跨工具外循环。

canonical: docs/B2-docs/ibm/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md
