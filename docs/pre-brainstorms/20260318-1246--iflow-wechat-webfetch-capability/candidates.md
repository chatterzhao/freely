# Candidates

## C-20260318-1246：把 URL 内容摄取能力显式化为 Freely skill

- problem: 当前“AI 直接解读链接”更像工具私有能力，Freely 尚未把它定义成可追溯、可失败、可替换的正式能力。
- change:
  - 新增 `url-content-intake` 能力层，识别普通网页、微信公众号文章、PDF/文档页等 URL
  - 根据工具能力矩阵选择抓取路径：平台 `WebFetch`、本地 HTTP 抓取、本地 browser/MCP 抓取
  - 规范输出：`fetch_status`、`content_kind`、`content_excerpt`、`failure_reason`、`recommended_next_step`
- acceptance_hint:
  - Freely 能明确区分“工具原生 WebFetch 能力”和“本地抓取能力”
  - 对公众号链接能显式区分正文页、验证页、受限页
  - 抓取失败时提供下一步建议，而不是把 URL 原样丢给模型
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
