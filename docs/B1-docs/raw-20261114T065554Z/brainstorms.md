# B1 Brainstorm — raw-20261114T065554Z

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文）:
  - 设计文档: `docs/system/workspace/commands.md`「wt-close 执行位置：(project-root, develop 工位)」「正常收口: PR 已合并，清理工位和分支」；`skills/freely-workflow-guarded-execution/SKILL.md:42` 自称「Skill 是流程的唯一权威来源——不依赖本提示的摘要」；`docs/LAWS.md`「一个工位只处理一个 raw issue」。
  - 既有验收测试: `test-wt-close-test-premerge-guard.py` S2「guard has NO --force/--discard-unmerged exception」（protected 分支守卫不得放宽）；`test-wt-close-branch-count.py`、`test-wt-close-dryrun-safety.py`。
  - 门禁源码注释/理由: `wt-close:795`「--force 只有一个目标: 彻底丢弃。如果意图不是丢弃，STOP」；`wt-close:797-800`「如果认为"已经 merge 了，可以删除" → 用不带 --force 的正常 wt-close → 不带 force 报错 → 说明没有 merge」；`wt-close:198-201` 已有 `_has_merge` / `rev-list develop --merges --grep raw-<key>`。
  - 既有同类实现: `wt-close:804` 的保留路径 `freely chat --new-issue "extract: ..."`；`governance-merge-gate` 的 `--range` two-dot diff。
  - 配置约束: 无。
- 判定（五分类）: **实现偏差 + 实现未完成**——守卫把「PR 已 merge + 追加提交」误判成「从来没 merge」（偏差），且缺少「补合并 PR」这条路径与「逐提交判定」（未完成）。设计本身（`--force` 只用于彻底丢弃）是对的。
- 与既有断言的冲突: 无。本轮**不**修改 protected 分支守卫，`test-wt-close-test-premerge-guard.py` S2 保持原样。
- 影响面: `wt-close`（守卫、USAGE、参数、理由清单、Phase 6 提示）、`freely-workflow-guarded-execution` 阶段 9、`commands.md`、新增 `postmerge_commit_guard.py` 与一条 AT。

### 0.1 全局适配反思（四问）

1. **类别**：这是**收口流程的决策规范**（生命周期边界），不是副本传播、不是实现 bug 修复。
2. **职责边界**：规范权威归 skill（流程唯一权威）；**机器判定**归 `wt-close` 守卫；提示语只是把规范喊出来。三者不能混：只改提示语 = 贴标语，`--force` 照样一步丢掉。
3. **结构性冲突**：若把「有用就补合并」做成必须逐次人工确认的问答，会拖慢每轮收口；若把「无用」做成自由文本理由，会变成补字段就过。故判定必须基于**可验证的 git 事实**（patch-id 等价性 + 承接 raw 是否真实存在）。
4. **门禁失配**：现有守卫只测「`develop..branch` 是否非空」，不区分「从未 merge」与「已 merge + 追加提交」。本轮是**细分 + 收紧**，不是放宽；不得为让流程走通而放宽 `--force`。

## 1. 现象（本轮真实案例）

R33.16 的 PR #4442 已合并，分支上追加提交 `712e7550c`（内容仅 `platform_state: closed` 等 3 个副本字段）。`wt-close` 报未合并提交，两处提示都断言「没有 merge / 大概率 pr-merge-guarded 没执行成功」，诱导 `--force --discard-unmerged`。

实际正确解法：`git merge develop` → 补合并 PR #4641 → 正常 `wt-close`，**零强制参数**。差点白干。

## 2. 查证：规范不存在

| 位置 | 现状 | 缺口 |
|---|---|---|
| `wt-close:782-813` 未合并守卫 | 「没有 merge」；保留路径只有 `freely chat --new-issue "extract: ..."` | 无「补合并 PR」 |
| `wt-close:1290-1306` Phase 6 提示 | 一律「分支未合并到 develop」+ 直接给丢弃命令 | 同上，主动诱导丢弃 |
| `wt-close:427` 合法理由 | 只有「该方案已被否决」 | 把丢弃等同于方案被否决；本轮提交是正确副本状态，套不上 |
| `_require_reason` (442-445) | 只校验前缀 | 不校验逐提交判定 |
| `commands.md:193-194` / 阶段 9 / `LAWS.md` | 语法、两行命令、派生工位规则 | 无决策规范 |

**关键发现**：`wt-close:198-201` 已有 `_has_merge`（`rev-list develop --merges --grep raw-<key>`）能判断「这个 raw 是否 merge 过」，但守卫没用它。属接线缺口，不是新增能力。

## 3. 方案

| 方案 | 做法 | 评价 |
|---|---|---|
| A | 只改两处提示语文案 | 贴标语；`--force` 照样丢 → 不防乱丢 ❌ |
| B | 加一个「逐提交判定」必填字段 | 补字段就过，用户明确反对 ❌ |
| C | 独立 Python 判定器（`postmerge_commit_guard.py`）+ 守卫按 git 事实分情形放行 + skill 定义规范 + 提示语追问 | 可测、可验证、三层各司其职 ✅ |
| D | 情形 B 一律禁止丢弃 | 堵死「已等价落盘/已另行抽取」的合法收口 ❌ |

采用 C。

### 3.1 判定器 `postmerge_commit_guard.py`

输入 `--project --branch [--target develop]`，输出 JSON：

- `has_merge`：`rev-list <target> --merges --grep "raw-<key>" --count > 0`
- `commits`：`rev-list <target>..<branch>` 逐条 `{sha, subject, is_merge, equivalent_in_develop}`
- `equivalent_in_develop`：用 `git cherry <target> <branch>` 的 `- <sha>` / `+ <sha>` 判定（标准 patch-id 比对）
- `all_equivalent` / `allow_discard`

### 3.2 两种情形的决策树

- **情形 A：从未 merge**（`has_merge=false`）→ 保持原逻辑：`--force --discard-unmerged --reason` 允许丢弃（方案被否决），提示强度不变。
- **情形 B：已 merge + 追加提交**（`has_merge=true`）
  - 全部追加提交 `equivalent_in_develop=true` → 内容已落盘，零损失，允许丢弃并**列出比对证据**；
  - 存在未落盘提交 → **默认拒绝丢弃**，提示补合并 PR 命令（首选）与 `freely chat --new-issue` 抽取路径；
  - 仅当显式 `--extracted-into <raw-key>` 且 `docs/B1-docs/raw-<key>/issue.md` 真实存在时，才放行丢弃（理由是可验证的承接物，不是自由文本）。

### 3.3 提示语

逐提交列出 `sha + subject + equivalent?`，逐条追问「有用→补合并 / 已落盘→证据 / 无用→承接 raw」，并写明 **two-dot diff 坑**：`governance-merge-gate --range develop..HEAD` 在分支落后 develop 时会把 develop 的新提交算成反向差异，看着像夹带实现；先 `git merge develop` 再判即可。

## 4. 证伪

- 「改提示语就够了」→ 否：`--force` 是执行入口，提示语不拦。
- 「patch-id 比对太重」→ 否：`git cherry` 是标准能力，只在 `--force` 路径执行（正常收口零开销）。
- 「情形 B 一律禁丢更安全」→ 否：内容已等价落盘时丢弃是零损失，禁掉会逼出 `--force` 手工绕过。
- 「新增 `--extracted-into` 是过度设计」→ 否：它是「无用也要有理由」唯一可机器验证的落点。

## 5. 边界

- **不放宽** `--force` / `--discard-unmerged` 的现有拒绝判定；不动 protected 分支守卫（S2 保持绿）；
- 不改 GATE 1、不改 `pr-merge-guarded`、不改 verdict 契约；
- 不自动创建 PR、不自动 merge——只给可执行路径；
- 不把「逐提交判定」做成文本字段校验（用 git 事实）。
