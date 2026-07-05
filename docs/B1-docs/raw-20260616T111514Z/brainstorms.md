# Brainstorm: write_config heredoc → Python 序列化

## Discovery
write_config() 用 bash `cat <<EOF` 拼接 TOML，绕过 freely_config.py 的 _toml_quote 和 _shell_quote。缺 10 个 posture/consent 字段。

## Research
freely_config.py cmd_init_toml 已支持 --value KEY=VALUE。可直接调用替代 heredoc。

## Decision
替换为 `python3 freely_config.py init-toml --value ...`，补齐 10 个缺失字段。
