## 0. 设计意图审计（先于方案）
### B0 前置：关键词广搜 + 多文档交叉
- 关键词族表（≥3 组；搜 docs/ bin/ .freely/）:
  - 功能名：`freely install`、`install-state-check`、`freely-package` → `bin/freely:23,36,40`、`docs/system/workspace/commands.md:41-50`、`bin/install-state-check`
  - 机制名：`@freely-dev-path`、`PATH entry`、`activate` → `bin/freely:37,40`、`~/.zshrc:75`（用户机）、`docs/B2-docs/gate/platform/raw-20261105T121046Z/...`
  - raw key / 门禁名：`raw-20261108T134701Z`、`raw-20261114T080106Z`、`check-runtime-size`、`check-bin-projection` → `.freely/goal-arch-debt.md:66,155,421,1666`、`bin/check-runtime-size`、`bin/check-bin-projection`
- 怀疑多份文档：是。安装态主题存在「当前生效实现（`bin/freely-package`、`bin/install-state-check`）」「历史局部文档（`bin/freely` 头部注释）」「当前权威恢复点（`docs/system/workspace/commands.md` §install-state-check 与 raw-20261114T080106Z 的 IDN）」三类，不能只读头部注释就下结论。
- 三类分层表:
  - 当前生效实现：`bin/freely-package --version auto --activate`、`bin/install-state-check`（权重：现状）
  - 历史局部文档：`bin/freely:23,36,40` 的 `freely install` 承诺（权重：仅背景，已被 R16 判定不做）
  - 当前权威恢复点：`docs/system/workspace/commands.md:41-50`、`docs/B2-docs/platform/issue-sync-entrypoint/raw-20261114T080106Z/...`（权重：当前真相）
- 矛盾清单：`bin/freely` 注释承诺 `freely install` 自动移除 `@freely-dev-path` 行；`commands.md` 只声明 `freely-package --activate` 与 `install-state-check`，无任何 install 分派。后者取代前者，前者过期。
- 二元决策：**继续**（方向 B：删除不存在的命令承诺，改用真实激活入口，并新增静态命令名契约检查；不实现第二份安装机制）。

### 外部锚点（引用原文，至少两类）
- 设计文档：`docs/system/workspace/commands.md:43`「`./bin/install-state-check`」、`:50`「不一致时返回非 0，并提示 `freely-package --version auto --activate`」。
- 既有验收测试：`docs/system/workspace/scripts/tests/test-install-state-cli.py`「it is deliberately NOT wired into runtime/freely, which sits exactly at its 27166-line budget」。
- 门禁源码注释/理由：`docs/B2-docs/gate/platform/raw-20261105T121046Z/code-reviews/implementation-decision-note.md`「不实现 `freely install`（issue 修复方案第 3 项的文档缺口另见残余风险）」。
- 既有同类实现：`bin/freely-package`、`bin/install-state-check`（薄投影，单一真相源）。

- 判定（五选一，附证据）：**实现偏差**——入口注释与命令真源不一致，导致用户按注释抄命令必然失败；不是设计缺失（R16 已明确方案 B）。
- 与既有断言的冲突：有。`bin/freely` 注释的 install 承诺与 `test-install-state-cli.py` 钉住的「不新增 runtime 分派、27166 行预算」冲突；必须改注释，不改 runtime。
- 影响面：`bin/freely` 头部注释、静态命令名契约检查（新）、`docs/system/workspace/commands.md`（真实入口说明），以及双平台副本一致性。

## 0.1 全局适配反思（四问）
- Q1 类别：流程能力 + 治理元数据修复（入口文档与 dispatcher 的一致性）。
- Q2 职责边界：`runtime/freely` 拥有命令分派；`bin/freely-package` 拥有安装态切换；本轮只修注释与契约检查，不产生第三真相源。
- Q3 结构性冲突：若按字面实现 `freely install` 会与 `freely-package --activate` 职责重叠，并在 27166 行预算上再加分派——反设计，排除。
- Q4 门禁失配：现有 `check-bin-projection` / `check-runtime-size` 测的是投影与行数，不测「文档承诺的命令是否存在」；新增静态契约检查补上这一维度，不放宽任何既有门禁。

## 1. Input / Problem / Brainstorm
- Input：raw-20261108T134701Z，R16 自举发现，GitHub #4746 与 Gitee IKTSRS 均已 open。
- Problem：`bin/freely:23,36,40` 承诺 `freely install` 与自动移除 `@freely-dev-path`，全仓无实现；用户机 `~/.zshrc` 留有该标记。
- Option A：实现 `freely install`（含 zshrc 标记增删）——与 `freely-package --activate` 重叠，违反 27166 行预算，排除。
- Option B：删除承诺，指向真实入口，新增静态命令名契约检查——采用。
- Option C：只删注释不加检查——同类脱线会复发，排除。

## 2. Decision: Option B
- 理由：单一安装真相源 + 可机读的防复发契约，改动面小、杠杆高，符合项目意图（吃狗粮、自举修自己）。
- 验收：RED 证明 baseline 仍承诺不存在的命令；GREEN 证明代码/文档无未实现命令名且契约检查能抓出反例。

## 3. Candidate
- candidate_id: C-20261108T134701Z-A
- status: promoted
- milestone: M-20261108T134701Z-A
