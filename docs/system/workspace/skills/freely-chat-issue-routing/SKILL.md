---
name: freely-chat-issue-routing
description: >-
  将 `freely chat` 命令收到的消息路由到正确的 raw issue。判断消息属于
  已有 issue（追加评论）还是需要新建 raw issue。

  Use when: `freely chat` 收到新消息需要路由判定。
  触发词："chat routing"、"路由消息"、"issue routing"、"这条消息归哪个 issue"。
loop: intake
owner: manager
supersedes: []
---

# freely-chat-issue-routing

将 `freely chat` 消息路由到正确的 issue。

## 职责

只做路由，不做价值判断。判断消息属于哪个已有 issue，还是需要新建 raw issue。

## 输入

- 用户消息文本
- `docs/B1-docs/ISSUES.md` 索引（用于快速匹配 open issue）
- 当前活跃的 issue（phase_state in {in_dev, in_verification}）

## 输出

```json
{
  "action": "new_issue" | "comment",
  "target": "<local_id>" | null,
  "label": "proposed" | "needs_research" | "forward_looking" | "reopen_candidate",
  "urgent": false,
  "reason": "简短说明路由决策理由"
}
```

## 路由规则

### 快速路径（脚本匹配，不调 AI）

1. 消息中包含明确的 issue 引用（`#123`、`raw-20260427T1030Z`、`I-20260426T0000Z-A`）
   → action=comment, target=<引用>

2. 消息长度 < 10 字符，且无实质内容
   → action=new_issue, label=proposed（B1 将判断为 dropped）

### AI 路径（语义匹配）

3. 消息内容与已有 open issue 的 title 语义相关
   → action=comment, target=<匹配的 issue>

4. 消息内容与已关闭 issue 相关
   → action=new_issue, label=reopen_candidate, 消息 body 引用关闭的 issue

5. 消息内容超前/探索性
   → action=new_issue, label=forward_looking

6. 无法判断
   → action=new_issue, label=needs_research

## 紧急判断

如果 target 指向的 issue 正在 dev-loop 中（phase_state in {in_dev, in_verification}），标记 `urgent: true`。

## 执行

路由结果返回后，由 `freely chat` 命令执行实际的写入操作：
- `action=new_issue` → 写入 `.freely/freely.db`（SQLite，不污染 protected branch），后续由 AI 创建工位时 wt-create 自动 materialize 到 `docs/B1-docs/`
- `action=comment` → 写入 `.freely/freely.db`；有对应工位时直接追加到 worktree 的 `docs/B1-docs/{target}/issue.md`

## 边界

- 不读完整的 issue.md 内容（只读 ISSUES.md 索引和 frontmatter 关键字段）
- 不做价值判断（不决定 promote/absorb/drop）
- 不做平台同步（sync 由 issue-sync 脚本异步执行）
