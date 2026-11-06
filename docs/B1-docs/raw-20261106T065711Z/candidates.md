---
candidate_id: C-20261106T065711Z-A
status: promoted
source_raw: raw-20261106T065711Z
created_at: 2026-11-06
milestone: M-20261106T065711Z-A
---

# Candidates

被否决的替代方案（title-only 精确搜索、削减重试、跨写缓存 remote head、与标题达标逻辑合并）属于预研结论，完整记录见 `brainstorms.md` §关键评审 与 `brainstorms.md` §Candidates b/c/d，不作为 candidate 立项。

## C-20261106T065711Z-A: 批量化治理门禁读取

- candidate_format_version: v2
- title: 只改执行方式、不改判定语义，去掉 Step 2e 与 governance-merge-gate 的本地 N+1 子进程
- status: promoted
- decision_reason: 实测 `pr-create-guarded` 347s 中 243s 是纯本地进程扇出（Step 2e 188s 逐文件 find/cat/grep，governance-merge-gate 55s 内 3423 次 git 子进程），且该门禁在 pre-commit / pre-push / pre-merge-commit / pr-create / pr-merge 都会跑。这是「先磨刀」型全局杠杆：本轮做完，后续约 60 条 issue 每轮省 5–7 分钟。用户明确要求「功能逻辑不要误修改，比如精确搜索是否真的符合需求」，已逐条证伪并撤回错误方向，只保留两项零语义变化优化。
- next_action: 先写 AT-001 回归测试确认 RED；实现 `RepoView` 与单进程扫描；跑 GREEN；做 6 种调用模式 verdict parity、4,363 份真实治理文档逐函数退化审计、7 个相关回归基线对比。
- revisit_trigger: 若未来语料规模再增一个数量级使 804 次文件 open 成为新瓶颈，另开 issue 评估增量扫描；本 PR 不引入状态与缓存失效语义。
- acceptance_criteria:
  - `governance-merge-gate` 对同一 `--range` / `--staged` 输入，优化前后 verdict、warning、退出码逐字节一致；staged > range > disk 优先级与 `FileNotFoundError` 文案不变。
  - `build_issue_index` 的 git 子进程数从 3423 降到个位数；`--range` 耗时降到秒级。
  - Step 2e 不再逐文件启动 find/cat/grep；804 份真实 issue.md 的 `unresolved` / `resolved` 计数与最终判定逐文件与旧实现一致；输出行格式（含 em dash）与失败块文案不变。
  - `search_raw_issue` 的搜索字段 / `--state all` / 分页 / `--limit 20`、客户端二次校验、`_retry_read` 3 次重试与 fail-closed、跨写不缓存 remote head，全部不变。
  - 7 个直接相关回归测试以未修改 develop HEAD 做基线对比，零新增失败。
- promotion_gate: AT-001 RED → GREEN + 6 种调用模式 parity + 4,363 份真实文档退化审计 + 相关回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: cProfile 定位 `build_issue_index` 54.5s / 3423 次 git 子进程；精确复制 Step 2e 源码 + 完整环境三次实测 187.76 / 187.69 / 188.74s；实测 `git cat-file --batch` 对 `:path` 与 `REF:path` 均与 `git show` 字节级一致；804 份真实文件计数等价、真实 grep 抽样 0 mismatch；纠正两处测量偏差（stdout 重定向到 /dev/null、误用精简 PATH 绕开 IDE shim）。
  - verdict: pass
- promoted_issue_id: I-20261106T065711Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20261106T065711Z/issues/I-20261106T065711Z-A.md
- milestone: M-20261106T065711Z-A
- session_refs: []
