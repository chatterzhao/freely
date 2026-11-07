---
candidate_id: C-20261103T132526Z-A
status: promoted
source_raw: raw-20261103T132526Z
created_at: 2026-11-07
milestone: M-20261103T132526Z-A
---

# Candidates

被否决的替代方案（保留旧 JSON 位置参数调用、bash 侧读 token、文本 grep 判状态、夹带关闭路径与双平台入口收口）见 brainstorms.md。

## C-20261103T132526Z-A: 平台写通道失败必报、部分成功可追

- candidate_format_version: v2
- title: gitee 写原语对齐真实 CLI 契约、token 权威单点、探测区分四类原因、部分成功独立退出码且先落 id 再写状态
- status: promoted
- decision_reason: 写通道失败被兜底成「合法空结果」，且平台探测把四类原因压成一个 False，导致「Gitee 上根本没有对象」与「平台不支持」都表现为成功或误导性错误。
- next_action: 建 AT-001（静态 + 隔离夹具行为 + 真机只读核验），改 issue-sync 写原语与创建记账、adapter 探测报因与退出码、freely 的 JSON 解析。
- revisit_trigger: 若引入第三个平台或把写通道整体迁到 adapter（#4166），需重新对齐退出码约定。
- acceptance_criteria:
  - gitee 写调用走 `--repo <repo> <sub> --flag`，失败非零且不产生「成功」外观。
  - 无 `GITEE_TOKEN` 环境变量时 Gitee 写通道照常执行（token 由 gitee-issue.py 读取）。
  - `_gitee_repo_from_url` 对 scp-like / ssh / https 三种形态均产出 `owner/repo`。
  - 一平台成功一平台失败时 `create` 退出 3、只落已创建平台 id、`platform_state` 保持原值。
  - 缺 `gh` 时报 `not installed` 而非 `unsupported platform`；`create-issue` 0/3/1。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行复核 6 处证据点；基线快照跑 AT-001 得 15 项失败；真实仓库只读核验 `_gitee_repo` 与 adapter 探测；逐条证伪 #4184 / #4154 / #4195 覆盖范围。
  - verdict: pass
- promoted_issue_id: I-20261103T132526Z-A
- promoted_issue_path: docs/B2-docs/gate/platform/raw-20261103T132526Z/issues/I-20261103T132526Z-A.md
- milestone: M-20261103T132526Z-A
- session_refs: []
