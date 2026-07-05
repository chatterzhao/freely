# 研究：阶段前缀式进度标识

日期：2026-03-08 16:30 UTC

## 背景

用户反馈当前 `in_progress` / `active` 这类状态词不够好用：

1. 看到“正在进行”并不知道是在 IBM 还是 dev-loop。
2. 需要再结合 `loop_stage` 才能理解真实阶段。
3. 状态词对 AI 和人类都不够自解释，容易继续回到“靠上下文猜”。

本轮研究目标不是简单改名，而是回答一个更硬的问题：

- 进度标识是否应该在单个值里同时表达“是否开始/进行/完成”与“处于哪个阶段”？

## 现状问题

当前模型分散在多个字段：

| 字段 | 语义 | 当前问题 |
|------|------|----------|
| `status` | 泛化状态 | 常见值如 `in_progress`、`completed` 缺阶段信息 |
| `loop_stage` | 阶段 | 能表达阶段，但不能一眼看出“未开始/进行中/已完成” |
| `milestone_state` | milestone 归属 | 又出现 `in_progress`、`completed`，和 issue / dev 语义重叠 |
| `runtime_state` | 运行会话状态 | 正确独立，但常被误当作执行阶段补丁 |

结果是：

```yaml
status: in_progress
loop_stage: ibm
```

需要同时读两个字段才能回答“它现在到底处于什么阶段”。

## 用户提出的方向

用户提出一个重要约束：

- 如果是进行中，应该用 `in_` 开头
- 如果是没开始，或者完成，也应该有统一的状态词前缀
- 从标识本身就能知道在哪个阶段，而不是只看到 `in_progress`

这意味着单纯把 `in_progress` 改为 `active` 没有解决问题，只是换了一个不带阶段信息的词。

## 候选方案

### 方案 A：保留当前拆分模型，只改名

示例：

```yaml
status: active
loop_stage: ibm
```

优点：
- 改动小
- 不影响现有 `loop_stage`

缺点：
- 主问题没有解决
- 仍然需要同时看两个字段
- `active` 仍然不知道是在 `ibm` 还是 `dev`

结论：不采纳。

### 方案 B：把阶段写进进行中状态

示例：

```yaml
status: in_ibm
status: in_dev
status: done_dev
```

优点：
- 阶段信息进入状态值本身
- 比 `in_progress` 更自解释

缺点：
- 如果只是临时枚举几个值，容易失控
- 没有明确的状态语法，后续会继续发明 `ready_for_dev`、`completed_dev`、`dev_done` 这类变体

结论：方向是对的，但需要升级成一套正式语法，而不是零散改名。

### 方案 C：采用“前缀 + 阶段名”的规范语法

新增一个规范字段，例如 `phase_state`，以单个值表达当前执行进度。

语法：

```text
phase_state := <prefix>_<stage>
```

其中：

- `prefix` 表达进度状态
- `stage` 表达所处阶段

建议前缀：

- `todo_`：尚未开始该阶段
- `in_`：正在执行该阶段
- `blocked_`：卡在该阶段
- `done_`：该阶段工作已完成，等待进入下一阶段或已完成交接

建议阶段：

- `pre_brainstorm`
- `ibm`
- `dev`
- `verification`
- `recovery`

示例：

```yaml
phase_state: todo_ibm
phase_state: in_ibm
phase_state: done_ibm
phase_state: todo_dev
phase_state: in_dev
phase_state: blocked_dev
phase_state: in_recovery
phase_state: completed
```

优点：
- 从一个值同时知道“进度”和“阶段”
- `in_` / `todo_` / `done_` 满足用户希望的统一前缀语义
- 机器可解析，人类可直读
- 可以约束允许值，不会无限扩张

缺点：
- 需要明确哪些组合有效，不能笛卡尔积放开
- 需要重新梳理现有 `loop_stage` / `status` / `milestone_state` 的职责

结论：推荐。

## 关键设计判断

### 1. 主进度标识应采用阶段前缀语法

如果目标是“看到标识就知道在什么阶段”，那主进度标识就不该继续使用 `in_progress` / `active`。

应改成：

- `todo_ibm`
- `in_ibm`
- `done_ibm`
- `todo_dev`
- `in_dev`
- `blocked_dev`

这样读到值本身就知道当前环节。

### 2. 不应继续让 milestone 归属字段承载执行阶段

即使采用阶段前缀式标识，也不建议让 `milestone_state` 继续承担阶段语义。

`milestone_state` 只应回答：

- 是否仍在 milestone 活跃范围内
- 是候选、已接纳，还是已完成归档

因此它应缩成队列归属，而不是执行进度。

建议值域：

- `candidate`
- `committed`
- `completed`

### 3. `runtime_state` 继续独立

`runtime_state` 回答的是：

- 当前 AI 会话能否 attach / resume / restart

这和“现在正在 IBM 还是 dev”不是一个维度，不能混。

### 4. `ready` 不保留，阶段交接使用 `done_*`

当前 `ready_for_dev` 是特殊短语，不符合统一前缀范式。

本轮收敛后：

- 不保留 `ready_*`
- 不采用 `todo_for_dev`
- 阶段完成统一使用 `done_*`

也就是说：

- IBM 阶段完成后使用 `done_ibm`
- 真正开始开发时切到 `in_dev`

原因：

1. `done_*` 表示“当前阶段完成，可进入下一阶段”
2. `completed` 留给整个 issue 生命周期终态
3. 不再为 handoff 额外发明第三套状态词

## 推荐模型

推荐把当前 issue / progress 的主执行标识收敛为 `phase_state`。

### 建议值域

候选有效值：

- `todo_pre_brainstorm`
- `in_pre_brainstorm`
- `done_pre_brainstorm`
- `todo_ibm`
- `in_ibm`
- `done_ibm`
- `in_dev`
- `blocked_dev`
- `in_verification`
- `in_recovery`
- `completed`

### 不建议开放的值

以下值不建议允许：

- `done_recovery`
- `blocked_ibm`
- `blocked_pre_brainstorm`
- `completed_dev`
- `ready_for_dev`
- `todo_for_dev`
- `pending_*`

原因：
- 会把“是否阶段内阻塞”与“是否需要 recovery”混成一层
- 会让词表快速膨胀
- 对路由没有额外帮助

### 配套字段

推荐保留以下职责分离：

| 字段 | 职责 |
|------|------|
| `phase_state` | 执行阶段 + 进度前缀的主标识 |
| `milestone_state` | 队列归属，不再承载执行阶段 |
| `runtime_state` | 会话续接能力 |
| `route_kind` | 下一跳路由 |

## 状态迁移草案

推荐主路径：

```text
todo_pre_brainstorm
-> in_pre_brainstorm
-> done_pre_brainstorm
-> todo_ibm
-> in_ibm
-> done_ibm
-> in_dev
-> in_verification
-> completed
```

异常路径：

```text
in_dev -> blocked_dev
blocked_dev -> in_recovery
in_recovery -> in_dev
```

## 分视角互评

### Reviewer A：命名与可读性视角

结论：

1. `in_` / `todo_` / `done_` 前缀是好方向，因为一眼可扫描。
2. 阶段必须紧跟在前缀后面，避免 `in_progress` 这类无阶段信息词。
3. `done_ibm` 比 `ready_for_dev` 或 `todo_for_dev` 更规范，因为它遵守同一语法。

风险提示：

- 如果允许 `dev_done`、`ibm_completed`、`ready_dev` 等同义写法，体系会再次失控。
- 必须强制只有一种语法。

### Reviewer B：治理与路由稳定性视角

结论：

1. 阶段前缀式标识可以减少规则判断分叉，适合让 AI 直接按字符串路由。
2. 但不能把 milestone 归属、执行阶段、runtime 续接能力合并成一个超级状态。
3. 如果 `phase_state` 成为唯一执行标识，则 `milestone_state` 必须缩到队列归属，不再出现 `in_progress`。

风险提示：

- 若直接把 `phase_state` 套到 milestone completed queue 而不保留 `milestone_state`，会失去“队列归属”这一层治理语义。
- `done_ibm` 和 `ready_for_dev` / `todo_for_dev` 不能并存，否则 handoff 判断会变模糊；必须选一个做唯一事实源。

### 互评收敛

两轮视角的共同结论：

1. 用户要求是合理的，主进度标识应包含阶段信息。
2. `active` / `in_progress` 不应继续作为主执行标识。
3. 最合理的落地方向是：采用 `phase_state=<prefix>_<stage>`，并把 `milestone_state` 降级为纯队列语义。
4. 阶段前缀固定为 `todo / in / done / blocked`，而 `completed` 只保留为整个 issue 生命周期终态。
5. `done_ibm` 应作为 `ready_for_dev` / `todo_for_dev` 的替代，不再继续保留例外命名。

## 建议下一跳

1. 在 issue-bound 治理项中提出字段迁移方案：
   - `status` 退出 issue 主状态职责
   - `loop_stage` 迁移或合并到 `phase_state`
   - `milestone_state` 收缩到队列归属
2. 先在 `LAWS` 中定义唯一词典、阶段流转图和允许值，再迁移 `milestones.md`、issue 模板与 skills。
3. 阶段 handoff 使用 `done_*`，不再保留 `ready_*` / `todo_for_*` 这类例外命名。

## 本轮收口结论

1. 主进度前缀不采用 `pending`。
2. 未开始但可直接推进的阶段统一使用 `todo_`。
3. 若需要表达“等待外部条件”，不新增 `pending_*`，而由 `blocked_*` 或独立依赖字段表达。
4. 阶段前缀固定为 `todo_`、`in_`、`done_`、`blocked_`；`completed` 只用于整个 issue 生命周期终态。
5. 本候选项进入正式 issue，继续在 milestone-owned IBM 中收敛字段迁移方案与状态图。
