# Brainstorms: raw-20261125T100958Z

## 0. 设计意图审计
- 锚点：commands.md「feedback edit 编辑已有 raw issue，仅平台写，不操作本地文件」；runtime/freely:25027 cmd_comment 已是纯平台命令；platform-adapter.py:1121 search_raw_issue（双平台只读发现）；:1106 update_issue（逐平台汇总）。
- 判定：**实现偏差**——edit 命令声明只操作平台，却无条件依赖本地 issue.md 提取 platform_ids，与 comment 的纯平台语义不一致。
- 冲突：无；修法对齐 comment。影响面：仅 cmd_feedback edit 分支。
## 0.1 四问
Q1 流程能力；Q2 与 issue-sync 共享平台发现职责，最终判定归 feedback edit；Q3 无结构性冲突（修改 raw 不等于实现它）；Q4 无门禁失配。
## 方案
A 要求 wt-create 先行——否决（修改 raw 不需要实现）；B 平台发现 ids + update-issue——采纳；C 回读平台 body——否决（引入平台为 body 真源，超出"仅显式参数"）。
