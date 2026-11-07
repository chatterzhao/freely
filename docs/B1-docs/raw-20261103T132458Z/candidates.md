---
candidate_id: C-20261103T132458Z-A
status: promoted
source_raw: raw-20261103T132458Z
created_at: 2026-11-03
milestone: M-20261103T132458Z-A
---

# Candidates

被否决的替代方案（无差别改整族 shim 含 post-checkout、把外部项目也判为环境故障、把 check-file-size 全量结果直接阻断 commit、给 `.githooks/bin` 注入 PATH）属自锁或越界，记录见 brainstorms.md，不作为 candidate 立项。

## C-20261103T132458Z-A: 门禁 fail-open 收敛为 fail-closed

- candidate_format_version: v2
- title: 统一退出码约定，6 个 shim / pre-commit.sh / pr-create-guarded / checkpoint-guard / check-file-size 全部不再把环境缺失翻译成通过
- status: promoted
- decision_reason: 门禁存在性与有效性脱钩是可信度根基问题（R9/R10 的前置）。必须复用「0/1/2」约定并精确保留外部项目、`post-checkout`、正常无 raw key 三类合法路径，同时用增量 file-size 门禁避免历史遗留自锁。
- next_action: 写 AT-001 RED（隔离 git 仓库真实 commit + 静态契约），改 10 个真源，跑 GREEN、真实工位 commit 冒烟、14 个回归基线对比。
- revisit_trigger: 若未来把 `.githooks/bin/git` 接进 PATH，另开 issue 验证 `--no-verify` 拦截；本 PR 不接线。
- acceptance_criteria:
  - 6 个 shim 无裸 `exit 0`、用 `-f`、缺失真身 `exit 2`；`post-checkout` 逐字节不变。
  - 隔离仓库缺真身时 `git commit` 被拒；真身存在但丢失 `+x` 时仍真实执行（sentinel 验证）。
  - `pre-commit.sh` hooksPath 不符/门禁真身缺失时非零；外部项目合法早退保留。
  - `pr-create-guarded` 每处 not-found skipping 伴随非零退出；正常无 raw key 路径仍继续。
  - `checkpoint-guard` 默认 required 时返回非零。
  - `check-file-size` 全量运行报出 `runtime/freely`；接入 pre-commit 用 `--staged-only` 且真实 commit 通过。
  - 14 个相关回归以未修改 develop HEAD 基线对比零新增失败。
- promotion_gate: AT-001 RED → GREEN + 真实 commit 冒烟 + 14 个回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐个 shim 核对真身存在性与触发场景；实测 check-file-size 历史 errors 数与全量耗时；隔离 git 仓库真实 commit 验证 fail-closed 与 `-x` 丢失；真实工位 commit 冒烟确认不自锁；10 个真源还原到 develop 做 RED 与 14 个回归基线对比。
  - verdict: pass
- promoted_issue_id: I-20261103T132458Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20261103T132458Z/issues/I-20261103T132458Z-A.md
- milestone: M-20261103T132458Z-A
- session_refs: []
