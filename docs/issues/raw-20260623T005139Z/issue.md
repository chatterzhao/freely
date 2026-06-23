---
local_id: raw-20260623T005139Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260623T005139Z-A
platform_ids:
  github:
    issue_id: '3376'
    url: https://github.com/chatterzhao/freely/issues/3376
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-23T00:51:56Z'
updated_at: '2026-06-23T00:51:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

### 1. wt-create --source 接受三种值但实际只应用一种

当前 `--source` 接受 `platform`、`chat-inbox`、`local`：

```bash
# wt-create L153
echo "Invalid --source '$source_val'. Must be 'chat-inbox', 'platform', or 'local'." >&2
```

但 `chat-inbox` 和 `local` 有问题：
- **chat-inbox**: chat 消息直接创建 raw issue，绕过 feedback，不经过平台。违反"所有 raw issue 必须在平台"的原则
- **local**: 纯本地 issue，无平台对应。与治理模型冲突
- 唯一正确的路径：`freely feedback` 创建平台 issue → `wt-create --source platform`

### 2. chat --new-issue 应走 feedback

当前 chat 的 `--new-issue` 路径建议 `wt-create --raw-key <id> --source chat-inbox`。应改为：先调 `freely feedback` 创建平台 issue，再 `wt-create --source platform`。

### 3. Manager 缺少 feedback 能力

Manager Tool Policy 未列出 `freely feedback`。Manager 需要在以下场景自行判断并创建：
- scan next_action = `[manager] freely feedback`（已有，但 Tool Policy 未体现）
- Worker 完成但有遗留 → 判断"这需要新 raw issue" → feedback
- 收口后发现遗漏/优化点 → feedback

### 4. manager-agent.md 可用命令表过时

L277: `pr-create-guarded` 描述仍写 `push→gh pr create`，应改为 platform-adapter

## 设计

### wt-create --source 简化

```bash
# 只接受 platform
case "$source_val" in
  platform) ;;
  *) echo "Invalid --source . Must be platform." >&2; exit 1 ;;
esac
```

chat-inbox 迁移路径：chat --new-issue → freely feedback → wt-create --source platform

### chat intake 修改

`cmd_chat` / `submit_human_frontdoor_message` 中 `--new-issue` 路径：
- 旧：建议 `wt-create --raw-key <id> --source chat-inbox`
- 新：自动调 `freely feedback --repo <repo> --title "..." --body "..."`，拿到 raw_key 后建议 `wt-create --raw-key <key> --source platform`

### Manager Tool Policy 更新

在允许的读写 Bash 命令中增加：

```
| `freely feedback --repo <repo> --title "..." --body "..."` | 创建新 raw issue | scan 发现新需求、Worker 完成有遗留、崩溃自愈 |
```

在 patrol 步骤 2（消费已完成的 Worker）中增加显式判断：
- "有遗留 → 判断是否需要新 raw issue → `freely feedback` → 新 raw_key 进入 scan"

在 manager-agent.md 可用命令表中：
- 修正 pr-create-guarded 描述：`push→platform-adapter create-pr`
- 修正 pr-merge-guarded 描述：`push→platform-adapter close-pr`

## 涉及文件

| 文件 | 改动 |
|------|------|
| wt-create | --source 校验改为只接受 platform |
| freely (cmd_chat, chat intake) | --new-issue 改为走 feedback |
| freely (usage) | wt-create --help 更新 source 说明 |
| manager-agent.md | Tool Policy 加 feedback，可用命令表修正 |
| worker-agent.md | Tool Policy 加 feedback（如 worker 需要评估新问题） |

## Acceptance Criteria
- wt-create --source 只接受 platform
- chat --new-issue 建议走 freely feedback
- Manager Tool Policy 明确列出 freely feedback
- manager-agent.md 命令描述不再引用 gh pr create
