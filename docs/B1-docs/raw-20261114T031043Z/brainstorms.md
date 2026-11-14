# B1 Brainstorm — raw-20261114T031043Z

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文）:
  - 设计文档: `ibm-framework.md`「sync 是本地→平台的唯一桥梁」「sync 触发是确定性的生命周期事件，不是 AI 判断」；`docs/LAWS.md`「一个工位只处理一个 raw issue」；`raw-20261103T091157Z`「跨 raw key 的文档回填必须单独 governance-only lane」。
  - 既有验收测试: `test-issue-sync-batch-closeout.py`（linked 收口判据与首次同步关闭）、`test-wt-close-children.py`。
  - 门禁源码注释/理由: `runtime/freely:24146`「running issue-sync batch before daemon scan」；`cmd-batch.sh` 的范围过滤注释「a raw-owning worktree may only sync its own issue and children (GATE 1)」。
  - 既有同类实现: `issue-sync-scope.py`（按 raw-key 过滤）；`merge_issue_sync.py`（按 raw-key 发现）。
  - 配置约束: 无。
- 判定（五分类）: **bug**（过滤用绝对路径，被工位名误匹配）+ **实现未完成**（daemon 自动 batch 不传范围，且没有只读/写入的分离）。
- 与既有断言的冲突: 无。过滤本意就是「只同步本 lane」，本轮只是让它真正生效。
- 影响面: `bin/issue-sync.d/cmd-batch.sh`、`docs/system/workspace/scripts/runtime/freely` 的 daemon 前置段、对应 AT。

### 0.1 全局适配反思（四问）

1. **类别**：这是**实现 bug + 范围策略未接线**，不是设计变更；副本传播的字段类判据属另一条 raw（`raw-20261114T051655Z`），本轮不碰。
2. **职责边界**：范围由 **lane 声明**（raw-key），`issue-sync` 只执行与拒绝；daemon 不拥有范围决策权，因而不应无参调用 batch。
3. **结构性冲突**：若把「全量同步」当成必须逐文档走 IBM 的流程，会变成反设计；本轮**不**走那条路——只修「lane 内误判为全量」这个错误。
4. **门禁失配**：GATE 1 判路径/身份，本轮变更不触碰判据模型；字段类判据由 `raw-20261114T051655Z` 统一处理。

## 1. 现象（已实测）

在 R33.18 与 R34.x 的 lane 工位里执行：

```bash
bin/issue-sync --project <wt> batch 20261114T033013Z
# [issue-sync] batch: 288 issue(s) to process ...
```

`--raw-key` 形同虚设：288 个文档（含大量其它 raw）被处理，产生平台 close/create 与 100+ 文档变更。

## 2. 根因

```bash
case "$issue_file" in *"$filter_key"*) ;; *) continue ;; esac
```

`$issue_file` 是**绝对路径**，而 lane 工位目录名形如
`.../freely-worktrees/fix-raw-<key>-<slug>/docs/...` —— **前缀本身就含 key**，
于是树内每一个文档都「匹配」，过滤完全失效。

（这也是 R33.18 那次「scoped batch 仍改其他 raw」的真实原因；当时在 `develop` 主仓里用 bogus key 探测返回 0，掩盖了问题——主仓路径不含 key。）

## 3. 方案

| 方案 | 做法 | 评价 |
|---|---|---|
| A | 只比较 `${issue_file#*/docs/}` 之后的相对路径 | 最小、语义准确：身份来自 doc 路径，与工位名无关 ✅ |
| B | 用 `promoted_from` / `local_id` 精确匹配 | 更严，但需要解析每个文件 frontmatter（当前循环已在后续读取，成本可接受）；可作为后续加固 |
| C | 让调用方传绝对路径白名单 | 与 `--raw-key` 语义重复 |

采用 A，并在输出里打印 `scope=<key|ALL>`，让「是否被限定」可观察。

### 3.1 daemon 侧

`runtime/freely` 在 daemon 扫描前执行无参 `issue-sync batch`：

- 在 lane 工位内 → 解析当前分支的 raw key 并传入；
- 在 develop/main/test-pre-merge → **不写**，只提示「全量同步需走治理车道」。

本轮先做「平台分支 → 跳过且提示」+「lane → 传 key」；`scan`/`apply` 三分与治理车道由 `raw-20261114T051655Z` 统一做，避免一次改太多。

## 4. 证伪

- 「过滤已生效」→ 否：实测 288 条被处理，第一条是 `raw-20260725T072209Z`。
- 「用绝对路径没问题」→ 否：工位名前缀含 key，恒真。
- 「daemon 传 key 会漏同步」→ 否：全量同步是治理车道的职责，不该由随机一次 `freely` 调用触发。

## 5. 边界

- 不改 GATE 1、不改字段类判据（后者是 `raw-20261114T051655Z`）；
- 不改 `batch` 的收口判据（`completed`）；
- 不手工关平台 issue；不新增「任意文档可改」的通道。
