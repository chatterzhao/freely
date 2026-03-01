# PRD

## 问题
当前仓库虽然已建立BMAD文档基线，但分支测试门禁存在缺口：
1. 仍可误推`develop`，与“测试先进入`pre-develop`”目标冲突。
2. hook缺少回归测试脚本，导致策略改动后可能静默失效。

## 目标
1. 将“仅合并/测试到`pre-develop`，禁止直推`develop`”固化为可执行规则。
2. 让`pre-push`对`main`和`develop`都形成硬门禁并输出明确策略提示。
3. 提供可执行回归脚本覆盖hook正反向行为。
4. 保持文档链路可追踪：Intent -> PRD -> EPIC -> STORY -> Code/Test。

## 范围
- 更新`docs/CONSTITUTION.md`分支策略描述，纳入`pre-develop`测试门禁路径。
- 更新`.githooks/pre-push`，阻止对`main`和`develop`的直接推送。
- 新增`bin/test-pre-push-hook`回归测试脚本。
- 更新`docs/planning/STORY.md`中的ore-test与开发后测试用例。
- 更新`README.md`本地执行说明。

## 非目标
- 不在本轮实现远端分支保护（GitHub/GitLab server-side）策略。
- 不在本轮重构`freely`主执行循环。

## 验收标准
1. 向`develop`推送时，`.githooks/pre-push`返回非0并显示拒绝原因。
2. 向`main`推送时，保持现有拒绝能力（除显式应急开关外）。
3. `bin/test-pre-push-hook`可一键执行并覆盖至少3个场景（develop阻断、main阻断、feature放行）。
4. 文档中存在清晰映射：Intent -> PRD -> EPIC -> STORY -> Code/Test。
