# Tasks

- issue_id: I-20260703T003829Z-A

## Task List

### A1: 修复 write_workcell_state 中 unsafe source
- [x] 将 `source "$state_file"` 替换为 `meta_env_value "$state_file" "LAST_ENTRYPOINT_MODE"`
- [x] 移除不再需要的 `unset LAST_ENTRYPOINT_MODE` 和 shellcheck disable
- 文件: docs/system/workspace/scripts/runtime/freely
- 行号: 8423-8428

### A2: 移除误提交的运行时文件
- [x] `git rm --cached .freely/run/workcell-state.env`
- .gitignore 已有 `.freely/` 规则，该文件不应被跟踪

### A3: 端到端验证
- [x] daemon start 成功且无命令注入
- [x] workcell-state.env 生成格式正确

### A4: 文档更新
- [x] B1 brainstorms + candidates
- [x] B2 设计文档（prd, pre-tests, IDN）
- [x] milestones.md 更新
- [x] Skill 流程文档加 cd 提醒
