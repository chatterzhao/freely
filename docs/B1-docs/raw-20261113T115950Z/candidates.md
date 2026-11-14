# B1 Candidates — raw-20261113T115950Z

## C-20261113T115950Z-A：pr-review-guarded 引导同步 L0

- status: promoted
- promoted_issue_id: I-20261113T115950Z-A
- promoted_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261113T115950Z/issues/I-20261113T115950Z-A.md
- milestone: M-20261113T115950Z-A
- kind: feature
- decision: 只改 `pr-review-guarded` 的两处引导文本（ACP prompt + 人工回退），新增 `intent` 维度；不改判定逻辑与 verdict 解析。
- 范围:
  1. ACP prompt：Instructions 增加 L0 段（外部锚点原文 + Q1–Q5 + 门禁改动四段证据），JSON 增加 `intent` 维度。
  2. 人工回退步骤：改为「1. 加载 skill → 2. **先做 L0** → 3. 再逐层四层 → 4. 结论写入含 `## L0：项目意图一致性` 段」。
  3. 新增 AT `test-review-guidance-l0.py`，CORE/CI_CORE 各 +1。
- 验收:
  - prompt 与人工提示都含 L0 关键要素（锚点 / Q1–Q5 / 四段证据 / 输出段）；
  - `review_verdict.parse_verdict` 行为不变（pass/fail/needs_changes/unknown 四例）；
  - 基线（develop）两处都不含 L0 → 红；
  - `bin/test-all --ci` 全绿。
- 不退化边界:
  - 不改 `review_verdict.py`、`pr-merge-guarded`、`governance-merge-gate`；
  - 不改 skill 的 L0 内容；不放宽门禁；不新增「L0 段存在性」门禁。
