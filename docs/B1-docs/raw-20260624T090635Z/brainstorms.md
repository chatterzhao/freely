# Brainstorms: tool-launchers.sh adapter/ACP dispatch 注册表驱动化

## Discovery

### Input
`docs/B1-docs/raw-20260624T090635Z35Z/issue.md`：tool-registry.toml Phase 1+2 完成了 TOML 格式迁移和 config_schema 字段抽象，但 runtime 中 adapter 查询、launch_kind、ACP dispatch、tool family 解析仍用硬编码 case 分支。新增工具（如 Cline）即使已配好 registry，也无法通过 ACP 启动。

### 当前硬编码分布
| 函数 | 行号 | 问题 |
|---|---|---|
| `tool_supported_adapters()` | L190 | `case "*)"` 只返回 `direct`，丢失 ACP |
| `tool_supported_launch_kinds_for_adapter()` | L212 | 硬编码 `codex:acp` 和 `*:acp` |
| `tool_run_acp_from_prompt_file()` | L783 | `case "*)"` → `"[ERROR] unsupported ACP launcher"` |
| `tool_run_direct_from_prompt_file()` | L597 | `case "*)"` → `"[ERROR] unsupported tool"` |
| `_resolve_tool_family()` | L307 | registry 未命中时硬编码 binary→family 映射 |
| `tool_supports_add_dir_boundary()` | L471 | 硬编码 `case "$tool"` |
| `monitor-ai-acp.sh` | L108 | permission fallback 硬编码三种工具 |

### registry 已有数据
每个 `[tool]` section 已声明：
- `adapters.supported` / `adapters.default` / `adapters.launch_kinds.*`
- `launch.acp.*` / `launch.direct.*`
- `aliases`（用于反向匹配 binary→family）
- `config_schema.fields.permission_bypass`

只差查询路径没打通。

## Research

### 方案 A：逐个迁移，保留 fallback
每个函数新增 registry 查询路径，未命中时保留旧硬编码作为 fallback。
**优点**：渐进式，风险低。**缺点**：两边维护，硬编码不会消失。

### 方案 B：全面注册表驱动，移除硬编码
所有函数改为 registry 优先，未注册工具走保守默认（如 direct-only、不报错但 warn）。
**优点**：消除硬编码。**缺点**：需要全面测试现有三工具。

### 方案 C（选）：registry 优先 + 最小的保守 fallback
registry 命中 → 用 registry 值。未命中 → 保守默认（direct-only、warn 但不报错）。不保留工具名硬编码。
**理由**：registry 已经是 canonical truth，保留硬编码只会制造分歧。

### ACP dispatch 特殊处理
claude 和 opencode 的 ACP 参数构建几乎相同，codex 有独立 bridge socket + 网络代理。通用化方案：
- 通用路径：参数从 `launch.acp.*` 读取
- codex 保留独立路径（auto_download + 独立 bridge socket + 网络代理）
- 新增 `*)` 分支走通用路径

## Decision

**Promote** 为一个 candidate。这是 P0——解决后新增工具（如 Cline）即可通过 ACP 启动。

### 涉及文件
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`（主战场）
- `docs/system/workspace/scripts/runtime/monitor-ai-acp.sh`（移除 fallback）

### 边界
- 不迁移 direct 模式 case 分支（direct 已 DEPRECATED）
- 不改变 `run-acp-prompt.py` / `acp-bridge.py` 架构
- 不迁移 ai-cli 的 login/save/switch（另见 P1/P2）

### 风险
- 现有 claude/codex/opencode 三工具行为必须不变
- codex 的独立 bridge socket / 网络代理 / auto_download 逻辑不能受影响
