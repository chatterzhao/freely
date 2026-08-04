---
name: freely-url-content-intake
description: >-
  当输入是 URL 时，识别平台并调用自带脚本抓取正文，或返回结构化
  失败信息（含失败原因和可重试条件）。

  Use when: 用户提供 URL 需要抓取内容。
  触发词："抓取"、"fetch URL"、"读取链接"、"这个网址"。
---

# skill:freely-url-content-intake

## 何时使用

- 用户输入包含 HTTP(S) URL
- 用户请求“读取这个链接”“看这篇文章”“总结网页内容”
- 当前任务需要把 URL 转成可读内容，而不是把 URL 原样丢给模型

## 工作流

1. 先按 [platform-patterns.md](references/platform-patterns.md) 识别平台。
2. 再按 [capability-matrix.md](references/capability-matrix.md) 选择抓取方式。
3. 调用 [scripts/fetch-url.sh](scripts/fetch-url.sh)。
4. 若返回 HTML，继续调用 [scripts/extract-readable-content.sh](scripts/extract-readable-content.sh) 提取可读正文。
5. 脚本必须返回结构化状态，而不是只打印原始网页：
   - `fetch_status`
   - `content_kind`
   - `failure_reason`
   - `recommended_next_step`
6. 成功时把正文继续交给后续流程；失败时明确说明原因和下一步建议。

## 微信公众号策略

- `mp.weixin.qq.com/s/*` 默认使用浏览器 UA 与常见请求头。
- 这是 skill 自带的本地方案，不依赖工具私有 `WebFetch`。
- 若抓到验证页、受限页或空页面，必须报告失败，不得假装抓到了正文。

## 边界

- 本 skill 只负责“抓取或明确失败”。
- 若已抓到 HTML，本 skill 负责做最小正文抽取。
- 更复杂的正文净化、登录态网站支持、browser/MCP 扩展由后续 issue 继续。

## References

- [platform-patterns.md](references/platform-patterns.md)
- [capability-matrix.md](references/capability-matrix.md)
