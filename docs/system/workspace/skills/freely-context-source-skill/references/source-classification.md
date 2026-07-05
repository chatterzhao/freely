# Source Classification

## Rules

- `source_class=discovery`
  - `PROJECT_INTENT`
  - chat / session evidence
  - human interruption
  - test
  - code-review
  - external issue
  - 治理漂移
  - 新运行时异常
- `source_class=milestone`
  - `docs/milestones.md` 中的 `candidate_issues` / `committed_issues` / `completed_issues`
- `source_class=continuation`
  - issue
  - `docs/progress/**`
  - `docs/recovery/**`
  - 系统监控命中的活跃执行上下文

## Output hints

- `discovery` 通常先去 `freely-doc-B1_IBM-execution`
- `chat_intake`（来自 freely.db 的未消费 chat）
  - 仍属于 `discovery`
  - 默认首跳：AI 判断 → 有价值的创建工位（wt-create 自动 materialize），噪声标记 consumed=-1
  - 语义：插话暂存于 SQLite，等待 AI 消费。与 `docs/B1-docs/` 中的 raw issue 不同，chat 尚未进入 IBM 生命周期
- `human interruption` 与 `external issue` 是默认 durable source families，但它们的 consumption / dedupe / closeout 规则不同，不能因为都属于 `discovery` 就混成一个来源池
- `github_raw_issue` / `gitee_raw_issue`
  - 仍属于 `discovery`
  - 默认首跳：`freely-doc-B1_IBM-execution`
  - 语义：外部原始 issue 仍未被 canonical milestone / issue linkage 消费，需要先做 intake / 预研 / 接纳或丢弃判断
- `github_linked_open_issue` / `gitee_linked_open_issue`
  - 仍属于 `discovery`，但不是 fresh intake
  - 默认首跳：先回 canonical milestone / issue / progress truth 做 drift reconcile
  - 语义：外部 issue 已有 canonical linkage，但外部面仍 open；先判断是否只是 closeout/publication 未收口，还是本地 continuation 真没做完
- `milestone` 需要再看队列和 `phase_state`
- `continuation` 需要再看 docs 完整度、`phase_state`、`runtime_state` 与恢复证据
