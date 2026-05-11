# 能力矩阵

| Platform | Local curl | Browser UA | Private WebFetch | Default recommendation |
|---|---|---|---|---|
| 微信公众号文章 | yes | required | optional | 本地浏览器 UA 抓取 |
| 通用网页 | yes | optional | optional | 通用抓取 |
| 登录态页面 | maybe | maybe | maybe | 明确失败并提示用户 |

原则：

- 优先使用可分享、可复用的本地方案。
- 不把单一工具的私有抓取能力视为唯一依赖。
