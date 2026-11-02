# Super-agent 原文归档与研究索引

## 来源

- 标题：**Super-agent 设计探索：迈向更自主的 Agent 系统**
- 作者：DeepSeek 产品部
- 原文：https://mp.weixin.qq.com/s/zoS7GlReWPhfCjENGxXCdg
- 发布时间：2026-10-31 05:29:47 UTC（时间戳 1793449787）
- 抓取时间：2026-11-01
- 抓取方式：浏览器 UA / Accept / Referer 请求，落原始 HTML，正文与图片本地化

微信公众号直连会触发 captcha；本次用完整浏览器头拿到了正常文章 HTML（3.7 MB），并保留 `source.html` 作为最终事实源，避免二手转述。

## 文件

| 路径 | 内容 |
|---|---|
| `source.html` | 微信原文原始 HTML（sha256 见 metadata.json） |
| `article.md` | 正文 Markdown（含 15 张图引用） |
| `assets/fig-01..15` | 原文图片，按出现顺序编号 |
| `metadata.json` | 标题/作者/发布时间/抓取时间/每个文件的 sha256 |
| `article-notes.md` | 按章节逐节笔记（文章说了什么，不混入 Freely 判断） |
| `image-index.md` | 15 张图的图注与用途索引 |
| `intent-map.md` | 按“功能/意图”把文章模块映射到 Freely 的初版矩阵（后续细化） |
| `example-project.md` | `dsh-superagent-prototype` 示例项目分析（后续细化） |
| `decisions.md` | 吸收/改造/不吸收的 ADR（后续细化） |

## 文章结构

1. Super-agent：四个基础特征（连续、高效、主动、持久）与五个模块
2. 双层架构：Router 层 / Worker 层，连续性与吞吐量的权衡
3. 事件驱动：Trigger、Fast/Slow 过滤、Thread 订阅直通、Inline & Spill/链式召回、投机执行
4. 面向人的交互：异步 ReAct Loop 全双工、多信道输出
5. 计算、状态与执行环境分离：云端 Agent Loop + 持久状态 + 端侧 daemon
6. Watchdog：外部 Control Loop，基础设施 + 语义进展
7. 初步实验：双层/直通/单 Session+Subagent 消融；Router 批处理
8. 开放问题：双层扩展、脱离 Session 的产品形态、A2A、安全隐私
9. 结语与示例项目声明

## 使用规则

- 原文事实以 `source.html` / `article.md` 为准；图片为原文截图/示意图。
- `article.md` 是自动转换稿：保留了标题、段落、列表、引用和图片顺序；微信的复杂排版/表格样式可能被简化，引用原文时以 `source.html` 校对。
- `fig-15` 是招聘广告，不是架构内容；保留是因为它是原文最后一张图，分析时标注为“非技术图”。
- 示例项目是 **research prototype**，不是正式产品；文章明确说部分设计是未来方向、未在原型实现。分析时必须区分“文章主张 / 原型实现 / Freely 现状”。
