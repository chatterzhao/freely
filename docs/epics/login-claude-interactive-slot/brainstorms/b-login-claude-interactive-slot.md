# B-Brainstorm: login claude 交互式 slot

## 来源

- `C-20260619T033758Z-A` — B1_IBM 阶段 produce，状态 promoted
- `raw-20260619T033758Z` — 初始 feedback issue

## 实现前置设计

### 改动面

单文件修改：`docs/system/workspace/scripts/runtime/ai-cli`

| 函数 | 改动类型 | 行数 |
|------|----------|------|
| `_prompt_generic_login_mode` | 新增 | ~12 |
| `_login_account_slot` | 新增 | ~50 |
| `cmd_login` claude 分支 | 修改 | ~14（替换 1 行） |
| `_login_apikey_alias` slot 命名 | 修改 | ~13（替换 1 行） |
| settings.json 模板 | 修改 | ~40（替换 4 行） |

### 设计原则

1. **参照既有模式**：`_prompt_generic_login_mode` 与 `codex_prompt_login_mode` 同构
2. **阻塞式交互**：`prompt_value` 无默认值实现阻塞等待，空输入 → 终止
3. **非交互兼容**：`--name` 标志跳过 prompt，`--yes` + 无 `--name` → 报错
4. **不破坏既有行为**：codex、iflow 路径完全不变

### 替代方案评估

| 方案 | 评价 |
|------|------|
| A. 修改 `tool_login_generic` 增加交互 | ❌ 影响 iflow 的轻量容器语义 |
| B. 新增 `_login_interactive_slot` 统一处理 | ⚠️ 过度抽象，account/apikey 行为差异大 |
| **C. 新增两个函数 + 修改路由** | ✅ 最小改动，职责清晰 |

### 验收标准

1. `freely ai login claude` → 两步交互（auth_mode + slot name），空输入终止
2. `freely ai login claude apikey --name foo` → 非交互创建
3. `freely ai login claude account --name foo` → 非交互创建
4. settings.json 为 Anthropic 官方完整骨架
5. opencode/cc/cc-use-codex-cli/kiro-cli 同样适用
