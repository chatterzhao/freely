# Brainstorms: 收敛 37 个 skill 的重叠分组

- source_raw: raw-20261104T075959Z
- 覆盖域：`docs/system/workspace/skills/` 37 个 skill、三个「重叠组」、frontmatter 字段、lint、路由测试、总数 ≤25。

## 真源普查（不照 issue 旧描述改）

- 实测 37 个 skill 目录，全部 frontmatter 只有 `name` / `description`，**零** `loop`/`owner`/`supersedes` → 方案 3 成立。
- `grep -rn "从 gate 源码提取" docs/` 命中 **1** 处：`freely-doc-B2_IBM-execution/SKILL.md:393` → 方案 4 成立。
- `docs/epics-map.svg` 已有 `epic-skills`，只有 1 个 story（`skill-yaml-frontmatter`）。

## 证伪：issue 的「三组重叠」假设基本不成立

| 组 | issue 判断 | 实测 | 结论 |
|---|---|---|---|
| 执行流程 dev-loop / test-execution / test-RED-execution | 重叠 | workflow skill 明确区分 RED → dev → GREEN 三阶段，每个 SKILL.md 头部都有全链路定位 | **不是重叠**，合并即破坏 TDD 顺序 |
| 人类中断 triage / handling / direct-answer | 重叠 | triage 做首次 reaction 路由、handling 做 manager 深度解释、direct-answer 由 runtime dispatcher 直接 claim | **同一 intake 链路的不同 owner**，合并会让 dispatcher 无法按 reaction 选 claim 路径 |
| Worktree 治理 hygiene / maintenance / multi-worktree | 重叠 | 分别判脏树阈值、merge 顺序与退役、fleet 批次 | 触发条件不同，可用**唯一入口 + 矩阵**消歧，不必删文件 |

因此「至少 2 组完成合并、总数 ≤25」是破坏性删并：会牵动 `AGENTS.md`、workflow skill、hooks、skill 索引、路由测试与打包白名单。按 R22/R23.5/R23.6 的 scope 收敛先例，本轮不做删除型重构，另立 raw 承接（先建索引兼容期再逐个删并）。

## 方案对比

1. **只删并**（issue 原方案）：token 下降最快，但路由回归面大、且合并的是分工而非重复 → 否决。
2. **只写文档矩阵**：零风险，但无法机器守护、frontmatter 仍漂移 → 不够。
3. **矩阵真源 + frontmatter 契约 + lint + 路由测试 + 消除重复枚举**（本轮）：零语义变化、可机检、给后续删并提供 `supersedes` 落点与唯一入口 → 采用。

## Decision

本轮交付 `skill-map.yaml`（37 条 loop/owner/输入输出/触发词 + 3 组重叠判定 + 12 个 loop 的路由入口）、37 份 frontmatter、`bin/check-skill-frontmatter`（0/1/2）、AT-001、CI 接线、epics-map story。删并型重构拆新 raw 排入 goal 队列。

## 验收标准字面矛盾（重要）

验收标准 4 写 `grep -r "从 gate 源码提取" docs/ 为 0`，但 B1 `issue.md` 正文**自己引用了这句短语** → 字面断言自指、永远不可能为 0。按 `AGENTS.md` 仓库分层，把检查范围收窄到能力目录 `docs/system/workspace/`，排除研发过程文档（B1/B2/milestones）。
