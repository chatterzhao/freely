# B1: FREELY_SKIP_IBM_GATE 配置化

## Problem
governance-merge-gate 的 is_governance_only_path() 中可跳过路径硬编码，
用户无法添加项目特定的治理目录。只能修改 Python 代码。

## Decision
Option A: config.toml [skip_ibm_gate] allowed_paths
- 用户在 config.toml 中添加允许的路径前缀
- governance-merge-gate 读取并合并
- 向后兼容：空列表 = 使用硬编码路径
