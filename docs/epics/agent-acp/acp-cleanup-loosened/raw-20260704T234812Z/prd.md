# PRD: #3731 ACP cleanup 遗漏修复

## Goal
补齐 #3731 未完成的 base_tool plumbing、修复语法错误和路径不一致、改进 hook 提示。

## 实现方案
逐项机械修复，无架构变化。详见 tasks.md。

## Dev-Loop Handoff
全部修改为静态代码变更，不涉及运行时逻辑改动。
交付给 `freely-dev-loop-execution`：应用已设计好的修改，通过语法检查。
