# Brainstorm: config.env → config.toml Complete Migration

## Discovery

### 当前状态（Phase 1+2 部分合并后）

**已改但有问题：**
| 文件 | 状态 | 问题 |
|------|------|------|
| `config_file()` | 返回 `.toml` | 文件不存在→daemon 起不来 |
| `global_config_file()` | 返回 `.toml` | 同上 |
| `load_config()` | 只读 toml | 无 fallback，直接 exit |
| `source_config()` | toml2env 转换 | 需要 toml 文件存在 |
| `write_config()` | 写 TOML 格式 | 格式正确 ✓ |
| `interruption-manager-handler:235` | 检查 toml | 不存在则 exit 1 |
| `signal-intent-handler:44` | 检查 toml | 不存在则 exit 1 |
| `ai-cli:1241,1509,1529,1550` | 检查 toml | 使用 toml |

**已做对：**
| 文件 | 状态 |
|------|------|
| `freely_config.py` | 完整 TOML 读写 ✓ |
| `toml2env` | TOML→shell env 转换 ✓ |
| `write_config()` | 生成 TOML 格式 ✓ |
| `.gitignore` | `.freely/` 已忽略，toml 不跟踪 ✓ |

### 涉及文件（12 个）
1. `freely` — load_config, config_file, write_config, source_config
2. `freely_config.py` — read/write/upsert/init-toml
3. `ai-cli` — 4 处 config.toml 检查
4. `interruption-manager-handler` — line 235-236
5. `signal-intent-handler` — line 44-45
6. `monitor-ai-acp.sh` — bridge_config_env
7. `manager-watchdog.sh`
8. `network-proxy-resolver.sh`
9. `bin/toml2env` — 转换器
10. `bin/pre-init-runtime` — 复制配置
11. `bin/check-file-size` — 旧 config.env 引用
12. `bin/deploy-skills`

### 全局配置
`~/.freely/config.env` → `~/.freely/config.toml`
`global_config_file()` 已改为 `.toml`，同样缺文件问题

## Research

### 方案 A：完全回退 config.env
- daemon 立即工作
- 丢失 TOML 优势
- 已合入代码大量回退→风险

### 方案 B：启动时自动迁移（选定）
- `load_config()`: 先试 config.toml → 不存在则读 config.env → 自动创建 config.toml → 记录迁移日志
- 全局配置同样处理
- 迁移后保留 config.env 不改名（向后兼容 1 周期）
- `freely init` 直接生成 config.toml（已实现 ✓）
- `interruption-manager-handler` 和 `signal-intent-handler` 改为 fallback

### 方案 C：只创建 config.toml 文件
- 手动 python3 脚本从 config.env 生成
- daemon 不自治，需人工干预
- 放弃

## Decision

**方案 B — 自动迁移**

### 实现清单
1. `load_config()`: toml missing → try env → auto-migrate → use toml
2. `interruption-manager-handler`: `[[ -f config.toml ]] || exit 1` → try env fallback
3. `signal-intent-handler`: 同上
4. `ai-cli`: 4 处检查改为 try toml → fallback env
5. `bin/pre-init-runtime`: 复制 config.toml 而非 config.env
6. `bin/check-file-size`: 更新注释
7. `freely_config.py`: 添加 `migrate-from-env` 命令
8. `config.toml.example`: 创建模板（不含敏感值）
9. 迁移后保留 config.env（不删除）
10. 全局配置 `~/.freely/config.toml` 同样 fallback

### 不做的
- 删除 config.env（保留兼容 1 周期）
- 修改 `write_config()`（已是 TOML ✓）
- 修改 `.gitignore`（`.freely/` 已忽略 ✓）

### 验收
- [ ] daemon 能从 config.env 自动迁移启动
- [ ] daemon 能从 config.toml 直接启动
- [ ] freely init 生成 config.toml
- [ ] 所有 handler 不会因缺 toml 退出
- [ ] 全局配置同样 fallback
