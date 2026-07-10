---
local_id: raw-20260623T005123Z23Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260623T005123Z-A
platform_ids:
  github:
    issue_id: '3375'
    url: https://github.com/chatterzhao/freely/issues/3375
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-23T00:51:41Z'
updated_at: '2026-06-23T00:51:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

当前项目中提及开发流程的文件存在多处不一致：

### 1. feedback 缺失
流程普遍从 `wt-create` 开始，缺少可选的 `feedback` 前置步骤。但：
- 人类/AI 从零开始时需要先 `freely feedback` 创建 raw issue
- Manager patrol 发现新任务时需要自己判断并创建 raw issue
- 收口后有遗留优化也需要新 raw issue

### 2. test 步骤缺失
`skill:freely-test-execution` 已创建，但大部分流程引用没有这步：
- dev-loop、B1_IBM、B2_IBM skill 的全链路行缺 test
- feat-execution 对比表缺 test
- fix-execution L15/L74-75/L95-96/L102 缺 test skill 引用
- AGENTS.md L25 从 B2 直接跳到 pr-create，丢了 dev 和 test

### 3. [命令]/[skill] 标记缺失
以下 skill 的全链路行没有标注类型：
- freely-dev-loop-execution L8
- freely-doc-B1_IBM-execution L8
- freely-doc-B2_IBM-execution L8

### 4. "↑ you are here" 位置错位
由于加了 test 步骤，所有箭头标注位移。应改为内联 `[本 skill 自此开始]`

### 5. 过时引用
- manager-agent.md L277 pr-create-guarded 描述仍写 `gh pr create`
- manager-agent.md skill 表缺 test-execution

## 设计

### 统一流程格式

首行为简写流程链，次行为完整调用格式：

```
feat: ([命令] feedback) → [命令] wt-create → [skill] B1 → [skill] B2 → [skill] dev → [skill] test → [命令] pr-create → [命令] pr-review → [命令] pr-merge → [命令] wt-close

     反馈: freely feedback --repo <repo> --title "<标题>" --body "<描述>"    (raw issue 不存在时需要)
     工位: wt-create --raw-key <key> --source platform --skill <skill> --slug <slug>
     B1:   skill:freely-doc-B1_IBM-execution
     B2:   skill:freely-doc-B2_IBM-execution                              [本 skill 自此开始]
     dev:  skill:freely-dev-loop-execution
     test: skill:freely-test-execution
     pr:   pr-create-guarded → pr-review-guarded → pr-merge-guarded
     收口: wt-close <branch>
```

fix 变体同理（dev→test→B1→B2 顺序不同）。

### 位置标记

旧格式：`>                                    ↑ you are here（快测沙箱策略，治理后置）`
新格式：在 skill 对应行后加 `[本 skill 自此开始]`

好处：增加或删除流程步骤不会导致箭头错位。

### feedback 表示

- 括号 `()` 表示可选（raw issue 已存在则跳过）
- 带完整参数签名：`freely feedback --repo <repo> --title "..." --body "..."`
- 注意 feedback 无 `--source` 参数（始终走 platform），无 `--project`（操作平台层）

## 涉及文件

| 文件 | 改动 |
|------|------|
| AGENTS.md | 流程加 feedback + dev + test，修正标记 |
| freely-fix-execution/SKILL.md | 流程格式统一，位置标记修正 |
| freely-feat-execution/SKILL.md | 流程格式统一，对比表加 test |
| freely-dev-loop-execution/SKILL.md | 全链路加标记+test，完成判定加 test skill |
| freely-doc-B1_IBM-execution/SKILL.md | 全链路加标记 |
| freely-doc-B2_IBM-execution/SKILL.md | 全链路加标记+test，完成自检加 test skill |
| freely-test-execution/SKILL.md | 位置标记修正 |
| three-loop-capability-lifecycle.md | flow 表格加 test gate 引用 |
| CONSTITUTION.md L111 | 流程加 test |
| manager-agent.md | skill 表加 test-execution，可用命令更新 pr-create 描述 |

## Acceptance Criteria
- 所有 10 个文件流程一致，格式统一
- feedback 作为可选前置步骤出现在所有 feat/fix 流程开头
- test skill 出现在 dev 和 pr 之间（feat）/ dev 和 B1 之间（fix）
- 所有全链路行有 [命令]/[skill] 标记
- 所有位置标记改为内联，不依赖箭头对齐
- manager-agent.md pr-create 描述不再写 gh pr create
