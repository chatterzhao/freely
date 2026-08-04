# Design — command lifecycle state contract

- issue_id: `I-20260721T223133Z-A`
- source_raw: `raw-20260721T223133Z`
- status: approved_for_red

## 1. 设计原则

所有生命周期命令遵循同一结构：

```text
observe → normalize → validate → plan transition → execute adapter effects → commit metadata → aggregate
```

任何命令不得通过“某个键存在”推断状态，也不得在外部副作用失败时提前提交本地终态。

## 2. 模块关系

```text
raw_metadata_contract
  ├─ schema/defaults/order
  ├─ parse legacy or strict-v1
  ├─ validate semantic invariants
  ├─ transition(current, event, payload)
  └─ atomic serialize

platform_adapter_registry
  ├─ configured platforms
  ├─ observe remote branch
  ├─ controlled push
  └─ ensure PR(create|reuse|update)

lifecycle commands
  ├─ feedback/raw-issue-pull
  ├─ wt-create/promotion/closeout
  └─ pr-create/pr-review/pr-merge
```

共享模块是唯一规则真源；Shell 入口只编排，不复制字段列表和五态分类。

## 3. raw metadata DSL

### 初始 payload

```text
new_raw(local_id, platforms, primary, timestamps, source)
  = schema=v1
  + phase(proposed, absorbed_into='', canonical='')
  + platform(open, ids=platforms)
  + promotion(children=[], source_candidate='')
  + terminal(completed_at='', closeout_note='')
  + sync(empty)
  + provenance(source)
```

### 事件

```text
transition(raw, worktree_created)
  = raw                         # 生命周期不变

transition(raw, promotion_started(issue_id, source_candidate?))
  = require raw.phase == proposed
  → append issue_id to promoted_children
  → optionally record source_candidate
  → updated_at=now

transition(raw, promotion_finalized(issue_id, issue_path))
  = require raw.phase == proposed
  → require issue_id in promoted_children
  → phase=absorbed
  → absorbed_into=issue_id
  → canonical_issue_path=issue_path
  → completed_at=now
  → updated_at=now

transition(raw, dropped(reason))
  = require raw.phase == proposed
  → phase=dropped
  → completed_at=now
  → closeout_note=reason
  → updated_at=now

transition(raw, platform_closed(at))
  = require raw.phase in {absorbed, dropped}
  → platform_state=closed
  → updated_at=at
```

序列化必须保留固定顶层字段顺序；`platform_ids` 内平台顺序按 registry 配置顺序稳定输出。

### 最终字段合同与历史依据

最终合同固定为 21 个字段，顺序以 `RAW_METADATA_FIELDS` 为唯一真源。历史证据确认：

- `promoted_children` 与 `source_candidate` 属于两阶段、1:N promotion。
- `completed_at` 与 `closeout_note` 是已有 raw 终态字段。
- `closeout_reason`、`closed_at`、`force_closed_*` 没有稳定 writer/reader 证据，不进入合同。
- `canonical_issue_path` 使用项目相对路径；`absorbed` 至少需要一个可验证的 `absorbed_into` 或 path，不强制二者同时存在。
- raw phase 仅为 `proposed | absorbed | dropped`；linked `I-*` 的 `completed` 不扩散到 raw。

`promote` 只登记 child，raw 保持 `proposed/open`；`promote-finalize` 选择首个可验证的已登记 `I-*` 作为主关系，同时保留完整 children 列表并形成合法 `absorbed/open`。平台关闭是后续独立事件。

## 3.1 历史约束与本次修正边界

本次不改变既有命令职责，只修正 metadata 的初始化与状态生产方式：

| 命令/阶段 | 历史设计原因 | 本次允许的动作 |
|---|---|---|
| `feedback` | 旧 issue 已确认它是 INPUT 操作，不能在 `develop` 直接落 `docs/B1-docs` 本地文件 | 在创建平台 raw issue 的载荷中一次性生成完整、固定顺序的 v1 flat schema；不在受保护分支写本地工作文档 |
| `raw-issue-pull` | 它是平台 → 工位的物化边界，负责补齐/同步 `platform_ids` | 物化同一 schema；保留已有字段和值，只允许按同步事件更新已有字段值；不得新增、删除或重排字段 |
| `wt-create` | 创建工位不是 B1/B2 absorption 事件 | 只创建并同步工位；不得把 `proposed` 改成 `absorbed`，不得写 absorption 字段 |
| B1/B2 promotion | `promote` 先记录 `promoted_children`，`promote-finalize` 才在 canonical issue 已物化后产生 absorption 事实 | 两步都只原子更新已有字段值：`promote` 更新 `promoted_children/source_candidate/updated_at`；`promote-finalize` 更新 `phase_state/absorbed_into/canonical_issue_path/completed_at/updated_at`；不扩展 schema |
| drop/closeout | 丢弃和平台关闭是不同事实，历史 closeout 门禁还承担测试/合并安全检查 | 只在各自事件中更新所属字段值；`wt-close` 不写 `issue.md` |

这条边界吸收了历史 issue `raw-20260625T003331Z` 与 `raw-20260507T073000Z` 的结论：`feedback` 的平台-only 约束仍有效；本次“feedback 字段一次性全”指创建载荷的 schema 完整性，不是恢复 develop 本地文件写入。历史 raw 文件不批量迁移。

## 3.2 状态迁移审查规则

实现每修改一个阶段，必须先核对该阶段的历史 issue 与当前消费者，回答两个问题：

1. 这个字段值是否代表该阶段真正发生的事实，而不是“命令成功执行”的副作用？
2. 该字段是否已在创建时存在；如果存在，本阶段只能更新其值，不能借机补字段或改变字段顺序？

不能证明答案时，保持原有状态行为并先补 B1/B2 证据；不得用“字段缺失”作为修改阶段语义的理由。

## 4. legacy 兼容策略

```text
parse(file):
  if schema_version == current:
    strict_validate(fields, order, types, invariants)
  else:
    normalize phase_state <- phase_state ?? status ?? proposed
    normalize missing optional values <- empty
    preserve original file unless explicit lifecycle transition
    require target resolution before dangerous absorbed operations
```

legacy 兼容是读取策略，不是“默认合法”。PR create/merge、受保护分支集成和 closeout 对不完整 absorbed 状态继续 fail closed。

## 5. PR 平台五态

以 local head 为参照：

| 分类 | 判定 | 允许动作 |
|---|---|---|
| absent | 远端 source ref 不存在 | adapter push，然后 ensure PR |
| behind | remote 是 local 祖先且不相等 | adapter fast-forward/lease push，然后 ensure PR |
| equal | head 相等 | 不 push，ensure PR |
| ahead | local 是 remote 祖先且不相等 | fail closed |
| diverged | 双方均非对方祖先 | fail closed |

执行策略：先观测所有平台。若任一平台为 `ahead/diverged/error/unsupported`，不对任何平台执行 push，避免部分更新。全部可推进时逐平台受控执行，最终要求每个平台达到：

```text
branch_state = equal_after_action
pr_state in {created, reused, updated}
```

任一执行失败，整体失败并保留逐平台恢复上下文。恢复文本只允许 `freely ...` 或 adapter 公开动作。

## 6. dry-run 顺序

```text
preflight governance
→ observe/classify all platforms
→ reject unsafe aggregate
→ controlled branch synchronization
→ ensure/reuse PRs
→ merge dry-run against synchronized remote heads
→ publish aggregate result
```

`pr-merge-guarded` 的真实 merge 继续强制 source head 等于每个要求参与的平台远端 head。dry-run 不再被用作 push 前的远端同步判定器。

## 7. 消费者迁移优先级

第一批必须迁移：

- `raw-issue-pull` 与 `wt-create`：消除非法状态生产。
- B1/B2 promotion 写入点：建立唯一 absorption 事件。
- `pr-create-guarded`、`pr-merge-guarded` 与 platform adapter：解除已有 PR 更新死锁。
- `task-lifecycle-scan.py` 与 governance merge gate：严格新 schema 和危险 legacy 组合。

第二批仅在其测试暴露语义差异时迁移：

- `pre-scan-fix.sh`
- `migrate-issue-phase-state`
- batch closeout
- `issue-index`

第二批不得继续新增字段存在性逻辑；可通过共享 CLI/解析模块读取 normalized view。

## 8. 失败原子性

- metadata 更新：同目录临时文件写入、校验、原子替换。
- 多平台：先全量观测再产生副作用；执行阶段保留每平台结果，禁止将部分成功报告为成功。
- PR 已存在：ensure 操作幂等；重跑不得创建重复 PR。
- 任何失败不回退用户已有提交，不使用 force push。
