# Brainstorm: pr-merge-guarded IBM 阶段引导
- 来源: raw-20260508T232413Z13Z (#262)
## Discovery
merge 失败时 AI 反复 merge→fail→fix→merge，不先用 --range dry-run 定位问题，不理解 IBM 阶段要求。
## Decision
报错输出加入 IBM 阶段自诊引导 + skill 参考 + dry-run 强调。
