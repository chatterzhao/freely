---
local_id: I-20260405-0027-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '103'
    url: https://github.com/chatterzhao/freely/issues/103
    synced_at: '2026-04-27T11:23:58Z'
  gitee:
    issue_id: IJFO8H
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8H
    synced_at: '2026-04-27T13:16:16Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:23:58Z'
hash: ''
created_at: '2026-04-27T11:23:58Z'
updated_at: '2026-06-21T15:21:47Z'
platform_state: closed
---

Freely 已经把 slot inventory、slot-first recovery、OAuth inventory sweep、launch-time confirmation 和 bounded network taxonomy 分别冻结为 canonical contract，但 Codex live auth truth 仍停留在 `~/.codex/auth.json` copy-in/copy-out。这个模型无法覆盖已经真实存在的 API-key/provider 模式，因为可用性与切换正确性同时依赖：

- `~/.codex/auth.json`
- `~/.codex/config.toml`
- provider-scoped `base_url` / `env_key` / auth-mode truth

如果不把 `apikey` 提升为一等 slot，Freely 就会在 dogfood 环境里继续误判：

- `save` 只能保存残缺 truth
- `switch` 会把旧 provider residue 留在 live config
- w

canonical: docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md
