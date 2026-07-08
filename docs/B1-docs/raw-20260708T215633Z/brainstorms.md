---
b1_id: B1-20260708T215633Z
phase_state: completed
source_raw: raw-20260708T215633Z
---
# B1: scan de-hardcode platforms + per-platform state sync

## Problem
1. 硬编码 github/gitee — 应读 config.toml FREELY_REPO_PLATFORMS
2. 只查 GitHub 状态 — 应遍历所有配置的平台
3. extract_github_id 单平台 — 应用 platform_ids dict
4. N=0 平台无提示 — 应硬阻塞报错

## Decision
1. _detect_platforms: config.toml → git remotes fallback → N=0 sys.exit
2. extract_platform_ids: 读 platform_ids YAML block → dict
3. 状态比对: 遍历 configured_platforms 逐平台比对
4. _build_sync_batch: platforms 动态列表
