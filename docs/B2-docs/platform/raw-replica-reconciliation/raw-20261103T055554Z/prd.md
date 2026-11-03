# PRD: raw replica 身份解析按 [RAW-key] 标题前缀

- issue_id: I-20261103T055554Z-A

## Goal
让 raw issue 的身份解析只认 canonical 标题前缀 `[RAW-{key}]`，body 中的交叉引用不再污染身份集合；消除 `ambiguous` 误伤导致的 PR 阻断。

## Modules
- `docs/system/workspace/scripts/sync/platform-adapter.py`
  - 新增纯函数 `_resolve_raw_identity(matches, raw_key) -> (match|None, error)`，统一标题前缀优先、多身份 ambiguous、单条兜底。
  - `_discover_one` 使用该解析；`ambiguous` 时仍返回 ambiguous，`not found` 时返回 missing。
  - `_unique_raw_issue` 使用同一解析，保证 close-raw 等调用方语义一致。
- `docs/system/workspace/scripts/tests/test-platform-adapter-raw-identity.py`（新）：unit 覆盖标题优先 / 多身份 ambiguous / 兜底单条 / no match。

## Invariants
- 多真实身份（>=2 个标题前缀命中）必须 ambiguous，绝不静默选第一个。
- 标题无命中时保持旧行为（单条可用），不新造 missing。
- 不改变 reconcile 的 fail-closed 判定；只修正"身份来源"。

## Non-Goals
- 不改 raw issue 标题/正文生成格式，不回写历史 issue。
- 不修改 scan/`raw-reconciliation-gate` 的消费逻辑。
- 不处理平台搜索 API 的其它过滤语义。

## Eval Plan
- unit：`test-platform-adapter-raw-identity.py`。
- integration：真实平台 `discover_raw_replicas('20260807T114900Z')` 必须两个平台 `status=ok`（修复前为 ambiguous）。
- real-environment：即可由上面真机调用覆盖（需要有效平台凭据）。

## Dev-Loop Handoff
先写 RED 单测（`_resolve_raw_identity` 不存在 → 失败），再实现 helper 与两处调用点，最后跑 unit + 真机 discover。
