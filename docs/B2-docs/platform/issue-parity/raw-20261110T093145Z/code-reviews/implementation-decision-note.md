# Implementation Decision Note
- issue_id: I-20261110T093145Z-A
- issue_path: docs/B2-docs/platform/issue-parity/raw-20261110T093145Z/issues/I-20261110T093145Z-A.md
- decision: 在既有 `raw_title_contract` 单一所有者里增加 fenced-code-block 感知的 `find_local_heading`，物化 / 副本 gate / H1 backfill 三处复用；gate 无真实 H1 时给显式诊断
- why_this: 立项假设「物化没写 H1」被前置评审否掉（#4181 早已修过）。真实根因是三处裸 `^#\s+` 正则把 python 代码块注释当 H1：物化跳过注入、gate 借注释当 LOCAL title 并丢弃正文、backfill 跳过修复，导致健康 raw 的首个 PR 被误导性的 `content_diverged` 挡下（R23.13 实际踩到，靠手工补 H1 绕过）。
- alternatives_considered: ①`wt-create` 后补一次 H1——治标且让职责更模糊；②只改 gate——物化仍不写 H1、backfill 仍跳过；③放宽副本一致性检查——削弱 fail-closed 治理，明确否决；④另造一套 H1 工具函数——项目已有单一所有者，重复必然再次漂移；⑤手工批量回填历史 B1 文档——制造大规模 diff，回填工具修好后按需执行即可。
- boundary_non_goals: 不改 `canonical_raw_title` / `local_heading_title` / `is_canonical_raw_title` / `platform_title` 语义；不改 Q2 兼容分支与身份回退；不改 `canonical_projection` 的 labels / comments / state / severity 维度；不放宽检查；不批量回填历史文档；不删除文件。
- residual_risk: ①finder 只处理 ``` / ~~~ 围栏（0–3 空格缩进、长度 ≥3、闭合同字符），缩进 >3 空格的围栏或 HTML 注释包裹的伪标题仍可能误判；②`missing_local_title` 是新增诊断码，调用 `freely_wt_assert_raw_reconciled_readonly` 的 facts 集合未包含它，但 gate 返回非零且 receipt 的 ok=false，行为上仍 fail-closed；③历史 B1 文档中若有「只有代码注释、无真实 H1」的，需按需跑 backfill 才会补上，本轮未主动改。
- verification: AT-001 基线 RED `2 ok / 12 failed`（`_local_record` 借注释当 title）→ 工位 GREEN `14 ok / 0 failed`；`test-materialize-h1` 18 项 + 8 个相关测试 + `test-all --ci` 全绿。
- self_bootstrap_findings: ①立项假设错误，用 `git log -L` 找到既有实现后改为「扩展既有契约」而非重写，节省一大圈；②三处裸正则（物化 / gate / backfill 两处）必须一次改全，漏掉 backfill 的 `--apply` 幂等复检会让既有套件 18 项中 1 项变红；③AT 的静态断言若检查字面量 ``` 会误伤用正则实现的代码，改为检查 `_FENCE`/`fence_char`；④AT docstring 含 `\s` 会触发 SyntaxWarning，改 raw 字符串。

## Implementation Decision Note
- decision: 既有契约扩展为代码块感知，三处复用 + 显式诊断
- why_this: 代码注释被误当 H1，健康 raw 首个 PR 被误挡
- alternatives_considered: 后置补 H1 / 只改 gate / 放宽检查 / 另造工具 / 批量回填
- boundary_non_goals: 既有契约语义、投影维度、检查强度、历史文档均不动
- residual_risk: 围栏语法边界、新诊断码未进 facts 集合、历史文档待按需回填
