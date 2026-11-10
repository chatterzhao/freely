---
candidate_id: C-20261109T085539Z-A
status: promoted
source_raw: raw-20261109T085539Z
created_at: 2026-11-10
milestone: M-20261109T085539Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261109T085539Z-A: worker 派发走 JSON Lines + NUL 流；python3 -c 边界 lint

- candidate_format_version: v2
- title: TSV 通道改 JSON Lines + NUL 解码；畸形行显式报告；新增 python3 -c 边界 lint 基线
- status: promoted
- decision_reason: AI prompt 含 tab 即字段错位，worker 被误标 `worktree_missing` 永久派不出去，且 `except: pass` 让畸形输入表现为「没有待派发任务」。
- next_action: 建 AT-001（5 静态 + 2 对照 + 9 行为）→ 基线 RED → 实现 → 真机 bash 冒烟。
- revisit_trigger: 若后续把派发改成并发或换 IPC，NUL 流契约需重述。
- acceptance_criteria:
  - RED：含 tab 的 submitted 任务被标 `worktree_missing`；当前机制对照证明错位。
  - GREEN：TSV 通道删除，派发走 JSON；tab/换行/引号逐字节保留；6 字段边界与顺序不变。
  - GREEN：畸形行报 stderr 并跳过；空输入干净 no-op；R22 回归全绿。
  - GREEN：lint 覆盖 `python3 -c` 插值且不误报 argv 安全形式，输出可计数基线。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: executable-reproduction + desk-research
  - summary: 实测 TSV 唯一消费点在 `freely:14134`、其它 3 处 `IFS=$'\t'` 属无关通道；108 个 lint 候选需逐处判定而非机械替换；状态文件 20 读/15 写需独立迁移。
  - verdict: pass
- promoted_issue_id: I-20261109T085539Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261109T085539Z/issues/I-20261109T085539Z-A.md
- milestone: M-20261109T085539Z-A
- session_refs: []
