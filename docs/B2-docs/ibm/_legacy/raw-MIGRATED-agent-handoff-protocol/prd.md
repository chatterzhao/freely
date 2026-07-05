# PRD: Agent Handoff Protocol v2

## Goal

将 handoffs 表从 AI 直接调用 CLI（`handoff.py update`/`insert`）的碎片化管道，重构为 **AI→JSON→Runtime** 的统一协议。消除 #343 暴露的分步不一致问题（validator 读 worker_prompts_csv，launcher 读 pending worker——两个读者读两个数据源），同时补全协议设计缺失的线程模型、消费状态机、多轮会话连续性。

## Motivation

当前 handoffs 表已投入使用（manager 125 条、worker 301 条），但：
- 5 个原因字段语义重叠（stop_reason / why_not_stop / why_not_delegate / blocked_reason / handoff_reason）
- parent_handoff_id 有字段但 Runtime 从不写入
- consumed_by 有字段但完全未使用
- 无 thread_id / previous_worker_handoff_id 串联多轮对话
- WORKER_HANDOFF_INJECT 只注入自己的 handoff_id，不注入父记录和前任上下文
- AI 分步执行 CLI 命令（Step B update + Step C insert），Runtime 分步验证——两个读者读两个独立数据源

## Dev-Loop Handoff

以下 6 个文件的改动构成完整实现，按依赖顺序：

1. **`handoff.py`** — 表结构 + CRUD + parse 子命令（无上游依赖）
2. **`freely-agent-manager.md`** — Agent doc 更新（依赖 handoff.py 的 JSON 格式定义）
3. **`freely-agent-worker.md`** — Agent doc 更新（同上）
4. **`freely`** — `build_prompt` + `WORKER_HANDOFF_INJECT`（依赖 agent docs）
5. **`freely`** — exit contract handler → consume_* 方法（依赖 handoff.py parse）
6. **`freely`** — scan 过滤 + session fork/prompt 判断（依赖 consume_delegate_workers）

每个文件改动后可通过 pre-tests.md 的对应断言独立验证。

## Non-Goals

- 不修改 ACP bridge（`start-lead-agent.sh`）
- 不修改 fleet supervision / scan 生成逻辑本身
- 不修改 `wt-close` / worktree 生命周期
- 不引入新的 IPC 机制（JSON 块通过现有 AI reply 文本传输）
