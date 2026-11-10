---
candidate_id: C-20261110T081029Z-A
status: promoted
source_raw: raw-20261110T081029Z
created_at: 2026-11-10
milestone: M-20261110T081029Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261110T081029Z-A: execution-network 族迁移 + 逐族 AT 可持续化

- candidate_format_version: v2
- title: 写侧改 `write --kv`、两处读者改 `values`、耦合测试改协议断言、两族 AT 的计数断言改单调守卫；全局状态 source 54 → 52
- status: promoted
- decision_reason: 恢复点建议的 manager_worker_launch 族经前置评审否掉（11 键不在白名单 + 55 测试耦合）；改选最小且真实活跃的 execution-network 族，同时修掉「上一族 AT 写死计数」这个会让每轮迁移互相拖红的固有缺陷。
- next_action: 建 AT-001（5 静态 + 6 行为，source 真实 freely）→ 改写入/读取 → 同步耦合测试 → 回归 → 拆白名单缺陷 #4264 并排进 goal。
- revisit_trigger: 若后续族的值可能含换行，需改用 JSON `read` 接口；若 lint 归零，把基线改为 0。
- acceptance_criteria:
  - RED：基线该族仍 heredoc + `source`；旧格式注入经真实函数真的创建 marker。
  - GREEN：AT-001 `11 ok / 0 failed`；TAB+JSON 落盘、旧格式兼容、注入不执行、恶意值逐字节。
  - GREEN：`check-state-file-sources` 计数 52 且 lint 通过；耦合回归 `test-freely-execution-network-failure-classification` 通过。
  - GREEN：R23.9 / R23.11 两族 AT 与 5 个相关测试 + `test-all --ci` 全绿。
  - GREEN：逐族 AT 计数断言为单调守卫，后续族迁移不再把上一族拖红。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 按形态与状态文件两维度重扫 54 处 source；否掉恢复点建议族并说明证据；验证 11 键不在白名单会抛 StateFileError；实测旧格式注入 PoC 创建 marker、新协议不创建；确认耦合测试与逐族 AT 的假红问题。
  - verdict: pass
- promoted_issue_id: I-20261110T081029Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T081029Z/issues/I-20261110T081029Z-A.md
- milestone: M-20261110T081029Z-A
- session_refs: []
