---
name: a2a-no-fallback
raw_key: raw-20260615T001626Z26Z
created: 2026-06-15T00:16:42Z
status: promoted
---

# 移除 A2A 文本 JSON 解析 Fallback (Phase 1+2) - Brainstorm

## 1. Discovery (发现)

### 问题来源
- 父 Epic `a2a-replace-handoff` 已完成 A2A 协议替换 Handoff 的核心实现
- 当前代码中仍然存在**双路径**：标准 `a2a-exit` 路径 + 旧的文本 JSON 解析 fallback 路径
- 双路径导致：
  - 维护成本增加（两套解析逻辑）
  - 测试负担加倍
  - 行为不一致的风险（哪个路径实际生效？）
  - 代码复杂度冗余

### 根因分析
```
a2a-exit (标准路径)      ────→   A2A Task State Machine
                               ↗
文本JSON解析 (fallback)  ────→   旧 handoff exit_kind 映射
                               ↘
                              worker-agent.md 等 prompt 文件仍需
                              维护两套指令

移除 fallback 后，全线走 a2a-exit，prompt 只需维护一套指令。
```

### 现有双路径问题

| 方面 | a2a-exit 标准路径 | 文本 JSON 解析 (fallback) |
|------|-------------------|--------------------------|
| 信号文件 | WORKERS 写入 last-exit-task.env | 旧 handoff 文件格式 |
| Prompt 指令 | 使用 a2a-exit 输出标准结构 | 输出 JSON block 供 tail+regex |
| 解析逻辑 | A2A Task 状态机驱动 | tail + regex 解析 |
| 持久化 | last-exit-task.env | last-workers-csv.txt / last-exit-kind.txt |
| 入口 | delegate_workers 等 | supervisor 循环中的旧逻辑 |

## 2. Research (研究)

### 涉及的组件

1. **`a2a_task.py`** - WORKERS 字段写入逻辑需要修复，确保 a2a-exit 正确写入到 last-exit-task.env
2. **Prompt 文件** - 所有 prompt 文件（manager-agent.md, worker-agent.md, 系统 prompt, repair prompt, delta prompt）需要从 JSON block 指令迁移到 a2a-exit 指令
3. **`parse_a2a_task_json_reply`** - 核心的文本解析函数，需要删除 tail+regex 路径
4. **持久化文件** - `last-workers-csv.txt`/`last-exit-kind.txt` 需要删除
5. **`a2a_task_parser.py`** - 文件级 parser 需要废弃或加 env guard
6. **Worker handoff** - 需要改用 DB 查询替代文本 extract

### Phase 1+2 范围评估

Phase 1 (信号文件 WORKERS 字段修复):
- 修改 `a2a_task.py`，确保 a2a-exit 写入 WORKERS 到 last-exit-task.env
- 修复范围小，影响集中

Phase 2 (更新所有 Prompt):
- 涉及 6+ 个 prompt 文件
- 每个文件需要检查：a2a-exit 指令 vs JSON block 指令
- 移除 WORKER_STATE_INJECT 中的 JSON block 指令
- 需要确保 prompt 变更后，AI 输出的格式可被 a2a-exit 正确解析

### 替代方案评估

#### 方案 A: Phase 1+2 先做，观察再决定是否继续 Phase 3-6
- **范围**: 修复信号文件 + 更新 Prompt
- **优点**: 风险最低，每 Phase 可独立回退
- **缺点**: 遗留代码仍然存在，可能产生混淆

#### 方案 B: 全部 6 Phase 一次性完成
- **范围**: Phase 1-6 全部完成
- **优点**: 彻底清除所有 fallback 代码
- **缺点**: 一次性改动范围大，回退困难

#### 方案 C: 不做（保持现状）
- **优点**: 零改动风险
- **缺点**: 持续维护双路径，代码复杂度持续上升

## 3. Decision (决策)

### 推荐方案: 方案 A - Phase 1+2 先做

**理由**:
1. Phase 1+2 解决了最急迫的问题：信号文件正确性和 Prompt 指令一致性
2. 每 Phase 独立可回退 (`FREELY_A2A_TEXT_PARSING_FALLBACK=1`)
3. 改动范围可控，适合当前 feature branch 的单次提交
4. Phase 3-6 涉及代码删除和重构，适合在后续 feature 中完成

### Boundary & Non-Goals

#### In Scope (Phase 1+2)
- 修复 `a2a_task.py` 的 WORKERS 字段写入
- 更新所有 prompt 文件为 a2a-exit 指令
- 移除 prompt 中的 JSON block 指令
- 移除 WORKER_STATE_INJECT 中的 JSON block 指令

#### Out of Scope (Phase 3-6)
- 删除 `parse_a2a_task_json_reply` 的 tail+regex 路径
- 删除 `last-workers-csv.txt`/`last-exit-kind.txt` 持久化
- 废弃 `a2a_task_parser.py`
- Worker handoff 改用 DB 查询

### 关键验收
- `a2a_task.py` a2a-exit 正确写入 WORKERS 到 last-exit-task.env
- 所有 prompt 文件中无 JSON block 指令残留
- `WORKER_STATE_INJECT` 中无 JSON block 指令
- `FREELY_A2A_TEXT_PARSING_FALLBACK=1` 可恢复旧行为

### 下一步
进入 B2_IBM 阶段，产出 I-* issue 和实现设计文档。

### 结论
Phase 1+2 是消除双路径的第一步，解决了最核心的信号文件正确性和 Prompt 指令一致性问题。后续 Phase 3-6 可逐步完成全面清理。
