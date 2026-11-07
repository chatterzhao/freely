---
schema_version: '1'
local_id: raw-20261105T122053Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261105T122053Z-A
platform_ids:
  github:
    issue_id: '4195'
    url: https://github.com/chatterzhao/freely/issues/4195
    synced_at: ''
  gitee:
    issue_id: IKT9DB
    url: https://gitee.com/zhaoquan/freely/issues/IKT9DB
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-05T12:20:53Z'
updated_at: '2026-11-07T07:58:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-07T08:05:00Z'
closeout_note: ''
---

# fix: 平台读通道失败时静默返回空清单，让 GitHub 57 条 open issue 凭空消失

workflow_kind: fix

## 根因

平台读通道把「读取失败」与「该平台确实没有 open issue」压成同一个返回值 `{}`，且聚合层不携带任何平台级健康标记。`gh issue list --json` 走 GraphQL，网关故障时报 `Bad Gateway`；`_open_issue_records_via_rest()` 的 REST 回退在同样故障时 `except Exception: return {}`，`list_open_issue_records()` 重试两次后也返回 `{}`。模块级聚合函数用 `_safe(...) or {}` 再吞一层，结果就是一个「正常的空字典」。

## 证据（2026-11-05 实测）

- 首次调用 `platform-adapter.list_open_issue_records()` 得到 50 条记录，全部是 `gitee:*`，`github:*` 为 0 条；同一时刻直接执行 `gh issue list --repo chatterzhao/freely --state open --limit 200 --json ...` 输出 `Post "https://api.github.com/graphql": Bad Gateway`。
- 立即按平台分别重试，GitHub 得到 57 条、Gitee 得到 50 条。也就是说那 50 条不是完整清单，而是「GitHub 整侧读取失败后的部分结果」。
- `platform-adapter.py:376-413` `_open_issue_records_via_rest()` 在 REST 也失败时静默 `return {}`；`:419-436` `GitHubHandler.list_open_issue_records()` 重试后 `return self._open_issue_records_via_rest()`；`:976-982` 聚合函数 `for issue_id, record in (_safe(h.list_open_issue_records) or {}).items()`，空字典不产生任何条目，也不产生错误标记。
- `task-lifecycle-scan.py:530-535` `get_platform_open_issues()` 只在**抛异常**时返回 `__degraded__`，但异常已在 adapter 内部被吞，所以这条降级分支实际不可达。
- `test-platform-open-parity.py:19-28` 把 `handler.list_open_issue_records() or {}` 直接当清单用；GitHub 侧为空时会算出 50 条 `gitee-only`，报出并不存在的差异。

## 影响

- 生命周期扫描会把 GitHub 上真实存在的 57 条 open issue 当作不存在，可能据此判断本地 raw 已失去平台副本、误推进或误清理。
- 双平台 parity 检查在网络抖动时产生假差异，掩盖真实差异。
- 「平台故障」与「平台无 issue」在结果里完全不可区分，运维无法判断是否需要重试，也没有可供自动重试依据的退出码。

## 修复方案

1. 读通道返回结构显式区分成功与失败：每个平台产出带 `ok` / `error` / `partial` 的状态，而不是裸 `{}`；GraphQL 与 REST 都失败时返回可识别的错误对象。
2. 模块级 `list_open_issue_records()` 对任一平台读取失败时，要么整体返回带降级标记的结果，要么抛出可读异常，禁止静默丢弃该平台；调用方据此决定是否重试。
3. `get_platform_open_issues()` 改为按结构中的失败标记生成 `__degraded__`，让 scan 能进入已有的降级语义；`test-platform-open-parity.py` 在降级时跳过而非报告假差异。
4. 保留现有 REST 回退能力，不删除；补一条针对「GraphQL 与 REST 同时失败」的测试，断言返回失败标记而不是空字典。

## 验收标准

- RED：mock GraphQL 与 REST 均失败，断言 `list_open_issue_records()` 含平台级失败标记；当前返回 `{}`。
- RED：mock 单平台失败，断言 scan 的 `get_platform_open_issues()` 产出 `__degraded__`；当前不会。
- GREEN：两平台均正常时返回 107 条（57 GitHub + 50 Gitee），结构不变、调用方无需改动。
- GREEN：单平台失败时 parity 检查不报假差异，并输出明确的重试提示。

## 边界

不改 `pull_raw_issue()` 的 FATAL 语义（那是另一条 issue 的范围）；不改写通道；不取消 REST 回退。
