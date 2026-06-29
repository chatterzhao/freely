---
name: freely-test-execution
description: >-
  TDD GREEN 阶段。在 test-pre-merge-* 测试工位逐条执行 pre-tests.md，
  先 `git cherry-pick` 同步全部 dev 提交，再跑全量测试。全部 GREEN
  才放行到 `freely pr-create-guarded` 命令。硬拦截：工位落后、未执行、
  无证据、有 failed 或 ghost pass。

  Use when: `freely-dev-loop-execution` skill 实现完成之后，提 PR 之前。
  触发词："GREEN"、"跑测试"、"验证"、"test"、"测试工位"、"全部通过"、
  "cherry-pick 测试"。
---

# skill:freely-test-execution

> 全链路: [cmd] freely feedback → [skill] freely-workflow-guarded-execution → [cmd] freely wt-create → [skill] freely-doc-B1_IBM-execution → [skill] freely-doc-B2_IBM-execution → [skill] freely-test-RED-execution → [skill] freely-dev-loop-execution → [skill][here] freely-test-execution → [cmd] freely pr-create-guarded → [cmd] freely pr-review-guarded → [cmd] freely pr-merge-guarded → [cmd] freely wt-close

## 在流程中的位置

```
feat: B1 → B2(写pre-tests) → RED(确认功能未实现) → dev(实现) → test-GREEN → pr
fix:  wt-create → B1 → B2(写pre-tests) → RED(确认bug可复现) → dev(修复) → test-GREEN → pr
```

test skill 位于 dev-loop 和 pr-create 之间。它是最后一道自动化验证闸门——任何一条测试不通过，都不能进入 PR。

## GREEN 的定义

```
每一条 acceptance item 必须同时满足:
  1. red-green-status = green（RED→dev→GREEN 循环完成）
  2. status = passed（测试已执行）
  3. actual_output 已填写且不是占位符（真实执行结果）
  4. evidence_file 存在且非空（证据可追溯）
  5. actual_output 与 expected_output 一致（测试真的通过了）

全部满足 → 全绿 → 进入 pr-create
有一条不满足 → 不绿 → 回 dev-loop 修复
```

## 三条铁律

1. **test 工位必须包含全部最新修改** — 跑测试之前，先确认 dev 工位的提交已全部 cherry-pick 到 test 工位。测试工位落后于开发工位 = 测试结果无意义。
2. **逐条执行，逐条写回** — 不批量改 status，不跳过。每条 acceptance item 都要有真实的 test_command 执行记录。
3. **全绿才过** — 有一条 failed 就不能进 PR。回 dev-loop 修，修完 cherry-pick 同步，重新跑全量测试。

## 执行步骤

```
1. 确认在与开发工位 raw key 相同的 test-* 测试工位（不在则硬拦截）

2. 同步最新代码: 确保 test 工位包含全部 dev 修改
   - 检查 dev 工位是否有 test 工位没有的提交:
     git -C <dev_wt> log --oneline <test_branch>..<dev_branch>
   - 如果有 → cherry-pick 到 test 工位
   - 如果 dev 有未提交的修改 → 提示先到 dev 工位提交
   - 原则: test 工位落后于 dev 工位 = 测的不是最终代码 = 测试作废

3. 按 pre-tests.md 逐条执行 test_command
   - 在 test-* 测试工位中运行
   - 收集输出到 evidence_file

4. 逐条判定 GREEN:
   - red-green-status = green? 不是 → 回 dev（可能还没跑 RED→dev→GREEN）
   - test_command 执行结果 = expected_output? 不一致 → failed
   - actual_output 已填写? 填空 → 未执行

5. 全部 green → 进入 pr-create-guarded
   有任何不 green → 回 skill:freely-dev-loop-execution 修复
     → 修复后提交 → cherry-pick 到 test 工位 → 重新跑全量测试

6. 清理测试运行环境
```

### 步骤 2 详细说明：确保 test 工位不落后

**这是最重要的步骤。test 工位代码落后于 dev 工位 = 测试结果完全作废。**

```bash
# 检查 dev 工位是否有 test 工位没有的提交
_dev_wt=$(git worktree list --porcelain | awk -v br="refs/heads/fix/raw-XXX" '
  $1=="worktree"{wt=$2} $1=="branch"&&$2==br{print wt;exit}')
_missing=$(git -C "$_dev_wt" log --oneline HEAD.. 2>/dev/null || true)

if [[ -n "$_missing" ]]; then
  echo "测试工位落后于开发工位，以下提交未同步:"
  echo "$_missing"
  echo "请先 cherry-pick 到测试工位:"
  echo "  git cherry-pick <commit-hash>..."
  exit 1
fi
```

### 步骤 4 详细说明：GREEN 判定标准

```bash
对每条 acceptance item:

# 检查 red-green-status
rg_status=$(grep "red-green-status:" item)
if [[ "$rg_status" != "green" && "$rg_status" != "not_applicable" ]]; then
  → 不绿。原因: TDD 循环未完成。回 skill:freely-dev-loop-execution
fi

# 检查执行结果
if actual_output != expected_output; then
  → 不绿。原因: 测试失败。回 skill:freely-dev-loop-execution 修复
fi
```

## 门禁拦截

| 检查 | 类型 | 说明 |
|------|------|------|
| 不在 test-* 测试工位 | **硬拦截** | 提示 cd 到 test 工位 |
| test 工位落后于 dev 工位 | **硬拦截** | cherry-pick 同步后再跑 |
| pre-tests.md 不存在 | **硬拦截** | B2 阶段未完成，回 `freely-doc-B2_IBM-execution` skill |
| test_command 为占位符 | **硬拦截** | 测试用例是假的，回 `freely-doc-B2_IBM-execution` skill 重新设计 |
| 全部 acceptance 都是 not_applicable | **硬拦截** | 糊弄测试，回 `freely-doc-B2_IBM-execution` skill 重新设计 |
| red-green-status != green | **硬拦截** | TDD 循环未完成，回 dev-loop |
| actual_output 为空 | **硬拦截** | 测试未执行，必须逐条跑完 |
| evidence_file 缺失或为空 | **硬拦截** | 无证据，证明不了测试执行过 |
| actual_output != expected_output | **硬拦截** | 有未通过测试，回 dev-loop |
| 跳过某条测试（status=pending） | **软拦截** | 需 --reason 说明为什么跳过 |

## 证据收集

测试证据写入 `.freely/run/test-evidence/` 目录：

```
.freely/run/test-evidence/
├── acceptance-1.log    # acceptance-1 的 test_command 输出
├── acceptance-2.log    # acceptance-2 的 test_command 输出
└── ...
```

## 完成后

```
全绿 → ./bin/pr-create-guarded
有红 → 回 skill:freely-dev-loop-execution 修复 → cherry-pick 同步 → 重新 test
```

## 不负责

- 不写 pre-tests.md（`freely-doc-B2_IBM-execution` skill 负责）
- 不修改源码（dev-loop 负责）
- 不跑 RED（skill:freely-test-RED-execution 负责）
- 不创建 PR 或 merge（branch-management 负责）

## 与上下层 skill 的关系

```
RED(全红确认) → dev(实现代码) → test-GREEN(本 skill, test-* 测试工位 GREEN 验证)
                                      │
                              全绿 → pr-create
                              不绿 → 回 dev-loop → 修 → cherry-pick → 重跑 test
```
