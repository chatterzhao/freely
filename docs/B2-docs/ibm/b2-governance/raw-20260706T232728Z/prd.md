# PRD: 封装命令文档系统化

## Goal

让任何人在任何时候都能从意图出发找到正确的封装命令，理解为什么必须用封装命令（因为封装了流程），被 hook 拦截时得到正向引导。

## 实现方案

### 架构：集中真源 + 分布触点

```
commands.md (权威参考)
    ↓ 引用/一致
    ├── AGENTS.md (入口，意图→命令速查表)
    ├── SKILL.md (流程执行者，正向引导)
    ├── .githooks/bin/gh (拦截点，说清"为什么"和"应该用什么")
    ├── pre-commit.sh (拦截点，流程提示)
    └── pre-push.sh (拦截点，流程提示)
```

### 6 个文件的具体改动

#### 1. `docs/system/workspace/commands.md` (新建)
封装命令权威参考。每个命令列出：
- 命令语法
- 封装了哪些步骤
- 使用场景（何时用）

#### 2. AGENTS.md
现有速查表增加两列：
- "你想做什么"（意图列）
- "它封装了什么"（流程步骤）

#### 3. freely-workflow-guarded-execution SKILL.md
铁律区域前增加"意图→命令速查"章节：
- 从开发者意图出发的表格
- 每行：意图 → 正确命令 → 错误做法 → 原因

#### 4. .githooks/bin/gh
每个拦截消息增加"为什么"说明：
```
[BLOCKED] gh pr create 不允许直接使用。
  直接用 = 跳过 pull develop、dry-run gate、push 门禁
  ✅ 使用: freely pr-create-guarded
     封装: pull develop → 冲突处理 → dry-run gate → push → 双平台创建 PR
```

#### 5-6. pre-commit.sh / pre-push.sh
拦截消息末尾增加：
```
[freely] 你刚才想做的是 git commit → 对应封装命令是 freely pr-create-guarded
[freely] 完整流程: feedback → wt-create → B1 → B2 → RED → dev → GREEN → pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close
```

## Dev-Loop Handoff

- 全部为纯文本/文档修改
- 无运行时行为变更
- 不需要代码编译或测试执行
- 验证方式：grep 检查文本内容存在性
