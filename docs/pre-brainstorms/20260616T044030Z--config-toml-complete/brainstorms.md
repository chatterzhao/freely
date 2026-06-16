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

### 方案 A：自动迁移（渐进式）
- load_config: toml missing → try config.env → auto-migrate → use toml
- 迁移后保留 config.env 不改名（向后兼容 1 周期）
- 所有 handler 保留 env fallback
- 缺点：代码中有两条配置读取路径（toml + env），增加维护负担
- 缺点：迁移代码（parse_env_file）是运行时死代码，迁移完成后永不再用

### 方案 B：彻底 TOML-only（选定）
- config.toml 是唯一配置格式，不存在 config.env 读取/迁移/回退
- `freely init` 释放 `config.toml.example` 到 `.freely/`，**不自动生成 config.toml**
- 启动时 config.toml 不存在 → 阻塞，提示用户 `cp config.toml.example config.toml` 并手工编辑
- 所有 handler/脚本 TOML-only，无 env 回退
- 优点：单一配置路径，零兼容负担，用户必须阅读注释理解每个配置项
- 优点：无需 parse_env_file、迁移代码、env fallback 代码

### 方案 C：手动迁移脚本
- 提供独立 Python 脚本从 config.env 生成 config.toml
- daemon 不参与迁移，需人工执行
- 放弃：daemon 不能自治，老用户迁移体验差

## Decision

**方案 B — 彻底 TOML-only，零 config.env**

### 正确流程

```
freely init:
  ├── 释放 config.toml.example → .freely/config.toml.example
  ├── 释放模板 → docs/
  ├── 初始化 freely.db
  └── 提示: cp config.toml.example config.toml + 编辑 + freely start
       （不自动生成 config.toml，确保用户手工阅读注释配置）

freely start (load_config):
  ├── config.toml 存在 → source_config → 校验 PROJECT_ROOT → 启动
  └── config.toml 不存在 → 阻塞:
        "config.toml not found"
        "cp .freely/config.toml.example .freely/config.toml"
        "然后按注释编辑"
```

### 实现清单
1. `freely_config.py`: 移除 parse_env_file、--from-env，不保留任何 config.env 代码
2. `freely_config.py`: 修复 dict_to_toml 表头排序、_shell_quote $/反引号、cmd_print 嵌套 dict
3. `load_config()`: config.toml 不存在时阻塞 + 明确提示（不迁移、不回退）
4. `freely init`: 移除 write_config 调用，只释放 config.toml.example
5. `freely init`: 移除 autonomy_contract、codex_config 等依赖 config.toml 的步骤
6. `network-proxy-resolver.sh`: 移除 source config.env 回退分支
7. `interruption-manager-handler`: `source_config`（TOML-only）
8. `signal-intent-handler`: `eval toml2env`（TOML-only，shell 转义已修复）
9. `bin/pre-init-runtime`: 复制 config.toml 并 sed 修正路径（已实现 ✓）
10. `bin/check-file-size`: 更新注释中的 config.env→config.toml
11. `config.toml.example`: 56 字段全量中文注释，ACP 默认值
12. `templates/config.toml.example`: init 时释放到 .freely/ 目录
13. AGENTS.md + freely-fix-execution/SKILL.md: config.env→config.toml

### 不做的
- **任何 config.env 读取/迁移/回退** — 彻底断点
- **freely init 自动生成 config.toml** — 用户必须手工配置
- 修改 `.gitignore`（`.freely/` 已忽略 ✓）
- 全局配置 fallback（全局配置同为 TOML-only，无 config.toml 则同样阻塞）

### 验收
- [x] freely init 释放 config.toml.example 到 .freely/
- [x] freely init 不生成 config.toml
- [x] load_config: config.toml 存在→正常启动
- [x] load_config: config.toml 不存在→阻塞+提示 cp example
- [x] 零 config.env 代码：无 parse_env_file、无 --from-env、无 source config.env
- [x] config.toml.example: 56 字段中文注释，ACP 默认值
- [x] 所有 shell 脚本 TOML-only（无 env source 回退）
- [x] dict_to_toml: flat keys 先于 sections（修复 upsert 数据错位）
- [x] _shell_quote: $ 和反引号已转义
- [x] 文档 AGENTS.md + SKILL.md: config.env→config.toml

## Additional gaps found

### config.toml.example 缺失字段
8 个 runtime posture 设置不在 template 中，已补充。

### freely init 不释放 template
`init` 之前只生成 `.freely/config.toml`（通过 write_config），不释放 `.freely/config.toml.example`。
修正后 init 不再生成 config.toml，只释放 example。

### freely package 不复制配置
`bin/freely-package` 没有 config 复制逻辑。打包时需要复制 `.freely/config.toml`（或让用户自行提供）。

### pre-init-runtime 已正确处理
`bin/pre-init-runtime` line 47-54 已处理 config.toml 复制和路径修正 ✓
