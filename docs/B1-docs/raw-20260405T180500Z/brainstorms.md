# 预研头脑风暴：test-pre-merge-family-promotion-gate-enforcement

## 背景

`I-20260405T161500Z-A` 已经把 `test-pre-merge-*` family 的 promote model 冻结成正式 owner，但当前仓库的治理真源和 gate 实现仍停留在旧模型：

1. `docs/CONSTITUTION.md` 仍允许 `feature/*` 直接作为 `develop` 的默认 promote source。
2. `docs/LAWS.md` 仍把 `test-pre-merge-*` 写成 replay 证据面，而不是 develop 前的必经 promote family。
3. `pre-test-merge-flow.md` 仍明确写着 shadow batch / not promote unit。
4. `pr-merge-guarded` 和相关 tests 也仍阻止 `test-pre-merge-* -> develop`，并允许 `feature/* -> develop`。

这说明下一个 follow-on 不能只改文档，也不能只改脚本。

## 为什么不能拆成两个 owner

如果先做 truth-source update、再单开 script enforcement：

1. 宪法/法律会先声明新模型，但实际 gate 仍执行旧模型，产生短期双真相。
2. 反过来若脚本先改，旧文档又会把新的 enforcement 解释成“实现偏差”。
3. `pr-merge-guarded`、hook、`governance-check` 的判定词典本来就依赖 `CONSTITUTION` / `LAWS` / references 的 merge source 语义，拆开后很容易返工。

因此更稳的收敛是：

- 一个 owner 同时完成：
  - 治理真源更新
  - protected-branch gate enforcement 更新
  - regression tests 更新

## 这条 owner 要解决什么

1. 把 `develop` 的正常 promote source 从旧模型切到新模型。
2. 明确 `test-pre-merge-*` family 是 `develop` 的合法 promote 入口，`feature/* -> develop` 作为正常路径被阻止。
3. 让 single-feature lane 与 explicit multi-bundle lane 在 gate 上共享同一 canonical family 前缀，而不是引入第二前缀。
4. 保持 `hotfix/* -> develop` 的既有合法路径。
5. 保持 lifecycle automation、manifest 生成、paired create 等仍为后续 owner，不在这一条里顺手扩大。

## 初步边界

### 应包含

1. `docs/CONSTITUTION.md`
2. `docs/LAWS.md`
3. `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
4. 必要的 `SKILL.md` / `AGENTS.md` / lane reference 对齐
5. `docs/system/workspace/scripts/worktree/pr-merge-guarded`
6. 相关 hook / governance gate / tests 中与 merge source 语义直接耦合的部分

### 不应包含

1. stale detection 的完整 automation
2. multi-bundle manifest 文件的最终格式与自动生成
3. `wt-create` paired create 或 batch-create UX
4. runtime / fleet-status 上的 family lifecycle surface

## 初步结论

1. follow-on 应先做 `promotion gate enforcement`，再做 `family lifecycle automation`。
2. `promotion gate enforcement` 应是一个单独 owner，但内部同时包含 truth-source update 与 script enforcement。
3. 只有这样，Freely 才不会在“模型已经改了，但 gate 还没改”或“gate 先改了，但治理真源还是旧的”之间摇摆。
