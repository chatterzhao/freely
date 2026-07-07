---
b1_id: B1-20260707T172110Z
phase_state: completed
source_raw: raw-20260707T172110Z
source_url: https://github.com/chatterzhao/freely/issues/3815
produced_candidate: C-20260707T172110Z-A
---

# B1: task-lifecycle-scan — 修复 7 个缺陷

## Discovery

### value_check: P0 阻塞
scan 是 Manager patrol 的 standing-source——返回 0 items = Manager 发现不了任何任务。

### 根因链
1. scan.py L740: `project = Path(sys.argv[1])` 取位置参数
2. freely shell L17132: 传 `--project $project` 
3. → `project = Path("--project")` 无效路径
4. → 所有 git/gh/gitee 操作失败
5. → 返回 0 items

### 7 缺陷
| # | 缺陷 | 严重度 |
|---|------|--------|
| A | 参数解析: sys.argv[1] vs --project | 🔴 |
| B | head_changed=False 跳过文件扫描 | 🟡 |
| C | 1b_reopen dead code | 🟡 |
| D | 不检测无 raw-{key} 的平台 issue | 🟡 |
| E | 硬编码平台检测（应复用 adapter） | 🟡 |
| F | agent_working import 静默失败 | 🟡 |
| G | extract_id 只查 GitHub | 🟡 |

## Decision: 最小改动——修复 A-G

### 子问题
- 参数解析: 改为 argparse --project（参照 bak.py）
- 平台检测: 改用 platform-adapter.configured_platforms() + list_open_issues()
- 1b_reopen: 集成到 Category 2 state-mismatch
- extract_id: 遍历所有平台

## Candidate: C-20260707T172110Z-A, promoted
