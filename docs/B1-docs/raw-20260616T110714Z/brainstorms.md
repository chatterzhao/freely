# Brainstorm: parse_env_file missing — removal, not restoration

## Discovery

`freely_config.py:cmd_init_toml` calls `parse_env_file()` but the function was removed in commit `a899aeb3`. Commit `5cc06494` added the `--from-env` flag and call but forgot to restore the definition → `NameError` at runtime.

## Research

### 方案 A：恢复 parse_env_file（否决）
- 恢复函数定义 + --from-env 迁移路径
- 缺点：保留 config.env 读取代码，与彻底 TOML-only 方向矛盾
- 缺点：parse_env_file 成为永久死代码（迁移一次后再也不会调用）

### 方案 B：删除 parse_env_file 及所有 config.env 迁移代码（选定）
- 彻底 TOML-only：无 config.env 读取/迁移/回退
- `freely init` 只释放 config.toml.example
- 启动时 config.toml 缺失 → 阻塞提示
- 优点：单一配置路径，零兼容负担

## Decision
**方案 B** — 删除，不恢复。本修复是 config-toml-complete clean-break 的一部分。
