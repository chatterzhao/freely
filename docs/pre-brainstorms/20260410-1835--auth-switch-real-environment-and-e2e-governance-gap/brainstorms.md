# Brainstorm - 20260410-1835--auth-switch-real-environment-and-e2e-governance-gap

一句话范围：本 worktree 只负责收紧测试治理的顶层验收标准, 检查 Freely 测试框架为什么没能兜住既有功能回归, 并明确为什么真实环境与端到端验收没有成为稳定硬门。

## Problem

这次 Codex 账号切号/启动恢复问题，没有在前置测试和最近几次 owner 修改中被发现。问题不只是“缺一个测试用例”，而是要追清从高层治理到 owner issue、`pre-tests.md`、hook/gate、merge followthrough 的整条链，为什么没有把“真实环境 + 端到端启动恢复”作为必过门。

本条预研只处理 testing/governance 线：

- 这类测试在体系里应该叫什么
- 高层真源是否已要求
- 最近 auth/account-switch owner 为什么没把它变成必测
- hook/gate 为什么没兜住
- 后续怎样让其他功能修改也能被这类测试面兜住

## Scope

1. 归类本问题对应的测试类型：
   - `Real-Environment`
   - 启动恢复链路上的 `End-to-End`
   - 对 Freely 自治能力而言，也属于 dogfood / post-merge followthrough 面
2. 审计高层真源：
   - `CONSTITUTION`
   - `LAWS`
   - IBM / PRD / pre-tests / issue materialization skill 真源
3. 审计执行门禁：
   - `pretests-gate`
   - `pre-commit.sh`
   - `pre-merge-commit.sh`
   - `governance-merge-gate`
4. 审计最近 auth/account-switch 相关 owner 的 `pre-tests.md`、review、verification 结论
5. 形成原因分层：
   - 规则缺失
   - 规则存在但 owner contract translation 变窄
   - gate 只消费既有 contract
   - 真实环境 surface 被合法豁免
   - review / residual risk 判断失真

## Out Of Scope

- 不在本条预研里直接改 runtime 切号代码
- 不把 merge gate 改成替 issue owner 自动发明测试设计
- 不要求全仓历史 issue 一次性重写

## Confirmed Facts

1. 高层真源不是没有要求：
   - `pre-tests.md` 固定四章 `Unit / Integration / End-to-End / Real-Environment`
   - Freely 自治能力默认还应回答 post-merge integration / real-environment / dogfood acceptance
2. hook/gate 不是空壳：
   - `pretests-gate` 确实检查四章、标量字段、not-applicable reason、acceptance items、artifact
   - `pre-commit` 会跑 `pretests-gate --staged-only`
   - `governance-merge-gate` 也会消费 owner issue 绑定的 `pre-tests.md`
3. 最近 auth/account-switch 的 narrow owner 没把“切到坏号后真实启动 Freely 观察日志”列为必过门：
   - `End-to-End` 和 `Real-Environment` 被标成 `protected_environment_only`
   - 替代证据主要是 integration 脚本和治理检查
4. 更早、更宽的 watchdog / unified-slot owner 其实写过更强的真实环境 contract，包括：
   - current dead slot 被跳过
   - `freely start` 不应在坏 slot 上继续 launch
   - manager bootstrap 应等到 later usable slot
5. 因此这次缺口不是“能力仍停留在研究”或“某个 worktree 丢了能力”，而是：
   - 高层 contract 存在
   - gate 也存在
   - 但最近窄 owner 没有继承这类真实环境 acceptance，且被合法豁免掉了
   - 同时，当 issue/pre-tests 文字只写 `bin/ai` / `codex exec` 这类命令面而不写 `auth switch` 等 family 词时，旧 gate 触发词也过窄，存在 adequacy guard 被绕开的风险
6. 用户要求本 worktree 不承担 runtime 修复，只负责把“为什么没发现、以后如何兜住”这条治理链追清。
7. 随着 runtime 线进一步收紧为 exec-only 单一 truth，这条治理线也必须同步收紧：
   - auth switch / startup recovery / watchdog 相关 owner 不能只写“inventory-level integration”
   - 必须明确覆盖真实 `codex exec` 驱动的切号与启动恢复验收
8. 因此这里要兜住的，不只是一般意义上的 `Real-Environment`，而是“以真实 exec 为最终判定面的 End-to-End / Real-Environment acceptance”。
9. 关于测试环境 lane 的最新边界也已经澄清：
   - `test-pre-merge-*` 只对应 `premerge-integration`
   - 它可以承担主线前集成验证，但不能替代 merge 后 canonical protected worktree 上的 `post-merge-followthrough`
   - 因此这次缺口不能简单解释成“没开 test-pre-merge 批次”；真正缺的是顶层验收标准没有把 feature-local 实坏号复现、premerge-integration、post-merge followthrough 这三层边界同时讲清
10. 用户最新又进一步澄清了 auth-switch 顶层语义，这也属于治理层必须写清的验收标准：
   - `freely start` 正常启动不应做开局全量健康扫号
   - 自动切号只在真实使用失败后触发
   - 自动切号找到第一个真实可用 slot 就停
   - 手工 `bin/ai switch codex` 才允许全量 sweep
   - 后台/定时 Codex availability probe 默认应关闭，因为真实 `exec` 探测会消耗 token

## Taxonomy

### 这类测试叫什么

对本问题，单一标签不够，至少要同时承认三层：

1. `Real-Environment`
   - 使用真实账号/slot/live auth，而不是纯 mock
2. `End-to-End`
   - 从坏号状态进入，触发 runtime 启动恢复，最终观察 `freely start` 和日志
3. `Post-merge application-native followthrough`
   - 若某些受保护环境或真实账号差异只能在 canonical lane 验证，则必须在 `pre-tests.md` 里提前写明

### 为什么以前没发现

不是“没有四章”。

而是最近 owner 把关键 surface 合法写成 not-applicable / protected-only，导致 gate 只检查“写得对不对”，不会检查“这次 scope 为什么能跳过真实环境启动恢复”。

## Root Cause Direction

### A. Owner contract drift

更宽的历史 owner 讲过真实启动恢复 contract，但最近的窄 owner 把自己定义成“preferred auth method narrow fix”，于是把更重的 real-env / E2E 面切掉了。

### B. Gate 只消费当前 owner truth

这是系统设计本来就明确的边界：gate 只消费当前 owner issue 绑定的 `pre-tests.md`，不会扫描历史更宽 contract 自动补回责任。

### C. `protected_environment_only` 被用得过宽

它原本应该表达“确实只能在受保护环境里验”，但最近被用来替代“真实坏号 + freely start + 日志观察”这类本来就应进入当前 owner 验收面的内容，导致风险被平滑掉了。

### D. Review 结论对残余风险判断过轻

当 review 同时宣称：

- narrow bug fix
- no architectural implications
- residual risk none

而实际 touched surface 已经关系到 auth switching / startup recovery / slot semantics 时，review 面已经偏乐观。

### E. 缺少 capability-family adequacy guard

当前 gate 会检查四章、结构、artifact、状态，但不会检查：

- 某个 owner 明明触到了 `auth switching / startup recovery / watchdog`
- 却把 `End-to-End` 和 `Real-Environment` 一起豁免
- 并只留下 integration/prose 级替代证据

这正是这次回归能合法穿过 gate 的关键设计缺口。

### F. “live evidence” 词面仍可能过虚

如果 IBM / PRD / checklist 只写“保留 live evidence”而不点名真实 `bin/ai`、真实 `codex exec`、真实 `freely start`，下游 owner 仍可能用抽象 artifact 名称把真实命令面稀释掉。

### G. 顶层验收标准对 test lane 分层表达还不够硬

这次进一步暴露出另一个高层设计问题：即便已经有 `feature-local / premerge-integration / post-merge-followthrough` 三条 lane，owner 很容易把它们理解成“任选一条有 artifact 就算覆盖”，而不是能力级分层验收。

对 auth switch / startup recovery / watchdog 这类问题，至少要区分：

1. dedicated feature / worker worktree 中的真实坏号复现与修复回归
2. `test-pre-merge-*` 中的主线前集成装配验证
3. merge 后 canonical protected worktree 中的真实环境 followthrough

如果顶层 skill / quality bar 不明确指出“这些 lane 不是互相替代关系”，那么下游 owner 仍可能错误地认为开了 `test-pre-merge-*` 就足以覆盖真实启动恢复验收。

### H. 顶层验收标准还缺少“触发时机与停止条件”约束

这次不只是 lane 没分清，连自动恢复的行为契约也没有在高层被写硬，导致实现容易把不同语义混成一条：

1. 正常启动
2. 真实失败后的内部恢复
3. 手工 `switch codex`
4. 后台定时 availability probe

如果 skill / quality bar / gate 只要求“有真实 `bin/ai` / `codex exec` 证据”，却不要求说明：

- 是启动前探测，还是使用中失败后恢复
- 是找到一个可用就停，还是必须全量 sweep
- 是否允许后台常驻 probe

那么实现即使“有真实环境测试”，也可能在错误的时机执行过度探测，依然通过表面验收。

## Chosen Approach

选择最窄、可执行、且不把 gate 变成“自动发明测试设计”的修补：

1. 先不改 runtime，也不让 merge gate 扫历史所有 owner。
2. 只在 issue-bound `pre-tests` adequacy 上加一条 follow-on guard：
   - 如果 issue 是 follow-on owner
   - 且 scope 落在 `auth switch / account switch / slot recovery / startup recovery / watchdog` family
   - 则不能把 `End-to-End` 与 `Real-Environment` 两章同时写成 `protected_environment_only`
   - 除非 `Acceptance Items` 里至少保留一条 machine-readable、artifact-backed 的 `real_env` 或 `post_merge_dogfood` 证据
3. 同步把这条要求写回 IBM skill / checklist / quality bar，避免下游 owner 再把它理解成“可以用 integration 脚本完全替代真实启动恢复”
4. 继续考虑是否要把 lane 分层要求上提到更高层真源，明确 `test-pre-merge-*` 不能替代 post-merge followthrough，也不能替代 feature-local 的真实坏号恢复复现
5. 对 auth/switch/startup-recovery/watchdog family，再加一条顶层契约：
   - `freely start`、自动恢复、手工 `switch`、后台 probe 的触发时机与停止条件必须分别写清

### Why This Instead Of Broader Options

1. 不要求 gate 猜 changed paths 或自动推导完整测试矩阵。
2. 不要求 follow-on owner 重新继承所有历史 pre-tests；只锁住这次真正漏掉的“不能双豁免”。
3. 仍保留 `protected_environment_only` 的合法用途，但要求保留至少一条更强的 live-evidence surface，避免把真实 `freely start` / 日志观察风险平滑掉。

## Implementation Targets

1. `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
2. `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
3. `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
4. `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
5. `docs/system/workspace/scripts/quality/pretests-gate`
6. `docs/system/workspace/scripts/tests/test-pretests-gate`

## Questions To Answer In Followthrough

1. 哪些类型的改动必须禁止把 `End-to-End` / `Real-Environment` 全部豁免掉
2. `protected_environment_only` 是否需要更窄白名单，或需要 replacement evidence 至少包含哪类真实链路
3. `pretests-gate` 是否应在某些 touched capability family 上增加 adequacy 提示，而不是只检查结构
4. 是否要把“账号切换 / 启动恢复 / runtime watchdog”归成一个必须保留真实环境验收的 capability family

## Verification Plan

1. 对最近 auth/account-switch 相关 owner 逐个核对：
   - issue scope
   - `pre-tests.md`
   - code review
   - gate 消费路径
2. 明确列出：
   - 哪些真实环境 / E2E 面被要求了
   - 哪些被豁免了
   - 豁免理由是否过宽
3. 产出后续改进方向：
   - 高层 wording 是否要收紧
   - IBM skill / checklist 是否要加约束
   - `pretests-gate` / merge gate 是否要加 adequacy diagnostics
4. 形成一个明确门禁原则：
   - 只要 owner scope 触达 auth switch / slot recovery / startup recovery / watchdog family，就不能把 `End-to-End` 与 `Real-Environment` 同时降成 `protected_environment_only`，除非 acceptance items 至少保留 `real_env` 或 `post_merge_dogfood` 级证据。
5. 明确 lane 分层结论：
   - `test-pre-merge-*` 只能回答 premerge integration 问题
   - 它不能替代 worker/feature worktree 内的真实坏号复现
   - 也不能替代 merge 后 protected branch 的 canonical followthrough
6. 明确行为契约结论：
   - 自动恢复不是全量 sweep
   - 手工 `switch` 才是全量 sweep
   - 后台定时 Codex probe 默认不应存在

## Exit Criteria

1. 已写清这类测试属于 `Real-Environment + End-to-End`，并可带 post-merge followthrough 面
2. 已写清这次没发现不是“没规则/没 gate”，而是 owner contract drift + legal exemption 过宽
3. 已形成后续治理修改的明确落点，而不是泛泛地说“再多写些测试”
4. 已明确把“真实 exec 驱动的切号/启动恢复验收”上升为这类 owner 的顶层 adequacy 要求
5. 已明确写清 `test-pre-merge-*` 的能力边界，避免它再次被误当成“可以替代真实环境 followthrough 的万能测试环境”
6. 已明确把“触发时机 + 停止条件 + 是否允许后台 probe”纳入顶层验收标准，而不是只检查有没有真实命令证据
