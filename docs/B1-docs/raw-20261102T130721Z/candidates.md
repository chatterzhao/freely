---
candidate_id: C-20261102T130721Z-A
status: promoted
source_raw: raw-20261102T130721Z
created_at: 2026-11-02
milestone: M-20261102T130721Z-A
---

# Candidates

## C-20261102T130721Z-A: 声明式工作树种子清单

- candidate_format_version: v2
- title: 用 tracked 清单 + 独立执行器替换 wt-create 里的逐条硬编码复制
- status: promoted
- decision_reason: `git worktree add` 不检出未跟踪文件，而工位运行依赖它们；上一轮为 `agent-table.toml` 加了一条硬编码 `cp`，这类补丁会随需求线性增长且换项目不可用。清单随仓库走、执行器可单测、`wt-create` 只留一个调用点。
- next_action: B2 物化 `I-20261102T130721Z-A`；先写 RED（执行器不存在 / 不复制 / 不校验越界），再实现并接入 `wt-create`，最后删掉硬编码那行。
- revisit_trigger: 若连续两个里程碑没有新增清单条目，且 `wt-seed list` 长期只有默认一条，说明抽象过重，可考虑并回 `wt-create`。
- acceptance_criteria:
  - 清单存在时按清单复制/链接；dev 与 test 两个工位都执行
  - 清单缺失时回落内置默认（`agent-table.toml`，copy，required=false）
  - 目标已存在 → skipped，不覆盖
  - 源缺失：required=true 失败并指出路径；required=false 告警继续
  - 绝对路径 / `..` 越界拒绝
  - link 模式生成软链接且源改动可见
  - `wt-create` 不再有硬编码的 agent-table 复制
- promotion_gate: RED→GREEN + 既有 worktree 相关测试全绿 + `governance-merge-gate --range develop..HEAD` 通过
- open_questions:
  - 是否需要在 `wt-close` 时清理 link（当前不清理，链接随工位目录一起删除）
  - 清单是否支持 glob（当前不，显式路径更可审计）
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 读 `wt-create:723-742`（既有 `.freely` clone 逻辑）、`.gitignore`（`.freely/` 整体忽略）、`templates/config.toml.example`（说明 config 是生成物）；确认硬编码 cp 是上一轮新增
  - verdict: pass
- promoted_issue_id: I-20261102T130721Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261102T130721Z/issues/I-20261102T130721Z-A.md
- milestone: M-20261102T130721Z-A
- session_refs: []

## C-20261102T130721Z-B: seed 漂移检查

- candidate_format_version: v2
- title: 巡检“工位缺少清单内文件”与“清单指向已不存在的源”
- status: needs_research
- decision_reason: 清单是声明式的，就会漂移：源被删、工位被手工清理。当前只能等运行时报错。
- next_action: C-A 合并后单独立 raw；定义 `wt-seed check --all-worktrees` 的只读输出格式。
- revisit_trigger: 出现第二次“工位缺 seed 文件导致运行失败”的事故
- acceptance_criteria:
  - 只读巡检，输出每个工位的缺失项
  - 不自动修复
- promotion_gate: 独立 B2 + RED/GREEN
- open_questions:
  - 是否纳入 scan 的每轮巡检（可能过重）
- acceptance_reviews: []
- promoted_issue_id: ''
- promoted_issue_path: ''
- milestone: M-20261102T130721Z-A
- session_refs: []
