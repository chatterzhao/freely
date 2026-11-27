## 0. 设计意图审计
### 外部锚点
- R59 discover-raw：GitHub 4 matches，全部是 #4734/#4731/#4645 正文引用，标题无身份前缀。
- `raw_title_contract` 规定身份由 `[RAW-<key>]` / `[I-<key>-A]` 标题前缀承载。
- create 对 indeterminate fail-closed 是正确设计，不能放宽。
### 判定
**身份判据错误**：两个 handler 用 body 文本参与身份匹配，制造假歧义。
### 影响面
只改 adapter 的搜索判据与 AT；不改 create 策略、不改标题格式。
## 0.1 四问
Q1 身份解析；Q2 与 raw_title_contract 共享身份真源；Q3 不要求额外工位；Q4 AT 直接断言前缀边界。
## 1. 决策
新增纯函数 `is_identity_title()`；两平台搜索只按规范标题前缀判定副本；合法多副本仍 ambiguous。
