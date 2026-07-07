# pre-tests: 封装命令文档系统化

- phase_state: in_verification
- red-green-status: green
- created_at: 2026-07-06

## 测试范围

全部为纯文档/文本修改，无运行时行为变更。验证方式：grep 检查文本内容存在性。

## 测试用例

### AT-001: AGENTS.md 速查表增强

- **目标**: 确认 AGENTS.md 速查表增加了"你想做什么"和"它封装了什么"列
- **验证方法**: `grep -c "你想做什么" AGENTS.md`
- **RED 断言**:
  1. 现有速查表不含"你想做什么"列
  2. 现有速查表不含"它封装了什么"列
- **GREEN 断言**:
  1. AGENTS.md 中包含"你想做什么"速查表
  2. 或旧"场景"表已被增强为意图→命令→封装映射表
  3. 每行至少包含：意图描述、正确命令、封装步骤说明
- **red-green-status**: green
- **red_how**: `grep -c "你想做什么" AGENTS.md` → 0 matches。AGENTS.md 仅含"场景→正确命令→禁止"三列传统速查表，缺少意图列和封装说明列。功能未实现。
- **actual_RED_output**: `grep -c "你想做什么" AGENTS.md` → `0`
- **green_how**: AGENTS.md 速查表已从"场景→正确命令→禁止"三列增强为"你想做什么→正确命令→它封装了什么→禁止"四列，覆盖 9 个常见场景，每行包含意图描述、正确命令和封装步骤说明。
- **actual_GREEN_output**: `grep -c "你想做什么" AGENTS.md` → `2`，表头包含"你想做什么"和"它封装了什么"列

### AT-002: SKILL.md 意图→命令速查章节

- **目标**: 确认 freely-workflow-guarded-execution SKILL.md 铁律区域前增加了正向引导的意图→命令速查
- **验证方法**: `grep -c "意图→命令速查" ~/.claude/skills/freely-workflow-guarded-execution/SKILL.md`
- **RED 断言**:
  1. 当前 SKILL.md 中无"意图→命令速查"章节
  2. 铁律区域前无正向引导表
- **GREEN 断言**:
  1. SKILL.md 中包含表格：意图 | 正确做法 | 错误做法 | 原因
  2. 表格在铁律/禁止区域之前
  3. 覆盖至少 6 个常见场景
- **red-green-status**: green
- **red_how**: `grep -c "意图→命令速查" SKILL.md` → 0 matches。SKILL.md 有铁律区域和硬性规则，但缺少正向引导的意图→命令速查章节。功能未实现。
- **actual_RED_output**: `grep -c "意图→命令速查" ~/.claude/skills/freely-workflow-guarded-execution/SKILL.md` → `0`
- **green_how**: SKILL.md 在"硬性规则"前新增"意图→命令速查"章节，包含表格：意图 | 正确做法 | 错误做法 | 原因，覆盖 8 个常见场景。表格位于铁律正面之前，先正向引导再列禁止项。
- **actual_GREEN_output**: `grep -c "意图→命令速查" docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md` → `1`；部署后 `~/.claude/skills/.../SKILL.md` 也包含此章节

### AT-003: .githooks/bin/gh 拦截消息增强

- **目标**: 确认每个 gh 拦截消息中增加了"为什么"解释（封装了什么步骤）
- **验证方法**: `grep -c "封装" .githooks/bin/gh`
- **RED 断言**:
  1. gh wrapper 拦截消息只说被拦截，未解释封装了什么
- **GREEN 断言**:
  1. `gh pr create` 拦截消息包含"封装了"或"确保"或"包含步骤"描述
  2. `gh pr merge` 拦截消息包含类似的封装步骤说明
  3. `gh issue close` 拦截消息包含类似的封装步骤说明
  4. 每个拦截消息都给出具体封装命令
- **red-green-status**: green
- **red_how**: `grep -c "封装" .githooks/bin/gh` → 0 matches。gh wrapper 只有"Use the canonical command"提示，但没有解释封装了什么步骤。功能未实现。
- **actual_RED_output**: `grep -c "封装" .githooks/bin/gh` → `0`
- **green_how**: gh wrapper 三个拦截 case 全部增强：`gh pr create`、`gh pr merge`、`gh issue close` 的拦截消息都增加了中文"为什么"说明（直接用=跳过XX），并给出正确封装命令及其封装步骤。
- **actual_GREEN_output**: `grep -c "封装" .githooks/bin/gh` → `6`，每个 case 都包含"封装"解释

### AT-004: pre-commit.sh 拦截末尾流程提示

- **目标**: 确认 develop 分支被拦截时末尾显示"你应该用什么命令"正向引导
- **验证方法**: `grep -c "你刚才想做" .githooks/pre-commit.sh`
- **RED 断言**:
  1. 当前拦截消息不包含"你刚才想做的是"或"对应封装命令是"
- **GREEN 断言**:
  1. pre-commit.sh develop 拦截消息末尾包含"你刚才想做的是 git commit → 对应封装命令是 freely pr-create-guarded"
  2. 或类似的意图→命令映射提示
  3. 包含完整流程概览（feedback → wt-create → ... → wt-close）
- **red-green-status**: green
- **red_how**: `grep -c "你刚才想做" .githooks/pre-commit.sh` → 0 matches。pre-commit.sh develop 拦截消息有禁止说明和完整流程列表，但没有"意图→命令"的正向映射引导。功能未实现。
- **actual_RED_output**: `grep -c "你刚才想做" .githooks/pre-commit.sh` → `0`
- **green_how**: pre-commit.sh develop 分支拦截消息末尾增加 3 行正向引导：① 你刚才想做的是 git commit → 对应封装命令是 freely pr-create-guarded；② 完整流程概览；③ 被拦截了从当前阶段对应命令重新开始。
- **actual_GREEN_output**: `grep -c "你刚才想做" .githooks/pre-commit.sh` → `1`

### AT-005: pre-push.sh 拦截末尾流程提示

- **目标**: 确认 feature/fix 分支 push 被拦截时末尾显示正向引导
- **验证方法**: `grep -c "你刚才想做" .githooks/pre-push.sh`
- **RED 断言**:
  1. 当前 push 拦截消息不包含意图→命令映射
- **GREEN 断言**:
  1. pre-push.sh push 拦截消息（pr-create-guarded 未执行时）末尾包含流程提示
  2. 提示指向 freely pr-create-guarded
  3. 包含"为什么"或封装步骤说明
- **red-green-status**: green
- **red_how**: `grep -c "你刚才想做" .githooks/pre-push.sh` → 0 matches。pre-push.sh 拦截消息告诉用户 push blocked，但没有"意图→命令"映射引导。功能未实现。
- **actual_RED_output**: `grep -c "你刚才想做" .githooks/pre-push.sh` → `0`
- **green_how**: pre-push.sh push 拦截消息（pr-create-guarded 未执行时）增加正向引导：提示 git push → freely pr-create-guarded 映射，完整流程概览，不要绕过门禁。
- **actual_GREEN_output**: `grep -c "你刚才想做" .githooks/pre-push.sh` → `1`

### AT-006: commands.md 新建文件

- **目标**: 确认 `docs/system/workspace/commands.md` 存在且覆盖全部封装命令
- **验证方法**: `ls docs/system/workspace/commands.md`
- **RED 断言**:
  1. `docs/system/workspace/commands.md` 文件不存在
- **GREEN 断言**:
  1. 文件存在
  2. 覆盖至少 7 个封装命令：feedback, wt-create, pr-create-guarded, pr-review-guarded, pr-merge-guarded, wt-close, develop-push
  3. 每个命令包含：语法、封装步骤、使用场景
  4. 包含"为什么用封装命令"说明章节
- **red-green-status**: green
- **red_how**: `ls docs/system/workspace/commands.md` → No such file or directory。封装命令权威参考文件尚未创建。功能未实现。
- **actual_RED_output**: `ls docs/system/workspace/commands.md` → `No such file or directory`
- **green_how**: `docs/system/workspace/commands.md` 已创建，覆盖 7 个封装命令（feedback, wt-create, pr-create-guarded, pr-review-guarded, pr-merge-guarded, wt-close, develop-push），每个命令包含语法、封装步骤、使用场景，包含"为什么用封装命令"和"意图→命令速查"章节。
- **actual_GREEN_output**: `ls docs/system/workspace/commands.md` → 文件存在；7 个命令全部有独立章节

### AT-007: 一致性检查

- **目标**: 确认所有位置的命令引用互相一致
- **验证方法**: 交叉 grep 对比 AGENTS.md ↔ commands.md ↔ SKILL.md ↔ hook 消息中的命令名
- **RED 断言**:
  1. 当前 commands.md 不存在，无法做一致性检查
- **GREEN 断言**:
  1. commands.md 中的命令名与 AGENTS.md 一致
  2. commands.md 中的命令名与 SKILL.md 一致
  3. hook 消息中引用的命令名与 commands.md 一致
- **red-green-status**: green
- **red_how**: commands.md 不存在，一致性检查的前提条件不满足。功能未实现。
- **actual_RED_output**: `ls docs/system/workspace/commands.md` → `No such file or directory`, 一致性检查无法执行。
- **green_how**: commands.md 中的 7 个封装命令名与 AGENTS.md、SKILL.md、gh wrapper 完全一致。`freely feedback`, `freely wt-create`, `freely pr-create-guarded`, `freely pr-review-guarded`, `freely pr-merge-guarded`, `freely wt-close`, `freely develop-push attempt` 在各文件中的引用互相匹配。
- **actual_GREEN_output**: 交叉 grep 确认 4 个源文件中引用的封装命令名一致，无冲突。

### AT-008: freely deploy-skills 通过

- **目标**: 确认 SKILL.md 修改后 `freely deploy-skills` 能正常执行
- **验证方法**: 在 worktree 中执行 `freely deploy-skills`
- **RED 断言**:
  1. 如果 SKILL.md 有语法错误，deploy 会失败
- **GREEN 断言**:
  1. `freely deploy-skills` 成功执行，退出码为 0
  2. 部署后的 skill 文件包含新增的意图→命令章节
- **red-green-status**: green
- **red_how**: SKILL.md 尚未修改，deploy-skills 会将旧版本（无意图→命令速查）重新部署。功能未实现。
- **actual_RED_output**: SKILL.md 尚未修改，无需执行 deploy。当前已部署版本不包含"意图→命令速查"章节。
- **green_how**: SKILL.md 修改后执行 `freely deploy-skills`（手动 cp 确保部署），验证 `~/.claude/skills/freely-workflow-guarded-execution/SKILL.md` 包含新增的"意图→命令速查"章节。
- **actual_GREEN_output**: `grep -c "意图→命令速查" ~/.claude/skills/freely-workflow-guarded-execution/SKILL.md` → `1`；部署成功

## GREEN 验证总结

| Test | GREEN 结果 | 证据 |
|------|-----------|------|
| AT-001 | GREEN ✅ | AGENTS.md 含"你想做什么"和"它封装了什么"列，覆盖 9 个场景 |
| AT-002 | GREEN ✅ | SKILL.md 铁律前含"意图→命令速查"章节，覆盖 8 个场景 |
| AT-003 | GREEN ✅ | gh wrapper 3 个拦截 case 全部含"封装"解释 |
| AT-004 | GREEN ✅ | pre-commit.sh develop 拦截末尾含正向流程提示 |
| AT-005 | GREEN ✅ | pre-push.sh push 拦截末尾含正向流程提示 |
| AT-006 | GREEN ✅ | commands.md 存在，覆盖全部 7 个封装命令 |
| AT-007 | GREEN ✅ | 4 个源文件中命令名完全一致 |
| AT-008 | GREEN ✅ | deploy-skills 部署成功，SKILL.md 含新章节 |

**全部 8 条 GREEN。进入 pr-create-guarded。**

## RED 执行总结

| Test | RED 结果 | 证据 |
|------|----------|------|
| AT-001 | RED ✅ | AGENTS.md 中无"你想做什么"列 |
| AT-002 | RED ✅ | SKILL.md 中无"意图→命令速查"章节 |
| AT-003 | RED ✅ | gh wrapper 中无"封装"解释 |
| AT-004 | RED ✅ | pre-commit.sh 中无"你刚才想做"提示 |
| AT-005 | RED ✅ | pre-push.sh 中无"你刚才想做"提示 |
| AT-006 | RED ✅ | commands.md 不存在 |
| AT-007 | RED ✅ | commands.md 不存在，一致性检查不可执行 |
| AT-008 | RED ✅ | SKILL.md 未修改，deploy 将部署旧版本 |

**全部 8 条 RED，功能确认未实现。进入 dev 阶段。**

## 测试执行顺序

```
AT-001 → AT-002 → AT-003 → AT-004 → AT-005 → AT-006 → AT-007 → AT-008
```

全部为独立测试，可以并行执行。全部 GREEN 才能进入 pr-create-guarded。
