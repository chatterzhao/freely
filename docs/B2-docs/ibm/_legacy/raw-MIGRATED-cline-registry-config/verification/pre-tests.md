# Pre-Tests
## A1: TOML 语法正确
- test_command: python3 -c "import tomllib; tomllib.load(open('docs/system/workspace/scripts/runtime/tool-registry.toml','rb'))"
- expected_output: (no error)
- actual_output:
- evidence_file:
## A2: registry query 可读
- test_command: python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml cline acp.binary
- expected_output: "cline"
- actual_output:
- evidence_file:
