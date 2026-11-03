---
b1_id: B1-20261103T121047Z
phase_state: completed
source_raw: raw-20261103T121047Z
source_url: https://github.com/chatterzhao/freely/issues/4139
produced_candidate: C-20261103T121047Z-A
created_at: 2026-11-03
---

# B1_IBM: pr-merge-guarded 批量 issue-sync 误关闭非本 lane open issue

## Input
- P0 事故：docs-only lane（raw-20261103T111400Z）合并时，pr-merge-guarded 的 _sync_issues_changed_in_merge 取 `git diff develop..src -- docs/B1-docs/**/issue.md` 的**全部**变化文档，对每个 raw/proposed 文档执行 phase→absorbed + issue-sync close。
- 结果：13 个与 lane 无关的真实 open issue 在 GitHub 全部被关闭（Gitee 6 个），已手工重开；日志 `[MERGE-GUARD] synced 29 issue(s) to platforms`。
- 附带发现：gitee-issue.py reopen 用 repo_path（/repos/{owner}/{repo}/issues/N）导致 Gitee 返回 404 "project or enterprise"；close 已用 repo_path_post + repo body 的 legacy 形态可用。

## Option A: 合并前跳过 issue-sync（否决）
- 会丢掉正常 lane 的 raw→absorbed 收口能力，导致平台 issue 永久 open。

## Option B: 按分支 raw key 限定同步范围（选定）
- 从 source branch 解析 raw key；changed_issues 只保留 id 含该 key 的条目（raw-<key> / I-<key>-*）。
- 分支名无 raw key 时保持旧行为（兼容）。
- 过滤逻辑抽成 `issue-sync-scope.py` 纯函数，可单测。

## Option C: 只处理 raw/absorbed 状态的文档（否决）
- 仍会关闭其他 lane 的 absorbed 文档，无法区分"本 lane 的收口"与"治理数据变更"。

## Decision: Option B（+ reopen 形态修复）
- 边界：不改正常 lane 的收口语义；不引入新平台写操作；只收紧 scope。

## Candidate
- candidate_id: C-20261103T121047Z-A；milestone: M-20261103T121047Z-A
