---
b1_id: B1-20261116T050414Z
phase_state: completed
source_raw: raw-20261116T050414Z
source_url: https://github.com/chatterzhao/freely/issues/4657
produced_candidate: C-20261116T050414Z-A
created_at: 2026-11-16
---

# B1_IBM: 标题规范化前移到 scan 漏斗

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文，至少两类）:
  - 门禁源码注释/理由：`docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py:1`「Read-only lifecycle gate for a configured raw replica set.」；`raw_reconciliation.py:102-109`「Create a deterministic, write-free receipt for one raw key.」
  - 既有同类实现：`docs/system/workspace/scripts/runtime/pre-scan-fix.sh:2-3`「This entry is deliberately read-only: scan preparation must not create lifecycle facts, worktrees, PRs, commits, or platform side effects.」
  - 历史设计决策：`docs/B1-docs/raw-20261105T051136Z/brainstorms.md:71`「不改平台读取通道、不改 scan 状态机。」
  - 既有验收测试/行为：`platform-adapter.pull_raw_issue()` 约 `:1549-1555`「canonical = canonical_raw_title(raw_key, title)」「[title] {plat}: normalized to {canonical}」——自动规范化早已实现，只在物化路径触发。
  - 用户结论（本 raw 评论，最终方案修订）：「从平台拿 raw issue 的那一刻起，后面看到的都是标准标题。」
- 判定（五选一，必须给证据）: **实现未完成**。标题达标契约（`raw_title_contract.py`）、平台写通道（`platform-adapter.py`）、自动规范化（`pull_raw_issue()`）三者都具备；缺的是把规范化接到**所有平台 raw 进入本地任务的唯一漏斗**（`freely task-source-scan`），且已 absorbed/CLOSED 副本因防重新物化守卫走不到既有路径。不是设计错误，也不是 bug（新命令能力缺失）。
- 与既有断言的冲突: **有，且必须冲突**——`pre-scan-fix.sh` 明写 scan 前置不得有平台副作用；字面「在 scan 内自动写标题」会破坏该契约。解决方式：不改前置辅助脚本、不改 `task-lifecycle-scan.py` 分析器；把写操作放到 scan 命令（`cmd_task_source_scan`）自己的显式 preflight 步骤，由 adapter 唯一通道执行、可审计、可 dry-run。谁改：本 issue 改命令编排，不动既有只读契约。
- 影响面: `docs/system/workspace/scripts/runtime/freely`（cmd_task_source_scan）；新增规范化模块/命令；`pr-create-guarded` Step 0b-pre；`raw-reconciliation` 诊断字段；`docs/milestones.md`；`bin/test-all` 注册新 AT。

## 0.1 全局适配反思（四问）

- Q1 类别: **流程能力**——平台 raw 身份在进入本地治理前的规范化前置，不是生命周期变更（不改 phase_state 机）。
- Q2 职责边界: `raw_title_contract.canonical_raw_title()` 拥有「标题应然格式」唯一判定；`platform-adapter.py` 拥有唯一平台写通道；`task-lifecycle-scan.py` 只做只读分析；`raw-reconciliation-gate` 只做只读判定。最终判定归契约 + adapter，命令编排只负责调用时机。
- Q3 结构性冲突: 若把平台写直接塞进分析器，会要求「每次 scan 都产生副作用」，与 `scan is cheap`、`pre-scan read-only` 反设计 → **改问题定义**为「命令级 preflight」，分析器保持纯净。
- Q4 门禁失配: 现有 gate 测的是身份唯一性（标题前缀）与副本一致性；本轮改的是「在 gate 之前把标题修达标」。维度一致，因此**不改 gate 判定、不放宽 ambiguous**，只补 `non_canonical_title` 结构化诊断与精简输出。

## Input

- 来源：GitHub #4657 / Gitee IKVLKU，2026-11-16 由 `freely feedback create --kind fix --severity P2` 创建。
- 物化工位：`fix/raw-20261116T050414Z-scan-title-normalize` + 同名 test-pre-merge。
- 本 raw 平台正文有两段：初版评审（pr-create 为主）+ 用户方案修订评论（scan 为主）。**以评论为准**：主入口前移到 scan，pr-create 降级为覆盖 CLOSED/absorbed 的兜底。
- 本轮前置检索已完成的证伪：`I-20261105T051136Z-A`（标题契约）、`I-20260725T030511Z-A`（只读 receipt）、`I-20261102T113816Z-A`（三态化）三族均 completed 且不覆盖本缺口；平台抽样 300 条 raw 中 6 条标题不规范且全 CLOSED，5 条 open 全达标 → 低频但命中即 100% 阻断 PR。

## Problem

1. `freely task-source-scan` 是所有平台 raw 进入本地任务的唯一漏斗，但没有任何标题规范化动作；标题缺 `[RAW-<key>]` 前缀时，`discover_raw_replicas()` 会退化成 ambiguous（3 个正文引用候选），PR 被 Step 0b 拦死。
2. 自动规范化能力在 `pull_raw_issue()`，只覆盖「物化时」；已 absorbed / 全 CLOSED 副本被防重新物化守卫挡住 → 对 PR 场景不可达。
3. `task-lifecycle-scan.py:518-540` 的 `_build_raw_key_index()` 只用 title 建 raw key 索引；标题不达标会让 fallback 索引缺失。而 `:809` 用的是 `title+body`，可从 body 的 `local_id: raw-<key>` 取权威 key → 规范化必须发生在建索引之前。
4. 门禁错误只倒 JSON receipt + 「resolve explicitly」，不告诉执行者该执行什么命令，也不给 from→to。

## Brainstorm

### Option A: 在 read-only gate 内部自愈

检测到标题不达标就由 `reconcile()` 直接写平台。优点一步到位；缺点破坏 write-free receipt、产生第二平台写通道、自愈掩盖 drift。→ **否决**（违反锚点 1/2）。

### Option B: 只在 pr-create 做 preflight

上一轮 raw body 的方案。优点不用动 scan；缺点太晚——scan 已经把不达标 raw 分派给本地任务，且 CLOSED/absorbed 之外的 OPEN raw 问题依旧存在。→ **降级为兜底**。

### Option C: scan 命令 preflight 主入口 + pr-create 兜底（推荐）

在 `cmd_task_source_scan` 调用分析器之前，对平台 OPEN raw 做窄规范化：从 `title+body` 取 key → `canonical_raw_title()` 算应然标题 → adapter `update-issue` 只改标题 → 打印 from→to → 再跑 scan。`pr-create-guarded` 保留同样的 preflight 覆盖 scan 看不到的 CLOSED/absorbed raw。门禁保持只读，只补诊断字段。优点覆盖唯一漏斗、可审计、幂等；缺点多一个 preflight 步骤。→ **采用**。

### Option D: 只修 pull_raw_issue 的守卫

放开防重新物化守卫让 CLOSED raw 也能 pull。优点改动小；缺点会重新物化已关闭 raw（11-14 刚修的污染路径），且 OPEN 未物化 raw 仍靠人工。→ **否决**。

## Decision: Option C

理由：用户明确指出 scan 是唯一漏斗；既有历史实现（Option D 的能力部分）已经存在但因设计约束不可达，正确修法是把同一契约接到正确时机，而不是重写能力或放宽门禁。B0 判定的「实现未完成」与选项 C 一一对应。

## Candidate

- candidate_id: C-20261116T050414Z-A
- status: promoted
- milestone: M-20261116T050414Z-A
