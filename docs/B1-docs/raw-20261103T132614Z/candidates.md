---
candidate_id: C-20261103T132614Z-A
status: promoted
source_raw: raw-20261103T132614Z
created_at: 2026-11-10
milestone: M-20261103T132614Z-A
---

# Candidates

被否决方案与面 3–6 的承接关系见 brainstorms.md。

## C-20261103T132614Z-A: 注册表路径单一所有者 + raw key 入口规范化

- candidate_format_version: v2
- title: 新增 `runtime/paths.sh` 作为 tool-registry 路径唯一来源并让缺失 fail-closed；`wt-create` 通过 `runtime/raw_key_canon.py` 规范化 legacy raw key
- status: promoted
- decision_reason: `deploy-skills` 与 `_init_acp_tool_setup` 各自拼了一份错误路径且都静默降级；`wt-create` 接受 legacy raw key 只告警，导致分支名与下游 `T...Z` 提取器不一致、`raw_key=""`。两者都属「同一值多副本」且已产生实际错误行为。
- next_action: AT-001（6 静态 + 3 registry 行为 + 4 raw key 行为）→ develop 基线 RED → 实现 paths.sh / fail-closed / canon legacy + CLI / wt-create 规范化 → GREEN → 回归 → PR。
- revisit_trigger: 若将来 `tool-registry.toml` 支持环境变量覆盖或迁出 `docs/`，需重述 `paths.sh` 的签名；若 A2A 状态机或数据库改用新 key 格式，需重述 legacy 转换。
- acceptance_criteria:
  - RED：develop `56d4cd2c9` 基线 + 最终版 AT-001 → `1 ok / 12 failed`（唯一 PASS 是显式 `--tools claude` 守卫）。
  - GREEN：AT-001 `13 ok / 0 failed`；注册表缺失时 `deploy-skills` 非零退出且 stderr 含 tool-registry；legacy 四种输入全部规范化。
  - GREEN：生产代码（`bin/`、`runtime/freely`、`worktree/wt-create`）无 `scripts/runtime/tool-registry.toml`。
  - GREEN：`test-wt-create-*`、`test-concurrency-singletons`、`test-db-single-writer` 等回归 0 新增失败；`bin/test-all --ci` 执行新 AT。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 在目标文件上逐处核对 `bin/deploy-skills:72` / `runtime/freely:21469` / `runtime/freely:67` / `tool-launchers.sh:56` / `worktree/wt-create:279-284` / `raw_key_canon.py`；确认 `bin/ensure-acp-binary` 已不存在（正文该条过时）；用 `git archive develop` 基线跑最终版 AT 得到真实 RED；在隔离树里复现 `deploy-skills` 的 claude fallback 与 `cline` 输出差异，据此设计 present 断言。
  - verdict: pass
- promoted_issue_id: I-20261103T132614Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132614Z/issues/I-20261103T132614Z-A.md
- milestone: M-20261103T132614Z-A
- session_refs: []
