# 研究：状态联动与会话证据治理

日期：2026-03-08

## 背景

Freely 最近几轮自举里已经出现三类重复问题：

1. 实际工作已经发生，但 milestone / issue / candidate 状态没有同步推进。
2. `in_progress` 同时承载 IBM 和 dev-loop，导致 AI 不知道何时该找 `progress`。
3. `session_refs` 只在 pre-brainstorm candidate 留痕，进入 issue / dev-loop / recovery 后缺少统一的会话证据字段。

## 当前症状

### 1. 状态已发生，但状态机没有一起移动

- 已有正式 IBM 产物的 issue，仍保留“继续补齐 IBM 产物”的过时下一步。
- 已写入 evidence 的 completed item 仍保留 `pending://issue-materialization`。
- 已 merge 的研究/治理工作仍停留在 `promoted` 占位态，没有明确进入 committed issue 或 completion verification。

### 2. 流程标识缺少唯一事实源

当前多个文档和技能散落使用：

- `source_class`
- `route_kind`
- `milestone_state`
- `status`
- `in_progress`
- `progress`
- `recovery`

但没有一个规范文件统一说明：

- 这些词各自代表哪个环
- 哪些字段可以共存
- 哪些状态迁移必须同步更新哪些文档

结果是 AI 工具只能靠上下文猜，而不是按规则执行。

### 3. 会话证据没有跨环传播

当前只要求在 pre-brainstorm candidate 写 `session_refs`，但没有要求：

- candidate 晋升到 milestone-owned issue 时复制会话证据
- dev-loop 开始时把当前活跃会话写入 `progress`
- recovery 时显式记录 `tool + session_id + jsonl_path`

## 收敛决定

1. 由 `docs/LAWS.md` 统一定义流程标识词典与状态联动矩阵。
2. `milestones.md` 必须区分 `loop_stage=ibm` 与 `loop_stage=dev_in_progress`，避免把 IBM 错误地绑定到 `progress`。
3. `session_refs` 使用结构化记录，最小字段：
   - `tool`
   - `session_id`
   - `jsonl_path`
   - `role`
4. 若当前 AI 工具无法暴露 jsonl 路径，允许使用 `unavailable://<reason>`，但不能省略 `session_id`。
5. skills 不再自由定义这些标识；统一引用 `LAWS` 中的规范语义。

## 建议下一跳

- 创建一个 issue-bound 治理项，绑定到当前 `workspace-routing-foundation` milestone。
- 在该 issue 中修订 `LAWS`、`PROJECT_INTENT`、`milestones.md` 与核心 skills。
