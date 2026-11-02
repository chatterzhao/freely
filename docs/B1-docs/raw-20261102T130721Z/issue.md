---
schema_version: '1'
local_id: raw-20261102T130721Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261102T130721Z-A
platform_ids:
  github:
    issue_id: '4126'
    url: https://github.com/chatterzhao/freely/issues/4126
    synced_at: ''
  gitee:
    issue_id: IKSF6S
    url: https://gitee.com/zhaoquan/freely/issues/IKSF6S
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-02T13:07:21Z'
updated_at: '2026-11-02T13:16:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-02T13:11:27Z'
closeout_note: ''
---

# [RAW-20261102T130721Z] feat: 工作树种子清单（worktree seed）——声明式复制未跟踪的本地配置

workflow_kind: feature

## 背景

`git worktree add` 只检出被跟踪的文件。凡是 `.gitignore` 忽略、但运行必需的本地配置，都不会出现在新工位里。当前已经踩到的例子：

- `.freely/agent-table.toml`（role → slot 映射）：缺失时 daemon 报 `AGENT_AI_TOOL not set`，而错误位置离根因很远；
- 上一轮只能为它写一段硬编码 `cp`，属于“每缺一个补一次”的补丁式做法。

这不该是特例。任何项目都可能有同类文件：`.env`、本地凭证、证书、缓存、生成物、`vendor/`、`node_modules/.cache` 等。

## 目标

给 freely 一个通用能力：**声明式的工作树种子（worktree seed）**。

- 项目维护一份清单，列出“工位创建后需要复制/链接进来的路径”；
- `wt-create` 在建完工位（dev 与 test 两个）后统一执行；
- 清单缺失时回落到内置默认（`agent-table.toml`），保证现有行为不倒退；
- 换项目时只改清单，不改脚本。

## 清单位置与格式

`docs/system/workspace/worktree-seed.toml`（随仓库跟踪，可被 clone 带到任何机器）：

    version = 1

    [[seed]]
    path = ".freely/agent-table.toml"
    mode = "copy"
    required = true

    [[seed]]
    path = ".env"
    mode = "copy"
    required = false

- `path`：相对项目根；禁止绝对路径与 `..`；
- `mode`：`copy`（默认，隔离、可改）或 `link`（软链接，跟随源文件变化）；
- `required`：源不存在时是失败还是告警（默认 `false`）。

## 行为约定

1. **幂等**：目标已存在则跳过，不覆盖工位内的本地修改。
2. **不越界**：源路径必须落在项目根内；解析后仍越界即拒绝。
3. **幂等可重放**：重复执行不产生副作用；`wt-create` 中途失败重试安全。
4. **可观测**：每次执行打印/返回 `copied / skipped / missing` 三类清单；`required` 的缺失让工位创建失败并指出具体路径。
5. **失败不留半成品**：`wt-create` 已有回滚逻辑，seed 失败走同一路径。

## 非目标

- 不做双向同步（工位改了不回写主树）；
- 不复制 `.git`、不复制 `.freely/freely.db`（该文件由既有 clone 逻辑处理，语义不同）；
- 不引入模板渲染（不做变量替换）。

## 验收

1. 清单存在时，按清单复制/链接；dev 与 test 两个工位都生效。
2. 清单不存在时，回落内置默认（`agent-table.toml`），行为与现在一致。
3. 目标已存在 → skipped，不覆盖。
4. 源缺失且 `required=true` → 工位创建失败，错误信息含路径；`required=false` → 告警继续。
5. 绝对路径 / `..` 越界 → 拒绝并报错。
6. `link` 模式生成软链接，源文件改动后工位内可见。
7. 既有 `wt-create` / worktree 相关测试全绿。
