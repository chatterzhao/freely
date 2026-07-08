---
local_id: raw-20260708T225753Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3838'
    url: https://github.com/chatterzhao/freely/issues/3838
    synced_at: ''
  gitee:
    issue_id: IJZS1O
    url: https://gitee.com/zhaoquan/freely/issues/IJZS1O
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T22:58:15Z'
updated_at: '2026-07-08T22:58:15Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 目标
在测试工位模拟 scan 所有分类组合，用真实平台 issue 验证跨平台检测，发现任何分类错误就修。

## 测试矩阵
每个组合用真时间戳格式的 raw key 创建本地 issue.md，在测试工位验证：

### 本地文档分类
1. raw + phase=proposed + 无工位 + platform_state空 → raw_not_started
2. raw + phase=proposed + 无工位 + platform_state=closed → merged_develop
3. raw + phase=空 + platform_state=closed → merged_develop
4. I-* + phase=in_dev → i_non_terminal
5. I-* + phase=done_b2_ibm → i_non_terminal
6. I-* + phase=in_verification → i_non_terminal
7. raw + phase=absorbed + 无工位 → merged_develop

### 平台跨平台检测
8. 使用已有双平台 issue (#3835/IJZS1H): GitHub=CLOSED, Gitee=OPEN → scan 检测到不一致

## 修复
测试中发现任何分类错误立即修，不等到最后。

## 恢复
- 测试工位: git checkout . 丢弃所有修改
- 平台 issue: 恢复到测试前状态(CLOSED→reopen)
