---
candidate_id: C-20261109T074900Z-A
status: promoted
source_raw: raw-20261109T074900Z
created_at: 2026-11-10
milestone: M-20261109T074900Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261109T074900Z-A: pkill -f 项目路径正则转义

- candidate_format_version: v2
- title: 新增 `freely_escape_regex()` 单一 helper（re.escape + argv），两处含 `${project}` 的 pkill 站点使用转义结果
- status: promoted
- decision_reason: 项目路径含正则元字符时，`pkill -f` 会把路径当通配符，停止项目 A 可能误杀项目 B 的 A2A server；实测 5 处 pkill 中 2 处有此问题。
- next_action: 建 AT-001（4 静态 + 2 对照 + 6 行为，含真实 pgrep 反向 PoC）→ 基线 RED → 实现 → 回归。
- revisit_trigger: 若后续新增「外部路径进 pkill/pgrep 正则」的站点，必须复用本 helper 并补断言。
- acceptance_criteria:
  - RED：未转义路径的正则会匹配 sibling 项目；真实 `pgrep -f` 未转义 pattern 命中 ≥2 进程。
  - GREEN：helper 转义 `. + ( [ $ *` 等元字符；两处 pkill 均使用；转义后只命中自己的进程且仍匹配自己。
  - GREEN：3 处固定 pattern pkill 逐字不动；`bash -n` 通过；相关回归 0 新增失败。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: executable-reproduction + desk-research
  - summary: 实测 5 处 pkill 仅 2 处含项目路径；面 1/2 真源在最新 develop 零命中、行号全漂移，按先例拆 #4254；确认无需改固定 pattern 站点。
  - verdict: pass
- promoted_issue_id: I-20261109T074900Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20261109T074900Z/issues/I-20261109T074900Z-A.md
- milestone: M-20261109T074900Z-A
- session_refs: []
