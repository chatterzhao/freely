---
b1_id: B1-20260705T231534Z
phase_state: completed
source_raw: raw-20260705T231534Z
source_url: https://github.com/chatterzhao/freely/issues/3758
produced_candidate: C-20260705T231534Z-A
created_at: 2026-07-06
---

# B1: ./bin/xxx → freely xxx 统一引用

## Input
- raw-20260705T231534Z (GitHub #3758)
- 项目已支持 `freely` 全局命令，但文档/脚本仍用 `./bin/xxx`

## Discovery

### 全量扫描结果 (~230 处)

| 类别 | 文件 | 数量 | 规则 |
|------|------|------|------|
| Hook 内部执行 | pre-commit/pre-push/pre-merge-commit/post-checkout/reference-transaction | ~38 | 改为 `freely xxx`（PATH 中有 freely） |
| 用户可见提示 | git-worktree-guard, hook 错误输出 | ~15 | 改为 `freely xxx` |
| 文档 | README.md, AGENTS.md | ~14 | 改为 `freely xxx`（chmod +x 保留） |
| bin/ help text | raw-issue-pull, deploy-skills, git-worktree-guard | ~10 | 改为 `freely xxx` |
| 生产脚本 | quality/, runtime/, worktree/ 脚本 | ~61 | 按上下文判断 |
| 测试文件 | tests/ | ~88 | 改为 `freely xxx` 或 `docs/B1-docs/` |

### 规则
- 用户可见 → `freely xxx`
- `source ./bin/xxx` → 保留（source 需要文件路径）
- `chmod +x ./bin/xxx` → 保留（安装指令）
- `./bin/xxx` 在 `-x "./bin/xxx"` 测试 → 保留（文件存在性检查）
- hook 脚本内部执行 gate → `freely xxx`

## Decision: 分类替换

1. 所有用户可见文本（echo/cat/help/usage/错误提示）→ `freely xxx`
2. `source ./bin/` + `chmod +x ./bin/` + `-x "./bin/` → 保留
3. hook 脚本中 `$(./bin/xxx ...)` 调用 → `freely xxx`

## Candidate
- candidate_id: C-20260705T231534Z-A
- status: promoted
- milestone: M-20260705T231534Z-A
