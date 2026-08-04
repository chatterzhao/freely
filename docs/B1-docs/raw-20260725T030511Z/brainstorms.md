---
b1_id: B1-20260725T030511Z
phase_state: completed
source_raw: raw-20260725T030511Z
source_url: https://github.com/chatterzhao/freely/issues/4074
produced_candidate: C-20260725T030511Z-A
created_at: 2026-07-25T03:05:37Z
---

# B1_IBM: 配置平台 raw 副本一致性

## Input

- 来源：`raw-20260725T030511Z`。
- 现象：平台 adapter 的 raw-key 比较大小写不对称；空匹配被作为可拉取记录，导致 `wt-create` 在临时工位创建后才失败。
- 影响：平台发现、raw 物化、PR 生命周期与关闭路径各自持有不完整且不一致的多平台判断。

## Discovery

- 已验证最小自举修补可使 owner 工位成功创建，且根目录临时改动已恢复。
- `platform-adapter.py` 是平台注册和 transport 的唯一合理边界，但 `pull_raw_issue()`、scan 和 lifecycle shell 脚本各自重建 raw 识别或副本判断。
- 现有 `list_open_issues()` 以无平台命名空间的 issue ID 扁平返回，不能作为多平台一致性判断输入。

## Brainstorm

### 方案 A：在每个 lifecycle shell 脚本补平台检查

优点是局部改动少；缺点是规则继续分散，`wt-create`、PR、close 会出现不同的 fail-open/fail-closed 语义。拒绝。

### 方案 B：把所有逻辑继续塞入 adapter

优点是调用方少；缺点是 transport、projection、比较、receipt 与 CLI 混在已超 1000 行的历史脚本中，复杂度继续扩散。拒绝。

### 方案 C：adapter 保持 transport，新增纯 reconciliation 模块

adapter 只负责按配置读取平台副本；纯模块负责 canonical projection、差异分类和只读 receipt；lifecycle 命令统一消费 gate。resolution 作为显式、有审计痕迹的独立路径。采用。

## Decision

采用方案 C，并拆为同一 owner issue 下的可验证切片：

1. 修正 adapter raw discovery 的规范化和空结果契约，返回带平台命名空间的完整副本记录。
2. 提供纯 reconciliation receipt：配置为空、平台不可达、分页不完整、缺副本、重复副本与内容差异一律明确为 `unknown`、`degraded` 或 `blocked`，不解释为空清单。
3. 在 `wt-create`、PR create/review/merge、`wt-close` 之前统一调用只读 gate；gate 不写本地或远端。
4. resolution 使用明确的 create、版本保护 edit 和幂等评论；重新读取一致后才持久化基线。

## Candidate

- candidate_id: `C-20260725T030511Z-A`
- status: promoted
- milestone: `M-20260725T030511Z-A`
- next_action: B2 物化配置平台 raw reconciliation 的设计与可执行测试计划。
