# B1: tool-registry.toml 移到 tools/

## Problem
tool-registry.toml 是系统级工具接入定义，当前放在 scripts/runtime/ 里与 daemon/monitor/bridge 等运行时代码混在一起，位置不对。

## Decision
docs/system/workspace/scripts/runtime/tool-registry.toml → docs/system/workspace/tools/tool-registry.toml
与 tools.md 同级，更新 3 个引用文件。
