# Brainstorm - STORY-003

## 背景
当前仓库已具备基础BMAD文档门禁（STORY-002），但分支门禁仍存在关键缺口：
1. `pre-push`只阻止推送到`main`，未阻止推送到`develop`。
2. 用户约束要求测试集成只能走`pre-develop`，不允许直接合并/推送到`develop`。
3. hook行为缺少可复现的回归测试脚本，门禁可靠性不足。

## 备选方案
1. 仅通过人工约定执行“只走pre-develop”
2. 在`pre-push`中强制阻止`develop`直推，并补充脚本化测试

## 权衡
- 方案1：改动最少，但很容易被误操作绕过，无法形成硬门禁。
- 方案2：一次实现即可持续复用，符合“测试优先门禁”和“可脚本化”原则。

## 决策
采用方案2：
- 更新宪法中的分支流转说明，明确`feature/* -> pre-develop -> develop`测试门禁路径。
- 升级`.githooks/pre-push`，阻止直接推送到`develop`与`main`。
- 增加`bin/test-pre-push-hook`作为回归测试脚本。

## 后续动作
- [x] 完成本轮PRD/EPIC/STORY更新并写入ore-test
- [ ] 实现hook策略与测试脚本
- [ ] 执行正反向测试并更新进度/recovery/review
