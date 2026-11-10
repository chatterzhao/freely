# Implementation Decision Note
- issue_id: I-20261110T130144Z-A
- issue_path: docs/B2-docs/platform/issue-sync-modules/raw-20261110T130144Z/issues/I-20261110T130144Z-A.md
- decision: `bin/issue-sync` 拆为 dispatcher + `bin/issue-sync.d/*.sh`；`sync/issue_create_contract.py` 成为平台 body/标签的单所有者；`bootstrap --delete` 改走 adapter
- why_this: 1330 行单文件让子命令无法独立 source/断言；两条 create 路径各自渲染 body 与标签（一处硬编码字面量、一处 `awk` 假剥离）；`bootstrap` 直连删是 adapter 之外唯一平台写。
- alternatives_considered: ①只拆文件不动 body——缺陷原样留着；②把 frontmatter 从平台 body 移除——会让 `pull_raw_issue()` 对所有新 raw 走 legacy 分支，丢 intake_id/workflow_kind/severity；③让 `feedback` 先写本地 issue.md 再复用 `issue-sync create`——改动了 raw 所有权（平台是源、本地由 pull 物化）；④`feedback edit` 一并纳入契约——标题可能为空，语义需另行决定。
- boundary_non_goals: 未改 `issue-write-one` 契约与 0/3/1 退出码、未改 promote/close 语义、未动 `raw_title_contract` 标题投影、未动 `feedback edit` 的拼装、未动 DEPRECATED 的 `bin/issue-sync-batch.py`。
- residual_risk: ①平台 body 形态变化（围栏 frontmatter + 表格 + 去 comment 段），旧 issue 在下次 update 时会被重写为新形态；②模块间仍是函数级 + 全局变量耦合，未参数化；③6 个夹具新增 `issue-sync.d` 依赖，未来再加模块必须继续同步夹具；④`test-issue-sync-replica-guard.py` 4 项既有失败未修（基线相同）。

## 三个决定的真实依据

### 1. 平台 body 保留 frontmatter 围栏（而不是趁机删掉）

`sync/platform-adapter.py:1486-1506` 的 `pull_raw_issue()` 用
`body.startswith("---")` 判断是否有 frontmatter：有且 `schema_version == '1'`
才走 `raw_metadata_contract.validate()` 的严格分支，否则走 legacy 分支，
`intake_id` / `workflow_kind` / `severity` 都不进本地文档。
所以「统一 body」的方向必须是**规范化**围栏，不是删除它。

副作用（有意接受）：`issue-sync create/update` 发给平台的 body 从「裸 YAML 键 +
`## 标题`」变成「围栏 frontmatter + `workflow_kind` + 表格 + 人类正文」。
旧形态以 `## 标题` 开头，`startswith("---")` 为假，一直走 legacy materialize，
所以这次变化反而让 issue-sync 建的 raw 与 `feedback` 建的 raw 物化路径一致。

### 2. `### comment-` 通道整体移出正文（行为变更）

旧 `_issue_body()` 的 `grep -v '^## Comments'` 只删标题、保留块正文，于是评论
会既作为平台 comment 同步、又嵌在 body 里出现一次。契约改为：`## Comments`
段落与每个 `### comment-<ts>` 块都不进 body 投影。评论仍由 `cmd_comment`
以真实平台评论推送，信息不丢。

### 3. 拆分的切法：按子命令，而不是按层

- 主文件只留 `main()` + 路径解析 + 模块加载 + 受保护分支守卫（161 行，基线 1330）；
- 共享逻辑按职责分 5 个 `lib-*`（frontmatter / state / replica / content / platform）；
- 9 个子命令各一个 `cmd-*.sh`，函数名与原来一致，`main()` 分派表不变。

不做的事：不改 `issue-write-one` 契约、不改 0/3/1 退出码、不改 promote/close
语义、不动 `raw_title_contract` 的标题投影。

## 明确的边界（本轮未做，留档）

- **`feedback edit` 仍用原来的 body 拼装**（`---` + 原 frontmatter +
  `workflow_kind` + 新正文），没有走契约。原因：`edit` 只替换人类正文、标题
  可能为空（adapter 收到空标题表示「不改标题」），而契约的 `## <title>` 需要
  一个标题；把 `edit` 纳进来要先决定「空标题时用平台现有标题还是本地标题」。
  这与本轮 create 契约无关，登记为后续。
- **模块之间仍是函数级耦合**（`cmd_*` 直接调 `lib-*` 的函数与全局变量），没有
  参数化接口。原因是 `set -euo pipefail` + 全局 `ROOT_DIR`/`ISSUES_DIR` 是既有
  约定，改成显式传参会同时动 20 多个函数；本轮目标是「可独立 source/断言」，
  已达成（AT 断言 11 个入口可调用）。
- **`bin/issue-sync-batch.py` 仍在**（DEPRECATED 头注释，`bootstrap` 仍调它）。
  它不在本 issue 的三项范围内。

## 测试面：顺手修绿的既有失败

`test-platform-write-channel` 在 develop 基线是 3 failed —— R26 把写收口到
adapter 后，该夹具没同步 `platform-adapter.py` / 契约 / `freely_user_env`，
于是 `_gh_write` 直接 `can't open file`。补夹具（含 gitee stub 的 `list` 返回
`[]`，因为 replica guard 现在会先问平台）后 `22 ok / 0 failed`。

`test-issue-sync-replica-guard.py` 的 4 项失败在基线同样失败，失败集合逐条相同
（仅时间戳不同），本轮未修：属 receipt/close-multi 路径的既有问题。

## 复用的坑

1. 模块文件头必须逐行 `#`：多行 docstring 只给首行加注释时，第二行会被 bash
   当命令执行，导致 source 阶段 `command not found`，AT 全红。
2. 夹具复制 `bin/issue-sync` 必须同时复制 `bin/issue-sync.d/`（fail-closed 会
   明确报缺失文件名）。
3. 静态断言读「完整程序」（主文件 + 模块拼接）才不会因拆分而误报。
4. adapter 需要 `scripts/runtime/freely_user_env.py`；夹具缺它会把导入失败
   误报成产品缺陷。
