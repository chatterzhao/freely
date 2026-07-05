# Brainstorm: 规范流程文档治理

## Discovery

### 当前状态

完整规范流程 `feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-merge-guarded → wt-close` 只在 `three-loop-capability-lifecycle.md` 一处完整描述。

其余关键文档缺口：

| 文档 | 问题 | 严重度 |
|------|------|--------|
| `AGENTS.md.example` | 只有 skill 路由表，无线性流程。`freely init` 后是用户/AI 第一入口 | 高 |
| `CONSTITUTION.md` | 只有 pr-create/pr-merge 后半段 | 中 |
| `freely-feat-execution/SKILL.md` | 链从 B1_IBM 开始，不含 feedback 入口 | 中 |
| `freely-doc-B1_IBM-execution/SKILL.md` | 无位置标记 | 低 |
| `freely-doc-B2_IBM-execution/SKILL.md` | 无位置标记 | 低 |
| `freely-dev-loop-execution/SKILL.md` | 无位置标记 | 低 |
| `freely-fix-execution/SKILL.md` | 无位置标记 | 低 |

### 涉及文件

1. `AGENTS.md.example` — 新增 "规范流程" 章节
2. `freely-feat-execution/SKILL.md` — 描述行补 feedback 入口 + 位置标记
3. `freely-fix-execution/SKILL.md` — 位置标记
4. `freely-doc-B1_IBM-execution/SKILL.md` — 位置标记
5. `freely-doc-B2_IBM-execution/SKILL.md` — 位置标记
6. `freely-dev-loop-execution/SKILL.md` — 位置标记
7. `CONSTITUTION.md` — 分支规范处补完整链路引用

## Research

### 方案 A：在每个文档独立写（选定）

每个文档在头部/描述行加位置标记，格式统一：
```
全链路: feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-merge-guarded → wt-close
                                                            ↑ you are here
```

AGENTS.md.example 新增完整章节，含三种变体（feat/fix/doc-only）。

- 优点：每个文档自包含，读者不用跳转
- 优点：改动范围可控，纯文档
- 缺点：链变更时需批量更新（但链不常变）

### 方案 B：集中到一个文档 + 交叉引用

只在 AGENTS.md 写完整链，其余文档用 "详见 AGENTS.md §规范流程" 引用。

- 优点：单点维护
- 缺点：读者需要跳转，打断阅读流
- 不适合：skill SKILL.md 是 AI agent 直接的 action context，不应强制跳转

### Decision

选方案 A。skill SKILL.md 是 AI 的直接行动上下文，位置标记必须内联。链不常变，散落维护成本低。
