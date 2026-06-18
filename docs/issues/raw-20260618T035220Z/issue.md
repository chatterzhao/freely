---
local_id: raw-20260618T035220Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T035220Z-A
platform_ids:
  github:
    issue_id: '2964'
    url: https://github.com/chatterzhao/freely/issues/2964
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T03:52:37Z'
updated_at: '2026-06-18T03:52:37Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

pr-merge-guarded 依赖 gh pr merge 或本地 git merge，只能检测 git 层面的文本冲突。当两个分支修改了同一文件的不同位置时，git 自动合并——即使合并结果破坏了功能。

### 实际案例

ef251886（receipt fix: --subject/--body split）和 15fa666c（pull fix: fetch+reset fallback）修改了 pr-merge-guarded 的不同行。Git 自动合并，没有冲突提示。但合并结果回退了 receipt fix——因为 15fa666c 基于旧版代码，不知道 receipt split 的存在。

后果：receipt 静默丢失 → reference-transaction hook 拦截所有 ref 更新 → develop 无法同步 → 开发者面对 "cannot advance without receipt" 错误完全不知道根因。

### 缺少的机制

| 阶段 | 当前 | 应该 |
|---|---|---|
| pre-merge | governance-merge-gate 只检查 IBM 文档 | 检查 merge diff 是否会导致已有功能退化 |
| merge 中 | git auto-merge，不验证语义正确性 | 验证关键 invariant |
| post-merge | reference-transaction hook 拦截无 receipt 的 ref | 已有，但错误信息不够 actionable |

### 具体改进

1. reference-transaction hook 拦截时，错误信息应包含具体 commit SHA 和修复指引
2. pr-merge-guarded 合并后立即检查 merge commit 是否包含 Freely-Merge-Path
3. 若缺少 receipt，阻塞并打印清晰错误，而不是靠之后的 ref update hook 拦截
