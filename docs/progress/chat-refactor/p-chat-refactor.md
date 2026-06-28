# Progress: chat 重构 — comment + discuss + archive

- issue_id: I-20260628T005815Z-A
- phase_state: in_dev

## Tech Stack Review

### 运行时依赖
| 依赖 | 可用性 | 说明 |
|------|--------|------|
| bash 3.2+ | ✅ 项目已用 | freely 主脚本 + pr-create-guarded + wt-close |
| Python 3 | ✅ 项目已用 | platform-adapter.py, freely_db_manager.py, scan.py |
| SQLite | ✅ 项目已用 | freely.db 已有 chats/sessions/a2a_tasks 表 |
| JSONL | ✅ 项目已用 | ACP session 证据、tool_switch_events |
| gh CLI | ✅ 项目已用 | GitHub API 操作 |
| ACP bridge | ✅ 项目已用 | run-acp-prompt.py, ensure-codex-acp |

### 新增依赖
| 依赖 | 需要 | 说明 |
|------|------|------|
| GitCode API | 需要 | platform-adapter 新增 discussion 端点 |
| GitHub Discussions API (GraphQL) | 需要 | 创建/回复/关闭 discussion |

## Architecture Check

### 边界约束（CONSTITUTION.md）
- ✅ 不涉及分支/worktree 规则变更
- ✅ 不绕过 protected branch 约束
- ✅ comment 不写本地文件，不污染 develop

### Loop 边界（PROJECT_INTENT.md）
- ✅ 不改 scan 分类逻辑（只删除 chat 扫描）
- ✅ 不改 a2a_tasks 协议
- ✅ 不改 ACP session 管理

### 循环依赖
- ✅ 新 skill 独立，不互相引用
- ✅ platform-adapter 新增方法不依赖新命令

## Acceptance Mapping

| raw issue acceptance | pre-tests 覆盖 |
|---------------------|---------------|
| comment 直写所有平台 | acceptance-1 (e2e) |
| close issue 拒绝 | acceptance-2 (unit) |
| discuss 新建 session | acceptance-3 (e2e) |
| discuss --archive 导出 | acceptance-4 (e2e) |
| agent-table.toml 配置 | acceptance-5 (unit) |
| 旧 chat 重定向 | acceptance-6 (unit) |
| comment→discuss→archive 联调 | Integration |
| Freely 自举不受影响 | End-to-End |
| 跨平台真实行为 | Real-Environment (not_tested, 需真实环境) |

## 实现进度
- [x] B1 + B2 文档
- [x] 阶段一：comment 命令（cmd_comment + get-issue-state）
- [x] 阶段二：discuss 命令（cmd_discuss + SQLite + adapter + agent-table）
- [ ] 阶段三：讨论执行 skill
- [ ] 阶段四：讨论归档 skill
- [ ] 阶段五：评论门禁
- [ ] 阶段六：旧 chat 拆除
- [ ] 阶段七：边界文档变更
