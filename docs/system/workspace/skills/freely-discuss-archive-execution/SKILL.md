---
name: freely-discuss-archive-execution
description: >- 讨论归档 skill。分析讨论 session、产出评论或 raw issue、记录产出 ID、
  关闭讨论。由 `freely discuss --archive` 命令通过 ACP session/prompt 触发。

  Use when: `freely discuss --archive` 命令触发归档。
  触发词："归档讨论"、"archive discussion"、"关闭讨论"。
---

# skill:freely-discuss-archive-execution

讨论 agent 接收到 ACP prompt 后加载本 skill 执行归档。

## 归档流程

### 1. 读取讨论
- 从本地 `.freely/discussions/{session-id}.jsonl` 读取全部消息
- 从 SQLite discussions 表获取元数据

### 2. 分析
- 归并所有 @raw-{key} 引用
- 对每个涉及的 open raw issue，提取相关讨论内容
- 判断：适合作为评论插入已有 issue，还是需要创建新 raw issue

### 3. 产出
- 适合已有 issue → `freely comment --issue raw-{key} <内容>`
- 不适合 → `freely feedback --title "..." --body "..."` 创建新 raw issue
- 可创建多个 raw issue

### 4. 记录
- 插入最后一条讨论消息（JSONL），记录所有产出 ID：
  ```json
  {"author":"discuss_01","body":"归档完成","refs":[],"created_at":"...","consumed":0,
   "archive_output":{"comments":[{"issue":"raw-xxx","platform":"github"}],
   "raw_issues":["raw-yyy","raw-zzz"]}}
  ```

### 5. 标记
- 标记 session 每条消息 consumed=1
- consumed=-1 表示该条消息被丢弃（无价值）

### 6. 关闭
- SQLite discussions 表 status → closed
- adapter close-discussion 关闭平台 Discussions
- 平台关闭确认后 → 移出 agent-id.env 对应条目

## 不负责
- 不自动触发（纯手工 via cmd_discuss --archive）
- 不修改讨论历史（只标记 consumed/discard）
- 不删除文件
