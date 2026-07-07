# RED 阶段审查指南

## 定位
RED 是 TDD 第一道闸门。Reviewer 检查：**actual_RED_output 是否来自真实执行**。

## 检查项

### 1. RED 执行真实性（★ 重点）

**核心原则：actual_RED_output 必须是真实命令执行的输出。**

| actual_RED_output | 判定 |
|-------------------|------|
| 具体错误信息/返回值 | PASS——真实执行 |
| `grep ... → 0` | FAIL——grep 不是执行测试 |
| `(执行后填写)` / `RED` / 空 | FAIL——占位符 |
| `修改前无此功能` | FAIL——主观判断，无证据 |

- [ ] 每条 AT 的 actual_RED_output 是真实执行输出吗？
- [ ] 有具体错误信息、返回值、异常输出吗？
- [ ] 意外 PASS？→ FAIL：测试设计有问题

### 2. 覆盖完整性
- [ ] feature 至少一条端到端测试？
- [ ] 全部 not_applicable → FAIL：糊弄

## 通过标准
- 全部 RED 真实 → PASS
- actual_RED_output 占位符 → FAIL：请真实执行测试

## 失败处理
输出具体失败项 → Worker 重新执行 RED
