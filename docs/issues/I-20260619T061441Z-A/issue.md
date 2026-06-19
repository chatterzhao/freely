---
local_id: I-20260619T061441Z-A
kind: i_issue
phase_state: completed
verification_artifact_dir: docs/pre-brainstorms/20260619T061441Z--a2a-exit-role-vs-agent-id/
platform_ids: {}
primary_platform: local
canonical_issue_path: docs/issues/I-20260619T061441Z-A/issue.md
source_candidate: docs/pre-brainstorms/20260619T061441Z--a2a-exit-role-vs-agent-id/candidates.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T06:20:00Z'
updated_at: '2026-06-19T06:20:00Z'
intake_id: ''
author: fix-execution
channel: ''
session_refs: []
raw_ref: raw-20260619T061441Z
---

# I-20260619T061441Z-A: a2a-exit --role vs --agent-id 参数不匹配修复

## 所属 Raw Issue
- raw-20260619T061441Z
- GitHub: https://github.com/chatterzhao/freely/issues/3036

## 影响
- Worker 委派链路完全中断：Manager 使用 `--agent-id worker` → task 创建为 agent_id=manager → Runtime 无法发现
- config_bool_enabled 函数名重复导致 slot 切换/工具恢复/代理配置等保护逻辑静默失败

## 修复内容

### 代码修复
1. `docs/system/workspace/agents/manager-agent.md`: `--agent-id worker` → `--role worker` (4 处)
2. `docs/system/workspace/a2a/acp-a2a-architecture.md`: `--agent-id=worker` → `--role=worker` (2 处)
3. `docs/system/workspace/scripts/runtime/a2a_task.py`: a2a-exit handler 添加 `--agent-id` → `--role` fallback
4. `docs/system/workspace/scripts/runtime/freely`: `config_bool_enabled()` 函数名修复

### 文档更新
5. `docs/system/workspace/three-loop-capability-lifecycle.md`: A2A 接口约定 + worker 状态机 + 数据流
6. `docs/system/workspace/three-loop-trace-contract.md`: §11 检查点注册 + A2A launch 事件
7. `docs/system/workspace/three-loop-lifecycle.svg`: Runtime Task Launcher 组件 + 接口陷阱标注

## B1_IBM
- brainstorms: docs/pre-brainstorms/20260619T061441Z--a2a-exit-role-vs-agent-id/brainstorms.md
- candidates: docs/pre-brainstorms/20260619T061441Z--a2a-exit-role-vs-agent-id/candidates.md
- decision: promote (方案 B)

## 验证
- [x] config_bool_enabled 函数名修复验证通过（bash -c 直接调用，true/false/1/0 返回正确）
- [x] a2a-exit --role worker 正确创建 task（argument parsing 逻辑验证）
- [x] a2a-exit --agent-id worker 向后兼容（fallback mapping 正确）
- [x] build 完整性确认：4 文件修改 + 3 文档更新 + 3 B1/B2 artifacts

### Verification Artifact
- brainstorms: docs/pre-brainstorms/20260619T061441Z--a2a-exit-role-vs-agent-id/brainstorms.md
- candidates: docs/pre-brainstorms/20260619T061441Z--a2a-exit-role-vs-agent-id/candidates.md
- test results: config_bool_enabled() unit test passed in test-pre-merge environment
- backward compat: a2a-exit handler fallback logic validated
