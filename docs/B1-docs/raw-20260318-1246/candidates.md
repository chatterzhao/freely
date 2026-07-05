# Candidates

## C-20260318-1246-A: legacy issue

- candidate_id: `C-20260318-1246`
- status: `completed`
- milestone: `M-20260318-url-content-intake-skill-and-wechat-fetch-governance`
- promoted_issue_id: `I-20260318-1246`
- promoted_issue_path: `docs/B2-docs/human/url-content-intake-skill-and-wechat-fetch-governance/issues/url-content-intake-skill-and-wechat-fetch-governance.md`
- decision_reason: 这条研究已经完成 materialization，canonical skill、bundled scripts、focused regression 与 owner closeout 均已进入 `develop`；不再保留为活跃待消费 candidate。
- next_action: 保持收口态；若后续扩大到更多站点、browser/MCP fallback 或统一顶层路由，再新开 lifecycle。
- revisit_trigger: 当 URL intake 的 bounded skill materialization contract 被证明过窄、必须进入新的能力面时，再重新进入 pre-brainstorm 判断。

- problem: 当前“AI 直接解读链接”更像工具私有能力，Freely 尚未把它定义成可追溯、可失败、可替换的正式能力。
- change:
  - 新增 `url-content-intake` 能力层，识别普通网页、微信公众号文章、PDF/文档页等 URL
  - 根据工具能力矩阵选择抓取路径：平台 `WebFetch`、本地 HTTP 抓取、本地 browser/MCP 抓取
  - 规范输出：`fetch_status`、`content_kind`、`content_excerpt`、`failure_reason`、`recommended_next_step`
- acceptance_hint:
  - Freely 能明确区分“工具原生 WebFetch 能力”和“本地抓取能力”
  - 对公众号链接能显式区分正文页、验证页、受限页
  - 抓取失败时提供下一步建议，而不是把 URL 原样丢给模型
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260318-1246-A/issue.md
- milestone: M-20260318-1246-A
- session_refs:
  - feature/url-content-intake-skill-materialization-20260318
