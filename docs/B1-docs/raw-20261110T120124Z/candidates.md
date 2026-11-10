---
candidate_id: C-20261110T120124Z-A
status: promoted
source_raw: raw-20261110T120124Z
created_at: 2026-11-10
milestone: M-20261110T120124Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261110T120124Z-A: 运维底座六项收口（watchdog / 事件字段 / 日志保留 / 打包卫生 / 凭据 / DB 版本）

- candidate_format_version: v2
- title: watchdog 不再诈死并持有 pid；`append_runtime_event` 增加 severity/trace_id；cycle/crash 日志按数量保留；打包排除 `__pycache__`/`*.bak.py`；Gitee token 改 header、Codex key 改 env；DB 加 `PRAGMA user_version` 且迁移失败即抛
- status: promoted
- decision_reason: 六项都是「失败或资源无界却不可见」：watchdog 首次违规即死、日志无法过滤关联、磁盘无限增长、安装包带缓存与死代码、同机 ps 可见密钥、迁移静默失败。
- next_action: AT-001（7 静态 + 4 行为）→ 基线 RED `0 ok / 11 failed` → 六项实现 → GREEN → 回归 → 真实 Gitee 只读验证 → PR。
- revisit_trigger: 若 watchdog 改为受管守护进程、事件日志改 JSON Lines、或 Gitee 认证方式变化，需重述断言与实现。
- acceptance_criteria:
  - RED：基线 11 项全 FAIL。
  - GREEN：AT-001 `11 ok / 0 failed`；真实 `gitee-issue.py get` 通过 header 认证。
  - GREEN：不改 `append_runtime_event` 调用签名、不改 `--key` CLI 语义、不改 #4158 的 output 守卫、不改 lifecycle-trace 的 seq 语义。
  - GREEN：DB/派发/契约/CLI help/并发回归 0 新增失败；`test-all --ci` 执行新 AT。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐项在目标文件核对（watchdog 全文、append_runtime_event、_rotate_log 与两处生成点、package 复制循环、gitee-issue api_request、ai-cli bundle 写入、DB 两处迁移）；`--output` 守卫确认已由 #4158 落地；用 `git archive` 基线跑最终版 AT 得到 RED `0 ok / 11 failed`；用真实 Gitee 只读 `get IKUEK0` 预演 header 认证成功。
  - verdict: pass
- promoted_issue_id: I-20261110T120124Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T120124Z/issues/I-20261110T120124Z-A.md
- milestone: M-20261110T120124Z-A
- session_refs: []
