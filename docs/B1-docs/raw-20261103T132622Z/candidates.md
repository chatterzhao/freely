---
candidate_id: C-20261103T132622Z-A
status: promoted
source_raw: raw-20261103T132622Z
created_at: 2026-11-09
milestone: M-20261103T132622Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261103T132622Z-A: 用 flock 与 CAS 取代「先检查后动作」的并发控制

- candidate_format_version: v2
- title: 启动锁改 flock fd 继承 + owner/age 校验；DB daemon 用 flock 抢 pid 文件并在 bind 前探测；派发改 `launching` CAS；SSE 收敛为单链路；pid 复用校验 cmdline
- status: promoted
- decision_reason: 五个面共享同一根因——没有原子性原语。后果是「DB 全停 + 双 supervisor + worker 重复拉起」，表现为 AI 行为怪异而非崩溃，现场无法定位；且 R20 #4163 以本条为前置。
- next_action: B2 精确定位派发器与 SSE 的行号 → 建 AT-001（每个面至少一条并发/行为断言）→ 实现 → 并发背靠背验证。
- revisit_trigger: 若引入跨机器调度或共享存储（NFS）导致 flock 语义不可靠，需改为 lease/CAS 服务。
- acceptance_criteria:
  - RED：背靠背两次 `freely start`（隔离临时项目）→ 只有一个 supervisor，第二个明确拒绝；当前可能两个都过。
  - RED：并发两次 `ensure_freely_db` → 只有一个 daemon、一个 socket inode；当前可能双 daemon。
  - GREEN：启动锁由 flock fd 持有并继承给 supervisor；锁回收带 age + owner（pid + cmdline）校验。
  - GREEN：DB daemon 抢锁成功才 bind；`_cleanup` 删文件前比对 pid 文件内容 == 自己。
  - GREEN：派发改为启动前 CAS 抢占（`update --state launching --claimed-by`），失败即跳过；同队列只剩一个派发器。
  - GREEN：SSE 只保留一条链路，watch-in-watch 死代码删除。
  - GREEN：`pkill -f` 前对 `$project` 做正则转义。
- promotion_gate: AT-001 RED → GREEN + 并发实测 + governance gate
- open_questions:
  - SSE 死代码与第二个派发器的确切行号需在 B2 定位（develop 行号已与 issue 写作时漂移）。
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 复核 9 个证据点中 4 个（`state_file_missing` 设置/消费点、5 处 `rm -rf "$lock_dir"`、db_manager 零 flock、`_generate_chat_id` 单写者注释）在 develop 上仍成立；确认与 #4148/#4236/#4163 不重叠且为 #4163 前置。
  - verdict: pass
- promoted_issue_id: I-20261103T132622Z-A
- promoted_issue_path: docs/B2-docs/runtime/concurrency/raw-20261103T132622Z/issues/I-20261103T132622Z-A.md
- milestone: M-20261103T132622Z-A
- session_refs: []
