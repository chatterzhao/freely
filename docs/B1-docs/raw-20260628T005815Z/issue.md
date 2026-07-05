---
local_id: raw-20260628T005815Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260628T005815Z-A
platform_ids:
  github:
    issue_id: '3601'
    url: https://github.com/chatterzhao/freely/issues/3601
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-28T00:58:36Z'
updated_at: '2026-06-28T17:43:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 概述

将旧的 freely chat 一分为二：评论（comment）和讨论（discuss），加上讨论导出技能。

## 一、评论 — 独立平台直写

### 命令
- freely comment --issue raw-{key} <原文>
- freely comment --issue raw-{key} --file <path>

### 行为
- adapter 并行写所有平台（GitHub + Gitee + GitCode），本地不留
- 成功后查 agent-id.env → 活跃工位 → ACP session/prompt 通知
- close 的 issue 提示用 --reopen 先打开
- I-* issue 不碰（I-* 内部维护）
- 处理状态用子评论 resolution：adopted/discarded

### 门禁
- pr-create-guarded / wt-close Phase 0：全平台扫描，有未处理评论 → 拦截
- 跨平台同步：SHA256 去重 → 补建 → 内容不同则 AI 语义合并

### 旧 chat 中的对应
- freely chat --issue <id> <msg> → 替换为 freely comment

## 二、讨论 — AI 群聊 + 平台同步

### Agent
- 讨论 agent，选 .ai-auth slot = 选模型
- 使用新 skill：讨论头脑风暴（借鉴 B1 发散→收敛框架，独立重建，B1 不动）

### 命令
- freely discuss                    新建 session + 创建平台讨论
- freely discuss --continue <id>    继续未关闭的 session
- freely discuss --export <id>      手工调导出 skill

### 群聊模型
- @raw-{key}、@raw-{key}#comment-{id}、@discussion-{id}、@discussion-{id}#{sub-id}
- 时间线：owner + 每条消息/回复的创建者
- 元数据记录各平台 discussion_id（Gitee 跳过，无 Discussions）

### 存储与同步
- 本地 freely.db（私有）+ 平台 Discussions（公开）
- webhook 优先，无则轮询，其他人平台回复 → sync 到本地

### 旧 chat 中的对应
- freely chat --conversation → 替换为 freely discuss

## 三、讨论导出 Skill

### 名字：freely-discuss-to-output

### 触发：freely discuss --export <session-id>（纯手工，不自动调用）

### 输入：本地 freely.db 的 session id

### 逻辑
1. 读取全部消息 → 归并 @raw-{key} 引用
2. 适合插入已有 open raw issue → 生成评论草稿 → 调 freely comment
3. 不适合 → 判断创建几个 raw issue → 调 freely feedback
4. 标记 session 消息 consumed/discard
5. 综合摘要写回 session

## 四、不纳入
- 旧的 freely chat --new-issue 自动调 feedback（之前已创建独立 issue）
- wt-create assignee 重构（已创建独立 issue）
- B1/B2 模板修复（已创建独立 issue）
- 旧 chat-inbox 本地物化路径清理（关联 chat 重构）
