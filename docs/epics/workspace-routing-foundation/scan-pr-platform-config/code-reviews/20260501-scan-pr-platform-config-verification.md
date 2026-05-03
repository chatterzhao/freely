# Verification: PR scan surface + FREELY_REPO_PLATFORMS config

- issue_id: `I-20260501-0000-A`
- issue_path: `docs/epics/workspace-routing-foundation/scan-pr-platform-config/issues/I-20260501-0000-A.md`
- verification_date: `2026-05-03`
- verifier: `human`

## Scope Verdict

- `PASS`: `FREELY_REPO_PLATFORMS` 配置变量正确声明
- `PASS`: `scan_repo_platform_prs()` 函数正确读取 CSV 配置并映射 CLI
- `PASS`: 空配置时向后兼容（无 PR surface）
- `PASS`: 非可用 CLI 的平台被跳过
- `PASS`: governance-check 无新增失败

## Commands

1. `./bin/governance-check`
2. `bash -n docs/system/workspace/scripts/runtime/freely`

## Implementation Decision Note

- decision: `为 task-source-scan 增加 open_pull_requests 扫描面，通过 FREELY_REPO_PLATFORMS 配置控制。`
- why_this: `通过配置而非硬编码支持多平台（github + gitee），最小化向后兼容风险。`
- alternatives_considered: `硬编码平台列表（不够灵活）；在外部脚本中扫描（增加集成复杂度）。`
- boundary_non_goals: `不修改现有的扫描逻辑；不引入 issue 同步；不添加新的平台 CLI。`
- residual_risk: `无 — 空配置时行为不变，配置的平台 CLI 不可用时静默跳过。`
