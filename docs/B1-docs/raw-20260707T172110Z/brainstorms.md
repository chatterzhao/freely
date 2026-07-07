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
| A | 参数解析: sys.argv[1] vs --project | 🔴 CRITICAL |
| B | head_changed=False 跳过文件扫描 | 🟡 |
| C | 1b_reopen dead code | 🟡 |
| D | 不检测无 raw-{key} 的平台 issue | 🟡 |
| E | 硬编码平台检测（应复用 adapter） | 🟡 |
| F | agent_working import 静默失败 | 🟡 |
| G | extract_id 只查 GitHub | 🟡 |

## Brainstorm

### 参数解析（缺陷 A）

**Option A: 改 scan.py 为 argparse**
- 优点: 与 bak.py 一致，标准做法
- 缺点: 需改 scan.py

**Option B: 改 shell harness 传位置参数**
- 优点: scan.py 不用改
- 缺点: shell 侧语义不清晰

**Decision: Option A** — argparse 是 Python 标准，bak.py 已验证。

### 平台检测/查询（缺陷 E）

**Option A: scan 自己检测（当前）**
- 优点: 无依赖
- 缺点: 硬编码 github/gitee，新平台需改 scan

**Option B: 复用 platform-adapter ✅**
- 优点: 新平台自动支持，逻辑集中
- 缺点: 增加 import 依赖

**Decision: Option B** — platform-adapter 已有 Handler 注册表。

### head_changed（缺陷 B）

**Option A: 始终扫描文件（去掉 head_changed 优化）**
- 优点: 简单，不遗漏
- 缺点: 每次全扫，性能略降

**Option B: 修复 head_changed 检测逻辑**
- 优点: 保留优化
- 缺点: 需确保 state file 路径正确

**Decision: Option A** — scan 频率不高，全扫更可靠。

### 1b_reopen（缺陷 C）

**Option A: 删除 dead code**
- 优点: 代码干净

**Option B: 集成到 Category 2 ✅**
- 优点: 保留功能

**Decision: Option B** — reopen 是有用场景。

## Decision: 修复 A-G，复用 platform-adapter

## Candidate: C-20260707T172110Z-A, promoted
