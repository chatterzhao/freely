# Implementation Decision Note
- issue_id: I-20260708T122837Z-A

## Decision
将 stage 分类函数从 scan() 函数内部的 dict literal 内联调用，改为模块级函数 + 后处理循环追加字段。

## Why This
- 函数定义在 dict literal 之后 → Python NameError → scan 返回 null
- 模块级函数可在整个模块中访问
- 后处理循环比内联调用更清晰、更易维护
- 批处理聚合在 items 收集完成后统一执行

## Alternatives Considered
1. 将函数定义移到 scan() 开头 → 可行但函数只能在 scan() 内使用
2. 将 stage/next_action 内联到 dict literal → 当前实现方式，失败
3. 后处理 + 批处理 → 选择此方案，模块级函数 + 后处理

## Boundary / Non-Goals
- 不修改 scan 的分类逻辑（category/subcategory 不变）
- 不修改 platform-adapter 集成
- 不修改 A2A liveness 检查
- 不改动 scan CLI 接口

## Residual Risk
- batch 聚合可能遗漏边界 case（如 1c platform-only 暂未实现）
- 新增字段可能影响下游 prompt builder（需同步更新）
