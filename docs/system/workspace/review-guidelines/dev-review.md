# Dev 阶段审查指南

## 定位
Dev 是实现阶段。Reviewer 检查：**代码是否修复了 RED 阶段发现的真实失败**。

## 检查项

### 1. TDD 忠实度（★ 重点）

**核心原则：代码必须直接针对 RED 阶段发现的每个失败。**

- [ ] 每条 AT 的 RED actual_RED_output 描述的失败，在 dev diff 中有对应修复吗？
- [ ] 修复方案合理吗（不是表面掩盖）？
- [ ] git commit 顺序正确吗（B1→B2→RED→dev→GREEN）？

### 2. PRD 忠实度
- [ ] 无 scope creep？无遗漏？

### 3. 对比审查
| 审查方式 | 判定 |
|---------|------|
| 对比 RED output 和 dev diff → 修复是否直接针对 RED 发现的问题 | 有效 |
| `grep -c "xxx" diff` → 确认某行存在 | 走过场 |

## 通过标准
- 全部通过 → PASS
- 代码与 RED 失败不对应 → FAIL：AT-00X 的 RED 失败未修复

## 失败处理
输出修复方向 → Worker 修改代码
