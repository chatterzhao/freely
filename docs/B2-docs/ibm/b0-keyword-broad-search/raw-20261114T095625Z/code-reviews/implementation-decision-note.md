---
issue_id: I-20261114T095625Z-A
issue_path: docs/B2-docs/ibm/b0-keyword-broad-search/raw-20261114T095625Z/issues/I-20261114T095625Z-A.md
phase_state: completed
---

- issue_id: I-20261114T095625Z-A
- issue_path: docs/B2-docs/ibm/b0-keyword-broad-search/raw-20261114T095625Z/issues/I-20261114T095625Z-A.md

## Implementation Decision Note
- decision: 只改 B1 skill 的 B0 段 + brainstorms 模板 + 完成自检 + 新 AT，补关键词广搜/三类分层/矛盾清单/二元决策/留痕五层；不做硬门禁。
- why_this: 真实 P0 误判风险来自"只读一份历史文档当现状"；方法论缺口经读源码逐条证实，无既有覆盖。
- alternatives_considered: 做成自动脚本扫描（超出 B1 研究动作边界、易误报，否决）；做成硬门禁强制字段（补空文本即绕过，与 skill 现有"刻意不做硬门禁"冲突，否决）。
- boundary_non_goals: 不改 L0/verdict、不自动 dropped、不追溯历史 raw、不改 runtime/其它 skill。
- residual_risk: 广搜质量仍依赖执行者；AT 只能钉住"模板要求存在"，无法保证执行者真做广搜——与 skill 既有"刻意不做硬门禁"取舍一致。
