---
name: freely-test-execution
description: 独立测试执行 skill——在 test-pre-merge 工位中逐条执行 pre-tests.md 的 test_command，收集 actual_output 和 evidence，全绿后进入 PR。硬拦截：不在 test 工位、未执行、无证据、有 failed。
---

# skill:freely-test-execution

> 全链路: dev → test → pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close
>                [本 skill 自此开始 — 执行 pre-tests → 全绿才放行]

## 在流程中的位置

```
feat: B1 → B2(写pre-tests) → dev(RED-GREEN实现) → test(执行验证) → pr
fix:  wt-create → B1 → B2(写pre-tests) → dev(RED-GREEN实现) → test(执行验证) → pr
```

test skill 位于 dev-loop 和 pr-create 之间。它是最后一道自动化验证闸门——任何一条测试不通过，都不能进入 PR。

## 三条铁律

1. **B2 就写好 test_command + expected_output** — 不是"应该测什么"，是"运行这条测试用例，期望这个结果"
2. **dev 先跑 RED 再 GREEN** — 先确认测试失败（证明测试有效），再实现到通过
3. **test skill 全绿才过** — 有一条 failed 就不能进 PR

## 执行步骤

```
1. cd 到 test-pre-merge 工位（不在则硬拦截）
2. 合并 fix/feature 分支到 test-pre-merge
3. 按 pre-tests.md 各条 acceptance 的 target_environment 准备运行环境
4. ⚠️ pre-tests.md 可执行性检查——拒绝 ghost pass、占位符命令（见下方详细说明）
5. 逐条执行 pre-tests.md 中的 test_command
6. 填写 actual_output + evidence_file
7. 对比 expected_output → passed | failed
8. 全部 passed（全绿）→ 达标，继续 pr-create
9. 有任何 failed（红色）→ 回 dev-loop 修复
10. 清理测试运行环境
```

### 步骤详细说明

#### 步骤 1：确认 test-pre-merge 工位

```bash
# 检查当前所在工位
git worktree list | grep "$(pwd)"

# 如果不在 test-pre-merge-* 工位中
→ 硬拦截: "请 cd 到 test-pre-merge 工位后再执行 test skill"
```

**硬拦截**：不在 test-pre-merge 工位拒绝执行测试。test-pre-merge 是隔离的测试沙箱，保护 develop 不受测试污染。

#### 步骤 2：合并待测分支

```bash
# 在 test-pre-merge 工位中
git merge feature/raw-XXX-<slug> --no-edit
# 或
git merge fix/raw-XXX-<slug> --no-edit

# 有冲突 → 记录 blocker，回 dev-loop
```

#### 步骤 3：准备测试运行环境（按需）

按 pre-tests.md 各条 acceptance 的 `target_environment` 准备运行环境。pre-tests.md 由 `skill:freely-doc-B2_IBM-execution` 指导编写，其中 `test_command` 和 `target_environment` 已声明测试用例所需的运行环境。

#### 步骤 4：pre-tests.md 可执行性检查（反 ghost pass）

**在执行任何 test_command 之前**，逐条检查 pre-tests.md 中的 acceptance item 是否真实可执行。

检查清单（每条 acceptance item 必须通过全部检查）：

| 检查项 | 判定标准 | 不通过时的处理 |
|--------|----------|----------------|
| test_command 真实性 | 不是占位符（`echo pass`、`echo ok`、`true`、`:` 等），是能验证改动的真实测试用例（单元测试、集成测试、端到端测试、API 调用、编译验证等均可） | **硬拦截** — 拒绝执行 |
| expected_output 可验证性 | 不是"任意输出"、"命令正常退出"等泛化描述，必须包含具体断言 | **硬拦截** — 拒绝执行 |
| not_applicable 理由充分性 | 如果某层标记 not_applicable，理由必须具体（不能是"不适用"三个字） | **硬拦截** — 拒绝执行 |
| 覆盖度检查 | 至少有一条 acceptance item 是真实的（非 not_applicable 且 test_command 非占位符） | **硬拦截** — 拒绝执行 |
| 测试层级充分性 | 如果改动涉及多模块协作 → 必须有集成测试；如果改动影响用户可见行为 → 必须有端到端测试。不能只有单元测试 | **硬拦截** — 拒绝执行 |

> ⚠️ **端到端测试和集成测试是 AI 编程中防止项目失败的最重要保证。**
> AI 生成的代码最容易在模块边界和端到端流程中出错。只跑单元测试不够。

**检测占位符命令的模式**：
```bash
# 以下模式视为占位符，拒绝执行：
- test_command 包含 "echo pass" 且 expected_output 为空或 "pass"
- test_command 为 "true" 或 ":"
- test_command 为空
- test_command 看起来像 mock（如 "echo test ok" 且 expected_output 无具体断言）
```

**不通过时的处理**：
```
❌ pre-tests.md 可执行性检查失败
   原因: <具体哪条 acceptance 的哪个检查项失败>
   建议: 回到 skill:freely-doc-B2_IBM-execution 重新设计 pre-tests.md
   说明: 糊弄测试是导致项目失败的严重失职行为。绝对不允许糊弄测试相关的任何环节。
         test_command 必须是真实可执行的测试用例，
         expected_output 必须有可验证的具体断言。
         参考 B2_IBM skill 中的「反糊弄铁律」。
```

**通过后**：继续执行步骤 5-10（逐条运行 test_command、收集证据、判定结果）。

#### 步骤 5-6：逐条执行测试

对 pre-tests.md 中每条 acceptance 项：

```bash
# 执行 test_command，收集输出
<test_command> > .freely/run/test-evidence/acceptance-<n>.log 2>&1

# 填写 pre-tests.md 中的 actual_output 和 evidence_file
```

#### 步骤 7-9：判定结果

```
全部 status=passed 且 evidence_file 存在且非空
  → ✅ 全绿，进入 pr-create-guarded

任何一条 status=failed 或 actual_output 为空
  → ❌ 回 dev-loop 修复，修完重新跑 test skill
```

## 门禁拦截

| 检查 | 类型 | 说明 |
|------|------|------|
| 不在 test-pre-merge 工位 | **硬拦截** | 提示 cd 到 test 工位 |
| pre-tests.md 不存在 | **硬拦截** | B2 阶段未完成，回 B2_IBM |
| test_command 为占位符（echo pass/true 等） | **硬拦截** | 测试用例是假的，回 B2_IBM 重新设计 |
| expected_output 无具体断言 | **硬拦截** | 预期输出不可验证，回 B2_IBM 重新设计 |
| 全部 acceptance 都是 not_applicable/mock | **硬拦截** | 糊弄测试是严重失职行为，回 B2_IBM 重新设计 |
| actual_output 为空 | **硬拦截** | 测试未执行，必须逐条跑完 |
| evidence_file 缺失或为空 | **硬拦截** | 无证据，证明不了测试执行过 |
| status 含 failed | **硬拦截** | 有未通过测试，回 dev-loop |
| 跳过某条测试（status=pending） | **软拦截** | 需 --reason 说明为什么跳过 |

### 硬拦截 vs 软拦截

- **硬拦截**：无法绕过，必须修复对应的检查项
- **软拦截**：可用 `--reason "违规绕过门禁中，理由充分，是：<业务理由>"` 绕过，仅限合理的业务场景

## 证据收集

测试证据写入 `.freely/run/test-evidence/` 目录：

```
.freely/run/test-evidence/
├── acceptance-1.log    # acceptance-1 的 test_command 输出
├── acceptance-2.log    # acceptance-2 的 test_command 输出
└── ...
```

每条 acceptance 项的 `evidence_file` 指向对应的日志文件。

## 完成后

```
全绿 → ./bin/pr-create-guarded → test worktree verify → merge chain
有红 → 回 skill:freely-dev-loop-execution 修复 → 重新 test
```

## 不负责

- 不写 pre-tests.md（B2_IBM 负责）
- 不修改源码（dev-loop 负责）
- 不创建 PR 或 merge（branch-management 负责）
- 不关闭 issue 或工位（wt-close 负责）

## 与 dev-loop 的交互

```
dev-loop: 实现 + RED-GREEN 验证
    ↓ (代码已提交，初步验证通过)
test skill: 正式逐条执行 pre-tests
    ↓ (全绿)
pr-create-guarded: 提 PR
```

dev-loop 中的 RED-GREEN 是快速迭代验证，test skill 是正式的全量回归验证。
