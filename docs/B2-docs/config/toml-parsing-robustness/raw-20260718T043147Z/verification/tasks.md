# Tasks: I-20260718T043147Z-A

- issue_id: I-20260718T043147Z-A
- owner: dev-loop

## Tasks

- [x] T1: 修复 `monitor-ai-acp.sh` awk pattern — 容忍 config.toml 等号两侧空格
  - 文件：`docs/system/workspace/scripts/runtime/monitor-ai-acp.sh`
  - 改动：awk 条件从 `$1 == k " ="` 改为容忍空格
  - commit: `cf6e94c42`

- [x] T2: 为 `freely_config.py` 新增 `get` 子命令
  - 文件：`docs/system/workspace/scripts/runtime/freely_config.py`
  - 改动：新增 `cmd_get()` + `_resolve_dotted()` + CLI 注册
  - 功能：基于 `tomllib.load()` 取值，支持点号嵌套 key

- [x] T3: `monitor-ai-acp.sh` 取值逻辑从 awk 迁移到 `freely_config.py get`
  - 文件：`docs/system/workspace/scripts/runtime/monitor-ai-acp.sh`
  - 改动：config.toml 取值行从 awk 替换为 `$SCRIPT_DIR/freely_config.py get`

- [x] T4: 全项目审计 shell 脚本中的 TOML 手写解析
  - 确认仅 `monitor-ai-acp.sh` 一处通过 awk 解析 `.toml` 文件
  - 其余读取 toml 的脚本（`freely_config.py`、`tool-registry-query.py`）均使用 Python `tomllib`，不受影响
  - `at001-self-heal-writeback.sh` 的 sed 已使用 `= *` 容忍空格

- [ ] T5: 验证 `freely_config.py get` 在 TOML 各种合法空格格式下均正确取值
  - `KEY = "value"`（等号两侧空格）
  - `KEY="value"`（无空格）
  - `KEY= "value"`（仅右侧空格）
  - `KEY ="value"`（仅左侧空格）
  - 不存在的 key → exit 1
