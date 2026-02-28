# EPIC

## Epic 列表
- EPIC-001: BMAD文档基线补全
- EPIC-002: BMAD门禁脚本化校验
- EPIC-003: 分支测试门禁（pre-develop优先）与hook回归测试

## 映射关系
- EPIC-001 -> PRD目标4
- EPIC-002 -> PRD目标4
- EPIC-003 -> PRD目标1、目标2、目标3

## 分解到STORY
- STORY-002（已完成）:
  - 完成文档基线补全
  - 实现`bin/bmad-check`
  - 更新README与验证记录
- STORY-003（本轮）:
  - 将分支流转策略更新为`feature/* -> pre-develop -> develop`
  - 升级`.githooks/pre-push`阻止`main/develop`直推
  - 实现`bin/test-pre-push-hook`并执行回归测试
