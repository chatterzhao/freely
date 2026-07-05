# Brainstorms: tool-registry-query.py 清理 JSON5 dead code
- raw_key: 20260624T061532Z
## Discovery
#3403 删除 tool-registry.json5 后，query tool 仍保留 _strip_json5/_load_json5/_load_registry 等 JSON5 兼容函数，成为死代码。
## Decision
删除全部 JSON5 相关函数，_resolve_registry 直接调用 _load_toml。
