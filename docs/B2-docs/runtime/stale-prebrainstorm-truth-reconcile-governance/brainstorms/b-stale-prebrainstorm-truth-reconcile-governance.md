# IBM Brainstorm - stale-prebrainstorm-truth-reconcile-governance

## Core framing

这条 owner 修的是 truth drift，不是 runtime behavior。

## Candidate implementation shape

### A. Policy

- stale / superseded / deferred / absorbed 有明确判断次序
- 只有 canonical truth 足够硬时才允许 reconcile

### B. Batch

- first batch 只覆盖代表样本
- 修改方式以 pointer-based 注释和状态说明为主

## Risks

- 不能把 deferred 删除成“已经做完”
- 不能因为文档纠偏顺手引入新能力承诺
- 不能碰共享索引导致无意义冲突
