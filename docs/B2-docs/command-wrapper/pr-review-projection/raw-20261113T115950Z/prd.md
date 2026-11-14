# PRD: pr-review-guarded 引导同步 L0

- issue_id: I-20261113T115950Z-A
- source_raw: raw-20261113T115950Z
- workflow_kind: feature
- milestone: M-20261113T115950Z-A
- story: command-wrapper/pr-review-projection（复用既有 story）

## 目标

评审的**执行入口**与 `freely-tdd-review/SKILL.md` 对齐：ACP prompt 与人工回退都先跑 L0
（项目意图一致性），再跑四层，使「四层全绿但整体漂移」无法通过。只改引导文本，不改
`review_verdict.py`、不改 `pr-merge-guarded`、不改任何门禁。

## 唯一改动范围

- `docs/system/workspace/scripts/worktree/pr-review-guarded`：
  - ACP prompt：开头声明 L0 先于四层、L0 失败即整体失败；Instructions 增加 Step 0（外部锚点原文 + Q1–Q5 + 门禁四段举证 + 禁止自证）；JSON 增加 `intent` 维度，且 `intent=fail` 强制 `verdict=fail`。
  - 人工回退步骤：改为「先 L0 → 再四层」，并要求 review 文档含 `## L0：项目意图一致性` 段。
- 新增 AT `test-review-guidance-l0.py`，`bin/test-all` 的 CORE / CI_CORE 各 +1。

## 不退化边界

- 不改 `review_verdict.py` 的解析与 `VALID` 词表；
- 不改 `pr-merge-guarded` / `governance-merge-gate` 的判定；
- 不改 skill 内 L0 的五项内容；不新增「L0 段存在性」门禁（否则可补字段通过）。

## 功能需求

- FR-1：prompt 明确 L0 先于四层，L0 失败即整体失败。
- FR-2：prompt 要求引用四类外部锚点原文，并逐条回答 Q1–Q5。
- FR-3：prompt 要求改门禁时给四段举证，并禁止用 B1/B2 自证。
- FR-4：JSON 增加 `intent` 维度，`intent=fail` 强制 `verdict=fail`。
- FR-5：人工回退先 L0 再四层，且 review 文档须含 L0 段。
- FR-6：verdict 解析行为与词表不变。

## 验收

AT-001 RED `10 ok / 26 failed`（develop `7820299c4` 快照）→ GREEN `36 ok / 0 failed`；
`bin/test-all --ci` 全绿。
