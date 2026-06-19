# PRD Quality Bar

`freely-doc-B2_IBM-execution` 中的 `prd.md` 不是面向人类回忆的摘要，而是给后续 AI 和人类共同消费的执行控制面。

## Minimum structure

达到 `done_b2_ibm` 前，`prd.md` 至少应覆盖：

1. `Goal`
- 这轮真正想让产品或治理发生什么变化

2. `Why Now`
- 为什么当前值得做，而不是继续停留在研究或等待

3. `Product Surface`
- 本轮会触达哪些产品面、文档面、技能面或运行面

4. `Non-Goals`
- 本轮明确不做什么，防止 scope 漂移

5. `Non-Negotiables`
- 不能为了“做出来”而突破的边界、治理规则、不变量或约束

6. `Context Pack`
- 当前事实、证据来源、已有实现、外部研究、前置限制

7. `Decomposition Tree`
- 目标如何被拆成若干可理解、可排序、可进入 dev-loop 的子块

8. `Prototype Path`
- 在全面实现前，最小验证原型或最小演示路径是什么

9. `Eval Plan`
- 成功、失败、退化、不可接受行为分别如何判定
- 默认先表达 integration / acceptance evidence，再决定哪些地方需要定向代码审查
- 默认先写 `environment`、`evidence`、`failure signal`、`failure handling / replay expectation`
- 对 Freely 自治能力，默认还要说明：
  - unit
  - pre-merge focused regression / smoke
  - integration
  - end-to-end
  - real-environment
  - post-merge integration acceptance
  - post-merge application-native real-environment acceptance
  - post-merge end-to-end dogfood acceptance
  - 若其中某类不适用，为什么不适用，替代证据是什么

10. `Execution Slices`
- 哪些 slice 可以独立实现、独立验证、独立回写

11. `Revisit Triggers`
- 当模型、工具、用户行为或外部条件变化时，何时必须重判这份 PRD

12. `Dev-Loop Handoff`
- 后续实现环如何消费这份 PRD，需要哪些最小引用和下一跳上下文

## Bar for `done_b2_ibm`

仅有 `Goal`、`Product Surface` 或一般性背景描述，不算达标。

进入 `done_b2_ibm` 前，至少还要满足：

- `pre-tests.md` 能从 `prd.md` 自然派生，而不是另起一套口头标准
- `pre-tests.md` 能直接表达 issue-level acceptance，且默认以 smoke / integration / regression / non-goals 这类行为视角组织
- `pre-tests.md` 至少固定 `Unit`、`Integration`、`End-to-End`、`Real-Environment` 四个章节；不适用时不得缺章
- `pre-tests.md` 能恢复每个关键 acceptance 面的 `environment`、`evidence`、`failure signal`、`failure handling / replay expectation`
- `Unit`、`Integration`、`End-to-End` 三章若不适用，`pre-tests.md` 必须写 `not_applicable_reason`、`not_applicable_explanation` 与必要的 `replacement_evidence`
- `Real-Environment` 章节必须固定写 `real_environment_status` 与 `real_environment_reason`，用于总结本次实现需要的真实环境测试是否已达标，或是否根本不需要真实环境测试
- 对 Freely 自治能力，`pre-tests.md` 默认不能缺少 integration / application-native real-environment / end-to-end dogfood 这些 post-merge 验收面；若缺少，必须显式写明不适用理由与替代证据
- 若当前 issue 是 auth/switch/startup-recovery/watchdog family 的 follow-on owner，`Real-Environment` 不能只停在文字结论；`Acceptance Items` 至少保留一条 artifact-backed 的 `real_env` 或 `post_merge_dogfood` 证据；对这类 owner，artifact 应优先覆盖真实 `bin/ai`、真实 `codex exec` 或真实 `freely start`
- `Unit`、`Integration`、`End-to-End` 三章所需的 acceptance target、testing layer、target environment、required evidence 与 blocker taxonomy 能从 `prd.md` 推导出来
- 若 `pre-tests.md` 进入 adequacy v2，`surface_kind`、`target_lane`、`promotion_gate` 也应能从 `prd.md` 的 eval plan / execution slice 直接推导出来
- `tasks.md` 能从 `prd.md` 的 decomposition / execution slices 派生，而不是与 PRD 脱节
- AI 读取 `prd.md` 后，能回答：
  - 目标是什么
  - 什么不能做
  - 先验证什么
  - 用什么判断成败
  - 下一步如何切片

## Testing Ladder Reference

PRDs MUST consume the five-level testing evidence ladder by reference — do not redefine levels locally.

Refer to `docs/epics/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/prd.md` for:

- **Five evidence levels**: script regression, integration, end-to-end scenario, application-native real-environment, protected-env post-merge acceptance.
- **Completion/retirement gate mapping**: per issue class, the minimum evidence level required.
- **Escalation rules**: lower levels cannot satisfy gates requiring higher levels.
- **Artifact-plane evidence closeout schema**: how `pre-tests.md` completion evidence is formatted.

The `pre-tests.md` `evidence_level` field in acceptance items MUST use the ladder level names from this reference, not ad-hoc labels.

## Failure signs

出现以下任一情况，说明 PRD 仍未达标：

- PRD 主要是 prose 背景说明，缺少执行结构
- `pre-tests.md` 与 `tasks.md` 需要额外聊天解释才能成立
- `pre-tests.md` 主要还是 wording review / “读代码后再判断怎么测”，而不是先表达 acceptance 行为
- `pre-tests.md` 缺少 `Unit`、`Integration`、`End-to-End`、`Real-Environment` 中的任一章节，或用自由发挥文本跳过某章节
- auth/switch/startup-recovery/watchdog follow-on owner 把 `Real-Environment` 写成 `pass`，却没有留下 artifact-backed 的 `real_env` 或 `post_merge_dogfood` acceptance item，或留下的 artifact 仍回避真实 `bin/ai` / `codex exec` / `freely start`
- `Eval Plan` 没有写 environment / evidence / failure signal，导致 merge 后该怎么验证无法恢复
- `pre-tests.md` 的 blocker taxonomy 仍要靠聊天解释，无法区分定义不完整与执行失败
- 没有写出 non-goals / non-negotiables
- 没有写出 revisit trigger，默认旧 workaround 永久有效
