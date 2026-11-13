# B1 Brainstorm — raw-20261113T113100Z

## 0. 立项来源

用户 2026-11-13 的观察：R33.8 / R33.9 / R33.10 三处实现**都通过了当时的评审**，但都被后续人工复核判定为设计漂移 / 能力降级 / 与整体矛盾。问题是评审 skill 本身没有这类规则，所以「不提出来就不会被发现」。

用户要求：抽象这种评审方式，建 raw 修 review 相关文档；并希望走 doc-only 快速合并。

## 1. 缺口证据（已读源码确认）

`docs/system/workspace/skills/freely-tdd-review/SKILL.md` 的核心方法只有一条主线：

> 审查就是检查每个「↓ 忠实消化？」箭头。判断标准：能从下层归纳回上层 → 消化到位。上层在下层中找不到对应 → 遗漏。下层出现了上层没有的东西 → 偏离。

四层分别是 Raw→B1、B1→B2、B2→实现、实现→测试，全部是**相邻层 fidelity**。

这个方法的盲区是结构性的：**如果上层本身错了，四层可以完全自洽地通过**。
R33.8 / R33.9 / R33.10 正是如此：
- B1 写了「linked 要能关」，B2 写了「close-linked 校验 kind + platform_ids」，AT 只验证「能关」——四层 fidelity 全绿，但整套设计绕开了 `issue-sync batch` 与 `phase_state` 生命周期。
- B1 写了「回收残留沙箱」，B2 写了「放宽 protected guard」——四层全绿，但与 `test-wt-close-protected-branch-guard` Test 1–3 直接冲突。
- 副本一致性判红时，B1/B2 没写「允许手工补 comment 块」，但实现这么做了，评审也没问「这是不是绕过门禁」。

结论：**缺一个以「本轮之外的项目资产」为锚的审查层**。

## 2. 抽象出的 L0：项目意图一致性 / 设计漂移检测

> L0 先于四层。四层的「自洽」不能替代 L0 的「一致」。

### 2.1 外部锚点优先于本轮自证

B1/B2 是本轮的产物，不能用来证明本轮正确。L0 必须引用**先于本轮存在**的资产原文：
1. 项目设计文档：`README.md`、`docs/CONSTITUTION.md`、`docs/LAWS.md`、`docs/PROJECT_INTENT.md`、`docs/system/workspace/scripts/README.md`、`contracts/**`。
2. **既有验收测试**：特别是指令式为「必须拒绝 / 必须阻止 / 必须 fail-closed」的断言（例如 `test-wt-close-protected-branch-guard` Test 1–3）。
3. 既有门禁的源码注释与理由（例如 `check-bin-projection` 的 "no permanent exemptions"、`raw_reconciliation._body()` 的 "platform copies never inline them"）。
4. 既有同类实现：是否已经存在同一能力？是否在造第二套？
5. 当前配置对能力的约束（例如 `.freely/config.toml [skip_ibm_gate].allowed_paths`）。

### 2.2 五个必答问题

| # | 问题 | 不通过的样子 |
|---|---|---|
| Q1 冲突 | 本轮实现是否与既有验收测试 / 契约 / README 的明确断言冲突？ | 有冲突却未在 review 中解释；或直接改测试断言来适配实现 |
| Q2 门禁强度 | 是否放宽、绕过或删除任何门禁？改后强度是否 ≥ 改前？ | 把「必须拒绝」改成「条件放行」却拿不出「当初设计错误」的证据 |
| Q3 能力降级 | 是否有能力被删除、强制执行变可选、fail-closed 变 fail-open、默认值变宽松？ | 为了流程走通把强校验降级为 WARN |
| Q4 第二套语义 | 同一概念是否出现了第二个真源 / 第二套判断？ | 已有 `phase_state`/`platform_state` 判定，又写入 `status: closed` |
| Q5 设计漂移 | 本轮是否在「修实现」的名义下改变了设计意图？ | 注释说「never on develop」，实现却写 develop |

### 2.3 门禁改动的举证责任

凡修改门禁 / 契约 / 安全边界，review 必须给出四段证据，缺一即不得 pass：
1. **当初为什么这样设计**：引用引入它的 commit / raw / 验收测试原文；
2. **现在为什么必须改**：是实现不达标、环境变化，还是设计本身错误；
3. **判定**：明确写「实现不达标（改实现）」还是「设计错误（改门禁）」；
4. **强度不降**：逐条说明改后仍满足原有断言；若必须放宽，列出等价补偿。

### 2.4 明确的失败判据（任一命中即 fail）

- 发现与既有验收测试/契约冲突，且 review 未解释；
- 为让本轮通过而修改/删除既有断言（而不是修实现）；
- 门禁被放宽且没有「当初设计错误」的证据；
- 出现第二套语义/真源；
- 用「本轮 B1 已决定」回答 Q1–Q5（自证）；
- 用手工补数据/补字段让门禁通过，而不是修数据链路。

### 2.5 与四层的关系

- L0 通过后才进入四层；L0 失败直接 fail，不必逐层看完。
- 四层发现的问题若涉及 L0（例如 B2 写了放宽门禁），必须回填 L0 结论。
- 输出格式新增 `## L0：项目意图一致性` 段落，逐条回答 Q1–Q5 并列出引用的锚点原文。

## 3. 真实案例（回填，不虚构）

把 R33.8 / R33.9 / R33.10 写成 skill 里的「L0 应命中」样例：
- R33.8：Q2（绕过 `phase_state` 门禁）、Q4（`status: closed` 第二套语义）、Q5（偏离 batch 单一路径）。
- R33.9/R33.10：Q1（与 Test 1–3 冲突）、Q2（放宽 protected guard）、Q5（沙箱跑完整生命周期）。
- R33.8 手工补 comment 块：Q5 + 「用补数据让门禁通过」。

## 4. 方案空间

| 方案 | 做法 | 评价 |
|---|---|---|
| A | 在 `freely-tdd-review/SKILL.md` 新增 L0 层 + 输出格式 + 案例 | 单一权威指南，ACP reviewer 与人工审查都读它 ✅ |
| B | 只改 `pr-review-guarded` 的 prompt | 绕过 skill 权威，且改动实现代码，超出「doc」范围 |
| C | 新增一个独立 lint 强制 verdict 含 L0 | 会改 verdict 契约与门禁，风险大，且可能变成「补字段就过」 |
| D | 只在 B2 模板加一句提示 | 太弱，评审者可以忽略 |

采用 A：只改评审 skill（权威指南），不碰 verdict 契约、不改门禁、不改代码逻辑；ACP 与人工审查都按 skill 执行。

## 5. 证伪

- 「四层已经能发现」→ 否：R33.8–R33.10 四层全绿仍漂移，因为错在上层。
- 「加 lint 更硬」→ 否：verdict 是自由文本，强制字段只会诱导「补字段」；L0 要求引用外部锚点原文，无法靠补字段通过。
- 「改 skill 属于 doc-only」→ 否：`.freely/config.toml [skip_ibm_gate].allowed_paths` 不含 `docs/system/workspace/skills/`，项目有意把 skill 当系统真源，必须走完整链路（本轮的 B1/B2/AT 即第一次实践）。
