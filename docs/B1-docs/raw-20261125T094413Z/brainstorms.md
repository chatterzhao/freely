# Brainstorms: raw-20261125T094413Z
## 0. 设计意图审计
- 锚点：test-evidence.py:124-130 validate 强制 HEAD 精确相等；用户澄清（平台评论）判据 = 语义影响（测试用例变/被测对象变才重测）；两类项目区分（用户项目 issue 字段是元数据、自举是测试对象）。
- 判定：**设计不完整**——判据是 HEAD 相等，不区分变更性质；一刀切白名单会在自举场景漏测。
- 四问：Q1 流程能力；Q2 与 test-gate 共享证据职责；Q3 无结构性冲突；Q4 现有门禁测 HEAD 相等，需引入等价维度但不放宽。
## 方案
采纳「依赖感知 + 证据沿袭」：lane 声明 evidence_sensitive_paths；attest-meta 计算 diff∩敏感面，空集才沿袭；硬排除 pre-tests/tasks/bin/runtime/system/tests/contracts/hooks/lock；validate 三态 current/equivalent/stale。默认无声明 → 全敏感必须重测。
