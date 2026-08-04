---
name: freely-worktree-hygiene-supervision
description: >-
  当 worktree 进入 checkpoint 预警、dirty-budget 漂移或提交边界失控时，
  指导 manager/worker 做 continuity、验证、原子提交或分流。

  Use when: worktree 状态异常需要卫生检查和处理。
  触发词："hygiene"、"卫生检查"、"dirty"、"checkpoint"、"提交边界"。
---

# skill:freely-worktree-hygiene-supervision

## 何时使用

- `checkpoint_required=true`
- dirty entries 已进入 warn/block 阈值
- 同一工位连续多轮仍未做 checkpoint commit / review / cleanup
- manager 需要决定是否委派专门的 hygiene 收口

## Worker 流程

1. 先读当前 worktree 的 hygiene 信号。
   - `freely checkpoint-guard`
   - `freely baseline-status --project <current-worktree>`

2. 若已达到最小验证门：
   - 先更新 issue / continuity artifact
   - 先切原子 checkpoint commit
   - 再继续下一批

3. 若改动混杂：
   - 优先按 ownership 拆分
   - 把无关实现分流到新 feature worktree

4. 若尚未达到最小验证门：
   - 先补最小验证
   - 再收口，不继续横向扩 scope

## Manager 流程

1. 读取项目级 hygiene 告警：
   - `freely wt-fleet-status`
   - `freely fleet-status --project <develop>`

2. 判断 owner：
   - 单工位局部收口：`worker-owned`
   - 需要分流/冻结/清理：`manager-owned`
   - 进程退出、切号、等待：`runtime-owned`

3. 给出清晰 handoff：
   - 目标 worktree
   - 目标 issue
   - `next_action=delegate_hygiene_worker|freeze|cleanup`

## 边界

- 不替代 `checkpoint-guard` 的阈值判定
- 不替代 runtime 的切号、sleep/recheck、进程重启
- 不要求机械提交；目标是把坏批次收成可回滚的原子边界
