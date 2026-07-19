# PRD: 清理全项目 lead-agent.md 悬空引用 + 修复 governance-check 落后 skill 路径

- issue_id: I-20260719T015321Z-A
- epic: agent-orchestration
- story: agent-role-cleanup

## Goal

彻底完成 2026-05-15 commit `1c505bf63` 启动但未完成的 lead-agent.md 移除后的引用清理，同步修复 governance-check 中指向不存在目录的 skill 路径。解除所有 raw issue 的 governance-check 阻塞。

## 实现方案

全项目搜索并替换 `lead-agent` → `manager`/`manager/worker`（按上下文），17 个文件。

### 核心修复

1. `governance-check` — 删除 lead-agent.md 文件检查 + 修复 skill 路径回到实际存在的目录
2. `start-lead-agent.sh` — `initial_read_targets` 删除 lead-agent.md，role 引用更新
3. `auto-loop-orchestrator/SKILL.md` — 主链描述更新
4. `context-source-skill/SKILL.md` — frontmatter/描述更新
5. `project-agents-contract.md` — 术语更新

### 配套修复

4 个治理测试文件删除 fake lead-agent.md fixture；scripts/README.md、tools.md、freely runtime 等引用更新。
