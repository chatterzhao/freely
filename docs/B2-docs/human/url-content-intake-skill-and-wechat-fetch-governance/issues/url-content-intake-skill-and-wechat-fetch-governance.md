# I-20260318-1246 URL 内容摄取 skill 与微信公众号抓取治理

- issue_id: `I-20260318-1246`
- title: `URL 内容摄取 skill 与微信公众号抓取治理`
- phase_state: `completed`
- milestone: `M-20260318-url-content-intake-skill-and-wechat-fetch-governance`
- epic-name: `workspace-routing-foundation`
- story-name: `url-content-intake-skill-and-wechat-fetch-governance`
- issue-name: `url-content-intake-skill-and-wechat-fetch-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260318/candidates.md`
- source_brainstorm: `docs/B1-docs/raw-20260318/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/human/url-content-intake-skill-and-wechat-fetch-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-url-content-intake-skill-and-wechat-fetch-governance.md`
- verification_artifact_dir: `docs/B2-docs/human/url-content-intake-skill-and-wechat-fetch-governance/code-reviews`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`iflow` 能直接解读微信公众号链接的研究已经收口，但 Freely 还没有把这类 URL 输入沉淀成正式能力。当前缺口是把研究结论物化成完整、可分享的 skill 套件，而不是继续停留在预研文本。

## Scope

- 新增 `skill:url-content-intake`
- skill 目录自带脚本，至少覆盖：
  - 微信公众号文章 URL
  - 通用 HTTP(S) URL
- 明确输出：
  - `fetch_status`
  - `content_kind`
  - `failure_reason`
  - `recommended_next_step`
- 为 skill 脚本补最小测试

## Non-Goals

- 不做全部站点的正文净化
- 不做完整 browser/MCP 抓取矩阵
- 不在本 issue 中接入所有现有路由器

## Acceptance

- `docs/system/workspace/skills/url-content-intake/` 存在完整 skill 目录
- skill 自带脚本，不依赖仓库中零散的同名能力脚本
- 微信公众号 URL 默认使用浏览器 UA 抓取策略
- 至少一条测试证明脚本按平台模式选择正确的 curl 参数
- pre-brainstorm candidate 已绑定到正式 issue 和 milestone

## Completion

- `docs/B1-docs/raw-20260318/brainstorms.md`
- `docs/B1-docs/raw-20260318/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/human/url-content-intake-skill-and-wechat-fetch-governance/issues/url-content-intake-skill-and-wechat-fetch-governance.md`
- `docs/B2-docs/human/url-content-intake-skill-and-wechat-fetch-governance/pre-tests.md`
- `docs/B2-docs/human/url-content-intake-skill-and-wechat-fetch-governance/code-reviews/20260401-url-content-intake-skill-verification.md`
- `docs/progress/workspace-routing-foundation/p-url-content-intake-skill-and-wechat-fetch-governance.md`
- `docs/system/workspace/skills/url-content-intake/SKILL.md`
- `docs/system/workspace/skills/url-content-intake/references/capability-matrix.md`
- `docs/system/workspace/skills/url-content-intake/references/platform-patterns.md`
- `docs/system/workspace/skills/url-content-intake/scripts/fetch-url.sh`
- `docs/system/workspace/skills/url-content-intake/scripts/extract-readable-content.sh`
- `docs/system/workspace/scripts/tests/test-url-content-intake-skill`

## Verification

- `bash docs/system/workspace/scripts/tests/test-url-content-intake-skill`
- `./bin/governance-check`

## Next

- `2026-04-01` 该能力已经在 canonical `develop` 中存在并通过最小 skill regression；本轮仅补齐 lifecycle 真源，owner 关闭。
- 后续如果要把 URL intake 扩到更多站点、browser/MCP fallback 或统一路由接入，应新开 lifecycle，而不是重开这个 bounded skill materialization owner。
