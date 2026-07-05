# Candidates: Agent 设计优化

## C-20260520-agent-skill-design-A: Agent doc 重构 + skill 触发约束

**Status:** needs_research
**Priority:** P0

### 改动

1. **Manager Agent doc 重构：**
   - 巡逻工作流改为决策树格式（每步绑定必调 skill）
   - 首跳简化为 4 步：读宪法 → 读法律 → 读 fleet → 判路由
   - 增补 `exit_kind` 使用指南中每种出口对应的 skill

2. **Worker Agent doc 重构：**
   - 开头加"必调 skill 约束表"：按 intent_kind 指定 skill
   - 改为决策树：读 prompt header → 判 intent_kind → 调对应 skill → 执行 → 交接
   - 移除冗余的"可用工具"大表（工具在 skill 里说明）

3. **intent_kind 扩展**（另开候选或合并）：
   - 新增 `merge`、`closeout`、`sync`
   - refine `edit`、`cleanup`、`promotion` 语义

### 影响

- Manager 产出更规范的委派（指定正确的 intent_kind + skill）
- Worker 不会裸写代码而不调 skill
- Agent doc 精简 → prompt 更小 → cache hit 更好

---

## C-20260520-agent-skill-design-B: Worker prompt 必填字段增强

**Status:** needs_research
**Priority:** P1

### 改动

1. Worker prompt header 新增 `skill:` 字段（必填）
2. Runtime 校验：Worker prompt 缺 `skill:` → `LAUNCH_REJECT_REASON` 明确提示
3. Manager agent doc：委派 Workers 步骤，明确"必须指定 skill"

### 影响

- Worker Agent 明确知道自己该调哪个 skill
- Runtime 可以校验 Worker 是否按规范执行

---

## C-20260520-agent-skill-design-C: 工具角色绑定

**Status:** needs_research
**Priority:** P2

### 改动

1. 定义 Manager-only 工具（wt-create, deploy-skills, freely-package）
2. 定义 Worker-only 工具（dev-loop 相关）
3. 定义共享工具（pr-merge-guarded, wt-close, issue-sync）
4. Agent doc 明确："你只能使用你的角色允许的工具"

### 影响

- 防止 Worker 越权创建工位
- 防止 Manager 越权执行 dev-loop

---

## C-20260520-agent-skill-design-D: Skill 懒加载（中长期）

**Status:** needs_research
**Priority:** P3

### 改动

参考 Hermes：prompt 只注 skill 索引，Agent 按需调 `skill_view` 加载完整 skill。

### 影响

- Prompt size 大幅减小
- Agent 更聚焦当前任务
- 需要 runtime 支持 skill_view 工具

---

## Promotion Decision

待决定：哪些候选 promote 到 I-* issue，优先级排序。
