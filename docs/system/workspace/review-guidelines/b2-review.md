# B2 阶段审查指南

## 定位
B2 是设计到交付的阶段。Reviewer 检查：**pre-tests 是否设计了真正可验证行为正确性的测试**。

## 检查项

### 1. I-* issue + PRD 完整性（快速过）
- [ ] I-* issue 文件存在，字段齐全
- [ ] 实现方案基于 brainstorms 分析结论

### 2. Pre-tests 行为验证质量（★ 重点）

**核心原则：test_command 必须验证"改动的行为是否正确"，不是验证"代码有没有这行"。**

| 测试类型 | 示例 | 判定 |
|---------|------|------|
| 行为测试 ✅ | "执行两次 close → git status 无变化" | PASS |
| 行为测试 ✅ | "制造 dirty → 运行命令 → 确认被阻塞" | PASS |
| 代码存在测试 ❌ | `grep -c "feature" file` → 1 | FAIL |
| 语法测试 ❌（仅此不够） | `bash -n file` | 仅作补充 |

- [ ] 每条 test_command 是否**可执行**（不是占位符）？
- [ ] 每条 test_command 是否验证了**行为正确性**？
- [ ] 如果 test_command 是 grep / bash -n / py_compile → **FAIL**

### 3. 文档完整性
- [ ] tasks.md + code-reviews/ + IDN 5 字段

## 通过标准
- 全部通过 → PASS
- test_command 全是 grep/bash -n → FAIL：测试只验证代码存在性，不验证行为

## 失败处理
输出具体失败项 → Worker 回到 B2 重新设计 pre-tests
