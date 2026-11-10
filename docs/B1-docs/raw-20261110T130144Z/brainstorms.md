---
raw_id: raw-20261110T130144Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 前置评审（#4286 正文写于 2026-11-10 13:01Z，行号按当时真源）

| 验收项 | 真源核对 | 结论 |
|---|---|---|
| `bin/issue-sync` 拆子命令模块、主文件行数 -50% | 实测 `wc -l` = 1330 行；`main()` 在 1263-1326，其余全是函数定义 | **本轮修复**：主文件降到 161 行，14 个模块在 `bin/issue-sync.d/` |
| `feedback` 与 `issue-sync create` 共用 body 剥离函数与标签常量 | `runtime/freely:25602` 硬编码 `kind/raw,phase/proposed,severity/${severity}`；`_labels()` 在 shell 里自己拼；`_issue_body()` 的 `awk` 只删 `---` 行、**不删 frontmatter 键**，把 YAML 当正文发出去 | **本轮修复**：`sync/issue_create_contract.py` 单所有者 |
| 两条路径 body/标签逐字一致 | 现状不一致：`feedback` 发 `---` 围栏 frontmatter，`issue-sync` 发裸 YAML 键 | **本轮修复**：统一渲染，AT 断言两条路径输出相同 |
| `bootstrap --delete` 迁 adapter 或登记例外 | `bin/issue-sync-bootstrap:24` 直接 `gh issue delete "$2" --yes`，是 adapter 之外唯一平台写 | **本轮修复**：adapter 增 `delete_issue` + `issue-write-one ... delete`，bootstrap 改调 |
| 部分成功 0/3/1 退出码 | R26 已核对：adapter `create-issue` 与 `issue-sync close` 已实现 | **已实现**，本轮不重复 |

## 关键约束（决定方案形状）

**平台 issue 是 raw 的耐久副本。** `platform-adapter.pull_raw_issue()`
（:1486-1506）会从平台 body 里解析 frontmatter，`schema_version == '1'` 才走严格
分支并 `validate()`；没有围栏就走 legacy 分支，`intake_id`/`workflow_kind`/`severity`
全部丢失。因此「body 剥离」不能理解成「把 frontmatter 从平台 body 里删掉」，
而是**把 frontmatter 规范成一份带围栏的块，再把人类正文单独渲染**。
旧 `_issue_body()` 的 `awk` 恰好相反：删掉围栏、留下键值，于是平台 body
以 `## 标题` 开头（`startswith("---")` 为假）→ 所有 issue-sync 创建的 raw
其实一直走 legacy materialize 分支，YAML 只是噪音。

## 方案方向

### 方向 A：契约模块 + 每子命令一个模块（选中）

- `sync/issue_create_contract.py` 拥有 `strip_frontmatter()` / `split_workflow_kind()` /
  `drop_comment_channel()` / `platform_body()` / `labels_for()`，CLI 两种入口
  （`body --file`、`labels --file|--kind`）供 shell 调用；
- `bin/issue-sync` 只剩路径解析、模块加载、分支守卫、`main()` 分派；
- `bin/issue-sync.d/` 下 `lib-*.sh`（共享）+ `cmd-*.sh`（每子命令一个）。

### 方向 B：只拆文件、不动 body（否决）

能过「行数 -50%」但两条 create 路径继续各自渲染，缺陷原样留着；下一轮还是同一处。

### 方向 C：把 frontmatter 从平台 body 移除（否决）

会让 `pull_raw_issue()` 对所有新 raw 走 legacy 分支，静默丢掉 `intake_id` /
`workflow_kind` / `severity` —— 用「更干净的外观」换「元数据丢失」，不可接受。

### 方向 D：`feedback` 写本地 issue.md 再复用 `issue-sync create`（否决）

会改动 raw 创建的所有权（现在平台是源、本地由 `raw-issue-pull` 物化），
超出本 issue；契约模块已能达到同一目的且不碰所有权。

## 被否决

- 用 `source bin/issue-sync.d/cmd-create.sh` 单文件加载（缺依赖函数，必须带
  `lib-*`；AT 改为断言「source 主文件后 9 个 `cmd_*` 全部可用」）；
- 让 `feedback edit` 也走契约（`edit` 的语义是替换人类正文，标题可能为空；
  留作后续，见 implementation-decision-note 的边界声明）。

## fidelity 基线

- RED：`bin/issue-sync` 1330 行、无 `issue-sync.d`、无契约模块、`feedback`
  硬编码标签、bootstrap 直连 `gh issue delete` → `6 ok / 29 failed`。
- GREEN：主文件 161 行、9 个 `cmd-*` 模块 + 5 个 `lib-*`、两条路径 body/标签
  逐字相同、bootstrap 走 adapter → `35 ok / 0 failed`。
- 已知既有失败（develop 基线同样失败，非本轮引入）：`test-issue-sync-replica-guard.py`
  4 项（receipt/close-multi 路径，失败集合与基线逐条相同）；local `test-all` 的
  `test-github-label-autocreate.py`。
- 顺手修绿：`test-platform-write-channel` 在 develop 基线 3 failed（R26 把写收口到
  adapter 后夹具没同步 adapter/契约），本轮补夹具后 `22 ok / 0 failed`。
