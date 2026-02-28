# PRD：Pre-Test 文档门禁

## 问题陈述
Freely 的运行命令缺少对“文档先行、测试先行”的自动检查，导致在无 pre-test 设计时也可进入开发/运行阶段，破坏 BMAD 的可追溯性与测试门禁强度。

## 目标
1. 在启动前自动检查 BMAD 必需文档是否存在。
2. 强制要求存在 `docs/PRE_TEST.md`，且包含至少一个结构化测试用例。
3. 让检查能力可单独执行，便于 CI/人工预检。

## 范围
- `bin/freely` 增加文档门禁检查能力与 `doctor` 子命令。
- `start` 命令接入门禁。
- 文档体系补齐 PRE_TEST 说明。
- 提供脚本化测试。

## 非目标
- 不实现完整 CI 平台。
- 不覆盖所有业务质量规则，只先落地 pre-test 最小硬门禁。

## 验收标准
1. `freely doctor --project <abs_path>` 在文档缺失或 pre-test 为空时返回非 0。
2. `freely start` 在门禁失败时直接退出并给出失败原因。
3. 文档链路可追溯：Intent -> PRD -> EPIC -> STORY -> Code/Test。
