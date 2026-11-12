---
raw_key: raw-20261112T031638Z
created_at: 2026-11-12
platform_ids:
  github: '4310'
  gitee: IKUSRE
---

# B1 预研 — issue-sync 保护分支提示引用幽灵 skill 名 + protected-root 调用噪音

## 0. 覆盖域（raw 提到的每个点都必须被分析到）

raw #4310 提到 4 个具体点 + 1 个伴随面：

| raw 中的点 | 本轮普查结论 |
|---|---|
| `bin/issue-sync:126` `skill:freely-fix-execution` | 确认存在，活代码，每次 protected-root 调用都打印 |
| `bin/issue-sync:127` `skill:freely-feature-execution` | 确认存在，同上 |
| `bin/issue-sync:131` `--skill <freely-fix-execution\|freely-feature-execution>` | 确认存在，**且缺必填 `--kind`**（比 raw 描述更严重） |
| `AGENTS.md.example:146` `--skill <skill>` | 确认存在，缺 `--kind` |
| 伴随面：`wt-create` 每轮 ERROR+WARN 噪音 | 确认可复现，**根因与文案无关**，见 §2 |

本轮开工位时 `wt-create` 的输出**当场完整复现**了全部 5 个点（证据留存
`/tmp/r336-wt-create-before.log`，并抄入 B2 verification）。

### 0.1 普查扩大到全仓（raw 只列了 4 处，实际更多）

`grep -rnE "freely-fix-execution|freely-feature-execution|freely-feat-execution"`
排除 `docs/B1-docs/` `docs/B2-docs/` `.git/` 后的全部命中，逐条定性：

| 位置 | 性质 | 处置 |
|---|---|---|
| `bin/issue-sync:126,127,131` | **活代码运行时文案** | 修（M1） |
| `docs/system/workspace/scripts/quality/pretests-gate:570` | **活代码门禁错误文案**，`red_green_not_green` 时打印 | 修（M1） |
| `docs/system/workspace/scripts/worktree/wt-close:1155,1159,1163` | **活代码**，分支未合并时的 UNMERGED 警告 | 修（M1） |
| `docs/system/workspace/AGENTS.md.example:146` | 模板，缺 `--kind` | 修（M1） |
| `docs/system/workspace/hooks/reference-transaction.sh:118` | **机械替换产物**：`--skill <freely-workflow-guarded-execution\|freely-workflow-guarded-execution>` 两个选项完全相同，且缺 `--kind` | 修（M1） |
| `docs/system/workspace/scripts/worktree/pr-create-guarded:158` | **注释语义错误**：说「wt-create derives prefix from --skill」，实际由 `--kind` 决定；且同名重复两次 | 修（M1） |
| `docs/system/workspace/three-loop-capability-lifecycle.md:206,359` | 文档，`--skill <skill>` 缺 `--kind` | 修（M1） |
| `docs/system/workspace/scripts/runtime/freely:1110,10771,11361,11407,13430` | **活代码 runtime 帮助/拒绝文案**，5 处 `--skill <skill>` 缺 `--kind` | 修（M1，触发 Step 2.5） |
| `docs/system/workspace/commands.md:75,87` | **不是缺陷**：`--skill` 作为可选覆盖参数被正确记录 | 不改 |
| `tests/test_a2a_task_insert.py:83,200` | **fixture 字面量**，仅作 DB 字段值，无存在性校验 | 不改（见 §1.2） |
| `docs/system/workspace/scripts/tests/test-worker-task-json-boundary.py:55,134` | 同上，fixture 字段值 | 不改 |
| `docs/system/workspace/scripts/runtime/task-lifecycle-scan.bak.py`（11 处） | **死备份**：全仓零引用；`bin/freely-package:188` 打包时 `find -name '*.bak.py' -delete` | 不改（见 §1.3） |
| `docs/system/workspace/scripts/tests/test-projection-consistency.py:9,10,42` | R33 AT 自身的 `GHOST_SKILLS` 黑名单常量与文档字符串 | 不改（黑名单必须列出幽灵名） |
| `docs/system/workspace/scripts/tests/test-wt-close-protected-branch-guard:82` | **测试固化了幽灵名**：断言 guard 必须含幽灵名才 PASS | 修（M3，反向断言） |

## 1. 根因分析（不修表面症状）

### 1.0 skill 历史变迁评审（**先查提交历史，再定性；本节纠正了初稿的一处错误**）

初稿把这三个名字写成「从不存在」，**这是错的**。查全历史后确认它们是
**真实存在过、后被正式退役的 skill**，不是凭空捏造的名字。证据链（按时间序）：

| 提交 | 日期 | 事实 |
|---|---|---|
| `042a54a67` | 2026-05-11 | `refactor: rename all 33 skills with freely- prefix` —— 加 `freely-` 前缀，`fix-execution` → `freely-fix-execution` |
| `462661fbf` / `0486eee90` | 2026-06-25 | `refactor: rename skill dir feat→feature (#3521)` —— **`freely-feat-execution` → `freely-feature-execution`**，所以 feat 是 feature 的旧名，不是第三个独立 skill |
| `2495ca2af` | 2026-06-29 | **关键决策提交**：`fix(wt-create): --kind replaces --skill for branch prefix selection`。提交信息原文：`--kind fix\|feature\|hotfix now determines branch prefix` / `--skill defaults to freely-workflow-guarded-execution (optional override)` / `Renamed old fix/feature SKILL.md to .bak` |
| `a4029fa15` | 2026-06-29 | `Reapply "Merge ... fix-flow-unify"` —— 删 `freely-fix-execution/SKILL.md`（-235 行），新增 `freely-workflow-guarded-execution/SKILL.md`（+221 行） |
| `cf7f4f4a1` | 2026-06-29 | 中间有一次 `Revert`，随后被 `Reapply` 覆盖 —— **最终态是「已退役」**，不是回退态 |

**权威替代关系（新 → 旧）**：

```
freely-workflow-guarded-execution   ← 唯一流程入口（新，现行）
  ├─ 取代 freely-fix-execution      ← 已退役（旧）
  └─ 取代 freely-feature-execution  ← 已退役（旧）
        └─ 旧名 freely-feat-execution（2026-06-25 改名为 feature）
```

`--kind` 与 `--skill` 的关系 likewise 由 `2495ca2af` 定死：
**`--kind` 是新的必填参数（决定分支前缀），`--skill` 是旧的分支前缀选择器、
现降级为可选覆盖（默认 workflow-guarded）**。所以 §1.2 的结论成立且现在有
提交信息直接背书，不是推测。

**当前态核验（防回退）**：
- `git cat-file -e develop:.../freely-fix-execution/SKILL.md` → 不存在 ✓
- `git ls-tree develop .../freely-fix-execution/` → 目录不存在（连 `.bak` 也已清）✓
- `skills/` 下无任何 `*fix-execution*` / `*feature-execution*` 目录残留 ✓
- `skill-map.yaml` 的 `skills` 只含 `freely-workflow-guarded-execution`；
  `aliases` / `merge_groups` **不含**这三个名字 —— 说明它们不是 R28.5 那批
  「合并但保留 alias」的 skill，而是**更早就整体退役**的，因此**不应给它们造 alias**
  （§3 Option C 的否决理由据此加强）。
- `freely-workflow-guarded-execution/SKILL.md` 正文两处自称「Freely 所有开发工作的
  **唯一流程入口**」，且 `supersedes: []`。

**文档冲突的裁决**：`fix-flow-unify` 的 IDN 写「不合并 fix 和 feature 为一个 skill」，
与「两者都被 workflow-guarded 取代」表面冲突。按提交历史裁决：该 IDN 描述的是
**流程语义层面**（fix 与 feature 的 RED 阶段结论不同，不抹平差异），而
`2495ca2af` + `a4029fa15` 做的是**入口层面**的合并（一个 SKILL.md 承载两种 kind）。
现行 `workflow-guarded/SKILL.md` 的「fix 与 feature 的唯一差异」章节正好同时体现
两者——**入口统一、语义保留**。故两份文档并不真冲突，本轮方向与两者都一致。

**本轮不是回退**：本轮把残留指引从「已退役的旧入口」指向「现行唯一入口」，
方向与 `2495ca2af` / `a4029fa15` 完全一致，是**补齐当年漏改的文案**，
不是恢复旧 skill、也不是撤销任何既有决策。

### 1.1 文案面根因：R33 的验收覆盖面不足，而非替换不彻底

R33（#4179）修的是「AGENTS 生成器 + 模板」，AT-001 的 c13 断言
（`test-projection-consistency.py:179-186`）只遍历生成器与模板两类文件。
（术语澄清：本文沿用 R33 的「幽灵名」说法，但准确含义是
**「已退役 skill 的残留引用」**，而非「从不存在的名字」——见 §1.0。）
**幽灵名在仓库里有 4 类载体**：① 生成器/模板（R33 已覆盖）② `bin/` 与
`scripts/` 的运行时错误文案（未覆盖）③ 文档（未覆盖）④ 测试断言（未覆盖，
且其中一条把幽灵名当成「必须存在」的正向判据）。

所以根因是**「零幽灵名」这条验收的扫描域定义得太窄**，只修文案会再次漏网。
必须同时把扫描域扩到活代码 + 文档，并给「合法出现」建立显式白名单
（AT 黑名单常量、fixture 字面量、死备份），否则新断言必然假红。

### 1.2 证伪一：`--skill` 并未废弃（raw 描述有误，需纠正）

raw 写「`--skill` 参数也已被 `--kind fix|feature` 取代」。**实测不成立**：

- `wt-create:22` 明确 `--skill <name>  Override workflow skill (default: freely-workflow-guarded-execution)`；
- `wt-create:109` 仍有 `--skill)` 解析分支；
- `commands.md:75,87` 把它记录为可选覆盖参数。

真正的缺陷是：**这些提示把可选的 `--skill` 当成必填主参数展示，却漏掉了真正
必填的 `--kind`**（`wt-create:203` `Missing required: --kind`）。照提示抄命令
会直接失败。所以修法不是「删掉 --skill」，而是**把 `--kind <fix|feature|hotfix>`
补进提示、把 `--skill` 降级为可选或省略**。`commands.md` 因此不改。

### 1.3 证伪二：`.bak.py` 与 fixture 不是缺陷（避免过度扩大改动面）

- `task-lifecycle-scan.bak.py`：全仓零引用（`grep -rn "task-lifecycle-scan.bak"`
  除自身外无命中），真源是同目录 `task-lifecycle-scan.py`；`bin/freely-package:188`
  打包时显式 `find "$dst" -name '*.bak.py' -delete`。它不进安装态、不被执行。
  改它等于给死代码做美容，且会让「零幽灵名」断言被迫覆盖死文件。
  **决策：不改，列入白名单并写明理由**；其删除属独立的死代码清理议题，不在本轮。
- 两个测试里的 `"skill": "freely-fix-execution"` 是 DB 字段 fixture 值，
  被测代码（`h_a2a_task_insert` / worker task JSON 边界）不校验 skill 是否存在。
  改成真名不影响断言语义，但会让「幽灵名不得出现」的扫描必须区分
  「面向用户的指引」与「任意字符串 fixture」。**决策：不改，列入白名单**。

### 1.4 噪音面根因：`issue-sync` 的 ROOT_DIR 从脚本位置推导，忽略调用方 cwd

这是与文案**完全独立**的第二个缺陷，链路已逐层核实：

1. `wt-create:1002` 用 `( cd "$fix_target" && _pull_raw_issue ... )` 进入 **dev 工位**再拉取；
2. `_pull_raw_issue`（`wt-create:519-526`）调 `"$ROOT_DIR/bin/raw-issue-pull"`，
   此处 `$ROOT_DIR` 是**主仓**（脚本所在仓库），不是 cwd；
3. `bin/raw-issue-pull:53` `ROOT_DIR="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)}"`
   → 未设 `PROJECT_ROOT` 时回落到**主仓**；
4. `bin/raw-issue-pull:133` 调 `"$ROOT_DIR/bin/issue-sync" create "$local_id"`，
   **未传 `--project`**；
5. `bin/issue-sync:36` `ROOT_DIR="${ROOT_DIR:-$(dirname "${BASH_SOURCE[0]}")/..}"`
   → 又是**主仓**；`:117` 取 `git -C "$ROOT_DIR" rev-parse --abbrev-ref HEAD`
   → `develop` → protected guard 命中 → exit 1；
6. `raw-issue-pull:134` 捕获失败打印 WARN。

即：**cwd 已经在合法的 dev 工位里，但整条链路都用「脚本物理位置」而非
「调用方工作目录」判定分支**，于是必然撞主仓的 develop guard。
`issue-sync` 自己在 `:116` 的注释里就写明了正解
（`Callers on develop must use: issue-sync --project /path/to/worktree`），
只是 `raw-issue-pull` 没照做。

后果不止噪音：`issue-sync create` 失败意味着 **platform title 归一化与
platform_ids 补全这一步被跳过**（WARN 原文即 "platform title normalization
may be incomplete"），属真实功能缺失，不只是刷屏。

## 2. scope 判定：两个独立子问题 → 两个 candidate

| | C-A 文案面 | C-B 调用路径面 |
|---|---|---|
| 缺陷类型 | 指引内容错误（幽灵名 / 缺 `--kind`） | 路径解析错误（ROOT_DIR 忽略 cwd） |
| 影响 | 误导 agent 走向不存在的 skill / 抄了会失败的命令 | title 归一化被跳过 + 每轮 ERROR/WARN |
| 改动面 | `bin/issue-sync`、`pretests-gate`、`wt-close`、`runtime/freely`、hooks 模板、2 份文档 | `bin/raw-issue-pull` 一处传参 |
| 验收方式 | 静态扫描 + 真实触发 guard 看输出 | 真实新建工位看输出 + 平台 title 核对 |
| 可独立回滚 | 是 | 是 |

两者无依赖、可分别回滚、验收手段不同 → **拆两个 candidate**，同属一个
milestone、一个 PR（改动面都很小，合并评审成本低于拆两个 PR）。

## 3. 方案方向评估

### C-A 文案面

**Option A（采纳）：单源常量 + 全域扫描断言**
把正确指引文案收敛为一份可复用文本，各活代码引用它；AT 扫描域扩到
`bin/` + `scripts/`（排除 tests 黑名单与 bak）+ 指定文档，白名单显式列出
合法出现位置及理由。
- 论据：根治「扫描域太窄」这个根因；下次新增载体自动被拦。
- 代价：需设计白名单，且 `runtime/freely` 改动触发 Step 2.5（必须同轮加 unit test）。

**Option B：只逐处替换字面量，不扩断言**
- 论据：改动最小、最快。
- 否决：正是 R33 的做法，已被本轮证伪会再次漏网（pretests-gate / wt-close /
  runtime 5 处都是 R33 之后仍残留的）。不解决根因。

**Option C：把这三个名字加入 skill aliases 让它们「重新可达」**
- 否决（理由已按 §1.0 的提交历史加强）：R28.5 的 alias 机制是给
  **2026-11 那批合并、且刻意保留兼容入口**的 skill 用的（`skill-map.yaml` 的
  `aliases` 只有 4 条，全是那批）。而这三个名字在 **2026-06-29 就已整体退役**
  （`2495ca2af` 改 `.bak` → `a4029fa15` 删除 → 目录与 `.bak` 均已清空），
  `skill-map` 从未把它们登记为 alias。给它们造 alias 等于**撤销 6 月的退役决策**，
  是真正的回退，且会让「唯一流程入口」重新分裂成三个。方向性错误。

**Option D：删掉所有含幽灵名的提示段落**
- 否决：guard 提示是 agent 在被拦截时唯一的自救指引，删掉等于降低可诊断性；
  且 `test-wt-close-protected-branch-guard` Test 6 要求 guard 必须引用 skill。

### C-B 调用路径面

**Option A（采纳）：`raw-issue-pull` 调 `issue-sync` 时显式传 `--project "$target_repo"`**
`target` 已含 `docs/B1-docs/raw-{key}`，可推出工位根；或直接用 `$(pwd)`
（`wt-create` 已 `cd` 到 dev 工位）。显式传参正是 `issue-sync:116` 注释指定的用法。
- 论据：一处改动、语义明确、不改任何 guard 判据、不放宽门禁；
  同时修好 title 归一化被跳过的功能缺失。

**Option B：让 `issue-sync` 的 ROOT_DIR 默认改用 cwd**
- 否决：`ROOT_DIR` 被 14 个 `issue-sync.d/*` 模块与 `_issue_sync_rebind_paths`
  依赖，改默认值会影响所有调用方（含 `--project` 显式传参者）， blast radius 远超本轮。

**Option C：`raw-issue-pull` 在 develop 上跳过 `issue-sync create`**
- 否决：会把「title 归一化缺失」变成静默行为，掩盖真实功能缺口；
  且当前 cwd 本就在 dev 工位，跳过是不必要的功能降级。

**Option D：把 protected guard 降级为 WARN**
- 否决：直接削弱门禁，违反铁律。

## 4. fidelity 基线

- C-A 的验收必须能推出「**活代码与文档全域**零幽灵名 + 指引含必填 `--kind`」，
  而不是「某几处被替换」；白名单必须逐条写明理由，防止用白名单掩盖真缺陷。
- C-B 的验收必须能推出「**真实新建一次工位**，输出无 ERROR/WARN，且平台 title
  已归一化」，而不是「单测里 mock 通过」。
- 两个 candidate 的 promotion gate 都必须包含「既有 AT 全绿 + 三门禁全过」，
  且 C-A 因触及 `runtime/freely` 必须满足 Step 2.5（同轮新增 `tests/unit/t-*.sh`）。

## 5. 价值判定

- **不过时**：本轮开工位当场复现，且 `runtime/freely` 的 5 处拒绝文案会在
  agent 每次 launch 被拒时打印，属高频指引路径。
- **未被覆盖**：R33 已合并但其 AT 扫描域不含这些载体；R32.5（#4302）是投影化
  议题，不管文案内容。
- **部分缩窄**：`.bak.py`（死代码）与两处 fixture 明确排除，理由见 §1.3；
  `commands.md` 因 `--skill` 未废弃而不改，理由见 §1.2。
- 结论：两个 candidate 均 **promoted**，无 dropped。