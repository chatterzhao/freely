---
b1_id: B1-20261126T130151Z
phase_state: completed
source_raw: raw-20261126T130151Z
source_url: https://github.com/chatterzhao/freely/issues/4726
produced_candidate: C-20261126T130151Z-A
created_at: 2026-11-26
---

# B1_IBM: pr-merge followthrough 证据沿袭

## 0. 设计意图审计
### B0 广搜 + 分层
- 关键词族：followthrough / test-pre-merge / attest-meta → `pr-merge-guarded:649-655`、`test-evidence.py:174-226`。
- 三类分层：当前实现 = issue-sync commit 后 merge test 工位但无 attest；历史局部 = #4137/#4722 手工 attest；权威恢复点 = #4703 三态 validate。
- 矛盾清单：merge commit 内容已测试，却因 chain 断裂被判 stale → 同一份证据两种结论。
- 二元决策：继续（在封装命令内自动沿袭）。

### 外部锚点
- `test-evidence.py:174`「Carry test evidence forward across metadata-equivalent commits…」
- 实测 #4137/#4722：pr-merge 后 wt-close 报 stale，需手工 attest-meta 或重跑全量 CI。
- 判定：实现未完成（封装链缺一步）。
- 冲突：无；不改 validate 判据，只在合法等价时调用既有 attest-meta。

## 0.1 四问
- Q1 类别：流程能力（收口吞吐与可信度）。
- Q2 职责边界：test-evidence 拥有判据；pr-merge 只负责在等价时调用既有 CLI。
- Q3 结构性冲突：若放宽 wt-close 判据会产生第二真源 → 不动门禁，只在命令链补调用。
- Q4 门禁失配：现有 AT 测 attest-meta 本身，缺「封装命令是否自动调用」→ 新增 AT。

## Decision
在 issue-sync commit 同步 test 工位成功后，调用 `test-evidence.py attest-meta`（sensitive paths 保守默认），成功打印沿袭回执；失败打印重跑指引，不吞错。

## Candidate
- candidate_id: C-20261126T130151Z-A
- status: promoted
- milestone: M-20261126T130151Z-A
