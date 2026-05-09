# Brainstorm: Worker Prompt 保护工位阻塞

- 来源: raw-20260508T225041Z (#261)
- 日期: 2026-05-08，基于实际运行 7 小时数据
- 范围: 阻塞问题（缓存命中问题见 #263）

## 阻塞现象

daemon 运行 7 小时，生成 17 个 worker prompt，0 个执行成功。20+ 次 restart storm。

## 阻塞根因

Worker prompt 的 `Worktree:` 字段指向 `test-pre-merge-*`（保护分支），但 prompt 没有告诉 AI：

1. 当前工位是否可写
2. 对应的可写工位在哪（wt-create 创建的配对工位）
3. 如果不可写，应该如何操作

AI 在 cycle log 中已诊断出问题（`WORKER_PROMPTS_NOT_LAUNCHABLE`），但不知道配对工位路径。

**死循环路径**：

```
manager patrol → 生成 worker prompt（target: test-pre-merge）
  → runtime 尝试 launch → WORKER_PROMPTS_NOT_LAUNCHABLE
    → AI 报告错误 → end_turn → claude-agent-acp 退出
      → bridge 重启 → daemon 再次 patrol
        → 再次生成 worker prompt → 再次失败 → 循环
```

## 正常 vs 异常 Storm

### 正常 restart（不应计为 storm）

- AI 完成一轮工作后正常退出（`end_turn`，有产出）
- bridge 重启 server 准备下一轮
- 间隔 > 30s

### 异常 storm（应该计为 storm）

- AI 启动后 5 秒内退出（无产出）
- 连续 3+ 次/30s
- 当前 case：WORKER_PROMPTS_NOT_LAUNCHABLE 导致快速退出

## 阻塞原因总结

**唯一阻塞原因**：Worker prompt 生成时没有包含配对可写工位信息。

wt-create 创建的是配对工位：
- `test-pre-merge-{key}-{slug}` + `fix/raw-{key}-{slug}`（fix-execution）
- `test-pre-merge-{key}-{slug}` + `feature/raw-{key}-{slug}`（feat-execution）

但 prompt 生成代码（freely L9518-9522）只写入了 test-pre-merge 路径，没有：
1. 检查目标工位是否可写
2. 查找配对可写工位
3. 在 prompt 中写入 cd 路径

## 工位写规则

| Skill | test-pre-merge | fix/feature |
|-------|---------------|-------------|
| fix-execution | 可临时修改测试（dirty only，不 commit） | 正式提交 |
| feat-execution | 不可修改 | 所有开发+提交 |

## Decision

### 本 issue 修复

在 worker prompt 生成代码（freely L9518 附近）加入：
1. 检查 `$primary_branch` 是否为 `test-pre-merge-*`
2. 如果是，通过 `git worktree list --porcelain` 查找包含相同 raw-key 的 `fix/*` 或 `feature/*` 分支
3. 在 prompt 中明确写入配对可写工位路径和写规则

### 不做（本 issue）

- 不修改 storm 阈值
- 不修改 `claude-agent-acp` 行为
- 不处理缓存命中问题（见 #263）
- 不改变 worker prompt 的整体生成架构

## 后续相关 issue

- #263: ACP session cache 命中率 0%
- worker 在 fix/feature 自动 cd（runtime 层改进）
- storm 检测区分正常/异常退出
