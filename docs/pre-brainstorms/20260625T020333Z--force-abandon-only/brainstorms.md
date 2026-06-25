---
b1_id: B1-20260625T020333Z
phase_state: completed
source_raw: raw-20260625T020333Z
produced_candidate: C-20260625T020333Z-A
---
# B1: wt-close --force semantics = abandon-only

## 问题
`wt-close --force` 的语义模糊，既被用于跳过门禁错误（bypass gates），也被用于确定放弃 issue。这导致开发者遇到 gate 报错时倾向于 `--force` 跳过，而不是去修复根因。实际业务逻辑中 `--force` 应该只用于"放弃此 raw issue"，而不应用于绕过合法检查。

## 发散
- `--force` 的两个潜在含义：(1) 强制执行不管检查 (2) 确定放弃
- 当前代码中存在误导性的 example，演示了 `--force` 用于非放弃场景
- pretests gate 的错误信息只给了"用 --force 跳过"的路径，没有给"修复问题"的引导
- 已有 `I-20260625T020000Z-A`（gate error skill guidance）做了 skill 指针改进，但没有触及 `--force` 的语义

## 收敛
`--force` 应该只有一种语义：放弃此 raw issue。任何其他场景（gate 报错、pretests 未执行、测试失败等）都应引导用户去修复根因，而不是 `--force` 跳过。

## Decision
修改 `wt-close`：
1. `--help` 说明 `--force = 确定丢弃此 raw issue`
2. 添加不应使用 `--force` 的场景列表
3. pretests gate error 显示两条路：保留→修复 vs 放弃→force
4. 删除暗示 `--force` 用于非放弃场景的 examples

## Candidate: C-20260625T020333Z-A promoted
