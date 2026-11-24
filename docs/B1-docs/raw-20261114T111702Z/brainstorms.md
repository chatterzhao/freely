---
b1_id: B1-20261114T111702Z
phase_state: completed
source_raw: raw-20261114T111702Z
source_url: https://github.com/chatterzhao/freely/issues/4654
produced_candidate: C-20261114T111702Z-A
created_at: 2026-11-24
---

# B1_IBM: freely comment 引用未定义 PROJECT_ROOT

## 0. 设计意图审计（先于方案）

### B0 前置：关键词广搜 + 多文档交叉

- 关键词族表（≥3 组，搜 docs/ bin/ .freely/）:
  - 命令名 `cmd_comment` / `freely comment` → `docs/system/workspace/scripts/runtime/freely:25027`、`docs/B1-docs/raw-20261114T111702Z/issue.md`、`docs/B2-docs/platform/issue-sync-modules/raw-20261110T130144Z/verification/test-evidence/AT-001-GREEN.log`
  - 字段名 `PROJECT_ROOT` / `SELF_ROOT` → `docs/system/workspace/scripts/runtime/freely:32`、`:25095`、`:3687`、`:3707`、`docs/B1-docs/raw-20260618T031437Z/issue.md`
  - 门禁名 `check-runtime-size` / `.size-budget` → `docs/system/workspace/scripts/runtime/.size-budget`、`docs/system/workspace/scripts/runtime/split-plan.md:97`、`docs/system/workspace/scripts/tests/test-runtime-split.py`
  - 症状 `unbound variable` → `docs/B1-docs/raw-20260712T124601Z/issue.md`、`docs/B1-docs/raw-20260629T165403Z/brainstorms.md`、本 raw
  - raw key `20261114T111702Z` → `docs/B1-docs/raw-20261114T111702Z/issue.md`、`.freely/goal-arch-debt.md`
- 怀疑多份文档: 是。一个函数可能同时存在「当前实现」「B1 历史描述」「过期预算数字」三份说法，不得只读本 raw 就下结论。
- 三类分层表:
  - 当前生效实现: `docs/system/workspace/scripts/runtime/freely`（权重：现状；`cmd_comment` 真源，27166 行）
  - 历史局部文档: `docs/B1-docs/raw-20260618T031437Z/issue.md`（权重：仅背景，描述另一处 PROJECT_ROOT/SELF_ROOT 用法）；`docs/system/workspace/scripts/runtime/split-plan.md:3` 的「27158 行」（权重：历史快照，已被预算文件覆盖）
  - 当前权威恢复点: `docs/system/workspace/scripts/runtime/.size-budget` = `27166`、`.freely/goal-arch-debt.md` 当前恢复点（权重：当前真相）
- 矛盾清单: 本 raw 写「27158/27158 预算上限」，而 `.size-budget` 已是 `27166`——前者过期，但**结论不变**（当前文件正好 27166 行，仍不能新增行）；`split-plan.md:3` 同样过期。两者只作背景，以 `.size-budget` 为准。
- 二元决策: **继续**（附方向）——按 `candidate C-20261114T111702Z-A` 做等长变量替换，不改结构、不加行、不放宽门禁。无覆盖者，不 dropped。

### 外部锚点（引用原文，至少两类）

- 当前实现 / 已定义变量: `docs/system/workspace/scripts/runtime/freely:32`「`SELF_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd -P)"`」
- 当前实现 / 未定义变量来源: `docs/system/workspace/scripts/runtime/freely:3707`「`PROJECT_ROOT="$project"`」——位于 `write_supervisor_identity_truth()` 的 heredoc 内，是写进 identity 文件的文本，不是全局赋值；`:3687` 还显式 `unset ... PROJECT_ROOT ...`。证明 `cmd_comment()` 作用域下 `PROJECT_ROOT` 确实未定义。
- 门禁源码理由: `docs/system/workspace/scripts/runtime/split-plan.md:97`「`bin/check-runtime-size` 读 `runtime/.size-budget`，超过即 fail-closed；只许下调，不许上调。」
- 既有 raw 验收契约: `docs/B1-docs/raw-20261114T111702Z/issue.md`「等长替换、不新增行——`runtime/freely` 正处 `check-runtime-size` 的 **27158/27158 行预算上限**」

- 判定（五选一，附证据）: **bug**——设计正确（`SELF_ROOT` 是单一根路径真源，ACP 通知应当在评论写出后触发），实现偏差（`cmd_comment()` 误用了只在别处作用域出现的 `PROJECT_ROOT`）。按「实现偏差」修法会改错对象（去定义第二个根路径变量），故判 bug 更准确。
- 与既有断言的冲突: 有。`check-runtime-size` 断言行数 ≤ `27166`，而「在函数入口 `local PROJECT_ROOT=...`」的方案会新增一行 → 必须冲突；谁该改：本轮方案改为等长替换变量引用，不改门禁、不改预算。
- 影响面: `docs/system/workspace/scripts/runtime/freely` 的 `cmd_comment()` 两处（`:25095`、`:25097`）变量引用；`freely comment` 的 ACP worker 通知路径；`check-runtime-size` 行数门禁（必须保持绿）。不改平台写逻辑、不改 adapter。

## 0.1 全局适配反思（四问）

- Q1 类别: 治理元数据修复（运行时变量作用域 bug），不是生命周期变更、副本传播或流程能力。
- Q2 职责边界: 与 `runtime/freely:32` 的 `SELF_ROOT` 共享「项目根路径」职责；唯一判定归 `SELF_ROOT`，`PROJECT_ROOT` 只在 supervisor identity 文件里有意义，不引入第二套真源。
- Q3 结构性冲突: 若按字面可接受方案「新增 local 变量」，会要求上调 `.size-budget`（门禁明令只许下调）→ 反设计；因此问题定义收敛为「等长替换已有变量引用」。
- Q4 门禁失配: `check-runtime-size` 测的是行数维度，本轮改的是变量引用维度，两者不冲突但存在约束关系——不绕过、不放宽，用等长替换同时满足。

## Input

- `docs/B1-docs/raw-20261114T111702Z/issue.md`（platform 物化，phase_state=proposed）
- 平台: GitHub #4654 / Gitee IKVBSU
- 吃狗粮实测连续 3 次复现：平台评论双平台写成功，尾部 `runtime/freely:25095: PROJECT_ROOT: unbound variable`，rc 非 0。

## Problem

`cmd_comment()` 在 adapter 写出评论后执行 ACP worker 通知时，两处 `python3 -c` 插值 `${PROJECT_ROOT}`；该变量在 `set -u` 下未定义，导致命令在写成功之后中断。平台写成功掩盖了失败，worker 收不到评论通知；对依赖自动评论写关闭理由的收口链路构成误判风险。

## Brainstorm

### Option A: 在 `cmd_comment()` 入口新增 `local PROJECT_ROOT="$SELF_ROOT"`

一次定义，两处引用不变。但 `runtime/freely` 当前 27166/27166 行，新增一行必然触发 `check-runtime-size` 失败；上调预算又被 `split-plan.md:97` 明令禁止。**否决**。

### Option B: 把两处 `${PROJECT_ROOT}` 等长替换为 `${SELF_ROOT}`

复用已定义的单一真源；语义不变（`SELF_ROOT` 指向项目根）；行数不变；`agent_working.agent_list_by_raw_key` 调用参数不变。替换前后字符串长度：`PROJECT_ROOT` 与 `SELF_ROOT` 不等长，但**只替换变量名不改行数**，行数门禁按行为单位，不受列宽影响。**采纳**。

### Option C: 去掉 ACP 通知段

改动最小但删除既有能力，与 raw「保持通知语义」要求冲突。**否决**。

## Decision: Option B

等长（同行）替换 `cmd_comment()` 内两处 `${PROJECT_ROOT}` → `${SELF_ROOT}`；不新增行、不改平台写、不改门禁。该 bug 属实现偏差中的变量作用域错误，不是设计错误。

## Candidate

- candidate_id: C-20261114T111702Z-A
- status: promoted
- milestone: M-20261114T111702Z-A
