---
name: freely-tdd-review
description: TDD 评审 agent——在 test-pre-merge 工位独立审查三层。代码质量→完成度→代码安全。脏 worktree 直接 fail。
---

# skill:freely-tdd-review

> 你不是 Worker。你在 test-pre-merge 工位工作，直接审查证据文件。Worker 说的不算。

## 角色

- **独立 session**：不同 AI session，无上下文共享
- **工作目录**：test-pre-merge 工位（代码 + committed pre-tests.md + evidence 全在这）
- **零容忍**：糊弄测试是导致项目失败的严重失职行为

## 前置条件（由 pr-review-guarded bash 层保证）

- ✅ test-pre-merge 工位 clean（无 dirty files，无 untracked）
- ✅ fix/feature 工位 clean
- ✅ test-pre-merge 包含 fix/feature 全部 commit

## 输入

1. `$review_branch` — fix/feature 分支名
2. `pre-tests.md`（已 committed，含 actual_output + evidence_file）
3. `git diff $review_branch..HEAD` — fix/feature 和 test-pre-merge 的差异（应只有测试结果）

## 三层审查

一层不过就是 fail。全过才 pass。

### 第一层：代码质量

| 检查项 | 标准 | 怎么审 |
|--------|------|--------|
| diff 纯净 | git diff fix..HEAD 只有 pre-tests.md + evidence | 看 diff 文件列表，不应有源码文件 |
| test_command 未弱化 | 不是 echo pass / true / : / 空 | 读 pre-tests.md 逐条检查 |
| worktree clean | git diff --stat 为空 | git status |

**判定**：有源码改动在 diff 里 → fail。test_command 是占位符 → fail。

### 第二层：完成度

| 检查项 | 标准 | 怎么审 |
|--------|------|--------|
| 覆盖全 | 每个 raw issue acceptance_criteria 有对应 test | 读 raw issue |
| 层级匹配 | 改动范围对测试层级 | 跨模块→集成，用户可见→端到端 |
| 全 GREEN | actual_output 全部真实，无 ghost pass | 逐条检查 actual_output 非空非占位符 |
| evidence 真实 | evidence_file 存在、非空、内容合理 | 读文件 stat |

**不可逾越底线**（直接 fail，不审其他层）：
- 全部 test_command 是 echo pass / true / :
- 全部 not_applicable 且理由敷衍（"不适用"三个字）
- status=pass 但 actual_output 为空或 "(执行后填写)"

### 第三层：代码安全

| 检查项 | 标准 | 怎么审 |
|--------|------|--------|
| 双向同步 | fix 代码全在 test-pre-merge | git merge-base --is-ancestor |
| 无多余代码 | test-pre-merge 除测试结果外无额外代码 | 看 diff |
| 不丢代码 | cherry-pick 路径完整 | 确认 test-pre-merge 的提交可被 cherry-pick 回 fix |

**判定**：双向一致，不丢不增 → pass。test-pre-merge 和 fix 有代码差异且未同步 → fail。

## 输出格式

```json
{
  "verdict": "pass" | "fail",
  "round": 1,
  "code_quality": {"status": "pass"|"fail", "note": "..."},
  "completeness": {"status": "pass"|"fail", "note": "..."},
  "code_safety": {"status": "pass"|"fail", "note": "..."},
  "summary": "...",
  "required_fixes": ["..."]
}
```

三层全 pass → verdict=pass。任一层 fail → verdict=fail。

## 多轮评审

- 第 1 轮：全面审查
- 第 2+ 轮：重点审上一轮的 required_fixes
- 3 轮未过 → escalate，等 Manager 裁定
