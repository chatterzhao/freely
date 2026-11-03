---
b1_id: B1-20261103T055554Z
phase_state: completed
source_raw: raw-20261103T055554Z
source_url: https://github.com/chatterzhao/freely/issues/4131
produced_candidate: C-20261103T055554Z-A
created_at: 2026-11-03
---

# B1_IBM: raw replica 身份解析按 [RAW-key] 标题前缀

## Input
- raw-20261103T055554Z（GitHub #4131 / Gitee IKSK7I）
- 现象：`platform-adapter.py` 的 `search_raw_issue` 在 title 与 body 两处做子串搜索 `raw-{key}`；只要其它 issue 的正文/证据路径提到同一 key，就会返回多个匹配。`discover_raw_replicas` 把多匹配判为 `ambiguous`，`raw-reconciliation-gate` 直接 block，PR 流程无法继续。

## Problem
- raw issue 的平台身份是 `[RAW-{key}] <title>` 标题前缀；body 中的引用（其它 issue 的证据路径 `fix-raw-{key}/...`）不是身份声明。
- 当前搜索把 title 与 body 子串都当身份来源，命中集合不唯一 → 身份解析不唯一 → 生命周期门禁 fail-closed 误伤。
- 实例：`fix/raw-20260807T114900Z-scan-platform-adapter-import` 被 #4108 的证据路径引用同一 key 而 blocked。

## Brainstorm
### Option A: 标题前缀优先，body 仅兜底（选定）
- 先按 `^\[RAW-{key}\]`（大小写不敏感）过滤；精确命中恰好 1 条 → 采用；多条 → 仍 ambiguous（fail-closed）；0 条 → 回退到旧逻辑（单条匹配可用，多条 ambiguous）。
- 优点：把"身份声明"和"文本引用"分开；对历史/非标准 issue 保持兜底；最小改动、可单测。
- 缺点：prefix 格式依赖标题约定，需测试锁定。

### Option B: 只搜 title，完全去掉 body 搜索
- 否决：部分历史 raw issue 的标题可能没有 `[RAW-key]` 前缀；直接去掉 body 兜底会造成新的 missing。

### Option C: 只在 reconcile/scan 调用方做过滤
- 否决：`search_raw_issue` 被 reconcile、close-raw、human intake 等多处消费；同一身份规则应在源头统一，调用方各自过滤会重复且再次漂移。

## Decision: Option A
- 理由：身份规则集中到 platform-adapter 的解析层；标题前缀是平台 raw issue 的 canonical 身份，body 引用是噪音。多个"真实身份"仍然 fail-closed。

## 不做
- 不改 raw issue 标题/正文格式；不回写历史 issue。
- 不改 reconcile 的 fail-closed 语义。
- 不改 scan 的分类逻辑。

## Candidate
- candidate_id: C-20261103T055554Z-A
- status: promoted
- milestone: M-20261103T055554Z-A
