---
b1_id: B1-20261126T120834Z
phase_state: completed
source_raw: raw-20261126T120834Z
source_url: https://github.com/chatterzhao/freely/issues/4723
produced_candidate: C-20261126T120834Z-A
created_at: 2026-11-26
---

# B1_IBM: 退役门禁 freshness check 因 _sp 未定义静默失效

## 0. 设计意图审计
### B0 广搜 + 多文档交叉
- 关键词族：`pretests-retirement-gate` / `pretests_stale` → `docs/system/workspace/scripts/quality/pretests-retirement-gate:124-140`；`attest-meta` / `EQUIVALENCE_CHAIN` → `quality/test-evidence.py:174-226`；`test-evidence validate` → `pr-create-guarded`。
- 三类分层：当前生效实现 = gate 自带 失效的 HEAD 精确相等判据；历史局部 = #4137 人工重跑 CI 绕过；权威恢复点 = `test-evidence.py validate` 三态。
- 矛盾清单：pr-create/pr-merge 认 `equivalent`，wt-close 退役门禁不认 → 同一份证据两种判定。
- 二元决策：继续（删除自造判据，复用 validate 三态）。

### 外部锚点
- `quality/test-evidence.py:174`「Carry test evidence forward across metadata-equivalent commits…」
- `pretests-retirement-gate`「Only `freely test-gate run` can produce a trusted verdict: a real exit code, a real evidence file bound by sha256, and a HEAD matching this worktree.」——该注释在 #4703 后已过期，真正判据是三态 validate。
- 实测：#4137 评审元数据提交后 `attest-meta` 成功，pr-create/pr-merge 全过，wt-close 报 `[pretests_stale]`，被迫重跑 4m43s 全量 CI。

- 判定：实现偏差（自造判据引用未定义别名 _sp，try/except 静默吞掉 NameError，整段是死代码）。
- 冲突：无；不为让本轮通过而放宽门禁，复用既有 validate 判据。
- 影响面：仅 `pretests-retirement-gate`；不改 `test-evidence.py` 判据。

## 0.1 四问
- Q1 类别：治理元数据证据链一致性。
- Q2 职责边界：`test-evidence.py` 拥有证据新鲜度判定；退役门禁只消费 verdict。
- Q3 结构性冲突：若直接在退役门禁写第二套 equivalent 判据会产生第二真源 → 必须调用 validate。
- Q4 门禁失配：现有 self-check 测「HEAD 相等」，#4703 后真实判据是三态；改的是判据来源，不是放宽强度。

## Input / Problem / Decision
- Input：raw-20261126T120834Z，P1 fix。
- Problem：退役门禁的 失效的 HEAD 精确相等判据与 #4703 三态设计冲突，造成无谓全量重跑。
- Decision：删掉 `pretests_stale` 自造判据，validate 的 `ok`（current/equivalent 为 true，stale 为 false）成为唯一新鲜度判据；保留 not_tested、evidence_sha256 与 pretests-gate 校验。

## Candidate
- candidate_id: C-20261126T120834Z-A
- status: promoted
- milestone: M-20261126T120834Z-A
