# GREEN 阶段审查指南

## 定位
GREEN 是 TDD 最后闸门。Reviewer 检查：**测试是否验证了行为正确性，不是 ghost pass**。

## 检查项

### 1. 测试全 GREEN
- [ ] 所有 AT red-green-status = green？
- [ ] 有 failed → 回 dev
- [ ] 全部 pending → 根本没跑

### 2. 证据真实性（★ 重点——堵 ghost pass）

| actual_output | 判定 |
|--------------|------|
| 具体行为描述（如"执行两次后 git status 无变化"） | PASS |
| `grep → 1` / `bash -n → OK` | WARNING——代码存在测试 |
| `(执行后填写)` / `GREEN` / 空 | FAIL——ghost pass |

- [ ] 每条 actual_output 是真实执行结果吗？
- [ ] evidence_file 存在且内容具体吗？
- [ ] **全部 test_command 是 grep/bash -n？→ FAIL**：回到 B2 重新设计

### 3. 行为正确性最终确认
- [ ] 测试全部通过后，**能确认 bug 已修复 / 功能正确吗**？
- [ ] 不能 → FAIL：回溯到 B2 重新设计测试

## 通过标准
- 全部通过 → PASS
- ghost pass → FAIL：执行真实测试
- 全部 grep/bash -n → FAIL：测试不验证行为

## 失败处理
回 dev 修复 → merge test → 重新 GREEN
