# 预研头脑风暴：feature-owned-test-pre-merge-family

## 背景

当前仓库的 canonical 语义已经把测试批次前缀统一到 `test-pre-merge-*`，而 `pre-test-merge` 主要保留在历史 issue/path/brainstorm 留痕中。

这轮新问题不是“测试批次是否存在”，而是：

1. 如果未来每个 `feature/*` 都必须先做 develop-like 预集成测试，再进入 `develop`
2. 那么 `test-pre-merge-*` 是否应在创建 feature worktree 时自动配对创建
3. 这个配对对象是否与 feature 完全同生命周期
4. 命名前缀究竟应保留 `pre-test-merge-*` 还是 `test-pre-merge-*`

## 已确认事实

### 命名现状

全仓当前真正的 branch / hook / runtime / governance enforcement 都以 `test-pre-merge-*` 为 canonical 语义：

- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `docs/system/workspace/hooks/pre-push.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/worktree/worktree-common.sh`

`pre-test-merge` 仍大量存在于以下位置，但它们主要是历史 issue/path 名称或兼容说明：

- 历史 `pre-brainstorms/`
- 历史 `epics/` story / issue / task / verification 路径
- 少量旧叙述文本

结论：
- 新增能力、规则、命令、分支名只应使用 `test-pre-merge-*`
- `pre-test-merge` 仅允许作为历史兼容说明出现，不再创建新的同名前缀 branch / worktree / command

### 现有能力现状

- `freely wt-create` 当前只创建请求的单个 branch/worktree，不会自动配对测试批次
- `test-pre-merge-*` 当前定义为临时批次，必须从当前 `develop` 新建，用完即删
- 当前规范默认是“按需启用测试批次”，而不是“每个 feature 必经独立测试批次”

## 用户提出的新目标

目标并不是共享一个测试批次，而是：

1. 每个 `feature/*` 在进入 `develop` 前，都有自己的 develop-like 预集成测试面
2. 这个测试面必须以 canonical sibling worktree 形态存在，供多个测试 subagent 并行 `cd` 进去执行
3. `develop` 不再承担 merge 前测试面，避免多个待测 feature 相互污染
4. 若某 feature 的测试批次在验证期间落后 `develop`，则必须先吸收最新 `develop`，再重跑全量测试，之后才允许 promote 到 `develop`

这套目标本质上把 `test-pre-merge-*` 从“按需共享批次”提升为“每个 feature 的必经预集成 lane”。

## 关键问题

### 问题 1：`test-pre-merge-*` 是否应与 feature 一对一绑定

直觉上看，一对一绑定很合理，但如果把它定义成“完全同生命周期”，会出错。

原因：

1. feature 可能持续数天或更久存在
2. 其对应的测试批次可能因为 `develop` 前进而 stale
3. stale 后规范要求删除并重建测试批次
4. 但 feature 本身不应随之删除，只应继续存在并等待下一轮验证

所以更准确的模型不是：

- `feature/foo` <-> 一个永久固定的 `test-pre-merge/foo`

而是：

- `feature/foo` 拥有一个 `test-pre-merge` family
- 任一时刻最多一个 active canonical batch
- batch stale 后删除，再从当前 `develop` 重建新的 batch

结论：
- 生命周期不是“完全相同”
- 而是“feature owns a renewable test-pre-merge family”

### 问题 2：feature 创建时是否应立即自动创建测试批次 worktree

优点：

- 每个 feature 从 day-1 就具备独立的 develop-like 测试面
- 多个测试 subagent 可直接进入各自批次 worktree 并行执行，不抢 branch checkout
- 推广到“所有 feature 必经预集成测试”时，开发者心智更统一

成本和风险：

1. 很多 feature 在早期只需要本地实现和 unit/smoke，自始至终未必立刻需要 develop-like 集成面
2. 自动创建 paired worktree 会提前带来 tooling sync、依赖安装、缓存占用和本地目录膨胀
3. 若将“删除 feature 时自动删除 paired batch”做成强耦合，会误删仍需保留验证证据或待 rebuild 的测试面
4. 若 paired batch 固定不重建，会与 stale/rebuild 规则冲突

更稳妥的设计不是“eager hard-pair”，而是：

- 要么 `wt-create` 支持显式开关，例如 `--with-test-pre-merge`
- 要么采用“mandatory but lazy materialization”：
  - 每个 feature 在进入 promotion / integration testing 前必须 materialize 自己的 `test-pre-merge-*`
  - 但不是在 feature 创建第一秒就强制创建磁盘 worktree

当前更倾向的收敛：

- 如果治理改为“所有 feature 进入 develop 前都必须过自己的 test-pre-merge lane”，则：
  - `test-pre-merge` 是 feature 的必经 gate
  - 但不一定需要在 `wt-create` 时 eager 创建
  - 更适合在“首次需要 premerge-integration”或“进入 promote-check”时自动 materialize

### 问题 3：删除是否应成对发生

不能简单做成：

- 删除 feature -> 必删对应 `test-pre-merge-*`

因为存在三种情况：

1. feature 已保留，但旧测试批次 stale，应该先删测试批次、保留 feature
2. feature 即将 promote，但测试批次仍需保留到 verification evidence 写回完成
3. feature 被放弃或 merged-clean 后，才适合一并 retire 其 active batch family

更合理的规则：

- active test-pre-merge batch 的存在权依赖其来源 feature
- 但 cleanup 判定仍独立于 feature cleanup
- stale batch 可先删，feature 继续
- feature retire 时，应同时检查并清理其仍存活的 active/stale test-pre-merge family members

## 命名收敛建议

唯一 canonical 前缀：

- `test-pre-merge-*`

不再新增：

- `pre-test-merge-*`
- 单例 `pre-test-merge`

兼容策略：

- 历史 path / issue / brainstorm 可以继续保留 `pre-test-merge`
- 但必须在文档中显式声明其 canonical 语义映射到 `test-pre-merge-*`
- 新命令、新 hook、新工作树、新测试数据、新分支样例全部只用 `test-pre-merge-*`

## 命名派生建议

若 feature 采用：

- `feature/foo-bar-20260405-1615`

则其 active test batch 可派生为：

- `test-pre-merge/foo-bar-20260405-1615`

若需要 rebuild：

- `test-pre-merge/foo-bar-20260405-1615-r2`

这样能同时满足：

- 仍属于同一 feature-owned family
- 不强迫重用已 stale 的旧 batch 名称
- 允许 runtime / cleanup 清晰识别 family

需要单独验证的一点：
- 现有 `governance-check`、`pr-merge-guarded`、worktree path 派生、hook 正则是否允许 `test-pre-merge/<topic>` 这种 slash 形式；若不允许，则应改为：
  - `test-pre-merge-foo-bar-20260405-1615`
  - rebuild: `test-pre-merge-foo-bar-20260405-1615-r2`

当前更保守的建议是继续沿用现有正则友好的 dash 形式，而不是新增 slash 变体。

## 工作树与未跟踪文件

`git worktree` 只带 tracked 内容，不会自动带 develop 上的 untracked 文件。

因此 paired / family batch 的启动不应依赖“复制 develop 全部未跟踪文件”，否则会把偶然脏状态带入测试面。

更合理的策略：

1. 新建 `test-pre-merge-*` worktree 后，执行受控 `sync-tooling`
2. 用 install/bootstrap 命令重建依赖与缓存
3. 如确有必须跨工位携带的本地资产，只允许白名单同步，不做脏复制

## 初步结论

1. canonical 前缀必须唯一化为 `test-pre-merge-*`
2. 若未来改成“每个 feature 必经预集成 lane”，则应把 `test-pre-merge` 定义为 feature-owned family，而不是与 feature 完全同生命周期的一对一固定对象
3. `test-pre-merge` 必须以 canonical sibling worktree 形态 materialize，供测试 subagent 并行 `cd` 进入执行
4. 不建议把 eager auto-create 直接硬编码进当前 `wt-create` 默认行为；更合理的是：
   - 先在治理上把“是否 mandatory”定清
   - 再决定是 `wt-create --with-test-pre-merge` 还是 promotion 前自动 materialize
5. cleanup 应按 family 生命周期处理，而不是简单“删 feature 时必删唯一 paired batch”

## 不能只靠文档指导的约束

这条能力如果成立，不能停留在 `CONSTITUTION` / `LAWS` / skill reference 的口头指导层。

原因：

1. “每个 feature 进 `develop` 前都应经过自己的 `test-pre-merge`”本质上是 promotion gate，不是建议
2. “测试批次 stale 后必须重建”本质上是可执行拒绝条件，不是说明文字
3. “测试必须在 dedicated worktree 并行运行”本质上依赖物理隔离，不能靠操作者记忆

所以这里需要明确区分：

- 文档负责定义语义和边界
- hook / gate / wrapper 负责在关键入口阻止错误路径

### 应由 machine-enforced 的约束

#### 1. 命名前缀唯一化

约束：
- 新增 branch / worktree / runtime target / help text 不得再产出 `pre-test-merge-*`
- canonical 只允许 `test-pre-merge-*`

适合落点：
- `wt-create` / 后续 paired-batch create 命令
- 相关 hook / guard 的 branch pattern 校验
- `governance-check` 对新增规范样例与 receipt 的扫描

文档不足之处：
- 仅靠文档，后续很容易在新脚本、测试数据或 prompt 里再次引入第二前缀

#### 2. 进入 `develop` 前的必经验证面

约束：
- 若法律最终升级为“feature 必经自己的 `test-pre-merge` lane”，则没有 active verified batch receipt 的 feature 不得 promote 到 `develop`

适合落点：
- `freely pr-merge-guarded` 的 develop promotion 入口
- `governance-check` 对 merge receipt / issue evidence / verification artifact 的审计

文档不足之处：
- 只写在 skill 里，agent 仍可能直接从 feature merge 到 develop

#### 3. stale batch 不得继续消费

约束：

### 预研收敛更新（2026-04-05）

这轮讨论已经不只是“命名统一”或“是否 paired create”的问题，而是暴露出旧模型的治理痛点：

1. 旧规则允许 `feature/*` 直接 merge 到 `develop`，导致“忘了先过预集成 lane”仍然存在真实逃逸面。
2. 若多个 feature 直接先并到 `develop` 再测，会互相污染，失败根因不清，也会阻塞其他待测 feature。
3. 若多个 feature 想并行做 develop-like 集成验证，单仓切 branch 的方式会互相抢占；必须依赖独立 worktree 批次。
4. 现有 canonical 文案仍把 `test-pre-merge-*` 写成 “shadow batch + feature replay to develop”，与“让 develop 只接收经过预集成测试的东西”这个目标冲突。

因此，这个预研项真正要决定的是：

- `develop` 的唯一正常 promote 单位是什么
- `multi` 组合测试 lane 是验证证据，还是直接 promote 单位
- 这些约束由哪些 machine-enforced surfaces 承担

## 待冻结的设计决策

### 决策 A：develop 入口应从“feature replay”切到“test-pre-merge family promote”

当前更倾向的方向：

1. `feature/* -> develop` 作为正常路径应被禁止。
2. `develop` 的正常 merge source 应改为：
   - `test-pre-merge-*`
   - `hotfix/*`
3. 每个 develop-bound feature 必须先 materialize 自己的 `test-pre-merge` family 成员，并在对应 batch worktree 中完成主线前集成验证。

这样做的收益：

- `develop` 只吸收“已经在 develop-like 环境测过的树”
- 避免 feature 直接 promote 时把“忘测”变成制度漏洞
- protected branch gate 更容易明确禁止 `feature/* -> develop`

### 决策 B：`multi` 不应再发明第二种前缀

这轮预研已经收敛出一个命名结论：

- 不再引入 `test-pre-multi-merge-*`
- 若需要 multi 语义，只能放在 `test-pre-merge-*` family 里表达

推荐命名：

- 单 feature 批次：`test-pre-merge-<feature-key>-<ts>`
- multi bundle 批次：`test-pre-merge-multi-<topic>-<ts>`

这样：

- `develop` gate 只需要维护一个 canonical family 前缀
- 不会再次引入双前缀混乱

### 决策 C：multi bundle 的 promote 语义要区分“默认路径”和“显式 bundle 路径”

对 multi 闭环，subagent 评审出现两种不同结论：

1. 方案一：multi 只提供额外交互验证证据，最终仍分别走各自单 feature lane promote。
2. 方案二：multi 一旦作为 bundle 验证通过，就应直接作为最终 promote 单位进入 `develop`，否则会在“已测树”和“实际落地树”之间重新产生漂移。

当前更合理的收敛不是二选一绝对化，而是分成两条治理路径：

#### 默认路径：single-feature promote

- 每个 feature 都有自己的 `test-pre-merge-*` family。
- 一般情况下，进入 `develop` 的 promote 单位是该 feature 的 active single-feature batch。
- 若只需要验证单 feature 对 develop 的影响，不应额外制造 multi batch。

#### 显式 bundle 路径：multi promote

只有在多个 feature 被明确声明为“必须同进同退的 bundle”时，才允许使用 `test-pre-merge-multi-*` 直接 promote 到 `develop`。

此时必须同时满足：

1. multi batch 从当前 `develop` 创建
2. batch 内包含的 feature 列表、sha、merge 顺序被 machine-readable manifest 固定
3. 通过后只 promote 这个 multi batch，不再把成员 feature 的 single batch 再各自 promote 一遍
4. `develop` 若在此期间前进，或任一来源 feature head 变化，multi batch 立即 stale，必须删除并重建

这样可以同时满足：

- 默认情况下保持最简单的 single-feature 闭环
- 对强耦合 bundle，保证“测试通过的就是实际进入 develop 的树”

## machine-enforced 设计面（预研结论）

这轮讨论已经确认，以下内容不能停留在文档：

1. `develop` 禁止直接接受 `feature/*`
2. `develop` 只接受 `test-pre-merge-*` family 与 `hotfix/*`
3. `test-pre-merge-*` / `test-pre-merge-multi-*` 必须从当前 `develop` 创建
4. multi promote 必须要求 machine-readable manifest，至少记录：
   - `base_develop_sha`
   - `included_features`
   - `feature_shas`
   - `merge_order`
   - `created_at`
5. stale 检测必须进入 hook / gate / runtime status，而不是只在 skill 文案提示

优先 enforcement 落点：

1. `pr-merge-guarded`
2. `governance-check` / `governance-promotion-gate`
3. `wt-create` / 后续 batch-create wrapper
4. runtime / fleet-status 对 stale batch 与 active batch family 的暴露

## issue materialization 建议

这项预研不宜一次性 materialize 成一个过大的 issue。更合适的拆法：

1. issue A: `test-pre-merge family promotion model`
   - 冻结 develop merge source 规则
   - 冻结 single / multi 的 promote 语义
   - 对齐 `CONSTITUTION` / `LAWS` / branch-management references
2. issue B: `protected branch gate enforcement for test-pre-merge family`
   - 调整 `pr-merge-guarded`
   - 调整相关 hook / `governance-check`
   - 增加 shell regression tests
3. issue C: `test-pre-merge family lifecycle automation`
   - batch create wrapper
   - stale / rebuild detection
   - cleanup / runtime status surfaces

结论：

- 在 issue A 尚未 materialize 前，不应直接改 `CONSTITUTION` / `LAWS` / gate 实现。
- 先把 promote model 与 multi 语义在 candidate 中冻结，再由 milestone-owned issue 驱动后续修改。
- 若来源 `develop` 已前进、或 evidence 断裂、或 batch 与当前 target 已不再权威，则该 `test-pre-merge-*` 不能继续被当成有效验证面

适合落点：
- `pr-merge-guarded` 在 promote 前做 freshness check
- `governance-check` 做离线审计
- runtime / `fleet-status` / `live-status` 明确把此类 batch 标成 stale

文档不足之处：
- stale 是最容易“大家都知道但继续拿来用”的违规点，必须有硬拒绝或显式红灯

#### 4. 测试必须在正确 lane / worktree 中运行

约束：
- `feature-local` 不得在 protected branch 上伪装执行
- `premerge-integration` 不得在 `develop` 冒充
- 多个测试 subagent 应各自在目标 worktree 内执行，不依赖共享树切 branch

适合落点：
- `./bin/test-lane`
- worker / manager prompt contract
- 必要时 runtime 发 worker 时带 machine-readable `Worktree:` header

文档不足之处：
- 纯靠 README/skill，最常见的退化就是“先在当前树里跑一下看能不能过”

#### 5. 清理必须带 family 语义

约束：
- cleanup 不能只删 feature 本体，还要检查其 active/stale `test-pre-merge` family members
- 但也不能简单做成 feature 删除时无脑级联删测试批次

适合落点：
- 后续 `wt-remove` / cleanup helper
- `governance-check` 对残留 family members 的提示

文档不足之处：
- 没有工具面，最终一定会留下 stale batch 或误删仍需证据的批次

### 更适合先留在文档/skill 的内容

以下内容暂时不应先硬编码进 hook：

1. `wt-create` 是否默认 eager 创建 paired batch
2. paired batch 的命名细节是否带 rebuild suffix
3. 何时用 `--with-test-pre-merge`，何时 lazy materialize
4. family cleanup 的具体 UX 和命令形态

这些仍需要先通过 issue/materialization 收敛，再决定工具交互。

### 建议的 enforcement 分层

第一层：轻量 wrapper / gate
- `test-lane`
- `pr-merge-guarded`
- 未来的 test-pre-merge create / cleanup helper

第二层：hook
- 阻止错误 branch 上直接开发或错误完成 merge
- 不要一开始就让 hook 承担全部生命周期推理

第三层：审计与状态面
- `governance-check`
- `fleet-status`
- `live-status`

这样分层的原因：
- hook 适合阻止明显违规
- wrapper/gate 适合做有上下文的路径判断
- 审计/status 适合识别 stale、残留 family、receipt 缺失这类事后或跨树事实

## 当前更稳的收敛方向

若后续决定升级成“feature 必经 test-pre-merge lane”，最稳的推进顺序不是先改 `wt-create` 自动配对，而是：

1. 先在治理上定清是否 mandatory
2. 再把 `pr-merge-guarded` 变成真正的 promotion gate
3. 再补 freshness / stale check
4. 再补 create / cleanup helper
5. 最后才决定 `wt-create` 是否默认 eager paired creation

这样能避免把错误心智先固化进工具默认行为。

## 下一步需要回答的问题

1. Freely 是否真的要把“每个 feature 必经独立 test-pre-merge lane”升级为新的全局默认法律
2. 若答案是要：
   - `wt-create` 是否新增 paired creation 开关
   - 还是 `pr-merge-guarded` / promote 流程在缺失 active batch 时拒绝继续并提示创建
3. batch family 的 canonical naming 与 rebuild suffix 应如何落到 hook / regex / cleanup 规则
4. `wt-remove` / cleanup 流程是否需要新增“按 feature family 清理 test-pre-merge members”的能力

## Status Reconcile

- reconcile_status: `partially_materialized_and_deferred`
- why: `后续 canonical truth 已经先冻结了 test-pre-merge promote model 与 promotion gate enforcement，但“feature owns a renewable batch family”以及 eager/lazy materialization、family cleanup automation 仍是 follow-on。`
- stale_statement:
  - `把 feature-owned renewable batch family、rebuild orchestration、family cleanup automation 读成当前仓库已经完整落地的既成事实。`
- canonical_truth:
  - `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
  - `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/issues/test-lane-routing-and-enforcement-governance.md`
- materialized_scope:
  - `canonical naming 已统一到 test-pre-merge-*`
  - `develop-bound guarded promotion 已被收紧到 canonical test-pre-merge path`
- deferred_scope:
  - `feature-owned renewable family lifecycle automation`
  - `stale batch rebuild orchestration`
  - `family-aware cleanup helper`
- follow_on_note: `当前仓库里还没有单独名为 feature-owned-test-pre-merge-family-governance 的 owner issue；不要伪造不存在的 canonical pointer。family lifecycle automation 目前仍只能作为 follow-on 方向挂在现有 promotion-gate / lane / cleanup 讨论之后。`
- reconcile_note: `后续审计不应再把这篇里对 family automation 的构想当作“已经落地但门禁失效”；它们是明确未完结的 follow-on，不是功能回退。`
