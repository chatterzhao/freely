# PRD: B0 关键词广搜与二元决策
- issue_id: I-20261114T095625Z-A

## Goal
让 B1 B0 预研从"读列好的锚点"升级为"主动广搜 + 多文档分层 + 交叉比对 + 显式继续/dropped 决策"，防止 P0 因只看一份过期文档而误判方向。

## 实现方案
1. `skills/freely-doc-B1_IBM-execution/SKILL.md` B0 段增加：
   - 关键词族表（≥3 组：功能名/机制名/字段名/命令名/门禁名/raw key，搜 docs/** bin/** .freely/**）
   - 三类分层（当前生效实现 / 历史局部文档 / 当前权威恢复点 + 权重说明）
   - 矛盾清单（哪两份冲突、哪份过期被取代）
   - 二元决策（继续附方向 / dropped 附覆盖者证据；禁止以耗时/复杂度 dropped）
   - 留痕（dropped 用 freely comment 写回双平台）
2. brainstorms 模板 §0 增加对应结构化表格字段；完成自检加一项。
3. 新增 AT `test-b0-keyword-broad-search.py` 静态断言上述要求在 skill 与模板中出现，且"刻意不做硬门禁"仍在（防补字段就过）。

## 不退化边界
- 不改 review L0 五问与 verdict 契约；不新增硬门禁；不自动 dropped。
- 不做自动脚本扫描（广搜是 B1 研究动作，由 AT 钉住模板与自检）。
- 不改其它 skill、不改 runtime 行为。

## Dev-Loop Handoff
见 pre-tests.md。RED：develop 基线 AT 失败（skill 无广搜字段）；GREEN：新增后全绿。
