# B2 Brainstorm: Worker Launch 保护工位重定向

- I-*: I-20260509T022152Z-A
- source_candidate: `docs/pre-brainstorms/20260509T022152Z--worker-launch-writable-redirect/candidates.md`
- 日期: 2026-05-09

## B1 已收敛的决策

1. **不做自动重定向** — runtime 不应该猜测配对工位；主管负责选对工位
2. **Runtime 拒绝保护分支** — `worker_prompt_launchable_for_manager_project` 检查 target branch 前缀，非法则 return 1
3. **报错信息清晰** — 包含当前 branch 和允许的 prefix 列表，主管据此修 continuity

## 实现设计

### 入口

`worker_prompt_launchable_for_manager_project` (freely L9695) 是 worker launch 前的 launchability 检查。在该函数返回 1 时，runtime 已处理 `WORKER_PROMPTS_NOT_LAUNCHABLE` 路径（L13177）。

### 改动

在 L9706（已提取 `target_branch`）之后，解析 branch prefix：

```bash
case "$target_branch" in
  fix/*|feature/*|hotfix/*) ;;  # OK
  *)
    log_info "worker target branch '%s' is a protected branch; worker must target fix/* or feature/*" "$target_branch"
    return 1
    ;;
esac
```

### 允许列表范围

| Prefix | 状态 | 理由 |
|--------|------|------|
| `fix/*` | ✅ | 修复工位，可写 |
| `feature/*` | ✅ | 功能工位，可写 |
| `hotfix/*` | 待定 | 紧急修复工位，理论上可写但当前场景罕见 |
| `release/*` | ❌ | 发布冻结分支 |
| `develop` | ❌ | 保护分支 |
| `main` | ❌ | 保护分支 |
| `test-pre-merge-*` | ❌ | 保护分支（临时验证批次） |

### 边界情况

1. `hotfix/*` 暂不加入允许列表——hotfix 场景当前不经过 worker launch。后续可按需放宽
2. 空 branch 值（`worker_prompt_target_branch` 返回空）→ 视为无法判断，放行（避免破坏已有正常流程）
3. cleanup intent 只针对 absorbed merged lane，不涉及保护分支 redirect

## 不负责

- 不改变 AI prompt 格式
- 不改变 worker prompt 生成逻辑
- 不做自动重定向——由主管负责选对工位
