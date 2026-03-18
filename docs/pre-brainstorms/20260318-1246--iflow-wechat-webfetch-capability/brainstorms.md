# 20260318-1246 iflow / 微信公众号链接直读能力研究

## 背景

用户观察到 iflow 能直接解读微信公众号文章链接，这种能力可能适合作为 Freely 的通用 URL 内容摄取能力，而不应只依赖单一工具的隐式平台能力。

## 外部证据

1. iFlow 官方快速开始明确说明，使用 `Login with iFlow` 或心流 API Key 登录时，提供 `WebSearch` 和 `WebFetch` 服务；而 `OpenAI Compatible API` 模式明确不支持这两项能力。
   - 来源: https://vibex.iflow.cn/t/topic/42
2. 对用户提供的公众号链接 `https://mp.weixin.qq.com/s/MB5gKaZMv5RyXFRuubxdrg` 做本机直抓时，返回的是微信验证页，不是正文：
   - 页面标题为空
   - 页面正文包含 `环境异常`、`当前环境异常，完成验证后即可继续访问。`
3. 因此，iflow 若能“直接解读”这类链接，更合理的解释不是模型天然理解 URL，而是其平台侧 `WebFetch` 或等效网页抓取服务替用户完成了网页获取、反爬绕过或内容净化。

## 判断

### 已知

- 微信公众号文章链接本质上仍是网页 URL。
- 这类网页可能被普通 `curl`/HTTP 请求抓到，也可能返回验证码、环境异常页、客户端限制页。
- iflow 官方已公开宣称具备 `WebFetch` 服务。

### 推断

- iflow 的“直接解读链接”能力，本质上更像受托管的 URL 抓取能力，而不是 CLI 本地天然自带。
- 这个能力对 Freely 有价值，但应被定义为显式能力：
  - 输入: URL
  - 输出: 可读正文 / 抓取失败原因 / 下一步建议
  - 路由: 先抓取，再净化，再交给 AI

## 对 Freely 的启发

Freely 不应把“给 AI 一个 URL 看它会不会自己读”当作可靠工作流，而应考虑沉淀成正式能力：

1. `url-content-intake`
   - 统一处理网页、公众号、博客、公告页等 URL 输入。
2. `wechat-article-intake`
   - 明确区分：
     - 抓到正文
     - 抓到验证页
     - 抓到受限页
3. `tool-capability-aware routing`
   - 若当前工具具备平台侧 `WebFetch`，优先使用。
   - 若当前工具无此能力，则退回：
     - 本地抓取
     - 阅读模式净化
     - 明确失败并提示用户

## 风险

- 公众号链接存在反爬、验证码、地区/IP/UA 限制，不应假设始终可抓。
- 若 Freely 将该能力做成核心路径，必须允许“可失败且可回退”。
- 不应把 iflow 的平台私有能力误认为通用 CLI 标准能力。

## 建议

下一步应先物化一个候选：

- 研究 Freely 是否应新增 `url-content-intake` skill
- 明确 capability matrix：
  - iflow: 平台 `WebFetch`
  - codex: 依赖本地 fetch / browser / 用户给定内容
  - 其他工具: 逐个标注
- 再决定是否需要为微信公众号文章单独加子策略
