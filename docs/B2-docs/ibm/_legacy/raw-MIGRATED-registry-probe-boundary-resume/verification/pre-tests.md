# Pre-Tests
## A1: resume_target registry
- test_command: grep -c "_tool_registry_get.*session.cli.resume" docs/system/workspace/scripts/runtime/tool-launchers.sh
- expected_output: ">=2"
