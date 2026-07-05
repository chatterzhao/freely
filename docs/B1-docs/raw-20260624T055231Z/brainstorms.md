# Brainstorms: 彻底移除 JSON5 回退
- raw_key: 20260624T055231Z
## Discovery
#3399 重构不彻底，三个脚本保留了 JSON5 回退路径，tool-registry.json5 未删除。deploy-skills 只检测到 claude。
## Decision
删除 JSON5 文件，去除所有脚本中的 JSON5 回退逻辑，只读 TOML。
