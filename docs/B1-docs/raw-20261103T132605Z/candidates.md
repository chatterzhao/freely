---
candidate_id: C-20261103T132605Z-A
status: promoted
source_raw: raw-20261103T132605Z
created_at: 2026-11-09
milestone: M-20261103T132605Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261103T132605Z-A: `runtime/freely` 被 source 时无副作用、缺库不杀调用方

- candidate_format_version: v2
- title: 区分执行/被 source：sourced 时不改 shell 选项、缺库返回码 + `FREELY_LIB_LOAD_ERROR`、库加载段 0 处 `exit`；`stop_project_runtime` 用返回码替代 `exit`
- status: promoted
- decision_reason: 4 个控制面脚本 source 该库；缺一个库文件就让 watchdog/dispatcher/promotion gate/supervisor 同时退出，supervisor 表现为「watchdog 起不来」并 30 秒后拉停 daemon。且 source 会强加 `-euo pipefail` 给调用方。
- next_action: 建 AT-001（2 静态 + 4 行为）→ 改文件头与 `stop_project_runtime` → 回归。
- revisit_trigger: 若后续拆 `lib/state.sh` 等，`_FREELY_IS_SOURCED` 判定与加载段契约需随之迁移。
- acceptance_criteria:
  - RED：基线前 70 行有 2 处 `exit 1`；`freely_stop` 分支用 `|| exit 1`。
  - RED：基线 source 在隔离夹具里直接失败（无输出），sourcing 改变调用方 shell 选项。
  - GREEN：AT-001 `6 ok / 0 failed`。
  - GREEN：直接执行缺库仍 rc=1（行为不变）。
  - GREEN：`bash -n` 通过；4 个 source 调用方语法通过；`bin/test-all --ci` 与关键测试全绿。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 核对两处 `exit 1`、顶层 `set -e`、末尾 `BASH_SOURCE` 守卫、`freely_stop` 的 `|| exit 1`；确认 4 个调用方与 551 测试依赖「source 后函数可用」。
  - verdict: pass
- promoted_issue_id: I-20261103T132605Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132605Z/issues/I-20261103T132605Z-A.md
- milestone: M-20261103T132605Z-A
- session_refs: []
