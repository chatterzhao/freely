# Tasks: freely init ACP 工具准备 + tool-registry 下载配置
- issue_id: I-20260630T124528Z-A

## Task 1: tool-registry.toml — 四个工具新增 install_method + download_url
- 文件: `docs/system/workspace/scripts/runtime/tool-registry.toml`
- 改动:
  - `[claude.acp]`: 新增 `install_method = "npm"`, `download_url = "npm:@anthropic-ai/claude-agent-acp"`
  - `[codex.acp]`: 新增 `install_method = "github_release"`, `download_url` (整合现有 download_version/download_repo)
  - `[opencode.acp]`: 新增 `install_method = "npm"`, `download_url = "npm:@anthropic-ai/opencode"`
  - `[cline.acp]`: 新增 `install_method = "npm"`, `download_url = "npm:cline"`
- 依赖: 无

## Task 2: ensure-codex-acp → ensure-acp-binary 通用化
- 文件: `docs/system/workspace/scripts/runtime/ensure-codex-acp` (重命名/重写)
- 改动:
  - 接受 `--tool <name>` 参数（必需）
  - 读 `[<tool>].acp.binary`、`install_method`、`download_url`、`download_version`
  - 按 `install_method` 分发: `npm` → `npm install -g`; `github_release` → curl + tar
  - 缓存路径: `~/.cache/freely/acp/<tool>/<version>/<triplet>/<binary>`
  - 支持 `--dry-run` 仅输出路径不做下载
- 依赖: Task 1

## Task 3: cmd_init() 重写 ACP 工具准备步骤
- 文件: `docs/system/workspace/scripts/runtime/freely` (`cmd_init()` L20073-20132)
- 改动:
  - 删除硬编码 `case "$tool" in codex) ... ;; *) ... ;; esac`
  - 新增 `_init_acp_tool_setup()` 函数：循环 registry [tool] sections
  - 对每个 tool: 搜系统（PATH、npm list、~/.cache）→ 找到则记录 → 未找到则交互确认（stdin y/N）→ 调 ensure-acp-binary 下载
  - 写入 config.toml: `FREELY_ACP_<TOOL_UPPER>_BIN = "<path>"`
- 依赖: Task 2

## Task 4: _ensure_acp_bridge_running 从 config.toml 读 ACP binary 路径
- 文件: `docs/system/workspace/scripts/runtime/freely` (L13975-14001)
- 改动:
  - 优先: `get_config "FREELY_ACP_${TOOL_UPPER}_BIN"` → 找到且可执行 → 直接用
  - fallback: registry acp.binary → PATH 找
  - 最后 fallback: 现有 env var (FREELY_CLAUDE_ACP_BIN / FREELY_CODEX_ACP_BIN)
- 依赖: Task 3

## Task 5: _acp_bridge_health_check Shell 注入修复
- 文件: `docs/system/workspace/scripts/runtime/freely` (L13863-13879)
- 改动:
  - `sock.connect('$socket')` → `os.environ.get('FREELY_ACP_HEALTH_SOCKET', '')`
  - 调用方加 `FREELY_ACP_HEALTH_SOCKET="$socket"` 环境变量
- 依赖: 无

## Task 6: config.toml.example 新增 ACP binary 路径字段
- 文件: `templates/config.toml.example`
- 改动: 在 AI 工具适配器段下新增注释和字段
  ```toml
  # ACP binary paths (set by freely init)
  FREELY_ACP_CLAUDE_BIN = ""
  FREELY_ACP_CODEX_BIN = ""
  FREELY_ACP_OPENCODE_BIN = ""
  FREELY_ACP_CLINE_BIN = ""
  ```
- 依赖: Task 3

## Task 7: 更新 epics-map.svg
- 文件: `docs/epics-map.svg`
- 改动: 新增 `acp-tool-setup` epic + `init-registry-download` story
- 依赖: Task 1-6

## Task 8: RED+GREEN 验证
- 在 test-pre-merge 工位执行 pre-tests.md 全部 6 个 acceptance items
- 依赖: Task 1-7
