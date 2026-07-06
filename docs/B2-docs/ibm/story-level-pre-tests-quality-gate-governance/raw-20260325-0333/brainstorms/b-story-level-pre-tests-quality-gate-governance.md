# Brainstorm: story-level-pre-tests-quality-gate-governance

## Goal

把每个 story 下的 `pre-tests.md` 最低质量线冻结成可拒绝的治理 contract，避免后续 issue 用“文件存在但内容很弱”的方式绕过 testing gate。

## Key Decisions

1. `pre-tests.md` 质量 gate 先于“跑了多少测试”。
2. commands-only 的 `pre-tests.md` 不构成 acceptance control surface。
3. `pre-tests.md` 至少要能恢复：
   - acceptance target
   - testing layer
   - target environment
   - required evidence
   - blocker taxonomy
4. 以下两类失败必须分开：
   - `pre-tests.md` 自身不合格
   - 测试执行尚未完成或执行失败
5. 本 issue 只收紧质量 gate，不在同一批次引入完整 testing ladder 或 real-environment harness framework。

## Non-Goals

- 统一所有 story 的测试命名
- 直接实现新的 e2e runner
- 把所有历史 issue 的 `pre-tests.md` 全量重写

## Outcome

Freely 能在 doc-loop / IBM 阶段就拒绝低质量 `pre-tests.md`，而不是等到 verification 才发现 acceptance definition 本身就不稳。
