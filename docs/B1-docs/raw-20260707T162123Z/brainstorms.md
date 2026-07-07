---
b1_id: B1-20260707T162123Z
phase_state: completed
source_raw: raw-20260707T162123Z
source_url: https://github.com/chatterzhao/freely/issues/3813
produced_candidate: C-20260707T162123Z-A
---

# B1: close_issue/add_comment — per-platform ID + wt-close 双平台 + scan Gitee 检测

## Discovery

### value_check: P1 阻塞
当前 GitHub 0 open issue、Gitee 30 open issue——因为 close 只关了 GitHub。

### 现状分析

**issue.md 中的 platform_ids 结构（正确的）：**
```yaml
platform_ids:
  github:
    issue_id: '3813'
    url: https://github.com/...
  gitee:
    issue_id: IJZHOV
    url: https://gitee.com/...
```

**当前 close_issue API（有问题的）：**
```python
def close_issue(local_id: str, platform_issue_id: str) -> dict:
    return {h.name: h.close_issue(platform_issue_id) for h in _handlers()}
    # 传 '3813' 给 GitHub ✅，也传给 Gitee ❌（Gitee 需要 'IJZHOV'）
```

**当前 wt-close 调用（有问题的）：**
```bash
platform-adapter.py close github "$gh_id"   # 只关 GitHub，Gitee ID 不同被跳过
```

**当前 scan Gitee 检测（有问题的）：**
scan 调用 `list_open_issues()`，它遍历 handlers 调 `list_open_issues()`。
Gitee handler 的 `list_open_issues` 需要 GITEE_TOKEN + gitee-issue.py 正常工作。
但 scan 的 `platform_all_states` 返回空——可能 Gitee handler list_open_issues 有问题。

## Problem

1. `close_issue`/`add_comment` API 签名错误：接受单个 ID → 必须改为接受 platform_ids dict
2. `wt-close` 只调了 GitHub close
3. scan 没检测到 Gitee open issue

## Brainstorm

### 子问题 1：close_issue/add_comment API 怎么改

**Option A: 改为接受 platform_ids dict ✅**
```python
def close_issue(local_id: str, platform_ids: dict) -> dict:
    for h in _handlers():
        pid = platform_ids.get(h.name, {})
        issue_id = pid.get('issue_id', '') if isinstance(pid, dict) else str(pid or '')
        if issue_id:
            results[h.name] = h.close_issue(issue_id)
```
优点：调用方从 issue.md 读取 platform_ids 传入——新平台自动支持
缺点：需要改所有调用方

**Option B: close_issue 内部自己读 issue.md**
优点：调用方不变
缺点：紧耦合——违反 adapter 设计原则

**Decision: Option A** — platform_ids dict 是 issue.md 中已有的结构，调用方读一下传入即可。

### 子问题 2：wt-close 怎么关双平台

当前只关了 GitHub。改为从 issue.md 读 platform_ids → 遍历所有平台 close。

### 子问题 3：Gitee list_open_issues

当前 `list_open_issues()` 遍历 handlers，但 Gitee handler 的 list_open_issues 可能因为 token 或 API 问题返回空。需要在 B2 阶段验证。

### 子问题 4: add_comment 同样问题

`add_comment(local_id, platform_issue_id, comment_body)` 同样接受单个 ID。改为 dict。

## Decision: API 改为 platform_ids dict + wt-close 循环所有平台

## Candidate: C-20260707T162123Z-A, promoted
