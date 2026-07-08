---
local_id: raw-20260708T231255Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260708T231255Z-A
platform_ids:
  github:
    issue_id: '3840'
    url: https://github.com/chatterzhao/freely/issues/3840
    synced_at: ''
  gitee:
    issue_id: IJZS1R
    url: https://gitee.com/zhaoquan/freely/issues/IJZS1R
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T23:13:16Z'
updated_at: '2026-07-08T23:13:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 目标
一次性修复 scan 所有遗留问题，全站类型测试覆盖，Manager 收到 actionable 指导。

## 当前状态
5 个 PR 增量修改已合入 develop：
- #3830: station chain + two-level delegation + batch dedup
- #3832: classify fix + parse_frontmatter + platform_state
- #3834: de-hardcode platforms
- #3837: _sync_platform_direct update→close + extract_raw_key case
- #3839: _build_sync_batch keep items visible + 7-type test

## 仍需修复
1. agent_dead 检测：查 agent-working 表获取 agent_id + session_id
2. 全站测试：9 个 detect_station 返回值全覆盖
3. next_action 质量：确保每条 actionable，Manager 能直接执行
4. 跨平台状态检测：platform-only issue 能被 scan 发现

## 测试矩阵（全部 9 站）
每种创建模拟数据 + 运行 scan + 验证分类 + 验证 next_action + 清理

## 原则
- 一个 raw issue，一个 PR，一次做完
- B1 研究完整代码路径后再写代码
- pre-tests 覆盖所有站
- GREEN 全部通过才 PR
