# I-20260318-1908 URL 内容摄取 skill 与微信公众号抓取治理

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

## Status

- phase: `in_dev`
- owner: `feature/url-content-intake-skill-materialization-20260318`
