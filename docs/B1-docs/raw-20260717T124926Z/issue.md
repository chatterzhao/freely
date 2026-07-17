---
local_id: raw-20260717T124926Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T124926Z-A
platform_ids:
  github:
    issue_id: '3979'
    url: https://github.com/chatterzhao/freely/issues/3979
    synced_at: ''
  gitee:
    issue_id: IK1TPZ
    url: https://gitee.com/zhaoquan/freely/issues/IK1TPZ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T12:49:54Z'
updated_at: '2026-07-17T12:49:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 目标
wt-close 面向 agent 自治：不需要人类 `--force --reason` 话术,用机器可验证的判定链路替代。不丢任何既有收口功能（平台 close/远程分支删除/worktree remove/branch delete/agent_working release/Phase 4.5 worker cleanup）。

## 重构点（按 2026-07-17 排查的六个设计缺陷,保留功能→换判定语义）

### 1. 入口门禁改为自治判定（替代当前 ownership_guard 的人类 --force --reason 话术）

当前：未完成/异主 → 要求人类 `--force --reason`。
改为：
- **自有关闭（FREELY_AGENT_RAW_KEY 匹配目标 key）**：
  未完成但满足以下全部条件 → 允许关闭（该 key 确无进行中工作）:
  (a) agent_working 无该 raw_key 的活跃 worker_id/reviewer_id（无被派署 agent）
  (b) a2a_tasks 无 working/submitted/launched 状态的 task
  不满足 → 拒绝，输出 machine-readable"阻塞原因"使 agent 能决策下一步（如走 a2a-exit --state completed 收工后再关）
- **非自有关闭（FREELY_AGENT_RAW_KEY 不匹配或不设）**：
  允许的条件：目标 key 已完成（有 merge 证据）或已 dropped → 这是"收尾已合并 items"场景（如 scan 驱动的 platform-sync 收敛）。
  不允许的条件：目标 key 非完成且非自属 → 拒绝。runtime 需要 batch-reconcile 通道关闭非自有且已完成的 key（独立能力,不靠 wt-close 硬越权）
- **人类 --force --reason 保留**：仅用于"确定放弃"的例外场景,语义不变,不新增豁免面

### 2. 活跃 worker 从「查到就杀」改为「先收工后关闭」（Phase 4.5 前移为 Phase 0.5）

当前：查到活跃 worker → 发 shutdown 提示等 10s → 不等你反应直接 kill -9 → 继续删工位。
改为：查到活跃 worker → A2A session/prompt 发"此工位即将关闭,请 a2a-exit --state completed" →
等待 worker 自行完成并退出（可配等待上限,默认 120s）→ polling task state → 
(a) worker 按时 completed → 继续关闭
(b) worker 超时未完成 → 降级为"通知 manager 该 raw_key 的 worker 超时,manager 决策是否 force-close"
(c) --force 时仍走当前 kill-and-continue 路径（不丢功能）

### 3. agent_working 前置查询

当前：agent_working 只在关闭后释放。
改为：关闭前查询 agent_working——
(a) 若该 raw_key 有 reviewer_id（审查中）→ 拒绝关闭（审查未完成,或 reviewer 先 a2a-exit）
(b) 若该 raw_key 有 worker_id 但 a2a_tasks 无对应活跃 task → 允许（已僵尸）
(c) 合并到门禁判定（见 1）

### 4. test 工位 --force 删除至少 warn（不丢功能但补可观测）

当前：`git worktree remove --force "$_tp_wt" 2>/dev/null || true` 静默丢弃未提交测试证据。
改为：force 前检查 test 工位是否有未跟踪文件（`git status --porcelain`），有则 emit warning event + 日志行（不拦截关闭,不丢自动能力）

### 5. 分支匹配消歧

`_resolve_branch_from_raw_key` 用 `head -1` 取第一条,同名 raw 不同 slug 有杀错风险。
改为：若匹配到多条分支 → 取 namespace 匹配度最高的(优先 fix/raw-{key}-{same-slug}),多条同级同名 → 拒绝并要求显式传 branch 名。一条时才直接返回。

## 不丢功能清单（必须保留）
- 平台 issue close（Phase 1-3）
- 远程分支删除（Phase 4）
- worker 安全下线并 force-kill 兜底（Phase 4.5 — 前移但保留 kill 路径给 --force）
- agent_working 释放（Phase 5）
- worktree remove + branch delete
- --platform-only（只关平台不动工位）
- consistency check（dev↔test 一致性）
