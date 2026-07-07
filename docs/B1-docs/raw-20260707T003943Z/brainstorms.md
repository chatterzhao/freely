---
b1_id: B1-20260707T003943Z
phase_state: completed
source_raw: raw-20260707T003943Z
source_url: https://github.com/chatterzhao/freely/issues/3788
produced_candidate: C-20260707T003943Z-A
created_at: 2026-07-07
---

# B1: Gitee assignee API 修复 — wt-create 失败根因

## Input
- raw-20260707T003943Z: wt-create Gitee assignee check 修复
- GitHub issue #3788
- Kind: fix

## Discovery
### value_check
1. `platform-adapter.py` 中 `get_assignees()` 和 `set_assignee()` 对 Gitee 平台使用了错误的 API 调用方式
2. 导致 `freely wt-create` 在 Gitee issue 上失败（提示 raw-issue-pull failed）
3. 本人在实际操作中验证了这个 bug —— wt-create 确实因为 Gitee assignee API 失败而回滚整个工位创建

### scope_check
- 仅修改 `docs/system/workspace/scripts/sync/platform-adapter.py`
- 3 处改动：`get_assignees`(Gitee), `set_assignee`(Gitee), `pull_raw_issue`(错误分级)

## Problem
`gitee-issue.py` 使用 CLI 子命令模式（get/update），但 `platform-adapter.py` 试图用 REST 动词（GET/PATCH）调用，导致参数不兼容。

## Brainstorm

### Option A: 修改 gitee-issue.py 支持 REST 动词
- 优点：保持 platform-adapter.py 的统一调用风格
- 缺点：gitee-issue.py 已有稳定的 CLI 子命令模式，改动风险大

### Option B: platform-adapter.py 中 Gitee 路径改用 subprocess.run ✅
- 优点：改动最小，直接用 gitee-issue.py 已有子命令
- 缺点：Gitee 和 GitHub 的调用方式不一致

### Option C: 只在 pull_raw_issue 中 catch 异常不阻塞
- 优点：最简单
- 缺点：assignee 功能完全失效，不是真修复

## Decision: Option B
理由: gitee-issue.py 的 CLI 模式是已稳定接口，改它风险大于收益。platform-adapter.py 中 Gitee 部分直接 subprocess.run 调用即可。

## Candidate
- candidate_id: C-20260707T003943Z-A
- status: promoted
- milestone: M-20260707T003943Z-A
