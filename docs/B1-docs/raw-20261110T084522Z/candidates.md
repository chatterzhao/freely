---
candidate_id: C-20261110T084522Z-A
status: promoted
source_raw: raw-20261110T084522Z
created_at: 2026-11-10
milestone: M-20261110T084522Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261110T084522Z-A: 状态键白名单由自动扫描 lint 守护并补齐 65 键

- candidate_format_version: v2
- title: 新增 `bin/check-state-file-keys`（5 种写入形态抽取 + 差集失败）、`ALLOWED_KEYS` 77 → 142、注释改为 lint 校验、AT-001 用独立夹具验证扫描器自身
- status: promoted
- decision_reason: 白名单注释宣称「全量扫描」但实测漏 65 个键，导致兼容读取旧格式整份抛错、shell 侧 `|| true` 吞错后静默丢状态；会阻塞后续所有大族迁移。
- next_action: 建 AT-001（4 静态 + 7 扫描器 + 5 行为）→ 写 lint → 按实测补键 → 修两轮扫描器漏判 → 回归。
- revisit_trigger: 若将来新增第 6 种状态写入形态（如 python 直接写文件），需扩充 lint 抽取器并加夹具断言。
- acceptance_criteria:
  - RED：基线无 lint、白名单 77 键、issue 复现的 legacy 文件整份抛错；唯一 PASS 是「未知键仍拒绝」。
  - GREEN：AT-001 `16 ok / 0 failed`；lint missing=0 且 stale=0。
  - GREEN：65 个键 legacy 与 TAB+JSON 逐字节往返、恶意值不执行；issue 复现用例通过。
  - GREEN：伪造未知键仍被拒绝。
  - GREEN：扫描器夹具覆盖 6 类写入形态且无局部变量泄漏。
  - GREEN：R23.9/R23.11/R23.12 三族 AT + 10 个相关测试 + `test-all --ci` + 两个 lint 全绿。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐处核对 15 个 heredoc / 2 个 here-string / 4 个 printf / 3 个 echo / 6 个 --kv 写入点；实测 `read_state` 抛错；两轮修正扫描器自身漏判与过宽；验证补齐后差集与 stale 归零、未知键仍拒绝。
  - verdict: pass
- promoted_issue_id: I-20261110T084522Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T084522Z/issues/I-20261110T084522Z-A.md
- milestone: M-20261110T084522Z-A
- session_refs: []
