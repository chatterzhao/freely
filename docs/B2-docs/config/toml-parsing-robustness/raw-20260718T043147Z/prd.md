# PRD: config.toml 解析健壮性 — 从 awk 手写解析迁移到标准 TOML 解析器

- issue_id: I-20260718T043147Z-A
- epic: config
- story: toml-parsing-robustness

## Goal

消除 `config.toml` 取值因 TOML 等号空格格式变化而静默失败的风险。将 shell 脚本中手写的 awk TOML 解析替换为 `freely_config.py get`（基于 Python 标准库 `tomllib`），同时对 `monitor-ai-acp.sh` 的 awk pattern 做即时修复。

## 背景

原始 raw issue `raw-20260718T043147Z` 的症状是 Worker ACP bridge initialize 超时（opencode HTTP server 与 acp-bridge.py stdio JSON-RPC 协议不兼容）。B1 收敛结论是换 worker_slot 为 claude。

在 dev 阶段进一步发现：即使 slot 正确，`monitor-ai-acp.sh` 从 `config.toml` 读取 ACP binary 路径时，awk pattern `$1 == k " ="` 要求等号左侧恰好为一个空格。TOML 规范允许等号两侧任意空格（`KEY="v"`、`KEY = "v"`、`KEY= "v"`、`KEY ="v"` 均合法），手写 awk 无法覆盖所有变体，导致 ACP binary 路径可能读取失败 → bridge 仍然无法启动。

此为系统性问题：全项目所有 shell 脚本中凡是用 awk/sed/grep 解析 TOML 的地方，都面临同样的脆弱性。

## 实现方案

### 即时修复：`monitor-ai-acp.sh` awk pattern

修改 awk 条件使其容忍等号两侧空格（commit `cf6e94c42`）。

### 根治：`freely_config.py get` 子命令

为 `docs/system/workspace/scripts/runtime/freely_config.py` 新增 `get` 子命令：

```bash
freely_config.py get --project <project> --key <key>
```

- 基于 Python 标准库 `tomllib.load()` 解析，正确处理所有合法 TOML 语法
- 支持点号嵌套 key（`section.subkey`）
- 找到 → 输出原始值 exit 0；未找到 → exit 1
- shell 侧加 `|| true` 兜底

```bash
# 改前（awk — 脆弱，格式依赖）
config_path=$(awk -F'"' -v k="$config_key" '$1 == k " =" {print $2; exit}' "$project/.freely/config.toml")

# 改后（标准 TOML 解析 — 格式无关）
config_path=$("$SCRIPT_DIR/freely_config.py" get --project "$project" --key "$config_key")
```

**不做的事**：
- 不修改 `acp-bridge.py`
- 不为 opencode 添加 HTTP ACP 支持（独立 feature issue）
- 不影响其他已有的 `freely_config.py` 子命令（toml2env、init-toml、upsert、print）

## Dev-Loop Handoff

- 修改文件：
  - `docs/system/workspace/scripts/runtime/monitor-ai-acp.sh`（awk → freely_config.py get）
  - `docs/system/workspace/scripts/runtime/freely_config.py`（新增 get 子命令）
- 改动：1 行 awk 替换 + ~30 行 Python
- 验证：`freely_config.py get` 在 `=` 两侧有/无空格、等号前后空格不对称等格式下均正确取值
