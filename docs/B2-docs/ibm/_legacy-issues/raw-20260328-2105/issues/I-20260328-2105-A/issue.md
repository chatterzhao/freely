---
local_id: I-20260328-2105-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260328-2105/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '67'
    url: https://github.com/chatterzhao/freely/issues/67
    synced_at: '2026-04-27T11:21:13Z'
  gitee:
    issue_id: IJFO75
    url: https://gitee.com/zhaoquan/freely/issues/IJFO75
    synced_at: '2026-04-27T13:15:14Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/codex-verified-resume-evidence-governance/raw-20260328-2105issues/codex-verified-resume-evidence-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:13Z'
hash: ''
created_at: '2026-04-27T11:21:13Z'
updated_at: '2026-05-17T12:20:59Z'
platform_state: closed
---

Freely 已经把 `codex` 的 canonical continuity model 收敛为显式 session-addressed resume，但 `2026-03-28` 的 dogfood 现场证明当前恢复证据判定仍然过弱：

- `fresh` 首轮失败后，runtime 从 cycle log 观察到一个 `session_id`
- 同一轮又已经确认 `jsonl_path=unavailable`
- supervisor 仍把该 id 持久化为下轮 `resume_target`
- 后续连续对同一个不可恢复 thread id 执行 `resume`
- 直到进入 `restart_storm_pause`

隔离工位里直接执行 `codex exec resume 019d374c-6743-7020-a420-14573edb41cd ...` 也稳定报：

- `thread/resume failed: no rollout found for thread id ...`

这说明当前缺口不是“resume 不可用”，而是 runtime 把弱观

canonical: docs/B2-docs/config/codex-verified-resume-evidence-governance/raw-20260328-2105issues/codex-verified-resume-evidence-governance.md
