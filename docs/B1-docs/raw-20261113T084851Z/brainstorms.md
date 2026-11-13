# B1 Brainstorm — raw-20261113T084851Z

## 0. 用户强约束（本轮立项来源）

- 「实现必须符合整体项目的意图。不要冲突，不要矛盾，不要能力降级。」
- 「出现门禁问题，千万不要第一时间想着绕过。如果门禁要修改，也是要找到整个项目当时为什么要这样设计门禁……千万不能改错门禁。」

本轮不修改任何门禁，只修**数据链路的实现不达标**。

## 1. 设计意图（已核实项目自身源码）

1. `docs/system/workspace/scripts/lifecycle/raw_reconciliation.py` 的 `canonical_projection` 把 `title / body / state / labels / comments` 一起做 canonical hash；`_comments()` 同时读平台返回的 comments 与本地文档里的 `### comment-*` / `#### resolution-*` 块。
   `_body()` 的注释明确写着：**「Comment blocks live in the body but are compared separately, so the body projection must exclude them (platform copies never inline them)」** —— 即设计上**本地文档必须镜像平台评论**，平台副本不内联。
2. `bin/issue-sync` 头注释定义 raw 生命周期终点是 `configured-platform close (absorbed/closed)`；`raw_reconciliation.canonical_projection` 的注释明确写着 **「phase/* is a creation-time snapshot the platforms never update」** —— 平台 phase 标签不随本地 promote 更新，本地终态才是权威。
3. `wt-close` / `pr-create-guarded` 通过 `raw-reconciliation-gate.py --require-local` 做写入前 fail-closed 校验；这是门禁，不是可凑合的装饰。

## 2. 实现不达标之处（R33.8 收口时被迫造数据的根因）

- `platform-adapter.py::pull_raw_issue` 的 `body = details.get("body", "")` 之后**完全没有使用 `details["comments"]`**（`_discover_one` 通过 `**details` 已把 `fetch_issue` 的 comments 带进来）。
  → 每次 pull 从平台 body 重建本地文档，本地 `### comment-*` 块（由 `promote-finalize` 写入）被冲掉，而平台 comment 仍在 → `content_diverged`。
- 同一函数 `phase = "proposed"` 只读平台 `phase/*` 标签，且 `fm["phase_state"] = phase` 无条件覆盖。
  → 已 absorbed 的 raw 被重新物化回 `proposed`，`pr-create-guarded` 直接拒。
- R33.8 当时的处理是**手工编辑文档补回 comment 块、手工恢复 absorbed** —— 这是绕门禁而非修实现；下一次 pull 会稳定复现（R33.6 也出现过 `docs: restore raw absorption state after pull re-materialized it`）。

## 3. 方案空间

| 方案 | 做法 | 评价 |
|---|---|---|
| A | `pull_raw_issue` 把 `details["comments"]` 镜像成本地 `### comment-platform-<n>` 块；并对本地已终态的 raw 保留终态字段 | 符合 `_body()` / phase 快照注释所定义的设计意图 ✅ |
| B | 放宽 `raw_reconciliation` 的 comments 比较 | **改错门禁**，降低强度，禁止 |
| C | 让 `promote-finalize` 把 comment 写进平台 body | 与「平台副本不内联 comment」的设计矛盾，且改动面更大 |
| D | 继续在流程里手工补 comment 块 / 手工恢复 phase | 绕过门禁，禁止 |

## 4. 镜像格式为何成立

`_strip_meta()` 会剥掉以 `- ` 开头的 meta 行，剩下的文本与平台 comment 逐字比较（`_text` 折叠空白后 lower）。
所以本地块写成：

    ### comment-platform-1
    - source: platform
    - event: mirrored

    <平台 comment 原文>

即可让 `_comments()` 的 inline 集合与 remote 集合相等。heading 后缀不限定时间戳，正则 `^#{3,4}\s+(?:comment|resolution)-[^\n]+$` 可识别。

## 5. 证伪

- 「是平台没返回 comments」→ 否：`_discover_one` 的 `**details` 把 `fetch_issue` 的 `comments` 原样带进 replica；R33.8 的 gate receipt 里平台 comments 明确列出。
- 「absorbed 回退是 issue-sync create 干的」→ 否：`pull_raw_issue` 里 `fm["phase_state"] = phase` 已无条件覆盖，create 之前文档就已经是 proposed。
- 「改 gate 更省事」→ 否：gate 的 comments 比较是双向镜像契约，放宽会让平台/本地长期静默漂移。
