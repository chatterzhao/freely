# Brainstorms: raw-20261108T134853Z

## 问题

`freely feedback create`（以及任何走 `platform-adapter create-issue` 且带 labels 的路径）在**没有预置 severity 标签**的 GitHub 仓库上必然失败。

## 证据（2026-11-08 13:47Z 真机，R16 收口后）

- 执行 `./bin/freely feedback create --kind fix --severity P2 ...` 返回：`"github": {"status":"error","error":"could not add label: 'severity/P2' not found"}`、`"gitee": {"status":"created","issue_id":"IKTSRS"}`、`[feedback] PARTIAL: 1 platform(s) created, 1 failed.`
- `gh label list` 当时只有 `kind/raw`、`kind/linked`、`phase/*`，没有 `severity/*`。
- 结果 `raw-20261108T134701Z` 只有 Gitee 副本，GitHub 无单；补建需要在工位内走 `issue-sync create`。
- R15（#4187）的 AT-001 用 stub 只断言 create-issue 的 argv 里有 `severity/Pn`，**没有真机验证标签是否已存在**；该风险已写在 R15 的 IDN 残余风险①，但未闭环。
- R16 收口时为了按约定用 feedback 立项，先用 `gh label create` 一次性补了 `severity/P0|P1|P2`（只建标签，未关闭任何 issue、未手工清理工位/分支），feedback 随即恢复正常（#4230 / IKTSSM 双平台 created）—— 但这是人工止血，换台机器必然复发。

## 证伪（现有 open issue 未覆盖）

- #4187（R15，已关闭）：实现 severity 数据链，验收只到 argv；IDN 把标签前置列为残余风险。
- #4194（R16，已关闭）：安装态版本同步，与平台标签无关。
- #4183 / #4216 / #4221：分别是 B2 文档解析、test-gate 记录命令、wt-close 评论判定。
- open issue 标题过滤 `install|dev-path|zshrc|label|severity` 无匹配（除本条）。

## 关键设计

1. **只在失败后补救**：`GitHubHandler.create_issue` 首次失败且错误同时含 `not found` 与 `label` 时，才调用 `ensure_github_labels(labels)` 并**重试一次**。标签齐备的健康路径零额外 API 调用（幂等快路径）。
2. **不掩盖其他错误**：auth / permission / network 失败不重试、不建标签，原样返回 error。
3. **有限重试**：重试后仍失败就返回 error，绝不无限循环。
4. **每个标签只建一次**：`_label_names()` 去重分割；已存在标签的 `gh label create` 报错被忽略。
5. **Gitee 不动**：Gitee 的 `--labels` 在真机上自动容错（IKTSRS 创建成功），不需要相同处理。

## 被否决的替代方案

- 建单时不传 label、建完用 `gh issue edit --add-label` 补：仍需要标签存在，且失败后留下无标签半成品单。
- 每次建单前都 `gh label create`（无条件）：健康路径多 N 次 API 调用，纯浪费。
- 只在文档里要求人工预建标签：换台机器复发，不是机制保证。
- 让 `feedback` 自己 catch 错误并去掉 label 重试：会把「优先级丢失」重新引入，违反 R15 的验收。
