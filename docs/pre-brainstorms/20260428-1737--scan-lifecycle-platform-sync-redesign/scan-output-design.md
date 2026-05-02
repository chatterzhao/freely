# Scan 输出设计

## 核心原则

**完成的不记，只记没完成的。一个 raw → 多个 I-* 为一个对象，children 数组列出所有子任务。**

## 输出结构

```json
{
  "key": "20260428-1737",
  "raw_id": "raw-20260428-1737",
  "stage": "promoting",
  "title": "issue 生命周期与 scan 梳理重构",
  "children": [
    {"id": "I-20260428-1737-A", "phase": "in_dev", "pids": {"github": "170", "gitee": "IJFOXX"}},
    {"id": "I-20260428-1737-B", "phase": null, "pids": {}},
    {"id": "I-20260428-1737-C", "phase": "completed", "pids": {"github": "172", "gitee": "IJFOZZ"}}
  ],
  "incomplete": [
    "child_B_not_promoted",
    "raw_still_open_on_github",
    "child_C_gitee_not_closed"
  ],
  "next_action": "promote B → I-B; close raw on platforms; close C gitee",
  "ready": false
}
```

## Completion Checklist（逐 child 检查 + raw 检查）

```
for each raw→children group:
  raw checks:
    □ status is absorbed or dropped（所有 C promote 完毕）
    □ platform raw issue closed on GitHub
    □ platform raw issue closed on Gitee

  for each child I-*:
    □ created locally（issue.md 存在）
    □ created on GitHub（platform_ids.github 有值）
    □ created on Gitee（platform_ids.gitee 有值）
    □ phase_state is "completed"
    □ GitHub issue closed
    □ Gitee issue closed
    □ all local comments have platform_ids（已同步）
    □ no unresolved comments（status=pending）

  if raw.吸收到其他 I-*（absorbed_into 指向不同 key）:
    → 合并到那个 key 的 children 中
```

## Stage 判定

```
if raw 存在, 无 B1 目录 → B1_proposed
elif B1 存在, 无 candidates → B1_brainstorming
elif candidates 存在, 有未 promote → promoting（部分 or 全部）
elif 有 children 在 active phases → B2_active
elif 有 children 在 verification → B2_verifying
elif 有 children phase=completed 但平台未关 → 收口中
else → 未知
```

## 与 AI 的交互

```
scan 输出 → lead-agent 读取:
  1. 按 stage 分组: B1_* > promoting > B2_active > 收口中
  2. 同组按 ready 排序（ready=true 优先委派 worker）
  3. next_action 是脚本给出的建议，AI 可在理解上下文后调整
  4. scan 不替代 AI 判断——只是告诉 AI "这一项在这一步卡住了"
```
