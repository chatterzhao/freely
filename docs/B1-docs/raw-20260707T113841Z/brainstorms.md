---
b1_id: B1-20260707T113841Z
phase_state: completed
source_raw: raw-20260707T113841Z
source_url: https://github.com/chatterzhao/freely/issues/3803
produced_candidate: C-20260707T113841Z-A
created_at: 2026-07-07
---

# B1: 多阶段强制 Review 门禁

## Input
- raw-20260707T113841Z: feat — 多阶段强制 Review 门禁
- GitHub issue #3803
- Kind: feature

## Discovery

### value_check: 当前状态与影响

**影响程度: P0 严重**——当前审查机制完全依赖 Worker 自觉，存在系统性风险：

1. **审查跳过率估计 >50%**：Worker 可以直接报 state=completed 跳过所有 6 个 review stage。我们在本次会话中验证了这一点——Manager→Worker→Reviewer 的 A2A/SSE 协议已定义完整，但实际执行中 Worker 从未触发过 needs-review。
2. **自审偏差不可检测**：Worker 和 Reviewer 可能使用同一个 Claude model slot，无法区分"真审查"和"糊弄审查"。
3. **门禁无感知**：pr-create-guarded 通过了 7 个 PR 合并，但其中 0 个经过了独立的 B1/B2/RED/dev/GREEN 阶段审查。
4. **已有基础设施未落地**：input_required_reason.py 定义了 6 个 stage、reviewer-agent.md 定义了完整路由——但命令层没有强制使用。

**价值确认**: 此 issue 不是重复——虽然 reviewer-agent.md 和 A2A/SSE 协议已存在，但它们定义的是"审查可以怎么做"而不是"审查必须怎么做"。缺少的是命令层的硬兜底（pr-create-guarded 检查签名）和指南层的标准化（每个 phase 查什么）。这两个组件是全新的，没有被任何现有 candidate 覆盖。

### 现有基础设施（可复用的）

| 组件 | 文件 | 状态 |
|------|------|------|
| InputRequiredReason 枚举 | `docs/system/workspace/agents/input_required_reason.py` | ✅ 已有 6 个 review stage |
| Reviewer agent 定义 | `docs/system/workspace/agents/reviewer-agent.md` | ✅ role/slot/route 已定义 |
| A2A SSE 事件流 | `watchdog_sse.py` | ✅ Worker→Reviewer 路由已通 |
| ACP session/fork | `agent_working.py` | ✅ Manager→Reviewer fork |
| agent_working 表 | `agent_working.py` | ✅ UPDATE ONLY 约束 |
| pr-create-guarded gate chain | `pr-create-guarded` | ✅ 已有 5 步 gate |
| freely-review | `bin/freely-review` | ⚠️ ACP 不可用时静默跳过 (exit 0) |
| freely-tdd-review skill | `freely-tdd-review` | ✅ 四层审查方法 |

### 缺失的部分（需要新建/改造）

| 缺失 | 说明 |
|------|------|
| **阶段审查指南** | 每个 phase 没有独立的审查标准文档——Reviewer 不知道该重点查什么 |
| **review signature** | agent_working 表没有 review verdict 字段——无法判断某 phase 是否已被审查 |
| **命令门禁检查** | pr-create-guarded 不检查 review signature——Worker 可跳过所有审查直接提 PR |
| **缺失委派逻辑** | gate 发现 review 缺失时，没有自动委派 Reviewer 的逻辑 |
| **跨模型强制** | 没有机制保证 Reviewer 和 Worker 用不同 model slot |
| **Agent 提示词中的阶段定义** | Worker agent 的 prompt 中没有清晰的 "什么是 B1 完成" 定义 |

### 行业参考

| 项目 | 核心模式 | 可借鉴 |
|------|---------|--------|
| **Routa** | downstream distrust — 下游车道不信任上游产出，GATE 独立验证 | 阶段审查指南的设计——每个阶段有独立的检查标准 |
| **Karpathy AutoResearch** | 客观指标判定 — val_bpb 改进则保留，否则 reset | 不让 agent 自己判——外部指标决定 pass/fail |
| **Zed spawn_agent** | 同步阻塞等结果 — parent 调用 subagent，等 final message 返回 | 命令委派 Reviewer 后阻塞等 verdict |
| **BetterForAll Arena** | 对抗验证 — test agent 主动找漏洞 | Reviewer 的对抗姿态——尝试证伪，不只确认 |

## Problem

当前审查完全依赖 Worker 自觉通过 A2A state=input-required 触发。Worker 可以：
1. 不触发审查直接报 state=completed（跳过所有 review）
2. 自己审查自己（同一个 claude model slot）
3. pr-create-guarded 不检查 review 存在性——直接放行

**根因：审查触发权在 Worker 手里，没有硬兜底。**

## Brainstorm

### 子问题 1：审查指南如何抽象和注入

#### Option A: 硬编码在 Reviewer agent 的 system prompt 中
- 优点：简单
- 缺点：每次改指南要改 agent 定义；不同阶段无法区分

#### Option B: 独立文件 + 注入机制 ✅
- 每个 phase 一个 `review-guidelines/{phase}-review.md`
- Reviewer agent 启动时根据 review_stage 参数加载对应指南
- 优点：指南独立维护、易于增强、不同阶段不同标准
- 缺点：需要指南加载机制

#### Option C: 指南写在 A2A task message 中
- 优点：灵活，每次可不同
- 缺点：依赖调用方写对，无标准

**Decision: Option B** — 独立文件 + 注入。Reviewer agent 的 system prompt 中说 "根据 review_stage 参数加载 docs/system/workspace/review-guidelines/{stage}-review.md"。

### 子问题 2：审查签名存储在哪里

#### Option A: agent_working 表增加 review_verdict 字段
- 优点：已有表结构，UPDATE ONLY 约束天然适用
- 缺点：需要 schema 变更

#### Option B: 新表 review_signatures
- 优点：独立，不影响 agent_working
- 缺点：多一张表，关联查询复杂

#### Option C: 审查结果写入 I-* issue 的 frontmatter
- 优点：与 issue 文档在一起，git 可追溯
- 缺点：需要 git commit，审查变成有副作用

**Decision: Option A** — agent_working 表增加字段。已有 UPDATE ONLY 约束防止 Worker 伪造签名。增加 `review_stage`, `review_verdict`, `reviewed_by`, `reviewed_at`, `review_findings` 字段。

### 子问题 3：命令门禁如何检查 + 缺失时如何委派

#### Option A: 新增独立 gate 脚本（如 review-signature-gate）
- 优点：关注点分离
- 缺点：又多一个脚本

#### Option B: 集成到 pr-create-guarded 的 gate chain 中 ✅
- 在 Step 2c (IBM governance gate) 和 Step 2d (pretests evidence) 之间插入 "Step 2c2: Review signature check"
- 检查 agent_working 表中该 raw-key 的 review_signatures 是否覆盖所有已完成 phase
- 缺失时：阻塞 + 输出具体缺失 phase → 提示用户手动启动 review 或自动 ACP 委派

**Decision: Option B** — 集成到现有 gate chain。检查逻辑简单：扫描 agent_working 表 → 对比已完成 phase vs 已审查 phase → 缺失列表。

#### 委派策略

当 gate 发现缺失时：
```
Option A: 只报错，让用户手动解决
  - 简单但体验差

Option B: 自动 ACP 委派 ✅
  - gate 调用 ACP bridge → fork Manager→Reviewer → 注入对应阶段指南
  - 阻塞等 verdict → pass 写入签名 → 继续 gate chain
  - fail → 输出 findings → 提示用户修复
  - ACP 不可用时降级为人工审查提示
```

**Decision: Option B** — 优先自动委派，ACP 不可用降级为人工提示。

**★ 关键约束：上游改动 → 下游全部作废**

阶段间有依赖链。上游重做会 invalidate 下游所有 review signature：

```
B1 修了 → B2/RED/dev/GREEN review 签名全部作废
B2 修了 → RED/dev/GREEN review 签名全部作废
RED 修了 → dev/GREEN review 签名全部作废
dev 修了 → GREEN review 签名作废
```

命令兜底不是"缺哪个审哪个"——是"从最先缺失的阶段开始，后面全部重来"。

gate 检查逻辑：
1. 找最先缺失 review 的 phase（如 B2）
2. 阻塞 + 报告: "B2 及之后所有阶段 (B2→RED→dev→GREEN) 需要重新走"
3. Worker 从 B2 重新开始 → B2→RED→dev→GREEN 全部重做
4. 每个阶段完成后重新请求 review
5. 全部 PASS 后重新 pr-create-guarded

### 子问题 4：Agent 提示词如何让 Worker 知道何时停止

#### 当前问题
Worker agent prompt 没有阶段边界的清晰定义。B1/B2/RED/dev/GREEN 是什么、完成标志是什么——都没有。

#### Option A: 在 workflow skill 中增加阶段定义
- 每个 phase 完成后有明确的 "completion signal"
- Worker prompt 注入阶段定义

#### Option B: 阶段定义独立文件 + prompt 引用 ✅
- `docs/system/workspace/phase-definitions/{phase}.md`
- 每个文件定义：phase 是什么、输入是什么、输出是什么、完成标志是什么、完成后做什么（调 review）
- Worker prompt 中注入："你的当前阶段是 {phase}，完成后请参照 phase-definitions/{phase}.md"

**Decision: Option B** — 与 review-guidelines 对称设计。Worker 读 phase-definitions，Reviewer 读 review-guidelines。

### 子问题 5：跨模型强制

#### 实现方式
- agent-table.toml 中 reviewer slot 配置为不同 tool（如 `codex-apikey-xxx` 而非 `claude-apikey-xxx`）
- pr-create-guarded 的签名检查：验证 `reviewed_by.slot` != `worker_slot`
- 同一 tool 时降级为 warning（不阻塞，但提示风险）

## Decision

综合决策：**不是推倒重来，是在现有 A2A/SSE/ACP 架构上补三层**

```
Layer 1 (提示词): phase-definitions/{phase}.md → Worker 知道什么是完成
Layer 2 (指南):   review-guidelines/{phase}-review.md → Reviewer 知道查什么
Layer 3 (命令):   pr-create-guarded + review-signature-gate → 硬兜底 + 自动委派
```

### 改动范围

| 文件 | 操作 | 说明 |
|------|------|------|
| `review-guidelines/{b1,b2,red,dev,green}-review.md` | 新建 | 5 个阶段审查指南 |
| `phase-definitions/{b1,b2,red,dev,green}.md` | 新建 | 5 个阶段完成定义 |
| `agent_working.py` | 修改 | 增加 review verdict 字段 |
| `pr-create-guarded` | 修改 | gate chain 增加 review signature 检查 |
| `bin/freely-review` | 修改 | ACP 不可用时不应 exit 0 |
| `reviewer-agent.md` | 修改 | 指南注入机制说明 |
| `worker-agent.md` | 修改 | 阶段定义引用 |
| `input_required_reason.py` | 不变 | 已有 6 个 stage |

### 不改动的

- A2A/SSE/ACP 基础设施 —— 已有且工作
- agent-table.toml —— 已有 reviewer pool=99
- watchdog_sse.py —— 已有 needs-review 路由
- freely-tdd-review skill —— 已有四层审查方法

## Candidate
- candidate_id: C-20260707T113841Z-A
- status: promoted
- milestone: M-20260707T113841Z-A
