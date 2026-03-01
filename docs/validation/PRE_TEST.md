# Pre-Test 门禁文档

## 说明
本文件在开发前编写，是测试门禁输入。`freely doctor` 会检查本文件是否存在且是否包含至少一个 `CASE-` 用例。

## 测试范围
- 命令：`freely doctor`、`freely start`
- 关键规则：
  - 必需文档存在性检查
  - `PRE_TEST.md` 用例完整性检查
  - `start` 对门禁失败的阻断

## 开发前测试用例
- CASE-001：缺少 `docs/validation/PRE_TEST.md` 时，`freely doctor` 失败并返回非 0。
- CASE-002：`docs/validation/PRE_TEST.md` 存在但不含 `CASE-` 时，`freely doctor` 失败并返回非 0。
- CASE-003：`docs/validation/PRE_TEST.md` 含至少一个 `CASE-` 时，`freely doctor` 成功。
- CASE-004：文档门禁失败时，`freely start` 在启动 AI 前退出。

## 开发后补充回归用例
- CASE-005：`doctor` 输出包含每个缺失文档的明确路径。
- CASE-006：在合法文档集下，`doctor` 输出 `PASS` 并返回 0。

## 执行结果（2026-02-28）
- CASE-001：通过
- CASE-002：通过
- CASE-003：通过
- CASE-004：通过
- CASE-005：通过
- CASE-006：通过
