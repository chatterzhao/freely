# URL 平台模式

| Pattern | Platform | Strategy |
|---|---|---|
| `https://mp.weixin.qq.com/s/*` | 微信公众号文章 | 浏览器 UA 抓取 |
| `https://mp.weixin.qq.com/*` | 微信页面 | 浏览器 UA 抓取 |
| `https://github.com/*` | GitHub | 通用抓取或专用 CLI |
| `http://*` / `https://*` | 通用网页 | 通用抓取 |

规则：

- 优先匹配最具体的平台模式。
- 若没有特殊平台规则，则退回通用网页策略。
