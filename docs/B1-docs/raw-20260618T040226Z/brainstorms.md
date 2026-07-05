# Brainstorm: pr-review-guarded — 独立 PR review 门禁

## Discovery

### Source
- raw-20260618T040226Z (GitHub #2966)
- 发现链：ef251886 receipt fix 被 15fa666c 静默覆盖 → receipt 丢失 → develop 死锁 → 反思缺少 pre-merge review

### 问题

当前流程 `pr-create-guarded → pr-merge-guarded` 中间没有独立的 review 环节。导致：

1. **语义冲突静默通过**：git 自动合并不产生冲突文本，但功能退化。ef251886（receipt --body split）被 15fa666c（fetch+reset fallback）覆盖是典型案例。
2. **Review 证据分散**：Implementation Decision Note 在 dev-loop 产出，但没有统一的 review verdict 文档。谁审的、审了什么、结论是什么——这些信息散落在不同地方。
3. **门禁不完整**：governance-merge-gate 只检查 IBM 文档完整性，不检查代码级 invariant（如 receipt 逻辑是否保留）。
4. **Reviewer 身份模糊**：当前 review 由 dev-loop 内的 "acceptance_reviews" 字段声明，但没有独立的 review 执行步骤。

### 为什么不能靠现有机制

| 现有机制 | 为什么不夠 |
|---|---|
| governance-merge-gate | 只检查文档存在，不检查代码语义 |
| candidate acceptance_reviews | 在 B1 阶段，审的是 candidate 边界，不审代码实现 |
| Implementation Decision Note | 自述文件，没有独立 reviewer verdict |
| GitHub PR review | 需要人工操作，没有 machine-readable verdict 落盘 |

## Research

### 行业 PR Review 标准

| 平台/实践 | Review 机制 | Machine-readable |
|---|---|---|
| GitHub | PR Review API (APPROVE/COMMENT/REQUEST_CHANGES) | ✅ gh api |
| GitLab | Merge Request Approval | ✅ API |
| Gerrit | Code Review +2/-2 | ✅ labels |
| Linux kernel | email-based patch review, Reviewed-by trailer | ✅ git log |
| Google | CL review (Critique), readability review | ✅ internal |

共性规律：
- Review 是 merge 的独立前置步骤，不是附属品
- Reviewer 与 author 身份分离（即使 reviewer 是工具）
- Review decision 可机器读取，可被后续工具消费
- 可配置 "Require review before merging" 分支保护

### Freely 的差异

1. **Reviewer 可能是 AI**：subagent 或独立 Claude 进程做 review。需要明确的 review prompt 和评判标准。
2. **Review 证据落盘**：不像 GitHub 的 review comment 留在 PR 页面，Freely 需要 review 产物存入 `docs/B2-docs/.../code-reviews/`。
3. **Review 维度更广**：除了代码正确性，还要检查 Freely 特定的治理 invariant（receipt 完整性、phase_state 一致性、worktree 关联）。

### 可行性

- GitHub PR review API 可通过 `gh pr review` 命令行操作
- Review 文档格式已有 Implementation Decision Note 作为参考
- governance-merge-gate 已有扩展点（可以增加 review 文档检查）
- Reference transaction hook 已有 receipt 检查逻辑（可复用）

## Design

### 命令签名

```
freely pr-review-guarded <branch> [--reviewer <name>] [--verdict pass|fail|needs_changes]
```

### 执行流程

```
1. 验证 PR 存在（gh pr view）
2. 获取 PR diff（governance-merge-gate --range "base..HEAD"）
3. 执行 review 维度检查（见下文）
4. 生成 review 文档（docs/B2-docs/.../code-reviews/pr-review-{PR#}.md）
5. 输出 verdict
6. 可选：同步 GitHub PR review（gh pr review --approve / --request-changes）
```

### 6 个 Review 维度

| # | 维度 | 检查方法 | 关键 invariant |
|---|---|---|---|
| 1 | 语义冲突 | governance-merge-gate + 代码模式匹配 | receipt split 存在、_absorb_close_frontmatter 已删除 |
| 2 | IBM 完整 | governance-merge-gate | candidate → I-* → code-review 链完整 |
| 3 | Code review | 文件存在 + 字段完整 | Implementation Decision Note 格式正确 |
| 4 | Pre-test | verification 目录 + adequacy | 每个 acceptance item 有 verified status |
| 5 | Receipt | 如果修改 pr-merge-guarded | --subject/--body split 保留 |
| 6 | Worktree | git status + git worktree list | worktree 存在、干净、分支匹配 |

### Review 文档格式

`docs/B2-docs/{name}/code-reviews/pr-review-{PR#}.md`：

```markdown
# PR Review: #{PR#}
- pr_number: {PR#}
- branch: {source_branch}
- base: develop
- reviewer: {reviewer_name}
- review_date: {ISO timestamp}
- verdict: pass | fail | needs_changes

## 1. Semantic Conflict Check
- status: pass | fail
- evidence: {description}

## 2. IBM Completeness Check
- status: pass | fail
- evidence: governance-merge-gate output

## 3. Code Review Evidence
- status: pass | fail
- evidence: {implementation-decision.md path + field check}

## 4. Pre-test Evidence
- status: pass | fail
- evidence: {pre-tests.md path + acceptance items}

## 5. Receipt Integrity Check
- status: pass | fail | n/a
- evidence: {receipt split verified or not applicable}

## 6. Worktree Check
- status: pass | fail
- evidence: {worktree path, branch, cleanliness}

## Overall Verdict
- verdict: pass | fail | needs_changes
- notes: {actionable guidance if not pass}
```

### 门禁集成

**pr-merge-guarded 修改**：执行前检查 review 文档存在且 verdict=pass：
```
if ! grep -q 'verdict: pass' "docs/B2-docs/.../code-reviews/pr-review-{PR#}.md"; then
  echo "[MERGE-GUARD] PR review not passed. Run pr-review-guarded first."
  exit 1
fi
```

**governance-merge-gate 修改**：增加 review 文档存在性检查。

## Impact Analysis：需要修改的全部文件

### 新增
1. `bin/pr-review-guarded` — 主命令脚本
2. `docs/system/workspace/scripts/worktree/pr-review-guarded` — 真源脚本

### 流程链路更新（所有出现 pr-create → pr-merge 的地方）
3. `docs/system/workspace/skills/freely-feat-execution/SKILL.md` — 阶段 5→6 之间插入 pr-review
4. `docs/system/workspace/skills/freely-fix-execution/SKILL.md` — 同上
5. `docs/system/workspace/skills/freely-dev-loop-execution/SKILL.md` — 全链路声明
6. `docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md` — 全链路声明
7. `docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md` — 全链路声明
8. `docs/system/workspace/skills/freely-branch-management/references/release-hotfix-flow.md` — hotfix 流程

### 流程步骤在脚本中的引用
9. `docs/system/workspace/scripts/worktree/wt-create` — 下一步提示
10. `docs/system/workspace/scripts/worktree/pr-create-guarded` — 输出提示 "Next: pr-review-guarded"
11. `docs/system/workspace/scripts/worktree/pr-merge-guarded` — 前置检查 review verdict

### 错误消息 / 门禁
12. `docs/system/workspace/hooks/pre-push.sh` — 提示信息
13. `docs/system/workspace/hooks/reference-transaction.sh` — 不需要改（receipt 检查不变）
14. `docs/system/workspace/scripts/worktree/governance-merge-gate` — 增加 review 文档检查

### 文档
15. `AGENTS.md` — 核心开发流程 + 阶段表
16. `docs/system/workspace/ibm-framework.md` — 总览图

### 门禁速查表（多个 skill 中重复）
17. freely-feat-execution 门禁常见坑速查
18. freely-fix-execution 门禁常见坑速查

## Decision

**Promote**。pr-review-guarded 填补了 pr-create 和 pr-merge 之间的关键 gap。实施分两个 phase：

Phase 1（本 candidate）：pr-review-guarded 脚本 + review 文档格式 + 流程链路更新 + 门禁集成
Phase 2（后续）：GitHub PR review API 同步 + governance-merge-gate 审查维度扩展
