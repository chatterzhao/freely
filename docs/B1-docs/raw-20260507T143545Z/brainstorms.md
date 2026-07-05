# Brainstorm: 时间戳格式升级为带秒

## 来源
- `docs/B1-docs/raw-20260507T143545Z/issue.md` — GitHub #248
- #247 开发过程中发现 `_extract_issue_key` 正则 `\d{4}` 截断了 6 位秒

## 当前为什么不能直接进入 dev
- 改动涉及 4 个文件 12 处正则，需要全局搜索确保无遗漏
- 格式迁移策略需要明确：新格式 → 旧格式 → Bare 三向转换
- 必须兼容旧格式（已有 `20260503-0915` 等无秒 key）
- 老格式（4位 HHMM）需平滑升级为 6 位 HHMMSS

## 问题边界
| 格式 | 示例 | 精度 | 碰撞风险 |
|------|------|------|---------|
| Old | `20260503-0915` | HHMM 无秒 | 有 |
| New | `20260506T1000Z` | HHMM 无秒 | 有 |
| Bare | `20260430222144` | HHMMSS 有秒 | 低 |
| **Target** | `20260507T143500Z` | HHMMSS 带秒 | 无 |

改动范围：
- `task-lifecycle-scan.py`: 8 处正则 + `_normalize_key_variants` 增强
- `pre-push.sh`: 2 处正则
- `wt-create`: 2 处正则
- `issue-sync-batch.py`: 1 处正则

已正确的（不需改）:
- `task-lifecycle-scan.py:715,749` — 已用 `\d{4,6}Z`
- `wt-create:185` — 已用 `[0-9]{4,6}Z`
- `worktree-common.sh:54-56` — 已用 `[0-9]{4,6}`
- `chat-inbox.py:33` — 已用 `%H%M%S` 带秒

## 推荐下一跳
- Promote candidate → B2_IBM → 在 feature 工位逐一修改+验证
