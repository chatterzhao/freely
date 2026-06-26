- issue_id: I-20260626T150328Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260626T150328Z-A
- source_raw: raw-20260626T150328Z
- source_candidate: docs/pre-brainstorms/20260626T150328Z--toml-array-comma-join/candidates.md#C-20260626T150328Z-A
- verification_artifact_dir: docs/epics/toml-array-comma-join/code-reviews
- canonical_issue_path: docs/issues/I-20260626T150328Z-A/issue.md
- title: TOML array comma-join + feedback validation + bash 3.2 guard
- pre_tests_path: docs/epics/toml-array-comma-join/verification/pre-tests.md

# I-20260626T150328Z-A: TOML array comma-join + feedback validation + bash 3.2 guard

- source_candidate: `docs/pre-brainstorms/20260626T150328Z--toml-array-comma-join/candidates.md#C-20260626T150328Z-A`
- pre_tests_path: `docs/epics/toml-array-comma-join/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/toml-array-comma-join/code-reviews`

## 实现

### 修改文件

1. **`docs/system/workspace/scripts/runtime/tool-registry-query.py:111`**
   - `" ".join(str(v) for v in value)` → `",".join(str(v) for v in value)`
   - TOML 数组输出从空格分隔改为逗号分隔，与 bash 端 `tr ',' '\n'` 消费者对齐

2. **`docs/system/workspace/scripts/runtime/tool-launchers.sh:85`**
   - `for _a in $_aliases; do` → `for _a in ${_aliases//,/ }; do`
   - aliases 循环适配逗号分隔（此前依赖空格分词）

3. **`docs/system/workspace/scripts/runtime/freely` — `cmd_feedback`**
   - 新增 4 项格式校验：类型前缀、标题长度 ≤ 100、body ≥ 50 chars、必须有 `## ` section

4. **`docs/system/workspace/scripts/runtime/freely` — `_ensure_acp_bridge_running`**
   - 空数组 `for` 循环加 `[[ ${#_bridge_env[@]} -gt 0 ]]` 长度保护（bash 3.2 + `set -u` 兼容）

### 验证结果

- `tool-registry-query.py claude adapters.supported` → `direct,acp` ✅
- `tool-registry-query.py claude aliases` → `cc,cc-use-codex-cli,kiro-cli,iflow,claude-code` ✅
- `freely feedback` 拒绝无前缀标题 ✅、拒绝过长标题 ✅、拒绝过短 body ✅、拒绝无 `##` section ✅
