# STORY 看板

## STORY-001（文档）
背景：现有文档多为占位，无法指导执行。

验收标准：
- PRD/EPIC/STORY/PROGRESS/RECOVERY/BRAINSTORM 使用简体中文并可执行。
- 新增 `docs/PRE_TEST.md`，包含开发前测试用例。

验证：
- 人工检查文档完整性与追踪链。

依赖：
- 无。

## STORY-002（开发）
背景：需要在命令层强制执行文档门禁。

验收标准：
- `bin/freely` 增加 `doctor` 命令。
- `doctor` 校验必需文档存在，且 `PRE_TEST.md` 至少含一个 `CASE-` 用例。
- `start` 在门禁失败时拒绝继续。

验证：
- 命令行运行 `doctor` 与 `start` 的失败路径验证。

依赖：
- STORY-001。

## STORY-003（测试与评审）
背景：测试是主门禁，需自动化覆盖。

验收标准：
- 新增测试脚本覆盖缺失/非法/合法 pre-test 场景。
- 生成符合宪法命名规则的 review 记录。

验证：
- 测试脚本全部通过。

依赖：
- STORY-002。
