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

---

## 20260318-1258 实验验证结果（新增）

### 实验

使用 curl 模拟浏览器请求头访问同一公众号链接：

```bash
curl -sL \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
  "https://mp.weixin.qq.com/s/MB5gKaZMv5RyXFRuubxdrg"
```

### 结果

**成功获取正文内容！**

关键发现：
1. 微信公众号的反爬机制主要检测 User-Agent
2. 模拟浏览器 UA 后，文章内容在 `id="js_content"` 的 div 中
3. 可用 sed/grep 提取纯文本

### 提取正文的方法

```bash
# 保存 HTML
curl -sL -A "Mozilla/5.0..." "$URL" > /tmp/wx_article.html

# 提取纯文本
grep -A 500 'id="js_content"' /tmp/wx_article.html | \
  sed 's/<[^>]*>//g' | \
  sed 's/&nbsp;/ /g' | \
  sed 's/&amp;/\&/g' | \
  tr -s ' \n'
```

### 修正判断

之前认为"本机直抓会返回验证页"，实际上是**请求头问题**：
- 默认 curl UA 会被微信拦截 → 返回验证页
- 模拟浏览器 UA → 成功返回正文

### 对 Freely 的更新建议

`wechat-article-intake` 可以实现为本地方案：

```bash
# wechat-fetch.sh
fetch_wechat_article() {
  local url="$1"
  curl -sL \
    -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
    -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
    "$url"
}
```

### 局限性

- 此方法可能在以下情况失效：
  - 文章需要登录才能查看
  - IP 被微信风控
  - 文章已被删除
  - 微信更新反爬策略
- 应保留"可失败且可回退"设计

### 结论

**微信公众号文章可以通过本地 curl + 浏览器 UA 成功抓取**，不必完全依赖平台侧 WebFetch 服务。这为 Freely 提供了一个更可控的本地方案。

---

## 20260318-1305 URL 内容摄取能力路由设计（新增）

### 问题

当用户贴一个 URL（如公众号链接），Freely 如何知道该用什么方法处理？

### 设计方案：`skill:url-content-intake`

#### 1. 输入识别层

```
用户输入 → URL 模式匹配 → 平台识别
```

| URL 模式 | 平台 | 抓取策略 |
|----------|------|----------|
| `mp.weixin.qq.com/s/*` | 微信公众号 | curl + 浏览器 UA |
| `mp.weixin.qq.com/*` | 微信其他页面 | curl + 浏览器 UA（可能需登录） |
| `*.medium.com/*` | Medium | curl / web_fetch |
| `*.substack.com/*` | Substack | curl / web_fetch |
| `github.com/*` | GitHub | curl / gh CLI |
| 其他 HTTP(S) URL | 通用网页 | curl / web_fetch |

#### 2. 能力矩阵（Capability Matrix）

```
┌─────────────────┬────────────────┬────────────────┬────────────────┐
│ 平台            │ 本地 curl      │ web_fetch 工具 │ 需要登录       │
├─────────────────┼────────────────┼────────────────┼────────────────┤
│ 微信公众号      │ ✅ + UA        │ ✅             │ 部分           │
│ Medium          │ ✅             │ ✅             │ 否             │
│ Substack        │ ✅             │ ✅             │ 部分           │
│ GitHub          │ ✅ + gh CLI    │ ✅             │ 私有仓库需认证 │
│ 通用网页        │ ✅             │ ✅             │ 视情况         │
└─────────────────┴────────────────┴────────────────┴────────────────┘
```

#### 3. 路由决策树

```
输入 URL
    │
    ├─► 匹配平台模式？
    │       │
    │       ├─ 是 ─► 选择对应策略
    │       │
    │       └─ 否 ─► 尝试通用 curl
    │
    ├─► 本地抓取成功？
    │       │
    │       ├─ 是 ─► 提取正文 ─► 返回内容
    │       │
    │       └─ 否 ─► 降级策略
    │               │
    │               ├─► web_fetch 可用？ ─► 使用 web_fetch
    │               │
    │               └─► 不可用 ─► 提示用户：需手动复制或提供其他方式
    │
    └─► 需要登录？
            │
            └─► 提示用户：此页面需要登录，请手动复制内容
```

#### 4. Skill 结构设计

```
docs/system/workspace/skills/url-content-intake/
├── SKILL.md                    # 主技能定义
├── references/
│   ├── platform-patterns.md    # 平台 URL 模式匹配规则
│   ├── capability-matrix.md    # 能力矩阵定义
│   └── fallback-strategies.md  # 降级策略
└── scripts/
    ├── wechat-fetch.sh         # 微信公众号抓取脚本
    ├── generic-fetch.sh        # 通用网页抓取脚本
    └── content-extract.sh      # 正文提取工具
```

#### 5. SKILL.md 核心定义

```yaml
---
name: url-content-intake
description: 当用户输入 URL 时，识别平台类型并选择正确的抓取策略，将网页内容转换为可读文本供后续处理。
---

触发条件:
  - 用户输入包含 HTTP(S) URL
  - 用户请求"读取这个链接"、"看看这篇文章"等

输入:
  - url: 用户提供的 URL
  - context: 用户希望如何处理内容（摘要、分析、引用等）

输出:
  - content: 提取的正文内容
  - metadata: 标题、作者、发布时间等（如可获取）
  - source: 实际使用的抓取方法
  - fallback_used: 是否使用了降级策略
```

#### 6. 与 context-source-skill 的集成

`url-content-intake` 不是顶层路由 skill，而是被 `context-source-skill` 或 `doc-pre-brainstorm-execution` 调用的**能力 skill**：

```
用户输入 URL
    │
    └─► context-source-skill
            │
            ├─► source_class = discovery
            │
            └─► route_kind = pre_brainstorm
                    │
                    └─► doc-pre-brainstorm-execution
                            │
                            └─► 调用 url-content-intake 获取内容
                                    │
                                    └─► 基于内容继续 brainstorm
```

#### 7. 关键设计原则

1. **显式优于隐式**：不要假设 AI 工具能"自动理解 URL"，而是显式调用抓取能力
2. **可失败且可回退**：每种策略都有明确的失败检测和降级路径
3. **平台感知**：不同平台有不同的反爬机制，需要针对性处理
4. **渐进增强**：先尝试本地方案，再尝试平台能力，最后提示用户

#### 8. 实现优先级

1. **P0**：微信公众号抓取（已有验证方案）
2. **P1**：通用网页抓取 + 正文提取
3. **P2**：其他平台适配（Medium、Substack 等）
4. **P3**：需要登录的页面处理

### 下一步

1. 在 `docs/system/workspace/skills/` 创建 `url-content-intake/` 目录
2. 实现 `wechat-fetch.sh` 脚本
3. 定义平台模式匹配规则
4. 与现有 skill 路由集成
